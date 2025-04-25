from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
def login(request):
    """
    Maneja el login del usuario validando username, contraseña y municipio.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    municipio = request.data.get('municipio', '').upper()  # Normaliza a mayúsculas

    # Se obtiene el usuario o retorna error si no existe
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    # Validar la contraseña
    if not user.check_password(password):
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Se obtiene la lista de municipios permitidos registrados en el perfil del usuario
    try:
        allowed_municipios = user.profile.get_municipios_list()
    except Exception:
        return Response(
            {"error": "Perfil de usuario no configurado correctamente."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Verificar si el municipio enviado se encuentra en la lista permitida
    if municipio not in allowed_municipios:
        return Response(
            {"error": "El usuario no tiene acceso a este municipio."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Se genera o recupera el token de autenticación
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    """
    Registra un nuevo usuario y configura el perfil con la cadena de municipios (si se envía).
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        # Se genera el token para el nuevo usuario
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Retorna la información del usuario autenticado.
    """
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)