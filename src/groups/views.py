from competitions import services as competition_services
from competitions.forms import CompetitionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, reverse, Http404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, ListView
from groups.forms import GroupForm
from groups.models import Group
from groups.services import services
import logging


logger = logging.getLogger(__name__)


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_create.html'
    context_object_name = 'group'


    def get_success_url(self):
        services.add_user_to_group(
            group=self.object,
            user=self.request.user,
            role='TE'
        )
        return reverse('groups:group_list')


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template = 'group/group_detail.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get('group_id', None)
        try:
            return services.get_group_by_id(id)
        except:
            raise Http404(_('Group not found'))


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'


    def get_queryset(self, *args, **kwargs):
        logger.info(services.get_user_groups(user=self.request.user))
        return services.get_user_groups(user=self.request.user)


@login_required
def create_group_competition(request, group_id:int):
    if request.method == 'POST':
        form = CompetitionForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.group = services.get_group_by_id(group_id)
            form.save()
            return redirect(reverse('groups:group_detail', kwargs={'group_id':group_id}))
    else:
        form = CompetitionForm()
    data = {'tab-data': render_to_string(
        'groups/competition_create.html', {
            'group': services.get_group_by_id(group_id),
            'form': form,
        }, request).replace('\n', '')
    }
    return JsonResponse(data)


@login_required
def get_group_competitions(request, group_id:int):
    competitions = competition_services.get_group_competitions(group_id)
    data = {'tab-data': render_to_string( 
        'groups/group_detail_competitions_tab.html', {
            'competitions':competitions,
            'group_id': group_id,
        }, request).replace('\n', '')
    }
    return JsonResponse(data)


@login_required
def get_group_info(request, group_id:int):
    group = services.get_group_by_id(group_id)
    active_competitions = competition_services.get_active_group_competitions(group_id)

    return JsonResponse({'tab-data':render_to_string('groups/group_detail_group_tab.html', {
        'group': group,
        'competitions': active_competitions,
    }, request).replace('\n', '')})


@login_required
def get_group_members(request, group_id:int):
    group_members = services.get_group_members(group_id)
    user_role = services.get_user_role_in_group(group_id, request.user)
    data = {'tab-data': render_to_string(
        'groups/group_detail_members_tab.html', {
            'group_members': group_members,
            'group_id': group_id,
            'user_role': user_role,
        }, request).replace('\n', '')
    }
    return JsonResponse(data)


@login_required
def create_invite_link_to_group(request, group_id):
    pass
    