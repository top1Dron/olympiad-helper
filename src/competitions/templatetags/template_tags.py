from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag
def get_user_problem_status(problem, user):
    return problem.get_user_status(user)


@register.simple_tag
def status_display(status):
    statuses = {
        '': '',
        'PD': _('Pending'),
        'CE': _('Compilation error'),
        'WA': _('Wrong answer'),
        'RE': _('Runtime error'),
        'PA': _('Partially accepted'),
        'TO': _('Timeout'),
        'MO': _('Memory out'),
        'AC': _('Accepted'),
    }
    return statuses[status]


@register.simple_tag
def concat_strings(*args):
    return ''.join(map(str, args))

