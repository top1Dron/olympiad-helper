from django.conf import settings
from judge.models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage

import logging

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)

def get_all_available_problems():
    '''
    returns querydict of all problems with is_active=True
    '''
    return Problem.objects.filter(is_active=True, competition=None)


def get_all_submissions():
    '''
    returns all submitted problem solutions, where problems not in competitions
    '''
    return Solution.objects.filter(problem__in=Problem.objects.filter(competition=None))


def get_competition_submissions(competition_id):
    '''
    returns all submitted problem solutions, where problems in given competition
    '''
    return Solution.objects.filter(problem__in=Problem.objects.filter(competition=competition_id))


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