from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from status.views import StatusViewSet
from address.views import AddressViewSet
from post.views import PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'status', StatusViewSet)
router_v1.register(r'addresses', AddressViewSet)
router_v1.register(r'posts', PostViewSet)


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include(router_v1.urls)),
]

