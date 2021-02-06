from django.contrib import admin
from groups.models import Competition, CompetitionProblem, Group, GroupCompetition, Problem

admin.site.register(Competition)
admin.site.register(CompetitionProblem)
admin.site.register(Group)
admin.site.register(GroupCompetition)
admin.site.register(Problem)
