from modeltranslation.translator import register, TranslationOptions
from .models import Problem, Solution, SolutionTest, ProblemTest, ProgrammingLanguage, ProblemSamples, UserProblemStatus


@register(Problem)
class ProblemTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'difficulty', 'classification', 'input_condition', 'output_condition', 'special_warning')


@register(ProblemSamples)
class ProblemSamplesTranslationOptions(TranslationOptions):
    fields = ('sample_input', 'sample_output')