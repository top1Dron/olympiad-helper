from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
import competitions.models


STATUS = (
    # '''enum of execution tests results'''
    
    ('PD', _('Pending')),
    ('CE', _('Compilation error')),
    ('WA', _('Wrong answer')),
    ('RE', _('Runtime error')),
    ('PA', _('Partially accepted')),
    ('TO', _('Timeout')),
    ('MO', _('Memory out')),
    ('AC', _('Accepted')),
)
    
 
 
class ProgrammingLanguage(models.Model):
    '''model that describes available for solution submition programming languages'''

    name = models.TextField(_("Programming language"))
    extension = models.CharField(max_length=5)
    compile = models.CharField(max_length=300)
    execute = models.CharField(max_length=300)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('Programming language')
        verbose_name_plural = _('Programming languages')


class Problem(models.Model):
    '''model that describes olympiad problems'''

    DIFFICULTY = (
    #    """enum of problem difficulty"""

        ('VE', _('Very easy')),
        ('EA', _('Easy')),
        ('MD', _('Middle')),
        ('HD', _('Hard')),
        ('VH', _('Very hard')),
    )


    CLASSIFICATION = (
        # """enum of problem classification"""

        ('CB', _('Combinatorics')),
        ('BS', _('Breadth-first-search')),
    )

    number = models.SlugField(max_length=1000, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    description_photo = models.ImageField(null=True, blank=True)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY)
    classification = models.CharField(max_length=2, choices=CLASSIFICATION)
    input_condition = models.CharField(_("Input"), max_length=500)
    output_condition = models.CharField(_("Output"), max_length=500)
    special_warning = models.CharField(_("Warning"), max_length=500, null=True, blank=True)
    memory_limit = models.CharField(max_length=30)
    time_limit = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    competition = models.ForeignKey(
        to=competitions.models.Competition, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='problems')


    def __str__(self):
        return f'{self.competition.title}: {self.title}' if self.competition else self.title


    def get_user_status(self, user):
        try:
            return UserProblemStatus.objects.get(user=user, problem=self).status
        except UserProblemStatus.DoesNotExist:
            return ''
    

    @property
    def get_all_samples(self):
        return ProblemSamples.objects.filter(problem=self.pk)


    @property
    def get_all_tests(self):
        return ProblemTest.objects.filter(problem=self.pk).select_related('problem')


    class Meta:
        verbose_name = _('Problem')
        verbose_name_plural = _('Problems')


class ProblemSamples(models.Model):
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    sample_input = models.TextField(_("Sample input #"))
    sample_output = models.TextField(_("Sample output #"))


    def __str__(self):
        return self.problem.title + '- sample'


    class Meta:
        verbose_name = _('Problem samples')
        verbose_name_plural = _('Problem samples')


class ProblemTest(models.Model):
    '''model that describes Problem validation tests'''

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    test_number = models.IntegerField()
    input_data = models.TextField()
    output_data = models.TextField()


    def __str__(self):
        return f'{self.problem.title} - {self.test_number}'


    class Meta:
        verbose_name = _('Problem tests')
        verbose_name_plural = _('Problem tests')


class Solution(models.Model):
    """model that describes user submitted problem solution"""

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(to=ProgrammingLanguage, on_delete=models.CASCADE)
    solving_date = models.DateTimeField(verbose_name=_('Solving date'), auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS)
    program_code = models.TextField()
    avg_memory_usage = models.CharField(max_length=30)
    avg_time_usage = models.CharField(max_length=30)

    @property
    def get_all_tests(self):
        return SolutionTest.objects.filter(solution=self.id).select_related('solution', 'problem_test')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Solution')
        verbose_name_plural = _('Solutions')
        ordering = ('-solving_date', )
    


class SolutionTest(models.Model):
    '''model that describes passing problem validation tests in solution'''

    solution = models.ForeignKey(to=Solution, on_delete=models.CASCADE)
    problem_test = models.ForeignKey(to=ProblemTest, on_delete=models.CASCADE)
    memory_usage = models.CharField(max_length=30)
    time_usage = models.CharField(max_length=30)
    status = models.CharField(max_length=2, choices=STATUS)

    def __str__(self):
        return f'{self.solution.id} - {self.problem_test.test_number}'

    @property
    def test_number(self):
        return self.problem_test.test_number

    class Meta:
        verbose_name = _('Solution tests')
        verbose_name_plural = _('Solution tests')
        unique_together = ('solution', 'problem_test')


class ProblemComment(models.Model):
    '''model that describes comments from successfully passed Problem users for Problem'''

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(_("Publication date"), auto_now=True)


class UserProblemStatus(models.Model):
    '''model that describes status of solving the problem by user'''

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS)


    class Meta:
        verbose_name = _('User problem status')
        verbose_name_plural = _('User problem statuses')
        unique_together = ('user', 'problem')
