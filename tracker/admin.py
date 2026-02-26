from django.contrib import admin
from .models import Project, Task

# Branding
admin.site.site_header = "CodeSoft Manager Portal"
admin.site.site_title = "CodeSoft Admin"
admin.site.index_title = "Workspace Management"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Since your Project model has 'manager', we use that. 
    # If you haven't added a 'title' field to the Project model yet, 
    # we display 'id' or 'manager'.
    list_display = ('id', 'manager') 
    
    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # These names must match your Task model exactly (title, project, assigned_to, status)
    list_display = ('title', 'project', 'assigned_to', 'status')
    list_filter = ('status', 'project') # Adds a professional filter sidebar
    search_fields = ('title',) # Adds a search bar for tasks
    
    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}