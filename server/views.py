from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer
from django.db.models import Q
from .models import CommonData
from .serializers import CommonDataSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from server.authentication import MultiTokenAuthentication


@api_view(["POST"])
def register(request):
    """
    Create a user with: username, password, first_name, last_name, email,
    municipios (list[str]), permissions (list[str]).
    Returns: token + full user data.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(instance=user).data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    """
    Authenticates with username & password (+optional municipio check).
    Returns: token + full user data.
    """
    username  = request.data.get("username")
    password  = request.data.get("password")
    municipio = request.data.get("municipio", "").upper()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=400)

    # Optional municipality filter
    allowed_muns = user.profile.get_municipios_list()
    if municipio and municipio not in allowed_muns:
        return Response({"error": "User has no access to this municipio"}, status=403)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": UserSerializer(instance=user).data})

@api_view(["GET"])                               # ← solo lectura
@authentication_classes([MultiTokenAuthentication])   # ← token requerido
@permission_classes([IsAuthenticated])
def commondata(request):
    """
    GET /commondata?username=<user>

    Devuelve los registros de CommonData asociados al username
    (event_user_name | create_user_name | last_edit_name).
    El token se envía en el header:  Authorization: Token <token>.
    """
    username = request.query_params.get("username", "").strip()
    if not username:
        return Response({"error": "username query-param is required"}, status=400)

    qs = CommonData.objects.filter(
        Q(event_user_name=username) |
        Q(create_user_name=username) |
        Q(last_edit_name=username)
    )
    return Response(CommonDataSerializer(qs, many=True).data)
# ----------------------------------------------------------------------
@api_view(["POST"])                              # ← crear registro
@authentication_classes([MultiTokenAuthentication])
@permission_classes([IsAuthenticated])
def commondata_create(request):
    """
    POST /commondata/create
    Body JSON con TODOS los campos definidos en CommonDataModelSerializer.
    El token es obligatorio.  Devuelve el registro insertado.
    """
    serializer = CommonDataSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()             # inserta en la tabla
        return Response(CommonDataSerializer(instance).data, status=201)
    return Response(serializer.errors, status=400)