from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Project, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            # Only show employees, not managers
            from django.contrib.auth.models import User
            self.fields['assigned_to'].queryset = User.objects.exclude(username='Pratik_Valse')

# --- PUBLIC VIEWS ---

def index(request):
    """Sorts users to the correct dashboard based on their role."""
    if request.user.is_authenticated:
        if request.user.username == 'Pratik_Valse':
            return redirect('dashboard')
        else:
            return redirect('employee_dashboard')
    return render(request, 'tracker/index.html')
def portal_choice(request):
    # If not logged in, show the choice page with Login buttons
    if not request.user.is_authenticated:
        return render(request, 'tracker/portal_choice.html')
    
    # If already logged in, show the choice page with "Enter" buttons
    return render(request, 'tracker/portal_choice.html')
def signup(request):
    """Handles new user registration and redirects to the employee portal."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('employee_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

# --- MANAGER VIEWS ---

@login_required
def dashboard(request):
    """Displays projects managed by the logged-in staff member."""
    projects = Project.objects.filter(manager=request.user)
    return render(request, 'tracker/dashboard.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    """
    FIXED: Re-added this function to resolve the AttributeError in logs.
    Shows specific tasks within a project owned by the manager.
    """
    project = get_object_or_404(Project, id=project_id, manager=request.user)
    tasks = project.tasks.all()
    
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(project=project)
    
    return render(request, 'tracker/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'form': form
    })

# --- EMPLOYEE PORTAL VIEWS ---

@login_required
def employee_dashboard(request):
    """Displays tasks assigned specifically to the logged-in user."""
    my_tasks = Task.objects.filter(assigned_to=request.user).order_by('-id')
    return render(request, 'tracker/employee_dashboard.html', {'tasks': my_tasks})

@login_required
def update_task_status(request, task_id):
    """Allows employees to update the progress of their assigned tasks."""
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['TODO', 'IN_PROGRESS', 'DONE']:
            task.status = new_status
            task.save()
        return redirect('employee_dashboard')
    return render(request, 'tracker/update_task.html', {'task': task})