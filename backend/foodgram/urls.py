from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

backends_urls = [
    path('', include('api.urls')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(backends_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
