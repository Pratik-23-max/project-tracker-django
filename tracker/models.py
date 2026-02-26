from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    # MongoDB uses ObjectId, but Djongo handles the mapping for us
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # This creates a reference in the MongoDB document
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = False # Ensures it creates a collection in MongoDB

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')

    def __str__(self):
        return self.title