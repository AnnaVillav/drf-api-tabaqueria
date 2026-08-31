from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
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