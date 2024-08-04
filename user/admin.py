from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, Profile


class Admin(UserAdmin):
    list_display = ('phone', 'email', 'fullName', 'is_active', 'role')
    filter_horizontal = ()
    list_filter = ('is_active', 'role')
    fieldsets = ()
    search_fields = ('phone', 'last_name')
    ordering = ('pk', 'last_name')



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'fullName')
    list_display_links = ('phone', 'fullName')


admin.site.register(User, Admin)

admin.site.register(Profile, ProfileAdmin)
