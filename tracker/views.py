from django.shortcuts import render
from .models import Project

# No login required for dashboard now as requested
def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'tracker/dashboard.html', {'projects': projects})

def index(request):
    return render(request, 'tracker/index.html')