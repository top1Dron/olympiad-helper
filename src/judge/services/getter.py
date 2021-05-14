from django.conf import settings
from django.db import connection
from django.db.models import Q, QuerySet
from judge.models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage

import logging

logger = logging.getLogger(__name__)

# logging.disabled(logging.DEBUG)

def get_all_available_problems():
    '''
    returns queryset of all problems with is_active=True
    '''
    return Problem.objects.filter(is_active=True, competition=None).order_by('number')


def get_all_submissions():
    '''
    returns all submitted problem solutions, where problems not in competitions
    '''
    return Solution.objects.filter(
        problem__in=Problem.objects.filter(competition=None)
        ).select_related('user', 'problem', 'language')


def get_competition_submissions(competition_id: int):
    '''
    returns all submitted problem solutions, where problems in given competition
    '''
    return Solution.objects.filter(problem__in=Problem.objects.filter(
        competition=competition_id)
        ).order_by('-solving_date').select_related('user', 'problem', 'language')


def get_problem_by_number(number: str):
    '''
    returns problem by unique number
    '''
    return Problem.objects.get(number=number)


def get_or_copy_problem_to_competition(problem: Problem, competition):
    '''
    returns or creates new problem with given competition
    '''
    return Problem.objects.get_or_create(number=f'{competition.pk}_{problem.number}', defaults={
        'title': problem.title,
        'title_en': problem.title_en,
        'title_uk': problem.title_uk,
        'description': problem.description,
        'description_en': problem.description_en,
        'description_uk': problem.description_uk,
        'description_photo': problem.description_photo,
        'difficulty': problem.difficulty,
        'difficulty_en': problem.difficulty_en,
        'difficulty_uk': problem.difficulty_uk,
        'classification': problem.classification,
        'classification_en': problem.classification_en,
        'classification_uk': problem.classification_uk,
        'input_condition': problem.input_condition,
        'input_condition_en': problem.input_condition_en,
        'input_condition_uk': problem.input_condition_uk,
        'output_condition': problem.output_condition,
        'output_condition_uk': problem.output_condition_uk,
        'output_condition_en': problem.output_condition_en,
        'special_warning': problem.special_warning,
        'special_warning_en': problem.special_warning_en,
        'special_warning_uk': problem.special_warning_uk,
        'memory_limit': problem.memory_limit,
        'time_limit': problem.time_limit,
        'is_active': problem.is_active,
        'competition': competition
    })
        


def get_solution_by_id(id: int):
    '''
    returns solution by id
    '''
    return Solution.objects.get(pk=id)


def get_filtered_problems(filter_parameter: str):
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


def delete_problem(problem_number:str):
    problem = get_problem_by_number(problem_number)
    problem.delete()


def get_most_solvable_problems():
    with connection.cursor() as cursor:
        cursor.execute('SELECT problem_number, problem_title, solved_count, persent_of_resolve FROM "get_most_solvable_problems"();')
        return cursor.fetchall()


def get_most_unsolvable_problems():
    with connection.cursor() as cursor:
        cursor.execute('SELECT problem_number, problem_title, solved_count, persent_of_resolve FROM "get_most_unsolvable_problems"();')
        return cursor.fetchall()


def get_context_with_pagination_settings(*, context: dict):
    '''
    return context with pagination settings
    maximum pages = 10
    '''

    if not context.get('is_paginated', False):
        return context

    paginator = context.get('paginator')
    num_pages = paginator.num_pages
    current_page = context.get('page_obj')
    page_no = current_page.number

    if num_pages <= 10 or page_no <= 6: 
        pages = [x for x in range(1, min(num_pages + 1, 11))]
    elif page_no > num_pages - 6:
        pages = [x for x in range(num_pages - 9, num_pages + 1)]
    else:
        pages = [x for x in range(page_no - 5, page_no + 5)]

    context.update({'pages': pages})
    return context


def get_problems_by_classification(*, problems, classification: str):
    if classification == '':
        return problems
    return problems.filter(classification=classification[:2])


def get_problems_by_difficulty(*, problems, difficulty: str):
    if difficulty == '':
        return problems
    return problems.filter(difficulty=difficulty[:2])