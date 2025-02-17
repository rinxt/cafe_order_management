from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from cafe_orders.models import Dish, Order, OrderItem

class DishModelTest(TestCase):
    def test_dish_str(self):
        """
        Тестирует метод __str__ модели Dish.
        """
        dish = Dish.objects.create(name='Паста', price=Decimal('12.50'))
        expected = 'Паста - 12.50₽'
        self.assertEqual(str(dish), expected)

    def test_dish_price_min_value_validator(self):
        """
        Тестирует наличие валидации на минимальное значение для цены блюда.
        """
        dish = Dish(name='Неверное блюдо', price=Decimal('-1.00'))
        with self.assertRaises(ValidationError):
            dish.full_clean()


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name='Бургер', price=Decimal('8.75'))
        self.order = Order.objects.create(table_number=1)

    def test_order_item_price_property(self):
        """
        Тестирует вычисление стоимости позиции заказа.
        """
        quantity = 2
        item = OrderItem.objects.create(order=self.order, dish=self.dish, quantity=quantity)
        expected_price = self.dish.price * quantity
        self.assertEqual(item.price, expected_price)

    def test_order_item_str(self):
        """
        Тестирует строковое представление позиции заказа.
        """
        quantity = 2
        item = OrderItem.objects.create(order=self.order, dish=self.dish, quantity=quantity)
        expected = f"{self.dish.name} x {quantity} - {self.dish.price * quantity}₽"
        self.assertEqual(str(item), expected)

    def test_order_item_quantity_min_validator(self):
        """
        Тестирует валидацию количества в позиции заказа (не должно быть меньше 1).
        """
        item = OrderItem(order=self.order, dish=self.dish, quantity=0)
        with self.assertRaises(ValidationError):
            item.full_clean()


class OrderModelTest(TestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(name='Суп', price=Decimal('5.00'))
        self.dish2 = Dish.objects.create(name='Салат', price=Decimal('7.50'))
        self.order = Order.objects.create(table_number=5)

    def test_order_str(self):
        """
        Тестирует строковое представление заказа.
        """
        expected = f"Заказ {self.order.id} - Стол {self.order.table_number}"
        self.assertEqual(str(self.order), expected)

    def test_total_price_property(self):
        """
        Тестирует вычисление общей стоимости заказа.
        """
        # Создаем две позиции заказа:
        # Первая: 2 x Суп (2 * 5.00 = 10.00)
        OrderItem.objects.create(order=self.order, dish=self.dish1, quantity=2)
        # Вторая: 3 x Салат (3 * 7.50 = 22.50)
        OrderItem.objects.create(order=self.order, dish=self.dish2, quantity=3)

        expected_total = Decimal('10.00') + Decimal('22.50')
        # Пересчитываем общую стоимость заказа через свойство total_price
        self.assertEqual(self.order.total_price, expected_total)