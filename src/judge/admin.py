from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples, UserProblemStatus


@admin.register(Problem)
class ProblemAdmin(TranslationAdmin):
    list_display = ('title_uk', 'difficulty', 'is_active', 'competition')
    list_display_links = ('title_uk',)
    search_fields = ('title', )


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension', 'compile', 'execute')
    list_display_links = ('name',)


@admin.register(ProblemSamples)
class ProblemSamplesAdmin(TranslationAdmin):
    list_display = ('problem', 'sample_input', 'sample_output')


admin.site.register(Solution)
admin.site.register(SolutionTest)
admin.site.register(ProblemTest)
admin.site.register(UserProblemStatus)