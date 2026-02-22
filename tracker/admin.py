from django.contrib import admin
from .models import Project, Task

# Branding
admin.site.site_header = "CodeSoft Manager Portal"
admin.site.index_title = "Workspace Management"

# We use "Media" inside the classes to link the CSS
class CodeSoftAdminStyles:
    css = {
        'all': ('admin/css/custom_admin.css',)
    }

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to')
    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}