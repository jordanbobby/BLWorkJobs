from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from jobs.models import Member
from jobs.models import WorkJob
from jobs.models import Position

class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'

class UserAdmin(UserAdmin):
    inlines = (MemberInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(WorkJob)
admin.site.register(Position)

