from django.urls import path
from . import views
 
 
app_name = 'judge'
 
 
urlpatterns = [
    # path('create/', views.TextCreate.as_view(), name='create'),
    path('language/', views.api_show_language_dropdown, name='language'),
    path('task/<slug:slug>', views.TaskDetailView.as_view(), name='task'),
    path('task/<slug:slug>/submit', views.api_submit_solution, name='submit_solution'),
    # path('check-cpp/', views.)
]