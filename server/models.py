from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Permite guardar una cadena con nombres de municipios separados por comas, 
    # ej.: "CUITIVA, IZA, OTRO_MUNICIPIO"
    municipios = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ingrese los nombres de los municipios permitidos, separados por comas."
    )

    def get_municipios_list(self):
        # Convierte la cadena en una lista en mayúsculas, eliminando espacios en blanco
        return [mun.strip().upper() for mun in self.municipios.split(',') if mun.strip()]

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)