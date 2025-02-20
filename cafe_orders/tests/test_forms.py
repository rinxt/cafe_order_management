from decimal import Decimal
from django.test import TestCase
from cafe_orders.forms import OrderForm, OrderItemForm, OrderItemFormSet, OrderItemEditFormSet
from cafe_orders.models import Order, Dish

class OrderFormTest(TestCase):
    def setUp(self):
        self.active_order = Order.objects.create(table_number=5, status='pending')

    def test_order_form_choices_provided(self):
        """
        Проверяет, что при передаче списка свободных столов
        поле 'table_number' получает правильные варианты выбора.
        """
        free_tables = [1, 2, 3, 4]
        form = OrderForm(free_tables=free_tables)
        expected_choices = [(1, "Стол 1"), (2, "Стол 2"), (3, "Стол 3"), (4, "Стол 4")]
        self.assertEqual(form.fields['table_number'].choices, expected_choices)

    def test_order_form_valid(self):
        """
        Проверяет корректную валидацию формы, когда выбран свободный стол.
        """
        free_tables = [1, 2, 3, 4, 6]
        form = OrderForm(data={'table_number': '2'}, free_tables=free_tables)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.clean_table_number(), 2)

class OrderItemFormTest(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name="Salad", price=Decimal("5.50"))

    def test_order_item_form_valid(self):
        """
        Проверяет, что форма позиции заказа проходит валидацию
        при корректном значении количества.
        """
        form = OrderItemForm(data={'dish': self.dish.pk, 'quantity': 2})
        self.assertTrue(form.is_valid())


class OrderItemFormSetTest(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name="Soup", price=Decimal("3.25"))
        self.order = Order.objects.create(table_number=8, status="pending")

    def _get_valid_data(self):
        """
        Возвращает словарь с корректными данными для OrderItemFormSet.
        Префикс formset-а здесь ожидается как 'orderitems' (как в представлениях).
        """
        return {
            'orderitems-TOTAL_FORMS': '1',
            'orderitems-INITIAL_FORMS': '0',
            'orderitems-MIN_NUM_FORMS': '0',
            'orderitems-MAX_NUM_FORMS': '1000',

            'orderitems-0-dish': str(self.dish.pk),
            'orderitems-0-quantity': '2',
        }

    def test_order_item_formset_valid(self):
        """
        Проверяет, что inline formset для позиции заказа проходит валидацию
        при корректных данных.
        """
        data = self._get_valid_data()
        formset = OrderItemFormSet(instance=self.order, data=data, prefix='orderitems')
        self.assertTrue(formset.is_valid(), formset.errors)


class OrderItemEditFormSetTest(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name="Pasta", price=Decimal("7.00"))
        self.order = Order.objects.create(table_number=10, status="pending")

        self.order_item = self.order.items.create(dish=self.dish, quantity=1)

    def _get_valid_data(self):
        """
        Возвращает корректные данные для OrderItemEditFormSet.
        Префикс соответствует тому, который используется во view (например, 'orderitems').
        """
        return {
            'orderitems-TOTAL_FORMS': '1',
            'orderitems-INITIAL_FORMS': '1',
            'orderitems-MIN_NUM_FORMS': '0',
            'orderitems-MAX_NUM_FORMS': '1000',

            'orderitems-0-id': str(self.order_item.pk),
            'orderitems-0-dish': str(self.dish.pk),
            'orderitems-0-quantity': '3',
            'orderitems-0-DELETE': '',
        }

    def test_order_item_edit_formset_valid(self):
        """
        Проверяет, что OrderItemEditFormSet проходит валидацию при корректных данных.
        """
        data = self._get_valid_data()
        formset = OrderItemEditFormSet(instance=self.order, data=data, prefix='orderitems')
        self.assertTrue(formset.is_valid(), formset.errors)