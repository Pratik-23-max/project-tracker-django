# 🚀 FlowBoard — Project Management & Task Tracking Platform

FlowBoard is a full-stack project management and task tracking web application built with **Python and Django**.

It provides separate workflows for managers and employees to manage projects, assign and track tasks, monitor progress, and manage user profiles.

The application is deployed on **Render**, uses **PostgreSQL** for production data, and **Amazon S3** for profile-picture storage.

---

## 🌐 Live Demo

🔗 **Live Application:**  
https://project-tracker-fafq.onrender.com/

---

## 📌 Project Overview

FlowBoard was built to provide a centralized platform where managers can create and manage projects, assign tasks to employees, and monitor project progress.

Employees can view their assigned work, track task statuses, and manage their profile information.

The project also includes a REST API built with **Django REST Framework** and cloud-based media storage using **Amazon S3**.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- User authentication and login
- Protected views
- Manager and employee workflows
- Role-based access control
- Secure API access

### 📊 Manager Dashboard
- View managed projects
- Track project progress
- View total projects and tasks
- Monitor completed and pending tasks
- Calculate overall completion percentage
- Search projects
- Filter tasks by status

### 📁 Project Management
- Create projects
- Update projects
- Delete projects
- View project details
- Assign projects to managers
- Track project-specific tasks

### ✅ Task Management
- Create and manage tasks
- Assign tasks to employees
- Update task status
- Track completed and pending tasks
- Filter tasks by status
- Monitor project task progress

### 👨‍💻 Employee Dashboard
- View assigned tasks
- View assigned projects
- Track task status
- Monitor pending and completed work
- Employee-specific dashboard

### 👤 Profile Management
- User profile information
- Profile picture upload
- Profile pictures stored on Amazon S3
- Dynamic profile information on dashboards

### 🔎 Search & Filtering
- Project search
- Task status filtering
- Dynamic dashboard filtering

### 🌐 REST API
The project includes REST APIs developed using Django REST Framework.

Implemented concepts include:

- Serializers
- ViewSets
- Routers
- CRUD operations
- Authentication
- Authorization
- HTTP status codes
- Project API
- Task API
- Postman testing

---

# 🛠️ Tech Stack

## Backend
- Python
- Django
- Django REST Framework

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Database
- SQLite — Development
- PostgreSQL — Production

## Cloud & Deployment
- Amazon S3
- AWS IAM
- Render

## Libraries & Tools
- django-storages
- boto3
- WhiteNoise
- Gunicorn
- Postman
- Git
- GitHub

---

# 🏗️ Application Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         │    Browser       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Render      │
                         │  Django Server   │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Django   │  │PostgreSQL│  │ AWS S3   │
              │ Backend  │  │ Database │  │  Media   │
              └──────────┘  └──────────┘  └──────────┘
                    │
                    ▼
              ┌──────────────┐
              │ Django REST  │
              │     API      │
              └──────────────┘
