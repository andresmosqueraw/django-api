from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile  # Asegúrate de importar el modelo

class UserSerializer(serializers.ModelSerializer):
    # Campo para recibir la cadena de municipios separados por comas.
    municipios = serializers.CharField(
        write_only=True, 
        required=False, 
        help_text="Ingrese los nombres de los municipios permitidos, separados por comas."
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'municipios']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Se extrae el campo 'municipios', en caso de que se envíe
        municipios = validated_data.pop('municipios', '')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Se obtienen o crean el perfil del usuario para asegurarnos de que exista,
        # luego se actualiza con los municipios enviados.
        profile, created = UserProfile.objects.get_or_create(user=user)
        if municipios:
            profile.municipios = municipios
            profile.save()
        return user