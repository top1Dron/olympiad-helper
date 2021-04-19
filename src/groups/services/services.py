from groups.models import GroupUser, Group
from users.models import CustomUser
import six


def add_user_to_group(*, group, user, role):
    GroupUser.objects.create(group=group, user=user, role=role)


def get_user_groups(*, user):
    return Group.objects.filter(pk__in=(user_group.group.id for user_group in GroupUser.objects.filter(user=user)))


def get_group_by_id(id):
    return Group.objects.get(pk=id)


def get_group_members(group_id):
    return GroupUser.objects.filter(group=get_group_by_id(group_id))


def get_user_role_in_group(group_id, user):
    return GroupUser.objects.get(group=get_group_by_id(group_id), user=user).role


def create_invite_link(group_id):
    group_uuid = six.text_type(group_id) + six.text_type('SD')
    
    print(group_id)