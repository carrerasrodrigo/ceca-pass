from ceca_pass.models import Project, Password
from django.contrib import admin


class PasswordAdmin(admin.ModelAdmin):
    list_display = ('name', 'variable_name')
    list_filter = ('project', )
    search_fields = ['project__name', 'project__variable_name',
        'name', 'variable_name']

admin.site.register(Password, PasswordAdmin)
admin.site.register(Project)
