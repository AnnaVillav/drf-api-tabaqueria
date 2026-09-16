from django.urls import path

from .views import categoria_list, producto_detail, producto_list, VentaListCreateAPIView, VentaDetailAPIView, ClienteListCreateAPIView,


urlpatterns = [
    path(
        "productos/",
        producto_list,
        name="producto-list",
    ),
    path(
        "productos/<int:pk>/",
        producto_detail,
        name="producto-detail",
    ),
    path(
        "categorias/",
        categoria_list,
        name="categoria-list",
    ),
    path(
    "ventas/",
    VentaListCreateAPIView.as_view(),
    name="venta-list-create",
    ),

    path(
        "ventas/<int:pk>/",
        VentaDetailAPIView.as_view(),
        name="venta-detail",
    ),

    path(
        "clientes/",
        ClienteListCreateAPIView.as_view(),
        name="cliente-list-create",
    ),
]