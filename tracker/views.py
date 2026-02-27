from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Project, Task

# --- PUBLIC VIEWS ---

def index(request):
    # Fixed: Re-added the function definition and request parameter
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('employee_dashboard')
    return render(request, 'tracker/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Default new signups to the employee view
            return redirect('employee_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

# --- MANAGER VIEWS ---

@login_required
def dashboard(request):
    # Professional Logic: Managers should see projects they created
    projects = Project.objects.filter(manager=request.user)
    return render(request, 'tracker/dashboard.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    # Security check: Ensure the manager owns the project
    project = get_object_or_404(Project, id=project_id, manager=request.user)
    tasks = project.tasks.all() 
    return render(request, 'tracker/project_detail.html', {
        'project': project,
        'tasks': tasks
    })

# --- EMPLOYEE PORTAL VIEWS ---

@login_required
def employee_dashboard(request):
    # Fetch tasks assigned specifically to the logged-in user
    my_tasks = Task.objects.filter(assigned_to=request.user).order_by('-id')
    return render(request, 'tracker/employee_dashboard.html', {'tasks': my_tasks})

@login_required
def update_task_status(request, task_id):
    # Security check: Ensure only the assigned employee can update the status
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['TODO', 'IN_PROGRESS', 'DONE']:
            task.status = new_status
            task.save()
        return redirect('employee_dashboard')
        
    return render(request, 'tracker/update_task.html', {'task': task})
