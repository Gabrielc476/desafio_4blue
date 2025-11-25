from django.apps import AppConfig

class PersistenciaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.infraestrutura.persistencia.django'
    label = 'persistencia'  # Label curto para facilitar referências