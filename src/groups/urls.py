from django.urls import path
from groups import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.GroupCreateView.as_view(), name='group_create'),
    path('list/', views.GroupListView.as_view(), name='group_list'),
    path('<int:group_id>/info/', views.get_group_info, name='get_group_info'),
    # path('<int:group_id>/members/create-invite-link-to-group/', views.create_invite_link_to_group, name='create_invite_link_to_group'),
    path('<int:group_id>/members/<int:group_user_id>/delete/', views.delete_user_from_group, name='delete_user_from_group'),
    path('<int:group_id>/members/', views.get_group_members, name='get_group_members'),
    path('<int:group_id>/confirm_joining/', views.confirm_user_joining_the_group, name='group_join_confirm'),
    path('<int:group_id>/competitions/create-competition/', views.create_group_competition, name='create_competition'),
    path('<int:group_id>/competitions/', views.get_group_competitions, name='get_group_competitions'),
    path('<int:group_id>/', views.GroupDetailView.as_view(), name='group_detail'),
]
