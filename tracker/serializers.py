from rest_framework import serializers

from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = "__all__"

        read_only_fields = [
            "manager",
            "created_at"
        ]

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Project title must contain at least 3 characters."
            )

        return value
    def validate(self, attrs):

        if attrs["title"].strip().lower() == attrs["description"].strip().lower():
            raise serializers.ValidationError(
             "Title and description cannot be the same."
         )

        return attrs

class TaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task

        fields = "__all__"

        read_only_fields = [
            "assigned_to",
        ]