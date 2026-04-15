from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from django.contrib.auth.decorators import login_required

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description') # Required to fix IntegrityError
        status = request.POST.get('status', 'Pending')

        # Create the task and automatically set the assigned_to user
        Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status,
            assigned_to=request.user # Uses the logged-in user instead of manual choice
        )
        return redirect('project_detail', project_id=project.id)

    return render(request, 'tracker/project_detail.html', {'project': project})