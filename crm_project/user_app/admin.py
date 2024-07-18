from django.contrib import admin
from .models import User
from user_procedures_app.admin import UserProcedureTabAdmin


# Таблица отображения сотрудников
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # список отображения полей
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    # поле поиска
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    # настрока отображения полей конкретного сотруднка
    fieldsets = [
        (
            None,
            {
                "classes": ["wide"],  # будет занимать все доступное место на странице
                "fields": [
                    "first_name",
                    "last_name",
                ],
            },
        ),
        (
            "Контакты",
            {
                "classes": ["collapse"],  # будет скрыто в раскрывающемся меню
                "fields": ["username", "email", "phone_number"],
            },
        ),
        (
            "Группы и разрешения",
            {
                "fields": ["groups", "user_permissions"],
            },
        ),
        (
            "Статусы",
            {
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ),
        (
            None,
            {
                "fields": ["last_login", "date_joined"],
            },
        ),
    ]
    filter_horizontal = ("user_permissions",)
    # встраиваем таблицу отображения взятых в работу закупок, с возможностью добавления новой закупки
    inlines = [UserProcedureTabAdmin]
