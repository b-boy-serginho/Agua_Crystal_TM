from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Ubicacion, Factura, Producto, Detalle, User
from .serializers import ClienteSerializer, UbicacionSerializer, FacturaSerializer, ProductoSerializer, DetalleSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from django.db import connection

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class DetalleViewSet(viewsets.ModelViewSet):
    queryset = Detalle.objects.all()
    serializer_class = DetalleSerializer 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        cache_key = f"login_attemps_{username}"
        attemps = cache.get(cache_key, 0)
        if(attemps >=3):
            raise AuthenticationFailed("Cuenta temporalmente bloqueada, por multiples intentos")
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            cache.set(cache_key, attemps +1, timeout=60*5)
            raise AuthenticationFailed("Credenciales incorrectas")
        cache.delete(cache_key)

        user=self.user
        try:
            cliente = Cliente.objects.get(user=user)
            data['user_id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
            data['telefono'] = cliente.telefono
            data['direccion'] = cliente.direccion
            data['foto'] = cliente.foto
        except Cliente.DoesNotExist:
            data['user_id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesion cerrada correctamente"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token invalido o ya fue usado"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        telefono = data.get("telefono")
        direccion = data.get("direccion")
        foto = data.get("foto")
        if User.objects.filter(username=username).exists():
            return Response({"error": "nombre de usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        cliente = Cliente.objects.create(user=user, telefono=telefono, direccion=direccion, foto=foto)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "telefono": cliente.telefono,
            "direccion": cliente.direccion,
            "foto": cliente.foto,
        }, status=status.HTTP_201_CREATED)

class ReporteFacturaAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT auth_user.username, 
                       api_factura.id as numero_factura,
                       api_producto.nombre,
                       api_detalle.cantidad,
                       api_detalle.precio,
                       api_detalle.subtotal	
                FROM auth_user, api_factura, api_producto, api_detalle
                WHERE auth_user.id = api_factura.cliente_id
                  AND api_factura.id = api_detalle.factura_id
                  AND api_producto.id = api_detalle.producto_id
            """)
            resultado = cursor.fetchall()
        
        # Convertir resultado a JSON-like
        data = [
            {
                "username": r[0],
                "numero_factura": r[1],
                "producto": r[2],
                "cantidad": r[3],
                "precio": float(r[4]),
                "subtotal": float(r[5])
            }
            for r in resultado
        ]

        return Response(data)

class ResumenFacturasAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT auth_user.username, 
                       api_factura.importe_total, 
                       api_factura.importe_descuento, 
                       api_factura.fecha
                FROM auth_user, api_factura
                WHERE auth_user.id = api_factura.cliente_id
            """)
            resultados = cursor.fetchall()

        data = [
            {
                "username": fila[0],
                "importe_total": float(fila[1]),
                "importe_descuento": float(fila[2]),
                "fecha": fila[3]
            }
            for fila in resultados
        ]

        return Response(data)
    
# class ReporteFacturaAPIView(APIView):
#     def get(self, request):
#         detalles = Detalle.objects.select_related('factura', 'factura__cliente', 'producto')
#         data = []
#         for d in detalles:
#             data.append({
#                 "username": d.factura.cliente.username,
#                 "numero_factura": d.factura.id,
#                 "producto": d.producto.nombre,
#                 "cantidad": d.cantidad,
#                 "precio": d.precio,
#                 "subtotal": d.subtotal,
#             })
#         return Response(data, status=status.HTTP_200_OK)

# class ResumenFacturasAPIView(APIView):
#     def get(self, request):
#         facturas = Factura.objects.select_related('cliente')
#         data = []
#         for f in facturas:
#             data.append({
#                 "username": f.cliente.username,
#                 "importe_total": f.importe_total,
#                 "importe_descuento": f.importe_descuento,
#                 "fecha": f.fecha,
#             })
#         return Response(data, status=status.HTTP_200_OK)





