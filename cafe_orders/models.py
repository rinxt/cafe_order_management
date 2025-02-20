from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from typing import List, Tuple

from cafe_orders.constants import DISH_PRICE_MAX_DIGITS, DISH_PRICE_DECIMAL_PLACES, DISH_PRICE_MIN_VALUE, \
    DISH_NAME_MAX_LENGTH, DISH_STR_FORMAT, ORDER_TABLE_NUMBER_MIN_VALUE, ORDER_STATUS_CHOICES, DEFAULT_ORDER_STATUS, \
    ORDER_STR_FORMAT, DEFAULT_QUANTITY, ORDER_ITEM_QUANTITY_MIN_VALUE, ORDER_ITEM_STR_FORMAT


class Dish(models.Model):
    """
    Модель блюда.

    Attributes:
        name (CharField): Название блюда (максимальная длина 100 символов, уникальное).
        price (DecimalField): Цена блюда (максимально 7 знаков, 2 знака после запятой, минимальное значение 0.00).
    """
    name = models.CharField("Название блюда", max_length=DISH_NAME_MAX_LENGTH, unique=True)
    price = models.DecimalField(
        "Цена",
        max_digits=DISH_PRICE_MAX_DIGITS,
        decimal_places=DISH_PRICE_DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal(DISH_PRICE_MIN_VALUE))]
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта блюда.

        Returns:
            str: Строковое представление блюда в формате "Название - Цена₽".
        """
        return DISH_STR_FORMAT.format(name=self.name, price=self.price)


class Order(models.Model):
    """
    Модель заказа.

    Attributes:
        STATUS_CHOICES (List[Tuple[str, str]]): Список возможных статусов заказа.
        table_number (PositiveIntegerField): Номер стола (минимальное значение 1).
        status (CharField): Статус заказа (один из вариантов из STATUS_CHOICES, по умолчанию 'pending').
        created_at (DateTimeField): Дата и время создания заказа (автоматически устанавливается при создании).
        updated_at (DateTimeField): Дата и время обновления заказа (автоматически обновляется при каждом сохранении).
    """
    STATUS_CHOICES: List[Tuple[str, str]] = ORDER_STATUS_CHOICES

    table_number = models.PositiveIntegerField(
        "Номер стола",
        validators=[MinValueValidator(ORDER_TABLE_NUMBER_MIN_VALUE)]
    )
    status = models.CharField(
        "Статус заказа",
        max_length=10,
        choices=STATUS_CHOICES,
        default=DEFAULT_ORDER_STATUS,
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    @property
    def total_price(self) -> Decimal:
        """
        Вычисляет общую стоимость заказа.

        Returns:
            Decimal: Общая стоимость заказа.
        """
        total: Decimal = sum(item.price for item in self.items.all())
        return total

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта заказа.

        Returns:
            str: Строковое представление заказа в формате "Заказ id - Стол номер_стола".
        """
        return ORDER_STR_FORMAT.format(id=self.id, table_number=self.table_number)


class OrderItem(models.Model):
    """
    Модель позиции заказа.

    Attributes:
        order (ForeignKey): Заказ, к которому относится позиция.
        dish (ForeignKey): Блюдо, входящее в позицию заказа.
        quantity (PositiveIntegerField): Количество блюд в позиции (минимальное значение 1, по умолчанию 1).
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, default=1, on_delete=models.CASCADE, verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(
        "Количество",
        default=DEFAULT_QUANTITY,
        validators=[MinValueValidator(ORDER_ITEM_QUANTITY_MIN_VALUE)]
    )

    @property
    def price(self) -> Decimal:
        """
        Вычисляет стоимость позиции заказа.

        Returns:
            Decimal: Стоимость позиции заказа.
        """
        return self.dish.price * self.quantity

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта позиции заказа.

        Returns:
            str: Строковое представление позиции заказа в формате "Название_блюда x Количество - Цена₽".
        """
        return ORDER_ITEM_STR_FORMAT.format(
            dish_name=self.dish.name,
            quantity=self.quantity,
            price=self.price,
        )