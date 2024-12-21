from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from status.views import StatusViewSet
from address.views import AddressViewSet
from post.views import PostViewSet

from users.views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'status', StatusViewSet)
router_v1.register(r'addresses', AddressViewSet)
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router_v1.urls)),
]

