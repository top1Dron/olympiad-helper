from judge.decorators import limit_permisions
from judge.models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage
from judge.services import getter
from judge.services.memory_limites import MemoryLimiter
from datetime import datetime
from django.conf import settings


import logging
import os
import psutil
import resource
import subprocess
import time
import traceback

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)


def create_solution(user, problem_number, programming_language, source_code) -> int:
    solution = Solution.objects.create(
        user=user,
        problem=getter.get_problem_by_number(problem_number),
        language=ProgrammingLanguage.objects.get(pk=programming_language),
        program_code=source_code,
        status='PD',
        avg_memory_usage=0,
        avg_time_usage=0
    )

    return solution.pk


def submit_solution(problem_number, programming_language, source_code, solution_id):
    '''
    execution and testing user solution for problem with problem_number
    '''
    
    language = ProgrammingLanguage.objects.get(pk=programming_language)
    solution = getter.get_solution_by_id(solution_id)
    
    code_file_name = os.path.join(settings.MEDIA_ROOT, f'{datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")[:-3]}_{solution.user.username}')
    
    # print user code to file with language extension
    with open(f'{code_file_name}.{language.extension}', 'w', encoding='utf-8') as file:
        print(source_code, file=file, end='')

    problem = Problem.objects.get(pk=problem_number)
    tests = ProblemTest.objects.filter(problem=problem)
    error = ''

    if language.name in ('C++11', 'C++14', 'C++17'):
        error = _compile(language, code_file_name)

    execute_line = language.execute.replace('[codefilename]', code_file_name)
    time_limit = float(problem.time_limit)
    _execute(solution, tests, execute_line, time_limit, error)
    if os.path.isfile(code_file_name):
        os.remove(code_file_name)
    if os.path.isfile(code_file_name + '.' + language.extension):
        os.remove(code_file_name + '.' + language.extension)


def _compile(language, code_file_name:str) -> str:
    '''
    method for compile submitted code, 
    used only for compiled languages
    '''

    complile_string = language.compile.replace('[codefilename]', code_file_name)
    compilation = subprocess.run(complile_string, stderr=subprocess.PIPE, text=True, shell=True)
    return compilation.stderr


@limit_permisions
def _execute(solution, tests, execute_line, time_limit, compile_error=''):
    '''
    method for execution submitted code
    '''
    
    try:
        if compile_error == '':
            if len(tests) == 0:
                solution_status = 'NT'
            for test in tests:
                _test_execution(test, execute_line, time_limit, solution)
            solution_status = _get_solution_tests_status_counts(SolutionTest.objects.filter(solution=solution))
        else:
            solution_status = 'CE'
            logger.error(f"status - {solution_status}, {compile_error}")
        _final_update_solution_result(solution, solution_status)
    except Exception as e:
        logger.error(f'{type(e)} {traceback.format_exc()}')


def _test_execution(test, execute_line, time_limit, solution):
    '''
    executes given test of given solution with given time_limit
    TODO: realize memory_limit and memory calculation on executed test
    '''
    try:
        execution = subprocess.Popen(execute_line.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)
        execution.stdin.write(bytes(test.input_data, 'UTF-8'))
        execution.stdin.flush()
        
        test.output_data = test.output_data.replace('\r', '')

        start_time = time.time()
        test_output, test_error_string = execution.communicate(timeout=time_limit)
        test_output = test_output.decode('utf-8')
        test_error_string = test_error_string.decode('utf-8')
        # try:
        #     logger.info(f'{execution.name()} - {execution.cpu_times()}') 
        #     used_memory = execution.memory_full_info().uss / float(1 << 20)
        #     logger.info(used_memory)
        # except Exception as e:
        #     logger.error(f'{type(e)} {traceback.format_exc()}')
        end_time = time.time()
        finish_time = end_time - start_time
        test_status = 'PD'

        if test_error_string != '':
            logger.info(f'{test.problem} {test.test_number} - done failed. {test_error_string}')
            test_status = 'RE'
        elif test.output_data == test_output:
            logger.info(f'{test.problem} {test.test_number} - done successfully.')
            test_status = 'AC'
        else:
            logger.info(f'{test.problem} {test.test_number} - done failed')
            test_status = 'WA'
    except subprocess.TimeoutExpired:
        end_time = time.time()
        finish_time = end_time - start_time
        logger.info(f'{test.problem} {test.test_number} - timeout')
        test_status = 'TO'
    except MemoryError as me:
        logger.error(f'{test.problem} {test.test_number} - out of memory')
        test_status = 'MO'
    except Exception as e:
        logger.error(f'{type(e)} {traceback.format_exc()}')
    finally:
        SolutionTest.objects.create(
            status=test_status, 
            solution=solution, 
            problem_test=test, 
            time_usage=str(round(finish_time*1000, 2)), 
            memory_usage='1'
        )


def _get_solution_tests_status_counts(tests):
    '''
    function to count test execution statuses for returning Solution status
    '''
    judging = wrong_answers = timeout = memoryout = right_answers = 0
    for test in tests:
        if test.status == 'PD':
            judging += 1
        elif test.status == 'WA':
            wrong_answers += 1
        elif test.status == 'TO':
            timeout += 1
        elif test.status == 'MO':
            memoryout += 1
        elif test.status == 'AC':
            right_answers += 1
    return _get_solution_status({
        'judging': judging, 
        'wrong_answers': wrong_answers, 
        'timeout': timeout, 
        'memoryout': memoryout, 
        'right_answers': right_answers
    }, len(tests))


def _get_solution_status(answers:dict, test_count:int) -> str:
    '''
    function to return solution status using tuple with solution tests status counts
    '''
    status = 'PD'
    if answers.get('judging') == test_count:
        status = 'PD'
    elif answers.get('wrong_answers') > 0 and answers.get('right_answers') > 0:
        status = 'PA'
    elif answers.get('wrong_answers') > 0:
        status = 'WA'
    elif answers.get('timeout') > 0 and answers.get('right_answers') > 0:
        status = 'PA'
    elif answers.get('timeout') > 0:
        status = 'TO'
    elif answers.get('memoryout') > 0 and answers.get('right_answers') > 0:
        status = 'PA'
    elif answers.get('memoryout') > 0:
        status = 'MO'
    elif answers.get('right_answers') == test_count:
        status = 'AC'
    return status


def _final_update_solution_result(solution, solution_status):
    '''
    function for setting final values of solution submition
    '''
    solution.status = solution_status
    tests = SolutionTest.objects.filter(solution=solution)
    miliseconds = 0.0
    for test in tests:
        miliseconds += float(test.time_usage)
    if len(tests) > 0:
        solution.avg_time_usage = round(miliseconds / len(tests), 2)
    solution.save()