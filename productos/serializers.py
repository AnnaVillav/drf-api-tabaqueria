from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ["id"]


class ProductoPublicSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ["id", "nombre", "precio", "stock", "categoria"]
        read_only_fields = ["id"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all()
    )

    class Meta:
        model = Producto
        fields = "__all__"
        read_only_fields = ["id", "fecha_creacion"]