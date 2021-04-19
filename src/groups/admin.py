from django.contrib import admin
from groups.models import Group, GroupUser


admin.site.register(Group)
admin.site.register(GroupUser)
