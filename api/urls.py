from rest_framework import routers
from django.urls import path, include
from .views import (
    ClienteViewSet, UbicacionViewSet, FacturaViewSet,
    ProductoViewSet, DetalleViewSet, CustomTokenObtainPairView,
    LogoutView, RegisterView, 
    ReporteFacturaAPIView, ResumenFacturasAPIView
)

router = routers.DefaultRouter()

router.register('api/cliente', ClienteViewSet)
router.register('api/ubicacion', UbicacionViewSet)
router.register('api/factura', FacturaViewSet)
router.register('api/producto', ProductoViewSet)
router.register('api/detalle', DetalleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/reporte-facturas/', ReporteFacturaAPIView.as_view(), name='reporte_factura'),
    path('api/resumen-facturas/', ResumenFacturasAPIView.as_view(), name='resumen_facturas')
]
