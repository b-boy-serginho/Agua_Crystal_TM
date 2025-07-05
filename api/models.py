from django.db import models
from django.contrib.auth.models import User
User.objects.all()
from django.utils import timezone  # para la fecha actual

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='clientes/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Ubicacion(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    longitud = models.FloatField()
    latitud = models.FloatField()
    foto = models.ImageField(upload_to='ubicaciones/', null=True, blank=True)
    # def __str__(self):
    #      return self.foto.name if self.foto else "Sin foto"
    def __str__(self):
        nombre = str(self.cliente.user.username)
        foto_nombre = self.foto.name if self.foto else "sin_foto"
        return f"{nombre} - {foto_nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    def __str__(self):
        return self.nombre
    
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    importe_descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)  # aquí se guarda la fecha actual
    bloqueada = models.BooleanField(default=False)  # <--- NUEVO CAMPO

    def actualizar_total(self):
        total = sum(detalle.subtotal for detalle in self.detalle_set.all())
        self.importe_total = total
        self.save()
    # def actualizar_total(self, nuevo_total):
    #     self.importe_total = nuevo_total
    #     self.save()

    def __str__(self):
        return f"Factura #{self.id} - Cliente: {self.cliente.user} - Bs. {self.importe_total}"

class Detalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.factura.bloqueada:
            raise ValueError("Ya se uso esta factura, Crea una nueva")
        self.subtotal = self.cantidad * self.precio
        super().save(*args, **kwargs)
        self.factura.actualizar_total() # actualiza automáticamente el total de la factura
        self.factura.bloqueada = True   # Bloquea la factura después de agregar el detalle
        self.factura.save() 
        # self.factura.actualizar_total(self.subtotal) # Aquí copia el subtotal directamente al importe_total

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.factura.actualizar_total()  # también actualiza si se elimina el detalle
        # self.factura.actualizar_total(0)   # Puedes decidir si quieres resetear el total al borrar

