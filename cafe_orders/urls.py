"""
URL-конфигурация для приложения cafe_orders.

Этот файл определяет соответствие между URL-адресами и представлениями (views).
"""

from typing import List, Union
from django.urls import path, URLPattern
from . import views
from .constants import URL_PATHS, URL_NAMES

urlpatterns: List[URLPattern] = [
    path(URL_PATHS['dish_list'], views.dish_list, name=URL_NAMES['dish_list']),
    path(URL_PATHS['add_dish'], views.add_dish, name=URL_NAMES['add_dish']),
    path(URL_PATHS['edit_dish'], views.edit_dish, name=URL_NAMES['edit_dish']),
    path(URL_PATHS['delete_dish'], views.delete_dish, name=URL_NAMES['delete_dish']),
    path(URL_PATHS['order_list'], views.order_list, name=URL_NAMES['order_list']),
    path(URL_PATHS['add_order'], views.add_order, name=URL_NAMES['add_order']),
    path(URL_PATHS['edit_order_status'], views.edit_order_status, name=URL_NAMES['edit_order_status']),
    path(URL_PATHS['update_order'], views.update_order, name=URL_NAMES['update_order']),
    path(URL_PATHS['delete_order'], views.delete_order, name=URL_NAMES['delete_order']),
    path(URL_PATHS['delete_all_orders'], views.delete_all_orders, name=URL_NAMES['delete_all_orders']),
    path(URL_PATHS['update_order_status'], views.update_order_status, name=URL_NAMES['update_order_status']),
    path(URL_PATHS['calculate_revenue'], views.calculate_revenue, name=URL_NAMES['calculate_revenue']),
]