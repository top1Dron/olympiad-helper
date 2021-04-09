from competitions.forms import CompetitionForm
from competitions.models import Competition
from competitions import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, reverse, Http404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView, DetailView
from judge.models import Problem, Solution
from judge.tasks import task_submit_solution
from judge.forms import SubmitSolutionForm
from judge.services import execute_solutions, getter
import logging


logger = logging.getLogger(__name__)


class CompetitionCreateView(LoginRequiredMixin, CreateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'competitions/competition_create.html'
    context_object_name = 'competition'


    def get_success_url(self):
        return reverse('competitions:competition_list')


class CompetitionListView(ListView):
    model = Competition
    template_name = 'competitions/competition_list.html'
    context_object_name = 'competitions'


    def get_queryset(self, *args, **kwargs):
        logger.info(services.get_all_available_competitions(user=self.request.user))
        return services.get_all_available_competitions(user=self.request.user)


class CompetitionDetailView(DetailView):
    model = Competition
    template = 'competitions/competition_detail.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk', None)
        try:
            return services.get_competition_by_id(id)
        except:
            raise Http404(_('Competition not found'))

    
    def get_context_data(self, **kwargs):
        context = super(CompetitionDetailView, self).get_context_data(**kwargs)
        context['is_competition_in_group'] = True if self.object.group != None else False
        context['is_group_teacher'] = False if not context.get('is_competition_in_group') else services.is_group_teacher(self.object, self.request.user)
        logger.info(context)
        return context


def get_competition_problems(request, pk):
    problems = services.get_competition_problems(pk)
    competition = services.get_competition_by_id(pk)
    data = {}
    context = {
        'competition_id': pk,
        'problems': problems,
        'is_competition_in_group': True if competition.group != None else False,
        'is_group_teacher': False
    }
    if context['is_competition_in_group']:
        context['is_group_teacher'] = services.is_group_teacher(competition, request.user)
    data['tab-data'] = render_to_string(
        'competitions/competition_problems.html',
        context,
        request
    )
    return JsonResponse(data)


@login_required
def get_competition_solutions(request, pk):
    data = {
        'tab-data': render_to_string(
            'competition_problems/solution_list.html',
            {
                'solutions': getter.get_competition_submissions(competition_id=pk)
            },
            request
        )
    }
    return JsonResponse(data)


class ProblemDetailView(DetailView):
    model = Problem
    slug_field = 'number'
    template_name = 'competition_problems/problem_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return services.get_competition_problem(slug)
        except:
            raise Http404(_('Problem not found'))


    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        context['competition'] = self.object.competition
        context['is_active_for_submit'] = services.is_competition_active(self.object.competition.id)
        return context


@login_required
def api_submit_solution(request, pk, slug):
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
    return render(request, 'competition_problems/submit_solution.html', {'form': form, 'problem_number': slug})