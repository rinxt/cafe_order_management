"""
URL-конфигурация для API приложения cafe_orders.

Этот файл определяет маршруты для REST API, использующие ViewSet для заказов.
"""

from typing import List, Union
from django.urls import path, include, URLPattern, URLResolver
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router: DefaultRouter = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', include(router.urls)),
]