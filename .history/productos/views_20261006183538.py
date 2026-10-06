from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Categoria, Producto, Cliente, Venta
from .serializers import (
    CategoriaSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
    ClienteSerializer,
    VentaSerializer,
    VentaPublicSerializer,
)


@api_view(["GET", "POST"])
def producto_list(request):
    if request.method == "GET":
        productos = Producto.objects.select_related("categoria").all()
        serializer = ProductoPublicSerializer(productos, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
def producto_detail(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria"),
        pk=pk,
    )

    if request.method == "GET":
        serializer = ProductoPublicSerializer(producto)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProductoSerializer(
            producto,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "DELETE":
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Parte opcional de la consigna
@api_view(["GET", "POST"])
def categoria_list(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CategoriaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ClienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = (
        Venta.objects
        .all()
        .select_related("cliente")
        .prefetch_related("detalles__producto")
    )

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VentaPublicSerializer

        return VentaSerializer

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        venta = self.get_object()
        venta.activa = False
        venta.save()

        return Response({
            "status": "Venta cancelada con éxito"
        })

    @action(detail=True, methods=["post"])
    def reactivar(self, request, pk=None):
        venta = self.get_object()
        venta.activa = True
        venta.save()

        return Response({
            "status": "Venta reactivada con éxito"
        })

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.select_related("categoria").all()
    serializer_class = ProductoPublicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]