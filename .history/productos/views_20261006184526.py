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
        venta.save(update_fields=["activa"])

        return Response({
            "status": "Venta cancelada con éxito"
        })


    @action(detail=True, methods=["post"])
    def reactivar(self, request, pk=None):
        venta = self.get_object()

        venta.activa = True
        venta.save(update_fields=["activa"])

        return Response({
            "status": "Venta reactivada con éxito"
        })


    @action(detail=True, methods=["post"])
    def recalcular_total(self, request, pk=None):
        venta = self.get_object()

        total = sum(
            detalle.cantidad * detalle.precio_unitario
            for detalle in venta.detalles.all()
        )

        venta.total = total
        venta.save(update_fields=["total"])

        return Response({
            "status": "Total recalculado con éxito",
            "venta_id": venta.id,
            "total": venta.total
        })


    @action(detail=True, methods=["get"])
    def resumen(self, request, pk=None):
        venta = self.get_object()

        cantidad_productos = sum(
            detalle.cantidad
            for detalle in venta.detalles.all()
        )

        return Response({
            "venta_id": venta.id,
            "cliente": venta.cliente.nombre,
            "cantidad_productos": cantidad_productos,
            "total": venta.total,
            "activa": venta.activa,
            "fecha_venta": venta.fecha_venta
        })


    @action(detail=True, methods=["post"])
    @transaction.atomic
    def duplicar(self, request, pk=None):
        venta_original = self.get_object()

        nueva_venta = Venta.objects.create(
            cliente=venta_original.cliente,
            activa=True
        )

        for detalle in venta_original.detalles.all():
            DetalleVenta.objects.create(
                venta=nueva_venta,
                producto=detalle.producto,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario
            )

        total = sum(
            detalle.cantidad * detalle.precio_unitario
            for detalle in nueva_venta.detalles.all()
        )

        nueva_venta.total = total
        nueva_venta.save(update_fields=["total"])

        return Response({
            "status": "Venta duplicada con éxito",
            "venta_original": venta_original.id,
            "nueva_venta": nueva_venta.id,
            "total": nueva_venta.total
        })
class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.select_related("categoria").all()
    serializer_class = ProductoPublicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]