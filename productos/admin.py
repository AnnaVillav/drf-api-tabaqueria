from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',) #act y inac

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'stock', 'categoria', 'activo')
    list_filter = ('categoria', 'activo', 'marca')
    search_fields = ('nombre', 'codigo', 'marca') #barra busq