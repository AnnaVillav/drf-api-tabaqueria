from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

from .models import Categoria, Producto, Venta, Cliente
from .serializers import (
    CategoriaSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
    VentaPublicSerializer,
    VentaSerializer,
    ClienteSerializer,
)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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

class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.select_related("cliente").prefetch_related("productos")
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return VentaPublicSerializer
        return VentaSerializer

class VentaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.select_related("cliente").prefetch_related("productos")
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return VentaPublicSerializer
        return VentaSerializer

#opcional de clientes
class ClienteListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer