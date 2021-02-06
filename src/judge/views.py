from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from judge.services import getter, execute_solutions
from .forms import LanguageForm, SubmitSolutionForm
from .models import Problem, Solution
from .tasks import task_submit_solution
 
import logging
 

logger = logging.getLogger(__name__)


@login_required
def api_show_language_dropdown(request):
    if request.method == 'GET':
        language_form = LanguageForm()
    return render(request, 'judge/language.html', {'form': language_form})


class ProblemListView(ListView):
    model = Problem
    template_name = 'judge/problem_list.html'
    queryset = getter.get_all_available_problems()
    context_object_name = 'problems'
    # paginate_by = 10


class ProblemDetailView(DetailView):
    model = Problem
    slug_field = 'number'
    template = 'judge/problem_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return getter.get_problem_by_number(slug)
        except:
            raise Http404(_('Problem not found'))

@login_required
def api_submit_solution(request, slug):
    if request.method == 'POST':
        form = SubmitSolutionForm(request.POST)
        if form.is_valid():
            solution_id = execute_solutions.create_solution(
                user=request.user,
                problem_number=request.POST.get('problem_number'),
                programming_language=request.POST.get('programming_language'),
                source_code=request.POST.get('source_code')
            )
            task_submit_solution.delay(
                problem_number=request.POST.get('problem_number'),
                programming_language=request.POST.get('programming_language'),
                source_code=request.POST.get('source_code'),
                solution_id=solution_id
            )
            return redirect(reverse('judge:solution_detail', kwargs={'id':solution_id}))
    else:
        form = SubmitSolutionForm()
    return render(request, 'judge/submit_solution.html', {'form': form, 'problem_number': slug})


class SolutionDetailView(DetailView):
    model = Solution
    template = 'judge/solution_detail.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', None)
        try:
            return getter.get_solution_by_id(id)
        except:
            raise Http404(_('Solution not found'))


class SolutionListView(ListView):
    model = Solution
    template_name = 'judge/solution_list.html'
    queryset = getter.get_all_submissions()
    context_object_name = 'solutions'