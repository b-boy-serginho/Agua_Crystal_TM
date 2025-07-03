from django.db import models
from django.contrib.auth.models import User
User.objects.all()
from django.utils import timezone  # para la fecha actual

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    # foto = models.CharField(max_length=300, null=True, blank=True)
    # foto = models.ImageField(upload_to='clientes/')
    foto = models.ImageField(upload_to='clientes/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Ubicacion(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    longitud = models.FloatField()
    latitud = models.FloatField()
    foto = models.CharField(max_length=300)  # ampliado
    def __str__(self):
        return self.foto

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    imagen = models.CharField(max_length=3000)
    def __str__(self):
        return self.nombre
    
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    importe_descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)  # aquí se guarda la fecha actual

    def actualizar_total(self):
        total = sum(detalle.subtotal for detalle in self.detalle_set.all())
        self.importe_total = total
        self.save()

    def __str__(self):
        return f"Factura #{self.id} - Bs. {self.importe_total}"

class Detalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio
        super().save(*args, **kwargs)
        self.factura.actualizar_total()  # actualiza automáticamente el total de la factura

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.factura.actualizar_total()  # también actualiza si se elimina el detalle
