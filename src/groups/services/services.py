from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import reverse
from groups.models import GroupUser, Group
from urlshortening.models import get_short_url, get_full_url
from users.models import CustomUser
import six


def add_user_to_group(*, group, user, role):
    GroupUser.objects.get_or_create(group=group, user=user, defaults={
        'group': group,
        'user': user,
        'role': role
    })


def get_user_groups(*, user):
    return Group.objects.filter(pk__in=(user_group.group.id for user_group in GroupUser.objects.filter(user=user)))


def get_group_by_id(id):
    return Group.objects.get(pk=id)


def get_group_members(group_id):
    return GroupUser.objects.filter(group=get_group_by_id(group_id))


def get_user_role_in_group(group_id, user):
    return GroupUser.objects.get(group=get_group_by_id(group_id), user=user).role


def delete_user_from_group(group_user_id):
    group_user = GroupUser.objects.get(pk=group_user_id)
    group_user.delete()



def get_group_invite_link(scheme, group_id, domain):
    group_uid = urlsafe_base64_encode(force_bytes(group_id))
    invite_link = f"{scheme}://{domain}{reverse('groups:group_join_confirm', kwargs={'group_id': group_id})}"
    short_invite_url = get_short_url(invite_link)
    return f'{scheme}://{domain}/{short_invite_url.short_id}/'


def get_full_url(short_id):
    return get_full_url(short_id)