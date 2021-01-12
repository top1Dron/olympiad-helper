from django.conf import settings
from .memory_test import display_top
from .models import Task, Solution, SolutionTest, TaskTest, ProgrammingLanguage

import difflib
import logging
import os
import subprocess
import functools
import time
import tracemalloc

logger = logging.getLogger(__name__)

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

    tests = TaskTest.objects.filter(task=task_number).filter(language=programming_language)
    

    try:
        cfile = os.path.join(settings.MEDIA_ROOT, 'main.cpp')
        ofile = os.path.join(settings.MEDIA_ROOT, 'main')
        efile = os.path.join(settings.MEDIA_ROOT, 'main.exe')
        
        command_string = 'g++ ' + cfile + ' -o ' + ofile
        error_message = ''
        compile = subprocess.Popen(['/usr/bin/g++', "-o", ofile, cfile], stderr=subprocess.PIPE)
        # grep VmPeak /proc/$PID/status
        error = compile.communicate()[1]
        if error.decode('utf-8') == '':
            for test in tests:
                start_time = time.time()
                tracemalloc.start()
                # execution = subprocess.Popen(['/usr/bin/time', '-f "%e"', ofile, '$res2,', '$res3'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                execution = subprocess.Popen([ofile,], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                execution.stdin.write(bytes(test.input_data, 'UTF-8'))
                execution.stdin.flush()
                # finish_time = time.time() - start_time
                # snapshot = tracemalloc.take_snapshot()
                # memory_usage = display_top(snapshot)
                test.output_data = test.output_data.replace('\r', '')
                if test.output_data == execution.communicate()[0].decode('utf-8'):
                    # logger.info(f'{test.task} {test.test_number} - done successfully. Time: {finish_time}, memory: {memory_usage/1024}')
                    logger.info(f'{test.task} {test.test_number} - done successfully.')
                else:
                    logger.info(f'{test.task} {test.test_number} - done failed')
        else:
            logger.info(error.decode('utf-8'))
            
    except:
        pass