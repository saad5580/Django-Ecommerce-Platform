from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = () 
    list_filter = ()
    fieldsets = (
        # (None, {'fields': ('email', 'first_name', 'last_name', 'username', 'password')}),
        # ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # # Update this as well if you have custom fields to include when creating a user
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin')}
    #     ),
    # )

admin.site.register(Account, AccountAdmin)

