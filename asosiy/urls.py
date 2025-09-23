from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect


def favicon_view(request):
    """Favicon uchun redirect"""
    return redirect(f"{settings.STATIC_URL}img/logo.png")


urlpatterns = [
    path('haker/', admin.site.urls),
    path('favicon.ico', favicon_view, name='favicon'),
    path('', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
    path('files/', include('files.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
