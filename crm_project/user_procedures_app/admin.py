from django.contrib import admin
from user_procedures_app.models import Contract, ManagerProcedure, ProcedureForUser


# Таблица для отображения процедур в профиле менеджера
class UserProcedureTabAdmin(admin.TabularInline):
    model = ManagerProcedure
    fields = ["procedure"]
    search_fields = "procedure"
    extra = 1


# Таблица отображения менеджеров и их процедур
@admin.register(ManagerProcedure)
class ManagerProcedureAdmin(admin.ModelAdmin):
    # отображение полей в админке
    list_display = [
        "user",
        "procedure",
    ]
    # фильтры по имени
    list_filter = ["user"]
    # поиск по имени и процедуре
    search_fields = [
        "user",
        "procedure",
    ]
    search_help_text = "Поиск по имени (name) и процедуре (procedure)"


# Таблица отображения всех процедур которые в работе
@admin.register(ProcedureForUser)
class ProcedureForUserAdmin(admin.ModelAdmin):
    # отображение полей в админке
    list_display = [
        "number",
        "purchase_name",
        "customer",
        "price",
        "end",
        "status",
    ]
    # сортировка по дате и цене
    ordering = ["end", "-price"]
    # фильтры по дате и статусу
    list_filter = ["end", "status"]
    # поле для поиска по номеру и заказчику
    search_fields = [
        "number",
        "customer",
    ]
    search_help_text = "Поиск по номеру процедуры (number) и заказчику (customer)"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    # отображение полей в админке
    list_display = [
        "number",
        "status",
        "start",
        "end",
        "price",
        "purchase_name",
        "customer",
    ]
    # сортировка по дате и цене
    ordering = ["start", "status", "-price"]
    # фильтры по дате и статусу
    list_filter = ["start", "status"]
    list_editable = ["status"]
    # поле для поиска по номеру и заказчику
    search_fields = [
        "number",
        "customer",
        "purchase_name",
    ]
    search_help_text = "Поиск по номеру процедуры (number), заказчику (customer) и предмету закупки (purchase_name)"
