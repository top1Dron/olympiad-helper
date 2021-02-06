from django.conf import settings
from judge.models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage

import logging

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)

def get_all_available_problems():
    '''
    returns querydict of all problems with is_active=True
    '''
    return Problem.objects.filter(is_active=True)


def get_all_submissions():
    '''
    returns all submitted problem solutions
    '''
    return Solution.objects.all()


def get_problem_by_number(number):
    '''
    returns problem by unique number
    '''
    return Problem.objects.get(number=number)


def get_solution_by_id(id):
    '''
    returns solution by id
    '''
    return Solution.objects.get(pk=id)