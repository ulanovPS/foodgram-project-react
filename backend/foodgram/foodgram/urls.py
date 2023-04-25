"""foodgram URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import unit_of_measure_list

urlpatterns = [
    path('', include('grocery_assistant.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('units/', unit_of_measure_list, name='unit_of_measure_list'),
]

if settings.DEBUG:

    urlpatterns += path(
        '__debug__/',
        include('debug_toolbar.urls')
    ),
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
