from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.permissions import AllowAny




class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return Project.objects.filter(
                manager=self.request.user
            )

        return Project.objects.all()

    def perform_create(self, serializer):

        if self.request.user.is_authenticated:
            serializer.save(
                manager=self.request.user
            )
        
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):

        return Task.objects.filter(
            assigned_to=self.request.user
        )        