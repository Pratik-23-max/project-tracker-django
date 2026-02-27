from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    # This must match what is in your template link
    path('dashboard/', views.dashboard, name='dashboard'), 
    # This matches the 'employee_dashboard' name from your error page
    path('welcome/', views.employee_dashboard, name='employee_dashboard'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
    
    # Standard Login/Logout paths
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]