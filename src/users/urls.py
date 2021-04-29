from django.urls import path
from . import views
 
 
app_name = 'users'
 
 
urlpatterns = [
    path('login_or_signup/', views.api_get_login_and_register_user, name='login_or_signup'),
    path('signup/', views.api_signup_user, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.api_activate_account, name='activate_account'),
    path('login/', views.api_login_user, name='login'),
    path('logout/', views.api_logout_user, name='logout'),
    path('<str:username>/', views.user_profile, name='profile'),
    # path('password_reset/', views.api_password_reset name='password_reset'),
    # path('reset/<str:uidb64>/<str:token>', name='password_reset_confirm'),
    # path('reset/done', name='password_reset_complete'),
]