from competitions.models import Competition
from django.db.models import Q
from django.utils import timezone
from groups.services import services as group_services
from judge.models import Problem


def get_all_available_competitions(*, user):
    not_in_group_competitions = get_competitions_which_is_not_in_group()
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
    return Problem.objects.filter(competition=competition_id)


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