from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from groups.forms import GroupForm


class GroupCreateView(CreateView):
    form = GroupForm