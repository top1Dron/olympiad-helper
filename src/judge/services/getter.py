from django.conf import settings
from django.db.models import Q
from judge.models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage

import logging

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)

def get_all_available_problems():
    '''
    returns querydict of all problems with is_active=True
    '''
    return Problem.objects.filter(is_active=True, competition=None).order_by('number')


def get_all_submissions():
    '''
    returns all submitted problem solutions, where problems not in competitions
    '''
    return Solution.objects.filter(problem__in=Problem.objects.filter(competition=None))


def get_competition_submissions(competition_id):
    '''
    returns all submitted problem solutions, where problems in given competition
    '''
    return Solution.objects.filter(problem__in=Problem.objects.filter(competition=competition_id)).order_by('-solving_date')


def get_problem_by_number(number):
    '''
    returns problem by unique number
    '''
    return Problem.objects.get(number=number)


def get_or_copy_problem_to_competition(problem, competition):
    '''
    returns or creates new problem with given competition
    '''
    return Problem.objects.get_or_create(number=f'{competition.pk}_{problem.number}', defaults={
        'title': problem.title,
        'description': problem.description,
        'difficulty': problem.difficulty,
        'classification': problem.classification,
        'input_condition': problem.input_condition,
        'output_condition': problem.output_condition,
        'special_warning': problem.special_warning,
        'memory_limit': problem.memory_limit,
        'time_limit': problem.time_limit,
        'is_active': problem.is_active,
        'competition': competition
    })
        


def get_solution_by_id(id):
    '''
    returns solution by id
    '''
    return Solution.objects.get(pk=id)


def get_filtered_problems(filter_parameter):
    '''
    returns problems with entered filtered parameters in search field
    '''

    return get_all_available_problems().filter(
        Q(title_uk__icontains=filter_parameter) | 
        Q(title_en__icontains=filter_parameter) |
        Q(number__icontains=filter_parameter)
    )


def get_empty_problem_set():
    return Problem.objects.none()