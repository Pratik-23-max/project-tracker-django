from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task

# 1. Landing Page
def index(request):
    return render(request, 'tracker/index.html')

# 2. Signup Function (This was missing!)
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

# 3. Portal Choice Logic
@login_required
def portal_choice(request):
    if request.user.is_staff:
        return redirect('dashboard')
    return redirect('employee_dashboard')

# 4. Manager Dashboard
@login_required
def dashboard(request):
    projects = Project.objects.filter(manager=request.user)
    return render(request, 'tracker/dashboard.html', {'projects': projects})

# 5. Employee Dashboard
@login_required
def employee_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tracker/employee_dashboard.html', {'tasks': tasks})

# 6. Project Details & Add Task (Fixes IntegrityError)
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=request.user # Auto-assigns logged-in user
        )
        return redirect('project_detail', project_id=project.id)
    return render(request, 'tracker/project_detail.html', {'project': project})

# 7. Update Task Status
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
    return redirect('employee_dashboard')