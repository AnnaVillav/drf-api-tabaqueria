from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Venta, DetalleVenta

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


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono', 'direccion', 'fecha_registro', 'activo']
        read_only_fields = ['id', 'fecha_registro']



class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'marca', 'precio', 'stock', 'codigo', 'categoria', 'activo']
        read_only_fields = ['id']


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True
    )
    
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_id', 'cantidad', 'precio_unitario']


class VentaPublicSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'fecha_venta', 'detalles', 'total', 'activa']
        read_only_fields = ['id', 'fecha_venta']


#obj anid
class VentaSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    detalles = DetalleVentaSerializer(many=True)
    
    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'detalles', 'total', 'activa']
        read_only_fields = ['id', 'fecha_venta']
    
    def create(self, validated_data):
      
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        
        self._calcular_total(venta)
        
        return venta
    
    def update(self, instance, validated_data):
    
        detalles_data = validated_data.pop('detalles', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if detalles_data is not None:
            instance.detalles.all().delete()
            for detalle_data in detalles_data:
                DetalleVenta.objects.create(venta=instance, **detalle_data)
            self._calcular_total(instance)
        
        return instance
    
    def _calcular_total(self, venta):
       
        total = 0
        for detalle in venta.detalles.all():
            total += detalle.cantidad * detalle.precio_unitario
        venta.total = total
        venta.save()