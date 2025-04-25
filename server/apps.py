from django.apps import AppConfig

class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        # Importa el módulo para que se registren las señales.
        import server.models