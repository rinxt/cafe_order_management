from django.db.models.fields import DecimalField
from django.forms.models import ModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, ExpressionWrapper, F, QuerySet
from django.contrib import messages
from typing import List, Dict, Any, Optional

from .models import Order, OrderItem, Dish
from .forms import OrderForm, OrderItemFormSet, OrderItemEditFormSet
from .serializers import OrderSerializer


class DishForm(ModelForm):
    """
    Форма для создания и редактирования блюд.
    """
    class Meta:
        """
        Метаданные формы.
        """
        model = Dish
        fields: List[str] = ['name', 'price']


def dish_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список всех блюд.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ со списком блюд.
    """
    dishes: QuerySet[Dish] = Dish.objects.all()
    return render(request, 'cafe_orders/dish_list.html', {'dishes': dishes})


def add_dish(request: HttpRequest) -> HttpResponse:
    """
    Добавляет новое блюдо.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ с формой добавления блюда или перенаправление на список блюд после успешного добавления.
    """
    if request.method == 'POST':
        form: DishForm = DishForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Блюдо успешно добавлено.')
                return redirect('dish_list')
            except Exception as e:
                messages.error(request, f'Ошибка при добавлении блюда: {str(e)}')
    else:
        form = DishForm()
    return render(request, 'cafe_orders/add_dish.html', {'form': form})


def edit_dish(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Редактирует существующее блюдо.

    Args:
        request: Объект HTTP-запроса.
        pk: Первичный ключ блюда, которое нужно отредактировать.

    Returns:
        HttpResponse: Ответ с формой редактирования блюда или перенаправление на список блюд после успешного редактирования.
    """
    dish: Dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form: DishForm = DishForm(request.POST, instance=dish)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Блюдо успешно обновлено.')
                return redirect('dish_list')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении блюда: {str(e)}')
    else:
        form = DishForm(instance=dish)
    return render(request, 'cafe_orders/edit_dish.html', {'form': form})


