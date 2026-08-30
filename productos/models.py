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