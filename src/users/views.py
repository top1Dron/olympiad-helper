import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views as auth_views, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserCreationForm, LoginForm, CustomPasswordResetForm, PasswordResetConfirmForm, CustomUserChangeForm
from .services import get_and_activate_user, get_user_by_email, get_user_by_username
from .tasks import task_send_email
from .tokens import account_activation_token


logger = logging.getLogger(__name__)

def api_get_login_and_register_user(request, signup=False):
    signup_form = CustomUserCreationForm()
    login_form = LoginForm()
    return render(request, 'users/log.html', context={'signup_form': signup_form, 'login_form': login_form, 'signup':signup})


def api_login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.POST.get('next')
            if redirect_to:
                return redirect(redirect_to)
            return redirect(reverse('judge:problem_list'))
        else:
            user = get_user_by_email(email)
            if user is not None and user.is_active == False:
                messages.error(request, _('User is not active!'))
            else:
                messages.error(request, _('User with inputed email and password is not exists!'))
            login_form = LoginForm(request.POST)
            signup_form = CustomUserCreationForm()
            return render(request, 'users/log.html', context={'signup_form': signup_form, 'login_form': login_form, 'signup':False})


@login_required
def api_logout_user(request):
    logout(request)
    return redirect(reverse('judge:problem_list'))


def api_signup_user(request):
    if request.method == 'POST':
        # logger.info(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            logger.info(current_site.domain)
            mail_subject = _('Activate your account.')
            message = render_to_string(
                'users/account_activate_email.html',
                {
                    'user': user,
                    'scheme': request.scheme,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            to_email = form.cleaned_data.get('email')
            task_send_email.delay(subject=mail_subject, message=message, to=[to_email])
            messages.info(request, _('Please, confirm your email address to complete the registration and login from this page! If you don\'t receive the email, check the spam folder!'))
            return redirect(reverse('users:login_or_signup'))
        else:
            login_form = LoginForm()
            return render(request, 'users/log.html', context={'signup_form': form, 'login_form': login_form, 'signup':True})


def api_activate_account(request, uidb64, token):
    if get_and_activate_user(urlsafe_base64_decode(uidb64), token):
        messages.success(request, _('Successfully account activation. Now you can login to your account!'))
    else:
        messages.error(request, _('Activation link is invalid!'))
    return api_get_login_and_register_user(request)


def user_profile(request, username):
    user = get_user_by_username(username)
    return render(request, 'users/profile.html', {'user': user})


def edit_user_profile(request, username):
    form = CustomUserChangeForm(instance=get_user_by_username(username))
    # password_form = auth_forms.SetPasswordForm(user=get_user_by_username(username))
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=get_user_by_username(username))
        if form.is_valid():
            logger.info(form.is_valid())
            form.save()
            # password_form.save()
            return redirect(reverse_lazy('users:profile', kwargs={'username': username}))
        else:
            logger.info(form.is_valid())
            logger.info(form.errors)
    return render(request, 'users/edit_profile.html', {'form': form})


class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name='users/password_reset_email.html'
    success_url=reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm
    

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'