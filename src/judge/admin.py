from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples, UserProblemStatus
from .services import getter


@admin.register(Problem)
class ProblemAdmin(TranslationAdmin):
    list_display = ('title_uk', 'difficulty', 'is_active', 'competition', 'view_tests_link')
    list_display_links = ('title_uk',)
    search_fields = ('title', )

    def view_tests_link(self, obj):
        count = obj.get_all_tests.count()
        url = (
            reverse('admin:judge_problemtest_changelist')
            + '?'
            + urlencode({'problem__id': f'obj.id'})
        )
        return format_html('<a href="{}">{} tests</a>', url, count)
    
    view_tests_link.short_description = _('Tests')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('competition')


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension', 'compile', 'execute')
    list_display_links = ('name',)


@admin.register(ProblemSamples)
class ProblemSamplesAdmin(TranslationAdmin):
    list_display = ('problem', 'sample_input', 'sample_output')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('problem')


@admin.register(SolutionTest)
class SolutionTestAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('problem_test', 'solution')


@admin.register(ProblemTest)
class ProblemTestAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('problem')


admin.site.register(Solution)
admin.site.register(UserProblemStatus)