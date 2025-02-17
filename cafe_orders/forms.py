from django import forms
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
            all_tables: set = set(range(1, 16))
            occupied_tables: set = set(Order.objects.filter(status__in=['pending', 'ready'])
                                       .values_list('table_number', flat=True))
            free_tables = sorted(list(all_tables - occupied_tables))

        choices: List[Tuple[int, str]] = [(table, f"Стол {table}") for table in free_tables]
        if not choices:
            choices = []  # хотя такой случай маловероятен, но оставляем пустой список вариантов

        self.fields['table_number'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
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
        if Order.objects.filter(table_number=table_number).exclude(status='paid').exists():
            raise forms.ValidationError(
                "На данном столе уже оформлен активный заказ. "
                "Пожалуйста, выберите другой стол."
            )
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
            'dish': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
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
        if quantity < 1:
            raise forms.ValidationError("Количество должно быть не меньше 1.")
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