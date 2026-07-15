from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Task, Profile

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
        
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "image_preview",
    )

    search_fields = (
        "user__username",
        "phone",
    )

    def image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.profile_picture.url
            )
        return "No Image"

    image_preview.short_description = "Profile"