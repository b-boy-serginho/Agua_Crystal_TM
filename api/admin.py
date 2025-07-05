from django.contrib import admin

# Register your models here.
from .models import Cliente, Ubicacion, Factura, Producto, Detalle

admin.site.register(Cliente)
admin.site.register(Ubicacion)
admin.site.register(Factura)
admin.site.register(Producto)
admin.site.register(Detalle)
