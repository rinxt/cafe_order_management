"""
URL-конфигурация для приложения cafe_orders.

Этот файл определяет соответствие между URL-адресами и представлениями (views).
"""

from typing import List, Union
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/add/', views.add_dish, name='add_dish'),
    path('dishes/<int:pk>/edit/', views.edit_dish, name='edit_dish'),
    path('dishes/<int:pk>/delete/', views.delete_dish, name='delete_dish'),
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('orders/<int:pk>/edit/', views.edit_order_status, name='edit_order_status'),
    path('orders/<int:order_id>/edit_items/', views.update_order, name='update_order'),
    path('delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('orders/delete-all/', views.delete_all_orders, name='delete_all_orders'),
    path('orders/<int:pk>/update-status/', views.update_order_status, name='update_order_status'),
    path('revenue/', views.calculate_revenue, name='calculate_revenue'),
]