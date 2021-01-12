from django.contrib import admin
from .models import Task, Solution, SolutionTest, TaskTest, ProgrammingLanguage, TaskSamples

admin.site.register(ProgrammingLanguage)
admin.site.register(Task)
admin.site.register(TaskSamples)
admin.site.register(Solution)
admin.site.register(SolutionTest)
admin.site.register(TaskTest)