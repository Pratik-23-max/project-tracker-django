from django.contrib import admin
from .models import Project, Task

admin.site.site_header = "CodeSoft Manager Portal"
admin.site.index_title = "Workspace Management"

class CodeSoftMedia:
    css = {'all': ('admin/css/custom_admin.css',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    Media = CodeSoftMedia

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to')
    Media = CodeSoftMedia