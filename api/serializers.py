from rest_framework import serializers
from .models import Cliente, Ubicacion, Factura, Producto, Detalle

class ClienteSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False)
    class Meta:
        model = Cliente
        fields = [
            'id',
            'user',
            'telefono',
            'direccion',
            'foto',
        ]

class UbicacionSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False)
    class Meta:
        model = Ubicacion
        fields = [
            'id',
            'cliente',
            'longitud',
            'latitud',
            'foto',            
        ]

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'imagen',
        ]

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = [
            'id',
            'cliente',
            'importe_total',
            'importe_descuento',
            'fecha',
            'bloqueada',
        ]
        read_only_fields = ['importe_total', 'fecha', 'bloqueada',]

class DetalleSerializer(serializers.ModelSerializer):
    factura = serializers.PrimaryKeyRelatedField(queryset=Factura.objects.filter(bloqueada=False))
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    class Meta:
        model = Detalle
        # fields = '__all__'
        fields = [
            'id',
            'factura',
            'producto',
            'cantidad',
            'precio',
            'subtotal',
        ]
        read_only_fields = ['subtotal']

