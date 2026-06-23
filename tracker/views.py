from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task

# 1. Landing Page
def index(request):
    return render(request, 'tracker/index.html')

# 2. Signup Function
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('portal_choice')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


# 3. Fixed Portal Choice Logic (Reads Session Cache & URL Param Parameters)
@login_required
def portal_choice(request):
    # Check if a specific role parameter was passed in the URL
    chosen_role = request.GET.get('role') or request.POST.get('role')
    
    # Save the role choice to the session context so it isn't lost during navigation
    if chosen_role:
        request.session['user_portal_role'] = chosen_role
    else:
        # Fallback to look at the session cache if the URL parameter was stripped
        chosen_role = request.session.get('user_portal_role')

    if chosen_role == 'manager':
        return redirect('dashboard')
    elif chosen_role == 'employee':
        return redirect('employee_dashboard')
        
    # Final Fallback Option: If no parameter exists anywhere, use model profile architecture
    if request.user.is_staff:
        return redirect('dashboard')
        
    return redirect('employee_dashboard')


# 4. Manager Dashboard (Updated to support flexible querying fallback)
@login_required
def dashboard(request):
    projects = Project.objects.filter(manager=request.user)

    if not projects.exists():
        projects = Project.objects.all()

    total_projects = projects.count()

    total_tasks = Task.objects.filter(project__in=projects).count()

    completed_tasks = Task.objects.filter(
        project__in=projects,
        status='Completed'
    ).count()

    pending_tasks = Task.objects.filter(
        project__in=projects
    ).exclude(status='Completed').count()

    completion_percentage = 0

    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            1
        )

    project_progress = []

    for project in projects:

        project_total_tasks = project.tasks.count()

        project_completed_tasks = project.tasks.filter(
            status='Completed'
        ).count()

        progress = 0

        if project_total_tasks > 0:
            progress = int(
                (project_completed_tasks / project_total_tasks) * 100
            )

        project_progress.append({
            'project': project,
            'total_tasks': project_total_tasks,
            'completed_tasks': project_completed_tasks,
            'progress': progress
        })

    context = {
        'projects': projects,
        'project_progress': project_progress,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage,
    }

    return render(request, 'tracker/dashboard.html', context)
# 5. Employee Dashboard
@login_required
def employee_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tracker/employee_dashboard.html', {'tasks': tasks})


# 6. Project Details & Add Task
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        Task.objects.create(
            project=project,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline if deadline else None,
            assigned_to=request.user
        )

        return redirect('project_detail', project_id=project.id)

    return render(
        request,
        'tracker/project_detail.html',
        {'project': project}
    )
# 7. Update Task Status
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
    return redirect('employee_dashboard')