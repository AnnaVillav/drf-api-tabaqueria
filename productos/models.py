from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} (Activo: {self.activo})"
    

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    stock_minimo = models.IntegerField(default=0)
    codigo = models.CharField(max_length=50, unique=True)
    gramos = models.IntegerField(null=True, blank=True)  
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"{self.nombre} - {self.email} ({estado})"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ventas")
    productos = models.ManyToManyField(Producto, through='DetalleVenta', related_name="ventas")
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_venta'] 
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre} - Total: ${self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['venta', 'producto'] #q no repita el producto
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"