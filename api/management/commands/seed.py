from django.core.management.base import BaseCommand
from api.models import Cliente, Ubicacion, Producto, Factura, Detalle
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Carga datos de ejemplo (seeders) en la base de datos"

    def handle(self, *args, **kwargs):
        # Crear usuario
        user = User.objects.create_user(username='sergio', password='1234', email='sergio@example.com')
        # user, _ = User.objects.get_or_create(username='admin')
        # user.set_password('admin123')
        # user.save()

        # Crear cliente asociado
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

        # Crear factura desbloqueada
        factura = Factura.objects.create(cliente=cliente, importe_descuento=Decimal("0.00"))

        # Crear detalles
        Detalle.objects.create(factura=factura, producto=producto1, cantidad=2, precio=Decimal("5.50"))
        Detalle.objects.create(factura=factura, producto=producto2, cantidad=1, precio=Decimal("20.00"))
        # Este segundo producto fallará si la factura ya se bloqueó en el primero
        # Puedes evitarlo usando otra factura o quitar el bloqueo automático si solo estás sembrando

        self.stdout.write(self.style.SUCCESS("✅ Seeders creados correctamente."))
