from rest_framework import serializers
from .models import Order, OrderItem, Dish
from typing import List, Dict, Any, Optional


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderItem.

    Позволяет задавать блюдо по его названию (slug_field).
    Вычисляет поле 'price' (только для чтения).
    """
    dish = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Dish.objects.all()
    )
    price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)

    class Meta:
        """
        Метаданные сериализатора.
        """
        model = OrderItem
        fields: List[str] = ['id', 'dish', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.

    Использует вложенную сериализацию для элементов заказа (OrderItemSerializer).
    При создании и обновлении ожидает массив данных по ключу "items".
    Поля 'id', 'created_at', 'updated_at', 'total_price' доступны только для чтения.
    """
    items: OrderItemSerializer = OrderItemSerializer(many=True)

    class Meta:
        """
        Метаданные сериализатора.
        """
        model = Order
        fields: List[str] = ['id', 'table_number', 'status', 'created_at', 'updated_at', 'total_price', 'items']
        read_only_fields: List[str] = ['id', 'created_at', 'updated_at', 'total_price']

    def create(self, validated_data: Dict[str, Any]) -> Order:
        """
        Создает новый заказ и связанные с ним элементы заказа.

        Args:
            validated_data: Словарь с валидированными данными для создания заказа.

        Returns:
            Order: Созданный объект заказа.
        """
        items_data: List[Dict[str, Any]] = validated_data.pop('items', [])
        order: Order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance: Order, validated_data: Dict[str, Any]) -> Order:
        """
        Обновляет заказ.

        Args:
            instance: Объект заказа, который нужно обновить.
            validated_data: Словарь с валидированными данными для обновления заказа.

        Returns:
            Order: Обновленный объект заказа.
        """
        items_data: Optional[List[Dict[str, Any]]] = validated_data.pop('items', None)
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance