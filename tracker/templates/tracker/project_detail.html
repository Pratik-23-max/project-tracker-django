{% extends "tracker/dashboard.html" %}
{% load static %}

{% block content %}
<div class="container mt-4">
    <h2 style="color: #e67e22;">{{ project.title }}</h2>
    <p class="text-muted">{{ project.description }}</p>

    <hr style="border-color: #264b5d;">

    <h4 style="color: #eeeeee;">Add New Task</h4>
    <form method="POST" style="max-width: 500px;">
        {% csrf_token %}
        <div class="mb-3">
            <input type="text" name="title" class="form-control" placeholder="Task Title" required 
                   style="background: #1a1a1a; color: #eee; border: 1px solid #264b5d;">
        </div>
        <div class="mb-3">
            <textarea name="description" class="form-control" placeholder="Task Description" required 
                      style="background: #1a1a1a; color: #eee; border: 1px solid #264b5d;"></textarea>
        </div>
        <button type="submit" class="btn" style="background: #e67e22; color: white;">Create Task</button>
    </form>

    <h4 class="mt-5" style="color: #eeeeee;">Project Tasks</h4>
    <div class="row">
        {% for task in project.tasks.all %}
        <div class="col-md-6 mb-3">
            <div class="card" style="background: #1b1b1b; border: 1px solid #333; color: #ccc;">
                <div class="card-body">
                    <h5 class="card-title" style="color: #e67e22;">{{ task.title }}</h5>
                    <p>{{ task.description }}</p>
                    <p><small>Assigned to: <strong>{{ task.assigned_to.username }}</strong></small></p>
                    <span class="badge" style="background: #264b5d;">{{ task.status }}</span>
                </div>
            </div>
        </div>
        {% empty %}
        <p class="text-muted">No tasks added yet.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}