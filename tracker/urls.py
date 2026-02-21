from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Start on Login
    path('', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    
    # After login, user lands here
    path('welcome/', views.index, name='index'), 
    
    # Team Workspace destination
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]