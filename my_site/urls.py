from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Force Admin to use your custom login template
    path(
        'admin/login/',
        auth_views.LoginView.as_view(
            template_name='tracker/login.html'
        )
    ),

    path('admin/', admin.site.urls),

    # 2. Include app URLs
    path('', include('tracker.urls')),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )