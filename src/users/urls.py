from django.urls import path
from . import views
 
 
app_name = 'users'
 
 
urlpatterns = [
    path('login_or_signup/', views.api_get_login_and_register_user, name='login_or_signup'),
    path('signup/', views.api_signup_user, name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('login/', views.api_login_user, name='login'),
    path('logout/', views.api_logout_user, name='logout'),

    # path('create/', views.TextCreate.as_view(), name='create'),
]