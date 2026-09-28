from django.urls import path

from .views import categoria_list, producto_detail, producto_list


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
]