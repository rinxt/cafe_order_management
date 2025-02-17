from django.apps import AppConfig


class CafeOrdersConfig(AppConfig):
    """
    Конфигурация приложения 'cafe_orders'.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'cafe_orders'