def delete_dish(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Удаляет блюдо.

    Args:
        request: Объект HTTP-запроса.
        pk: Первичный ключ блюда, которое нужно удалить.

    Returns:
        HttpResponse: Ответ с подтверждением удаления блюда или перенаправление на список блюд после успешного удаления.
    """
    dish: Dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        try:
            dish.delete()
            messages.success(request, "Блюдо успешно удалено.")
            return redirect('dish_list')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении блюда: {str(e)}')
    return render(request, 'cafe_orders/delete_dish.html', {'dish': dish})


def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список заказов с возможностью фильтрации по номеру стола и статусу.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ со списком заказов и формой фильтрации.
    """
    table_query: str = request.GET.get('table', '').strip()
    status_query: str = request.GET.get('status', '').strip()

    orders: QuerySet[Order] = Order.objects.all()

    if table_query:
        if table_query.isdigit():
            try:
                table_number: int = int(table_query)
                orders = orders.filter(table_number=table_number)
            except ValueError:
                messages.error(request, 'Некорректный номер стола.')
        else:
            messages.error(request, 'Некорректный номер стола.')

    status_map: Dict[str, str] = {
        'в ожидании': 'pending',
        'готово': 'ready',
        'оплачено': 'paid'
    }

    if status_query:
        mapped_status: str = status_map.get(status_query.lower(), '')
        if mapped_status:
            orders = orders.filter(status__iexact=mapped_status)
        else:
            messages.error(request, 'Некорректный статус заказа.')

    context: Dict[str, Any] = {
        'orders': orders,
        'table_query': table_query,
        'status_query': status_query,
    }
    return render(request, 'cafe_orders/order_list.html', context)


def add_order(request: HttpRequest) -> HttpResponse:
    """
    Добавляет новый заказ.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ с формой добавления заказа или перенаправление на список заказов после успешного добавления.
    """
    all_tables: set = set(range(1, 16))
    occupied_tables: set = set(Order.objects.filter(status__in=['pending', 'ready']).values_list('table_number', flat=True))
    free_tables: List[int] = sorted(list(all_tables - occupied_tables))

    if not free_tables:
        messages.error(request, "Нет свободных столов на данный момент")
        return redirect('order_list')

    if request.method == 'POST':
        form: OrderForm = OrderForm(request.POST, free_tables=free_tables)
        formset: OrderItemFormSet = OrderItemFormSet(request.POST, prefix='orderitems')

        if form.is_valid() and formset.is_valid():
            try:
                order: Order = form.save(commit=False)
                order.status = 'pending'
                order.save()
                formset.instance = order
                if formset.has_changed():
                    formset.save()
                else:
                    messages.warning(request, 'Добавьте хотя бы одно блюдо к заказу.')
                    return render(
                        request,
                        'cafe_orders/add_order.html',
                        {'form': form, 'formset': formset}
                    )

                messages.success(request, 'Заказ успешно добавлен.')
                return redirect('order_list')
            except Exception as e:
                messages.error(request, f'Ошибка при создании заказа: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = OrderForm(free_tables=free_tables)
        formset = OrderItemFormSet(prefix='orderitems')

    return render(
        request,
        'cafe_orders/add_order.html',
        {'form': form, 'formset': formset}
    )


def update_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обновляет существующий заказ.

    Args:
        request: Объект HTTP-запроса.
        order_id: Первичный ключ заказа, который нужно обновить.

    Returns:
        HttpResponse: Ответ с формой редактирования заказа или перенаправление на список заказов после успешного обновления.
    """
    order: Order = get_object_or_404(Order, id=order_id)
    order_items: QuerySet[OrderItem] = order.items.all()
    initial: List[Dict[str, Any]] = [{'id': item.id, 'dish': item.dish, 'quantity': item.quantity} for item in order_items]

    if request.method == 'POST':
        formset: OrderItemEditFormSet = OrderItemEditFormSet(request.POST, instance=order, initial=initial, prefix='orderitems')
        if formset.is_valid():
            try:
                if formset.has_changed():
                    formset.save()
                    messages.success(request, 'Заказ успешно обновлен.')
                    return redirect('order_list')
                else:
                    messages.warning(request, 'Нет изменений для сохранения.')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении заказа: {str(e)}')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        formset = OrderItemEditFormSet(instance=order, initial=initial, prefix='orderitems')

    return render(
        request,
        'cafe_orders/update_order.html',
        {'order': order, 'formset': formset}
    )


def edit_order_status(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Редактирует статус заказа.

    Args:
        request: Объект HTTP-запроса.
        pk: Первичный ключ заказа, статус которого нужно изменить.

    Returns:
        HttpResponse: Ответ с формой редактирования статуса заказа или перенаправление на список заказов после успешного обновления.
    """
    order: Order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form: OrderForm = OrderForm(request.POST, instance=order)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Статус заказа обновлен.')
                return redirect('order_list')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса заказа: {str(e)}')
    else:
        form = OrderForm(instance=order)
    return render(request, 'cafe_orders/edit_order_status.html', {'form': form, 'order': order})


def delete_order(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Удаляет заказ.

    Args:
        request: Объект HTTP-запроса.
        pk: Первичный ключ заказа, который нужно удалить.

    Returns:
        HttpResponse: Перенаправление на список заказов после успешного удаления.
    """
    order: Order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        try:
            order.delete()
            messages.success(request, 'Заказ успешно удален.')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении заказа: {str(e)}')
    return redirect('order_list')


def delete_all_orders(request: HttpRequest) -> HttpResponse:
    """
    Удаляет все заказы.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Перенаправление на список заказов после успешного удаления.
    """
    if request.method == 'POST':
        try:
            Order.objects.all().delete()
            messages.success(request, 'Все заказы успешно удалены.')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении всех заказов: {str(e)}')
        return redirect('order_list')
    return render(request, 'cafe_orders/delete_all_orders.html')


def update_order_status(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Обновляет статус заказа через POST-запрос.

    Args:
        request: Объект HTTP-запроса.
        pk: Первичный ключ заказа, статус которого нужно обновить.

    Returns:
        HttpResponse: Перенаправление на список заказов после успешного обновления.
    """
    order: Order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status: Optional[str] = request.POST.get('status')
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if new_status in valid_statuses:
            try:
                order.status = new_status  # type: ignore
                order.save()
                messages.success(request, 'Статус заказа обновлен.')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса: {str(e)}')
        else:
            messages.error(request, 'Неверный статус заказа.')
    return redirect('order_list')


def calculate_revenue(request: HttpRequest) -> HttpResponse:
    """
    Вычисляет выручку от оплаченных заказов.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ с суммой выручки.
    """
    try:
        revenue_data: Dict[str, Any] = OrderItem.objects.filter(order__status='paid').aggregate(
            total_revenue=Sum(
                ExpressionWrapper(F('dish__price') * F('quantity'), output_field=DecimalField())
            )
        )
        revenue: Any = revenue_data.get('total_revenue') or 0
    except Exception as e:
        messages.error(request, f'Ошибка при расчете выручки: {str(e)}')
        revenue = 0
    return render(request, 'cafe_orders/revenue.html', {'revenue': revenue})


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра, создания, редактирования и удаления заказов.
    Включает поиск по номеру стола и статусу.
    Реализовано полное редактирование заказа (изменение блюд).
    """
    serializer_class: type = OrderSerializer
    filter_backends: List = [filters.SearchFilter]
    search_fields: List[str] = ['table_number', 'status']

    def get_queryset(self) -> QuerySet[Order]:
        """
        Возвращает queryset заказов с возможностью фильтрации по параметрам запроса.

        Returns:
            QuerySet: Отфильтрованный queryset заказов.
        """
        queryset: QuerySet[Order] = Order.objects.all().order_by('-created_at')
        table_query: str = self.request.query_params.get('table', '').strip()
        status_query: str = self.request.query_params.get('status', '').strip()

        if table_query and table_query.isdigit():
            try:
                table_number: int = int(table_query)
                queryset = queryset.filter(table_number=table_number)
            except ValueError:
                pass

        status_map: Dict[str, str] = {
            'в ожидании': 'pending',
            'готово': 'ready',
            'оплачено': 'paid'
        }
        if status_query and status_query.lower() != 'все статусы':
            mapped_status: Optional[str] = status_map.get(status_query.lower())
            if mapped_status:
                queryset = queryset.filter(status__iexact=mapped_status)
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request: HttpRequest) -> Response:
        """
        Action для поиска заказов по параметру "q".

        Args:
            request: Объект HTTP-запроса.

        Returns:
            Response: Ответ с сериализованными данными заказов.
        """
        q: str = request.query_params.get('q', '').strip()
        queryset: QuerySet[Order] = self.get_queryset()
        if q:
            if q.isdigit():
                queryset = queryset.filter(table_number=int(q))
            else:
                queryset = queryset.filter(status__iexact=q)
        serializer: OrderSerializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def delete_all(self, request: HttpRequest) -> Response:
        """
        Action для удаления всех заказов.

        Args:
            request: Объект HTTP-запроса.

        Returns:
            Response: Ответ с подтверждением удаления всех заказов.
        """
        try:
            Order.objects.all().delete()
            return Response({'status': 'Все заказы удалены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': f'Ошибка при удалении заказов: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)