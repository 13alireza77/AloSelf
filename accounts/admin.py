from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'email', 'is_superuser')
    list_filter = ('is_superuser', 'is_active')

    fieldsets = (
        (None,
         {'fields': ('phone', 'email', 'ida', 'date_joined',)}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'description': "phone and password for admin\nphone and ida for staff user",
            'classes': ('wide',),
            'fields': ('phone', 'email', 'ida', 'full_name', 'is_superuser')
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )
    search_fields = ('phone', 'email', 'ida',)
    ordering = ('phone', 'email')
    filter_horizontal = ()


class profileAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, profileAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
