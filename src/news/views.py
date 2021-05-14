from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news import services
from competitions import services as competition_services
import logging

logger = logging.getLogger(__name__)


class NewsListView(ListView):
    template_name = 'news/index.html'
    queryset = services.get_last_news()
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competitions'] = competition_services.get_five_ending_soon_competitions(user=self.request.user)
        return context
    