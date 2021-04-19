from django.contrib import admin
from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples, UserProblemStatus


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'difficulty', 'is_active')
    list_display_links = ('title',)
    search_fields = ('title', )


admin.site.register(ProgrammingLanguage)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSamples)
admin.site.register(Solution)
admin.site.register(SolutionTest)
admin.site.register(ProblemTest)
admin.site.register(UserProblemStatus)