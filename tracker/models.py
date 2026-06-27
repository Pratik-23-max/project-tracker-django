from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.title.strip():
            raise ValidationError({
                'title': 'Project title cannot be empty.'
            })

        if len(self.title.strip()) < 3:
            raise ValidationError({
                'title': 'Project title must contain at least 3 characters.'
            })

        if not self.description.strip():
            raise ValidationError({
                'description': 'Project description cannot be empty.'
            })

    def __str__(self):
        return self.title


class Task(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.title.strip():
            raise ValidationError({
                'title': 'Task title cannot be empty.'
            })

        if len(self.title.strip()) < 3:
            raise ValidationError({
                'title': 'Task title must contain at least 3 characters.'
            })

        if not self.description.strip():
            raise ValidationError({
                'description': 'Task description cannot be empty.'
            })

        if self.deadline and self.deadline < date.today():
            raise ValidationError({
                'deadline': 'Deadline cannot be in the past.'
            })

    def __str__(self):
        return self.title