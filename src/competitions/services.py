from collections import OrderedDict
from competitions.models import Competition
from django.db.models import Q, Count, F
from django.utils import timezone
from groups.services import services as group_services
from judge.models import Problem, UserProblemStatus
from judge.services import getter as judge_getter
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


def get_all_available_competitions(*, user):
    not_in_group_competitions = get_competitions_which_is_not_in_group().select_related('group')
    if str(user) == 'AnonymousUser':
        return not_in_group_competitions
    else:
        return Competition.objects.filter(
            Q(group__in=group_services.get_user_groups(user=user), 
                start_date__lte=timezone.now(), end_date__gte=timezone.now()) | 
            Q(pk__in=(competition.id for competition in not_in_group_competitions))
        )


def get_competitions_which_is_not_in_group():
    return Competition.objects.filter(group=None, start_date__lte=timezone.now(), end_date__gte=timezone.now())


def get_competition_by_id(id):
    try:
        return Competition.objects.get(pk=id)
    except:
        return None


def get_group_competitions(group_id):
    return Competition.objects.filter(group=group_services.get_group_by_id(group_id))


def get_active_group_competitions(group_id):
    group_competitions = get_group_competitions(group_id)
    return group_competitions.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())


def get_competition_problems(competition_id):
    return Problem.objects.filter(competition=competition_id).order_by('title')


def is_group_teacher(competition, user):
    user_role = group_services.get_user_role_in_group(competition.group.id, user)
    return True if user_role == 'TE' else False


def get_competition_problem(slug):
    return Problem.objects.get(number=slug)


def is_competition_active(id):
    competition = get_competition_by_id(id)
    current_time = timezone.now()
    if competition.start_date < current_time:
        if competition.end_date > current_time:
            return True
    return False


def is_competition_active_for_edit_problems(id):
    competition = get_competition_by_id(id)
    current_time = timezone.now()
    if competition.start_date > current_time:
        return True
    return False


def get_user_status_on_problems_in_competition(problem_number, user):
    problem = judge_getter.get_problem_by_number(problem_number)
    try:
        return UserProblemStatus.objects.get(problem=problem, user=user).status
    except UserProblemStatus.DoesNotExist:
        return ''


def add_problem_to_competition(*, competition, problem):
    new_competition_problem, creation_result = judge_getter.get_or_copy_problem_to_competition(problem, competition)
    if creation_result:
        for problem_sample in problem.get_all_samples:
            new_competition_problem.problemsamples_set.create(
                sample_input=problem_sample.sample_input,
                sample_output=problem_sample.sample_output
            )

        for problem_test in problem.get_all_tests:
            new_competition_problem.problemtest_set.create(
                test_number=problem_test.test_number,
                input_data=problem_test.input_data,
                output_data=problem_test.output_data
            )
    return creation_result
    

def get_competition_leaderboard(competition_id):
    '''
    return leaderboard of gived competition
    as ordered dict with keys: user__username and solved_problems_count
    '''
    users_count = OrderedDict()
    competition = get_competition_by_id(competition_id)
    for ups in \
        UserProblemStatus.objects.filter(problem__competition__pk=competition_id,
            status='AC').values('user__username'
                                ).annotate(solved_problems_count=Count('user__username'
            )).order_by('-solved_problems_count'):
        users_count[ups['user__username']] = ups['solved_problems_count']
    return users_count


def get_five_ending_soon_competitions(*, user):
    end_date = F('end_date')
    return get_all_available_competitions(user=user).order_by(end_date)[:5]