from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from foodgram.router import NewDefaultRouter
from users.urls import users_router
from recipes.urls import recipe_router

router_v1 = NewDefaultRouter()
router_v1.extend(users_router)
router_v1.extend(recipe_router)

backends_urls = [
    path('', include(router_v1.urls)),
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
