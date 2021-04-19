from competitions import views
from django.urls import path


app_name = 'competitions'


urlpatterns = [
    path('create/', views.CompetitionCreateView.as_view(), name='competition_create'),
    path('list/', views.CompetitionListView.as_view(), name='competition_list'),
    path('<int:pk>/', views.CompetitionDetailView.as_view(), name='competition_detail'),
    path('<int:pk>/leaderboard/', views.get_competition_leaderboard, name='get_competition_leaderboard'),
    path('<int:pk>/problems/', views.get_competition_problems, name='competition_problems'),
    path('<int:pk>/problems/add_or_find_problem', views.ajax_add_or_find_problem_to_competition, name='add_or_find_problem'),
    path('<int:pk>/problems/search/>', views.problem_list_in_search, name='search_problem'),
    path('<int:pk>/problems/<slug:slug>/', views.ProblemDetailView.as_view(), name='competition_problem_detail'),
    path('<int:pk>/problems/<slug:problem_number>/status/', views.get_user_status_on_problems_in_competition, name='get_user_problem_status'),
    path('<int:pk>/problems/<slug:slug>/submit/', views.api_submit_solution, name='submit_solution'),
    path('<int:pk>/solutions/list/', views.get_competition_solutions, name='competition_solution_list'),
]
