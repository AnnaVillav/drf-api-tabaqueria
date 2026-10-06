from rest_framework.routers import DefaultRouter
from productos.views import ClienteViewSet, VentaViewSet, ProductoViewSet

router = DefaultRouter()

router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'ventas', VentaViewSet, basename='ventas')
router.register(r'productos', ProductoViewSet, basename='productos')