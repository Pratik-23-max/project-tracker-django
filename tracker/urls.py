from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Ensure this name matches EXACTLY what is in your template
    path('employee-portal/', views.employee_dashboard, name='employee_dashboard'), 
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
]