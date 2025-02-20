from django import forms

from .constants import TABLE_NUMBERS, ORDER_STATUS_MAP, FORM_CONTROL_CLASS, MESSAGES, DEFAULT_QUANTITY
from .models import Order, OrderItem
from django.forms import inlineformset_factory
from typing import List, Optional, Any, Tuple


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказов.
    """

    def __init__(self, *args: Any, free_tables: Optional[List[int]] = None, **kwargs: Any) -> None:
        """
        Инициализирует форму заказа.

        Args:
            *args: Произвольные аргументы.
            free_tables: Список свободных столов (опционально). Если не предоставлен, вычисляется автоматически.
            **kwargs: Произвольные именованные аргументы.
        """
        super().__init__(*args, **kwargs)

        if free_tables is None:
            all_tables: set = set(TABLE_NUMBERS)
            occupied_tables: set = set(
                Order.objects.filter(status__in=[ORDER_STATUS_MAP['в ожидании'], ORDER_STATUS_MAP['готово']])
                .values_list('table_number', flat=True))
            free_tables = sorted(list(all_tables - occupied_tables))

        choices: List[Tuple[int, str]] = [(table, f"Стол {table}") for table in free_tables]
        if not choices:
            choices = []  # хотя такой случай маловероятен, но оставляем пустой список вариантов

        self.fields['table_number'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': FORM_CONTROL_CLASS}),
            label="Стол"
        )

    def clean_table_number(self) -> int:
        """
        Валидирует номер стола.

        Returns:
            int: Номер стола после валидации.

        Raises:
            forms.ValidationError: Если на выбранном столе уже есть активный заказ.
        """
        table_number: int = int(self.cleaned_data.get('table_number'))
        if Order.objects.filter(table_number=table_number).exclude(status=ORDER_STATUS_MAP['оплачено']).exists():
            raise forms.ValidationError(MESSAGES['no_free_tables'])
        return table_number

    class Meta:
        """
        Метаданные формы.
        """
        model = Order
        fields: List[str] = ['table_number']


class OrderItemForm(forms.ModelForm):
    """
    Форма для создания и редактирования позиций заказа.
    """
    class Meta:
        """
        Метаданные формы.
        """
        model = OrderItem
        fields: List[str] = ['dish', 'quantity']
        widgets = {
            'dish': forms.Select(attrs={'class': FORM_CONTROL_CLASS}),
            'quantity': forms.NumberInput(attrs={'class': FORM_CONTROL_CLASS}),
        }

    def clean_quantity(self) -> int:
        """
        Валидирует количество блюд в позиции заказа.

        Returns:
            int: Количество блюд после валидации.

        Raises:
            forms.ValidationError: Если количество меньше 1.
        """
        quantity: int = self.cleaned_data.get('quantity')
        if quantity < DEFAULT_QUANTITY:
            raise forms.ValidationError(MESSAGES['add_at_least_one_dish'])
        return quantity


OrderItemFormSet: Any = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)

OrderItemEditFormSet: Any = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=0,
    can_delete=True,
)