from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from root.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL


urlpatterns = [
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('admin/', admin.site.urls),
                  path('api/v1/', include('apps.urls'))
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL,
                                                                       document_root=STATIC_ROOT) + debug_toolbar_urls()
