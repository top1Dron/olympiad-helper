from django.contrib import admin
from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples

admin.site.register(ProgrammingLanguage)
admin.site.register(Problem)
admin.site.register(ProblemSamples)
admin.site.register(Solution)
admin.site.register(SolutionTest)
admin.site.register(ProblemTest)