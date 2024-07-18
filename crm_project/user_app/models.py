from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Добавление поля для номера телефона в модель User
    phone_number = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        db_table = "user"
        verbose_name = "Сотрудника"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
