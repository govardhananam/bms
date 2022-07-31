from django.conf.urls import handler500
from django.conf.urls.static import static
from django.conf import settings
from login import urls
from django import contrib
from django.contrib import admin, auth
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("login.urls")),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('student/', include("student.urls")),
    path('teacher/', include("teacher.urls")),
] 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
handler404 = "teacher.views.page_not_found_view"

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
handler500 = "teacher.views.internal_server_error_view"