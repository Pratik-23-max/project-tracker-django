from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main Portal Routes
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    
    # Dashboard Routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('welcome/', views.employee_dashboard, name='employee_dashboard'),
    
    # Detail and Action Routes
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
    
    # Authentication Routes
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    # Note: Modern Django requires a POST request to logout for security
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]