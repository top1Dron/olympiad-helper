from django.conf import settings
from judge.models import Task, Solution, SolutionTest, TaskTest, ProgrammingLanguage

import logging

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)

def get_all_available_tasks():
    '''
    returns querydict of all tasks with is_active=True
    '''
    return Task.objects.filter(is_active=True)


def get_all_submissions():
    '''
    returns all submitted problem solutions
    '''
    return Solution.objects.all()


def get_task_by_number(number):
    '''
    returns task by unique number
    '''
    return Task.objects.get(number=number)


def get_solution_by_id(id):
    '''
    returns solution by id
    '''
    return Solution.objects.get(pk=id)