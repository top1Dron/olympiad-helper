from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


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
    )

    number = models.SlugField(max_length=10, unique=True)
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


    def __str__(self):
        return self.title
    

    @property
    def get_all_samples(self):
        return ProblemSamples.objects.filter(problem=self.pk)


    @property
    def get_all_tests(self):
        return ProblemTest.objects.filter(problem=self.pk)


class ProblemSamples(models.Model):
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    sample_input = models.TextField(_("Sample input #"))
    sample_output = models.TextField(_("Sample output #"))


    def __str__(self):
        return self.problem.title + '- sample'


class ProblemTest(models.Model):
    '''model that describes Problem validation tests'''

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    test_number = models.IntegerField()
    input_data = models.TextField()
    output_data = models.TextField()


    def __str__(self):
        return f'{self.problem.title} - {self.test_number}'


class Solution(models.Model):
    """model that describes user submitted problem solution"""

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(to=ProgrammingLanguage, on_delete=models.CASCADE)
    solving_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS)
    program_code = models.TextField()
    avg_memory_usage = models.CharField(max_length=30)
    avg_time_usage = models.CharField(max_length=30)


    @property
    def get_all_tests(self):
        return SolutionTest.objects.filter(solution=self.id)


    def __str__(self):
        return str(self.pk)
    


class SolutionTest(models.Model):
    '''model that describes passing problem validation tests in solution'''

    solution = models.ForeignKey(to=Solution, on_delete=models.CASCADE)
    problem_test = models.ForeignKey(to=ProblemTest, on_delete=models.CASCADE)
    memory_usage = models.CharField(max_length=30)
    time_usage = models.CharField(max_length=30)
    status = models.CharField(max_length=2, choices=STATUS)


    def __str__(self):
        return f'{self.solution.id} - {self.problem_test.test_number}'


class ProblemComment(models.Model):
    '''model that describes comments from successfully passed Problem users for Problem'''

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(_("Publication date"), auto_now=True)
