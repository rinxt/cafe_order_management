from decimal import Decimal
from django.test import TestCase
from cafe_orders.models import Dish, Order, OrderItem
from cafe_orders.serializers import OrderSerializer, OrderItemSerializer


class OrderItemSerializerTest(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name='Пицца', price=Decimal('12.50'))

    def test_order_item_serializer_read(self):
        """
        Тестирует сериализацию объекта OrderItem.
        Проверяется, что вычисляемое поле 'price' рассчитано как dish.price * quantity,
        а поле 'dish' возвращается в виде slug (имени блюда).
        """
        order = Order.objects.create(table_number=1, status='pending')
        order_item = OrderItem.objects.create(order=order, dish=self.dish, quantity=2)
        serializer = OrderItemSerializer(order_item)
        data = serializer.data

        expected_price = self.dish.price * 2  # 12.50 * 2
        self.assertEqual(Decimal(data['price']), expected_price)
        self.assertEqual(data['dish'], 'Пицца')
        self.assertEqual(data['quantity'], 2)

    def test_order_item_serializer_write(self):
        """
        Тестирует процедуру валидации данных для создания/обновления OrderItem.
        Благодаря SlugRelatedField поле 'dish' принимает значение имени блюда.
        """
        input_data = {
            'dish': 'Пицца',
            'quantity': 3
        }
        serializer = OrderItemSerializer(data=input_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated = serializer.validated_data
        # Проверяем, что поле 'dish' преобразовалось в объект Dish
        self.assertEqual(validated['dish'], self.dish)
        self.assertEqual(validated['quantity'], 3)


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(name='Бургер', price=Decimal('8.00'))
        self.dish2 = Dish.objects.create(name='Пицца', price=Decimal('3.50'))

    def test_order_serializer_create(self):
        """
        Тестирует создание заказа с вложенными данными OrderItem.
        """
        input_data = {
            'table_number': 10,
            'status': 'pending',
            'items': [
                {'dish': 'Бургер', 'quantity': 2},
                {'dish': 'Пицца', 'quantity': 1},
            ]
        }
        serializer = OrderSerializer(data=input_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        self.assertEqual(order.table_number, 10)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 2)

        expected_total = (self.dish1.price * 2) + (self.dish2.price * 1)
        self.assertEqual(order.total_price, expected_total)

    def test_order_serializer_update(self):
        """
        Тестирует обновление заказа с вложенными данными.
        В данном примере обновление происходит удалением всех позиций и созданием новых.
        """
        # Сначала создаем заказ с одним OrderItem
        initial_data = {
            'table_number': 5,
            'status': 'pending',
            'items': [
                {'dish': 'Бургер', 'quantity': 1}
            ]
        }
        serializer = OrderSerializer(data=initial_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.items.count(), 1)

        update_data = {
            'table_number': 7,
            'status': 'ready',
            'items': [
                {'dish': 'Пицца', 'quantity': 3}
            ]
        }
        update_serializer = OrderSerializer(instance=order, data=update_data)
        self.assertTrue(update_serializer.is_valid(), update_serializer.errors)
        updated_order = update_serializer.save()

        self.assertEqual(updated_order.table_number, 7)
        self.assertEqual(updated_order.status, 'ready')
        self.assertEqual(updated_order.items.count(), 1)

        item = updated_order.items.first()
        self.assertEqual(item.dish, self.dish2)
        self.assertEqual(item.quantity, 3)

    def test_order_serializer_output_fields(self):
        """
        Проверяет, что при сериализации объекта заказа возвращаются все ожидаемые поля,
        включая read-only: 'id', 'created_at', 'updated_at', 'total_price'.
        """
        order = Order.objects.create(table_number=20, status='paid')
        OrderItem.objects.create(order=order, dish=self.dish1, quantity=2)
        serializer = OrderSerializer(order)
        data = serializer.data

        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertIn('total_price', data)
        self.assertIn('items', data)

        expected_total = self.dish1.price * 2
        self.assertEqual(Decimal(data['total_price']), expected_total)