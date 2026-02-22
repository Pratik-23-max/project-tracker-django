from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Entry point
    path('', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    
    # 2. Registration
    path('signup/', views.signup, name='signup'),
    
    # 3. The Welcome/Choice Page (The page you want to see after login/signup)
    path('welcome/', views.index, name='index'), 
    
    # 4. The Workspace
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]