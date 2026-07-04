from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(
            manager=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            manager=self.request.user
        )
        
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Task.objects.filter(
            assigned_to=self.request.user
        )        