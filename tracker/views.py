from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Project

def index(request):
    return render(request, 'tracker/index.html')

def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'tracker/dashboard.html', {'projects': projects})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') # Corrected redirect
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})