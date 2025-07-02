from rest_framework import serializers
from .models import Cliente, Ubicacion, Factura, Producto, Detalle

class ClienteSerializer(serializers.ModelSerializer):
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
            'fecha'
        ]
        read_only_fields = ['importe_total', 'fecha']

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        factura = serializers.PrimaryKeyRelatedField(queryset=Factura.objects.all())
        producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
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

