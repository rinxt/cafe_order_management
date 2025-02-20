# URL Paths
URL_PATHS = {
    'dish_list': 'dishes/',
    'add_dish': 'dishes/add/',
    'edit_dish': 'dishes/<int:pk>/edit/',
    'delete_dish': 'dishes/<int:pk>/delete/',
    'order_list': '',
    'add_order': 'add/',
    'edit_order_status': 'orders/<int:pk>/edit/',
    'update_order': 'orders/<int:order_id>/edit_items/',
    'delete_order': 'delete/<int:pk>/',
    'delete_all_orders': 'orders/delete-all/',
    'update_order_status': 'orders/<int:pk>/update-status/',
    'calculate_revenue': 'revenue/',
}

# URL Names
URL_NAMES = {
    'dish_list': 'dish_list',
    'add_dish': 'add_dish',
    'edit_dish': 'edit_dish',
    'delete_dish': 'delete_dish',
    'order_list': 'order_list',
    'add_order': 'add_order',
    'edit_order_status': 'edit_order_status',
    'update_order': 'update_order',
    'delete_order': 'delete_order',
    'delete_all_orders': 'delete_all_orders',
    'update_order_status': 'update_order_status',
    'calculate_revenue': 'calculate_revenue',
}

# Table Numbers
MIN_TABLE_NUMBER = 1
MAX_TABLE_NUMBER = 15
TABLE_NUMBERS = range(MIN_TABLE_NUMBER, MAX_TABLE_NUMBER + 1)

# Order Status Mapping
ORDER_STATUS_MAP = {
    'в ожидании': 'pending',
    'готово': 'ready',
    'оплачено': 'paid'
}

# Default Order Status
DEFAULT_ORDER_STATUS = 'pending'

# Revenue Calculation Status
REVENUE_CALCULATION_STATUS = 'paid'

# Template Paths
TEMPLATE_PATHS = {
    'dish_list': 'cafe_orders/dish_list.html',
    'add_dish': 'cafe_orders/add_dish.html',
    'edit_dish': 'cafe_orders/edit_dish.html',
    'delete_dish': 'cafe_orders/delete_dish.html',
    'order_list': 'cafe_orders/order_list.html',
    'add_order': 'cafe_orders/add_order.html',
    'update_order': 'cafe_orders/update_order.html',
    'edit_order_status': 'cafe_orders/edit_order_status.html',
    'delete_all_orders': 'cafe_orders/delete_all_orders.html',
    'revenue': 'cafe_orders/revenue.html',
}

# Search Fields for OrderViewSet
ORDER_SEARCH_FIELDS = ['table_number', 'status']

# Success and Error Messages
MESSAGES = {
    'dish_added_success': 'Блюдо успешно добавлено.',
    'dish_added_error': 'Ошибка при добавлении блюда: {error}',
    'dish_updated_success': 'Блюдо успешно обновлено.',
    'dish_updated_error': 'Ошибка при обновлении блюда: {error}',
    'dish_deleted_success': 'Блюдо успешно удалено.',
    'dish_deleted_error': 'Ошибка при удалении блюда: {error}',
    'table_number_invalid': 'Некорректный номер стола.',
    'status_invalid': 'Некорректный статус заказа.',
    'order_added_success': 'Заказ успешно добавлен.',
    'order_added_error': 'Ошибка при создании заказа: {error}',
    'order_updated_success': 'Заказ успешно обновлен.',
    'order_updated_error': 'Ошибка при обновлении заказа: {error}',
    'no_changes_to_save': 'Нет изменений для сохранения.',
    'order_status_updated_success': 'Статус заказа обновлен.',
    'order_status_updated_error': 'Ошибка при обновлении статуса заказа: {error}',
    'order_deleted_success': 'Заказ успешно удален.',
    'all_orders_deleted_success': 'Все заказы успешно удалены.',
    'all_orders_deleted_error': 'Ошибка при удалении всех заказов: {error}',
    'revenue_calculation_error': 'Ошибка при расчете выручки: {error}',
    'no_free_tables': "Нет свободных столов на данный момент",
    'add_at_least_one_dish': 'Добавьте хотя бы одно блюдо к заказу.',
}

# Form Constants
FORM_CONTROL_CLASS = 'form-control'
DEFAULT_QUANTITY = 1

# Dish Model Constants
DISH_NAME_MAX_LENGTH = 100
DISH_PRICE_MAX_DIGITS = 7
DISH_PRICE_DECIMAL_PLACES = 2
DISH_PRICE_MIN_VALUE = '0.00'

# Order Model Constants
ORDER_STATUS_CHOICES = [
    ('pending', 'В ожидании'),
    ('ready', 'Готово'),
    ('paid', 'Оплачено'),
]
ORDER_TABLE_NUMBER_MIN_VALUE = 1

# OrderItem Model Constants
ORDER_ITEM_QUANTITY_MIN_VALUE = 1

# String Formatting
DISH_STR_FORMAT = "{name} - {price}₽"
ORDER_STR_FORMAT = "Заказ {id} - Стол {table_number}"
ORDER_ITEM_STR_FORMAT = "{dish_name} x {quantity} - {price}₽"

# Serializer Constants
ORDER_ITEM_FIELDS = ['id', 'dish', 'quantity', 'price']
ORDER_FIELDS = ['id', 'table_number', 'status', 'created_at', 'updated_at', 'total_price', 'items']
ORDER_READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at', 'total_price']