from django import forms
from user_procedures_app.models import Contract, ProcedureForUser


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = (
            "method",
            "number",
            "purchase_name",
            "customer",
            "price",
            "start",
            "end",
            "purchase_link",
        )

    method = forms.CharField(
        label="Способ определния поставщика",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите способ определния поставщика",
            }
        ),
    )
    number = forms.CharField(
        label="Номер процедуры",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите номер закупки",
            }
        ),
    )
    purchase_name = forms.CharField(
        label="Предмет закупки",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите предмет закупки",
            }
        ),
    )
    customer = forms.CharField(
        label="Заказчик",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите название Заказчика",
            }
        ),
    )
    price = forms.DecimalField(
        label="Цена контракта",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите цену контракта",
            }
        ),
    )
    start = forms.DateField(
        label="Дата подписания контракта участником",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Введите дату подписания контракта участником",
            }
        ),
    )
    end = forms.DateField(
        label="Дата заключения контракта",
        required=False,  # необязательно поле дял заполнения
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Введите дату заключения контракта",
            }
        ),
    )
    purchase_link = forms.URLField(
        label="Ссылка на процедуру",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ссылку на закупку",
            }
        ),
    )


class ProcedureForUserForm(forms.ModelForm):

    class Meta:
        model = ProcedureForUser
        fields = (
            "method",
            "number",
            "purchase_name",
            "customer",
            "price",
            "start",
            "update",
            "end",
            "purchase_link",
        )

    method = forms.CharField(
        label="Способ определния поставщика",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите способ определния поставщика",
            }
        ),
    )
    number = forms.CharField(
        label="Номер процедуры",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите номер процедуры",
            }
        ),
    )
    purchase_name = forms.CharField(
        label="Предмет закупки",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите предмет закупки",
            }
        ),
    )
    customer = forms.CharField(
        label="Заказчик",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите название Заказчика",
            }
        ),
    )
    price = forms.DecimalField(
        label="Начальная цена",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите начальную цену",
                "min": "0.00",
                "step": "0.01",
            }
        ),
    )
    start = forms.DateField(
        label="Дата размещения процедуры",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Введите дату размещения процедуры",
            }
        ),
    )
    update = forms.DateField(
        label="Дата изменения документации",
        required=False,  # необязательно поле дял заполнения
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Введите дату изменения документации",
            }
        ),
    )
    end = forms.DateField(
        label="Дата окончания подачи заявок",
        required=False,  # необязательно поле дял заполнения
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Введите дату окончания подачи заявок",
            }
        ),
    )
    purchase_link = forms.URLField(
        label="Ссылка на процедуру",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ссылку на закупку",
            }
        ),
    )
