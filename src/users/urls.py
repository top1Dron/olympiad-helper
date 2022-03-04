from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
 
 
app_name = 'users'
 
 
urlpatterns = [
    path('login_or_signup/', views.api_get_login_and_register_user, name='login_or_signup'),
    path('signup/', views.api_signup_user, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.api_activate_account, name='activate_account'),
    path('login/', views.api_login_user, name='login'),
    path('logout/', views.api_logout_user, name='logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_user_profile, name='edit_profile'),
    # path('reset/<str:uidb64>/<str:token>', name='password_reset_confirm'),
    # path('reset/done', name='password_reset_complete'),
]