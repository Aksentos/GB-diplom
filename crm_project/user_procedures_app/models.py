from django.db import models
from django.core.validators import MinValueValidator
from user_app.models import User


# Create your models here.
class ProcedureForUser(models.Model):
    STAUS_CHOICES = [
        ("at_work", "В работе"),
        ("submitted", "Подана"),
        ("withdrawn", "Отозвана"),
    ]
    method = models.CharField("Способ определния поставщика", max_length=30)
    number = models.CharField("Номер процедуры", max_length=25)
    purchase_name = models.CharField("Предмет закупки", max_length=500)
    customer = models.CharField("Заказчик", max_length=200)
    price = models.CharField("Начальная цена", max_length=150)
    start = models.DateField("Размещено")
    update = models.DateField("Обновлено")
    end = models.DateField("Окончание подачи заявок", max_length=25)
    purchase_link = models.URLField("Ссылка на процедуру", max_length=300)
    status = models.CharField(
        verbose_name="Статус", max_length=10, choices=STAUS_CHOICES, default="at_work"
    )

    class Meta:
        db_table = "procedures_for_user"
        verbose_name = "Процедуру"
        verbose_name_plural = "Все Процедуры в работе"

    def __str__(self) -> str:
        return f"{self.number} {self.price}"


class ManagerProcedure(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Менеджер")
    procedure = models.ForeignKey(
        to=ProcedureForUser, on_delete=models.CASCADE, verbose_name="Закупка"
    )

    class Meta:
        db_table = "managers_procedures"
        verbose_name = "Процедуру"
        verbose_name_plural = "Процедуры менеджеров"

    def __str__(self) -> str:
        return f"{self.user} {self.procedure}"


class Contract(models.Model):
    STATUS_CHOICES = [
        ("at_signing", "На подписании"),
        ("at_performance", "На исполнении"),
        ("executed", "Исполнен"),
    ]
    status = models.CharField(
        "Статус", max_length=14, choices=STATUS_CHOICES, default="at_signing"
    )
    method = models.CharField("Способ определния поставщика", max_length=30)
    number = models.CharField("Номер процедуры", max_length=25)
    purchase_name = models.CharField("Предмет закупки", max_length=500)
    customer = models.CharField("Заказчик", max_length=200)
    price = models.DecimalField(
        "Цена контракта",
        max_digits=11,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    start = models.DateField("Дата подписания контракта участником", null=True, blank=True, default=None)
    end = models.DateField("Дата заключения контракта", null=True, blank=True, default=None)
    purchase_link = models.URLField("Ссылка на процедуру", max_length=300)

    def __str__(self) -> str:
        return f"{self.number} {self.status}"

    class Meta:
        db_table = "contracts"
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
