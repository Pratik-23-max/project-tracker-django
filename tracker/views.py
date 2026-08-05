from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   # <-- ADD THIS
from .models import Project, Task, Profile
from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProjectSerializer

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
    """
    Redirect users automatically based on their role.
    """

    if request.user.is_superuser:
        return redirect("dashboard")

    return redirect("employee_dashboard")


# 4. Manager Dashboard (Updated to support flexible querying fallback)
@login_required
def dashboard(request):

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")

    projects = Project.objects.filter(
        manager=request.user
    )

    if query:

        projects = projects.filter(
            title__icontains=query
        ) | projects.filter(
            description__icontains=query
        )

    total_projects = projects.count()
    total_employees = User.objects.exclude(
    is_superuser=True
).exclude(
    id=request.user.id
).count()

    total_tasks = Task.objects.filter(
        project__in=projects
    ).count()

    completed_tasks = Task.objects.filter(
        project__in=projects,
        status="Completed"
    ).count()

    pending_tasks = Task.objects.filter(
        project__in=projects
    ).exclude(
        status="Completed"
    ).count()

    completion_percentage = 0

    if total_tasks > 0:

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            1
        )

    project_progress = []

    for project in projects:

        total = project.tasks.count()

        completed = project.tasks.filter(
            status="Completed"
        ).count()

        progress = 0

        if total > 0:

            progress = int(
                (completed / total) * 100
            )

        # Recent tasks for this project
        recent_tasks = project.tasks.all()

        if status_filter:

            recent_tasks = recent_tasks.filter(
                status=status_filter
            )

        project_progress.append({

            "project": project,

            "total_tasks": total,

            "completed_tasks": completed,

            "progress": progress,

            "recent_tasks": recent_tasks,

        })
        profile = Profile.objects.filter(
    user=request.user
).first()

    return render(

        request,

        "tracker/dashboard.html",

        {

            "project_progress": project_progress,

            "total_projects": total_projects,

            "total_tasks": total_tasks,

            "completed_tasks": completed_tasks,

            "pending_tasks": pending_tasks,

            "completion_percentage": completion_percentage,

            "query": query,

            "status_filter": status_filter,
            
            "total_employees": total_employees,
            
            "profile": profile,

        }

    )
    
    

# 5. Employee Dashboard
@login_required
def employee_dashboard(request):

    tasks = Task.objects.filter(
        assigned_to=request.user
    )

    today = date.today()

    pending_tasks = tasks.filter(
        status='Pending'
    )

    in_progress_tasks = tasks.filter(
        status='In Progress'
    )

    completed_tasks = tasks.filter(
        status='Completed'
    )

    overdue_tasks = tasks.filter(
        deadline__lt=today
    ).exclude(
        status='Completed'
    )

    due_today_tasks = tasks.filter(
        deadline=today
    ).exclude(
        status='Completed'
    )

    recently_completed = completed_tasks.order_by(
        '-created_at'
    )[:5]
    
    profile = Profile.objects.filter(
    user=request.user).first()
    context = {

        'tasks': tasks,

        'pending_count': pending_tasks.count(),

        'in_progress_count': in_progress_tasks.count(),

        'completed_count': completed_tasks.count(),

        'overdue_count': overdue_tasks.count(),

        'today_count': due_today_tasks.count(),

        'due_today_tasks': due_today_tasks,

        'overdue_tasks': overdue_tasks,

        'recently_completed': recently_completed,
        
        'today': date.today(),
        
        'profile': profile,
    }

    return render(
        request,
        'tracker/employee_dashboard.html',
        context
    )

# 6. Project Details & Add Task
@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        manager=request.user
    )

    employees = User.objects.exclude(
        id=request.user.id
    ).exclude(
        is_superuser=True
    )

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        assigned_to = get_object_or_404(
            User,
            id=request.POST.get('assigned_to')
        )

        try:

            task = Task(
                project=project,
                title=title,
                description=description,
                priority=priority,
                deadline=deadline if deadline else None,
                assigned_to=assigned_to
            )

            task.full_clean()

            task.save()

            return redirect(
                'project_detail',
                project_id=project.id
            )

        except ValidationError as e:

            return render(
                request,
                'tracker/project_detail.html',
                {
                    'project': project,
                    'employees': employees,
                    'today': date.today().isoformat(),
                    'errors': e.message_dict,
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'deadline': deadline,
                }
            )

    return render(
        request,
        'tracker/project_detail.html',
        {
            'project': project,
            'employees': employees,
            'today': date.today().isoformat()
        }
    )
# 7. Update Task Status
@login_required
def update_task_status(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        assigned_to=request.user
    )

    if request.method == 'POST':

        task.status = request.POST.get("status")

        task.save()

    return redirect('employee_dashboard')
#8.create project view
@login_required
def create_project(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only managers can create projects."
        )

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')

        try:

            project = Project(
                title=title,
                description=description,
                manager=request.user
            )

            project.full_clean()

            project.save()

            messages.success(request, "Project created successfully!")

            return redirect("dashboard")

        except ValidationError as e:

            return render(
                request,
                'tracker/create_project.html',
                {
                    'errors': e.message_dict,
                    'title': title,
                    'description': description,
                }
            )

    return render(
        request,
        'tracker/create_project.html'
    )
#delete project view
@login_required
def delete_project(request, project_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only managers can perform this action."
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        manager=request.user
    )
    project.delete()

    messages.success(request, "Project deleted successfully!")

    return redirect(...)

        
#edit project view
@login_required
def edit_project(request, project_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only managers can perform this action."
    )
    

    project = get_object_or_404(
        Project,
        id=project_id,
        manager=request.user
    )

    if request.method == 'POST':

        project.title = request.POST.get('title')
        project.description = request.POST.get('description')

        try:

            project.full_clean()

            project.save()

            messages.success(request, "Project updated successfully!")

            return redirect(...)

        except ValidationError as e:

            return render(
                request,
                'tracker/edit_project.html',
                {
                    'project': project,
                    'errors': e.message_dict,
                }
            )

    return render(
        request,
        'tracker/edit_project.html',
        {
            'project': project
        }
    )
#edit task view
@login_required
def edit_task(request, task_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden(
        "Only managers can perform this action."
    )

    task = get_object_or_404(
        Task,
        id=task_id,
        project__manager=request.user
)

    employees = User.objects.exclude(
        id=request.user.id
    ).exclude(
        is_superuser=True
    )

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.deadline = request.POST.get('deadline') or None

        task.assigned_to = get_object_or_404(
            User,
            id=request.POST.get('assigned_to')
        )

        try:

            task.full_clean()

            task.save()

            messages.success(request, "Task updated successfully!")
        

            return redirect(
                'project_detail',
                project_id=task.project.id
            )

        except ValidationError as e:

            return render(
                request,
                'tracker/edit_task.html',
                {
                    'task': task,
                    'employees': employees,
                    'errors': e.message_dict
                }
            )

    return render(
        request,
        'tracker/edit_task.html',
        {
            'task': task,
            'employees': employees
        }
    )
    
#delete task view
@login_required
def delete_task(request, task_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only managers can perform this action."
    )

    task = get_object_or_404(
        Task,
        id=task_id,
        project__manager=request.user
    )

    project_id = task.project.id

    task.delete()

    messages.success(request, "Task deleted successfully!")



    return redirect(
        'project_detail',
        project_id=project_id
    )
@api_view(['GET'])
def api_projects(request):

    projects = Project.objects.all()

    serializer = ProjectSerializer(
        projects,
        many=True
    )

    return Response(serializer.data)