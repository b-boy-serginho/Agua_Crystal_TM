# api/seed.py

from django.contrib.auth.models import User
from api.models import Cliente, Ubicacion, Producto, Factura, Detalle
from django.core.files.base import ContentFile
from django.utils import timezone
from decimal import Decimal

def run():
    # Crear usuario y cliente
    user = User.objects.create_user(username='sergio', password='1234', email='sergio@example.com')
    cliente = Cliente.objects.create(
        user=user,
        telefono=71234567,
        direccion="Av. Las Flores",
    )

    # Crear ubicación
    Ubicacion.objects.create(
        cliente=cliente,
        longitud=-66.153,
        latitud=-17.391,
    )

    # Crear productos
    producto1 = Producto.objects.create(nombre="Agua 2L", descripcion="Botella de agua de 2 litros")
    producto2 = Producto.objects.create(nombre="Bidón 20L", descripcion="Bidón grande para uso doméstico")

    # Crear factura
    factura = Factura.objects.create(cliente=cliente, importe_descuento=Decimal("0.00"))

    # Crear detalles
    Detalle.objects.create(factura=factura, producto=producto1, cantidad=2, precio=Decimal("5.50"))
    Detalle.objects.create(factura=factura, producto=producto2, cantidad=1, precio=Decimal("20.00"))

    print("✔ Datos de prueba insertados exitosamente.")
