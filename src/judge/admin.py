from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples, UserProblemStatus


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