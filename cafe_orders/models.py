from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from typing import List, Tuple


class Dish(models.Model):
    """
    Модель блюда.

    Attributes:
        name (CharField): Название блюда (максимальная длина 100 символов, уникальное).
        price (DecimalField): Цена блюда (максимально 7 знаков, 2 знака после запятой, минимальное значение 0.00).
    """
    name = models.CharField("Название блюда", max_length=100, unique=True)
    price = models.DecimalField(
        "Цена",
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта блюда.

        Returns:
            str: Строковое представление блюда в формате "Название - Цена₽".
        """
        return f"{self.name} - {self.price}₽"


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
    STATUS_CHOICES: List[Tuple[str, str]] = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField("Номер стола", validators=[MinValueValidator(1)])
    status = models.CharField("Статус заказа", max_length=10, choices=STATUS_CHOICES, default='pending')
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
        return f"Заказ {self.id} - Стол {self.table_number}"


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
    quantity = models.PositiveIntegerField("Количество", default=1, validators=[MinValueValidator(1)])

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
        return f"{self.dish.name} x {self.quantity} - {self.price}₽"