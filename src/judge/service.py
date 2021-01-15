from django.conf import settings
from signal import alarm, signal, SIGALRM, SIGKILL
from .memory_test import display_top
from .models import Task, Solution, SolutionTest, TaskTest, ProgrammingLanguage
from .services.memory_limites import MemoryLimiter

import difflib
import logging
import os
import subprocess
import functools
import time
import traceback
import tracemalloc
import resource

logger = logging.getLogger(__name__)

MAX_VIRTUAL_MEMORY = 10 * 1.048576 * 1024 * 1024

def get_all_available_tasks():
    '''
    returns querydict of all tasks with is_active=True
    '''
    return Task.objects.filter(is_active=True)


def get_task_by_number(number):
    '''
    returns task by unique number
    '''
    return Task.objects.get(number=number)


def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))


# def test_on_time()


def submit_solution(task_number, programming_language, source_code):
    '''
    execution and testing user solution for task with task_number
    '''
    
    language = ProgrammingLanguage.objects.get(pk=programming_language)
    if language.name == 'Python 3.9.0':
        logger.info(language)
    elif language.name == 'gcc 8.3.0':
        check_submition_c_plus_plus(source_code, task_number, programming_language)
    # logger.info(f'{task_number}, {programming_language}, {source_code}')


def check_submition_c_plus_plus(source_code, task_number, programming_language):
    '''
    method for execution and testing code on c/c++ using gcc 8.3.0
    '''

    # print user code to cpp file
    with open(f'{os.path.join(settings.MEDIA_ROOT, "main.cpp")}', 'w', encoding='utf-8') as file:
        print(source_code, file=file, end='')

    task = Task.objects.get(pk=task_number)
    tests = TaskTest.objects.filter(task=task).filter(language=programming_language)
    # memory_limiter = MemoryLimiter(float(task.memory_limit))
    

    try:
        cfile = os.path.join(settings.MEDIA_ROOT, 'main.cpp')
        ofile = os.path.join(settings.MEDIA_ROOT, 'main')
        efile = os.path.join(settings.MEDIA_ROOT, 'main.exe')
        
        command_string = 'g++ ' + cfile + ' -o ' + ofile
        error_message = ''
        compile = subprocess.Popen(['/usr/bin/g++', "-o", ofile, cfile], stderr=subprocess.PIPE)
        error = compile.communicate()[1]
        if error.decode('utf-8') == '':
            for test in tests:
                
                # tracemalloc.start()
                # execution = subprocess.Popen(['/usr/bin/time', '-f "%e"', ofile, '$res2,', '$res3'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                # os.system("chmod 100 .")
                # 'ulimit -p 100; su judge -c \"', '; exit;\"'float(task.memory_limit) * 1.048576 * 1024 * 1024), preexec_fn=limit_virtual_memory()
                
                try:
                    execution = subprocess.Popen([ofile,], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                    execution.stdin.write(bytes(test.input_data, 'UTF-8'))
                    execution.stdin.flush()
                    # returncode = -1
                    # try:
                    #     logger.info(execution.communicate())
                    #     returncode = execution.returncode
                    # except subprocess.TimeoutExpired:
                    #     returncode = 124 # Code for TLE
                    
                    # snapshot = tracemalloc.take_snapshot()
                    # memory_usage = display_top(snapshot)
                    test.output_data = test.output_data.replace('\r', '')

                    start_time = time.time()
                    output = execution.communicate(timeout=float(task.time_limit))[0].decode('utf-8')
                    end_time = time.time()
                    finish_time = end_time - start_time
                    logger.info(finish_time*1000)
                    
                    if test.output_data == output:
                        # logger.info(f'{test.task} {test.test_number} - done successfully. Time: {finish_time}, memory: {memory_usage/1024}')
                        logger.info(f'{test.task} {test.test_number} - done successfully.')
                    else:
                        logger.info(f'{test.task} {test.test_number} - done failed')
                except subprocess.TimeoutExpired:
                    end_time = time.time()
                    finish_time = end_time - start_time
                    logger.info(finish_time*1000)
                    logger.info(f'{test.task} {test.test_number} - timeout')
                except MemoryError as me:
                    logger.error(f'{test.task} {test.test_number} - out of memory')
                except Exception as e:
                    logger.error(f'{type(e)} {traceback.format_exc()}')

                # kill all process spawned by user 'judge'
                # os.system("pkill -u judge")

                # Make directly readable / executable again.
                # os.system("chmod 777 src")

                # logger.info("Return Code : "+str(returncode))
        else:
            logger.error(error.decode('utf-8'))
            
    except:
        pass