from decimal import Decimal
from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from rest_framework.test import APITestCase
from cafe_orders.models import Dish, Order, OrderItem

# Тесты для представлений с блюдами
class DishViewsTests(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name='Тест', price=Decimal('10.00'))

    def test_dish_list_get(self):
        """
        Тестирование отображения списка блюд.
        """
        url = reverse('dish_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/dish_list.html')
        # Проверяем, что в контексте передается список блюд
        self.assertIn('dishes', response.context)
        self.assertIn(self.dish, response.context['dishes'])

    def test_add_dish_get(self):
        """
        Тестирование GET запроса для добавления блюда.
        """
        url = reverse('add_dish')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/add_dish.html')
        self.assertIn('form', response.context)

    def test_add_dish_post_valid(self):
        """
        Тестирование успешного добавления нового блюда.
        """
        url = reverse('add_dish')
        data = {
            'name': 'Новое блюдо',
            'price': '15.50'
        }
        response = self.client.post(url, data=data)

        self.assertRedirects(response, reverse('dish_list'))
        self.assertTrue(Dish.objects.filter(name='Новое блюдо').exists())

    def test_add_dish_post_invalid(self):
        """
        Тестирование отправки некорректных данных при добавлении блюда.
        """
        url = reverse('add_dish')
        data = {
            'name': '',
            'price': '15.50'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/add_dish.html')

    def test_edit_dish_get(self):
        """
        Тестирование GET запроса страницы редактирования блюда.
        """
        url = reverse('edit_dish', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/edit_dish.html')
        self.assertIn('form', response.context)

    def test_edit_dish_post_valid(self):
        """
        Тестирование успешного обновления блюда.
        """
        url = reverse('edit_dish', kwargs={'pk': self.dish.pk})
        data = {
            'name': 'Updated Dish',
            'price': '20.00'
        }
        response = self.client.post(url, data=data)
        self.assertRedirects(response, reverse('dish_list'))
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, 'Updated Dish')
        self.assertEqual(self.dish.price, Decimal('20.00'))

    def test_delete_dish_get(self):
        """
        Тестирование GET запроса для подтверждения удаления блюда.
        """
        url = reverse('delete_dish', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/delete_dish.html')
        self.assertIn('dish', response.context)

    def test_delete_dish_post(self):
        """
        Тестирование удаления блюда по POST запросу.
        """
        url = reverse('delete_dish', kwargs={'pk': self.dish.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('dish_list'))
        self.assertFalse(Dish.objects.filter(pk=self.dish.pk).exists())


class OrderViewsTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(table_number=1, status='pending')
        self.dish = Dish.objects.create(name='Order Dish', price=Decimal('10.00'))

    def test_order_list_without_filters(self):
        """
        Тестирование отображения списка заказов без фильтрации.
        """
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/order_list.html')
        self.assertIn('orders', response.context)
        self.assertIn(self.order, response.context['orders'])

    def test_order_list_with_valid_table_filter(self):
        """
        Тестирование фильтрации заказов по номеру стола.
        """
        url = reverse('order_list')
        response = self.client.get(url, {'table': '1'})
        self.assertEqual(response.status_code, 200)
        orders = response.context['orders']
        self.assertIn(self.order, orders)

    def test_order_list_with_invalid_table_filter(self):
        """
        Тестирование фильтрации заказов по некорректному номеру стола.
        """
        url = reverse('order_list')
        response = self.client.get(url, {'table': 'abc'})

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Некорректный номер стола' in str(m) for m in messages))

    def test_add_order_get(self):
        """
        Тестирование GET запроса для создания заказа.
        """
        url = reverse('add_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/add_order.html')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    def test_add_order_post_valid(self):
        """
        Тестирование успешного создания заказа.

        Для отправки корректных данных формы заказа и formset'а учитываются
        management-поля formset'а. Обратите внимание: формат и имена полей
        зависят от реализации OrderForm и OrderItemFormSet.
        """
        self.order.delete()

        url = reverse('add_order')
        order_data = {
            'table_number': '2',
        }
        formset_data = {
            'orderitems-TOTAL_FORMS': '1',
            'orderitems-INITIAL_FORMS': '0',
            'orderitems-MIN_NUM_FORMS': '0',
            'orderitems-MAX_NUM_FORMS': '1000',
            'orderitems-0-dish': str(self.dish.pk),
            'orderitems-0-quantity': '3',
        }
        post_data = {**order_data, **formset_data}

        response = self.client.post(url, data=post_data)
        self.assertRedirects(response, reverse('order_list'))

        new_order = Order.objects.filter(table_number=2).first()
        self.assertIsNotNone(new_order)

        self.assertEqual(new_order.items.count(), 1)
        order_item = new_order.items.first()
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.dish, self.dish)

    def test_delete_order_post(self):
        """
        Тестирование удаления заказа.
        """
        url = reverse('delete_order', kwargs={'pk': self.order.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('order_list'))
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())

    def test_delete_all_orders_post(self):
        """
        Тестирование удаления всех заказов.
        """
        Order.objects.create(table_number=2, status='pending')
        url = reverse('delete_all_orders')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('order_list'))
        self.assertEqual(Order.objects.count(), 0)


class RevenueViewTests(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name='Тест блюдо', price=Decimal('50.00'))
        self.order_paid = Order.objects.create(table_number=3, status='paid')
        OrderItem.objects.create(order=self.order_paid, dish=self.dish, quantity=2)

    def test_calculate_revenue(self):
        """
        Тестирование вычисления выручки от оплаченных заказов.
        """
        url = reverse('calculate_revenue')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe_orders/revenue.html')
        self.assertIn('revenue', response.context)

        self.assertEqual(Decimal(response.context['revenue']), Decimal('100.00'))



class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name='API Dish', price=Decimal('20.00'))
        self.order = Order.objects.create(table_number=5, status='pending')

    def test_search_action_by_table_number(self):
        """
        Тестирование поиска заказа по номеру стола через API.
        Предполагается, что URL для action `search` доступен по пути <orders_url>/search/
        """
        # Если OrderViewSet зарегистрирован с именем 'order-list' через DefaultRouter
        list_url = reverse('order-list')
        search_url = list_url + "search/"
        response = self.client.get(search_url, {'q': str(self.order.table_number)})
        self.assertEqual(response.status_code, 200)
        # Ожидается список заказов (хотя бы один)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_delete_all_action(self):
        """
        Тестирование удаления всех заказов через API.
        Предполагается, что URL для action `delete_all` доступен по пути <orders_url>/delete_all/
        """
        list_url = reverse('order-list')
        delete_all_url = list_url + "delete_all/"
        response = self.client.post(delete_all_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 'Все заказы удалены')
        self.assertEqual(Order.objects.count(), 0)