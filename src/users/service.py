from .models import CustomUser
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail

def send_email(subject:str, message:str, to:list):
    '''
    function for send email
    '''
    send_mail(
        subject, 
        message, 
        settings.EMAIL_HOST_USER, 
        list(to),
        fail_silently=False,
    )


def get_and_activate_user(uid, token) -> bool:
    '''
    function for confirming email confirmation
    '''
    try:
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    else:
        return False


def get_user_by_email(email):
    user = CustomUser.objects.get(email=email)
    if user is not None:
        return user
    else:
        return None