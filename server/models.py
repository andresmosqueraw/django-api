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
        
class CommonData(models.Model):
    activity_name    = models.CharField(max_length=1000)
    activity_code    = models.CharField(max_length=100)
    address          = models.CharField(max_length=1000)
    city_code        = models.CharField(max_length=100)
    city_desc        = models.CharField(max_length=1000)
    capture_date     = models.DateTimeField(null=True, blank=True)
    capture_x        = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    capture_y        = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    event_user_name  = models.CharField(max_length=1000)
    create_date      = models.DateTimeField(null=True, blank=True)
    create_user_name = models.CharField(max_length=1000)
    event_date       = models.DateTimeField(null=True, blank=True)
    event_x          = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    event_y          = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    last_edit_date   = models.DateTimeField(null=True, blank=True)
    last_edit_x      = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    last_edit_y      = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    last_edit_name   = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "commondata"       # Usa la tabla ya creada
        verbose_name = "Common data"
        verbose_name_plural = "Common data"