import datetime
from django.db import models


# БД с новыми процедурами
class NewProcedures(models.Model):
    method = models.CharField("Способ определния поставщика", max_length=30)
    number = models.CharField("Номер процедуры", max_length=25)
    purchase_name = models.CharField("Предмет закупки", max_length=150)
    customer = models.CharField("Заказчик", max_length=200)
    price = models.CharField("Начальная цена", max_length=150)
    start = models.DateField("Размещено")
    update = models.DateField("Обновлено")
    end = models.DateField("Окончание подачи заявок", max_length=25)
    purchase_link = models.URLField("Ссылка на процедуру", max_length=150)

    # Имена табличек в админке
    class Meta:
        verbose_name = "Новую процедуру"
        verbose_name_plural = "Новые процедуры"

    def __str__(self) -> str:
        return f"№ {self.number}, НМЦК: {self.price}, Предмет закупки: {self.purchase_name}"


# БД с архивными процедурами
class Archive(models.Model):
    method = models.CharField("Способ определния поставщика", max_length=30)
    number = models.CharField("Номер процедуры", max_length=25)
    purchase_name = models.CharField("Предмет закупки", max_length=150)
    customer = models.CharField("Заказчик", max_length=200)
    price = models.CharField("Начальная цена", max_length=150)
    start = models.DateField("Размещено")
    update = models.DateField("Обновлено")
    end = models.DateField("Окончание подачи заявок", max_length=25)
    purchase_link = models.URLField("Ссылка на процедуру", max_length=150)

    def __str__(self) -> str:
        return f"№ {self.number} {self.end} {self.purchase_name}"

    # Проверка на "срок годности"
    def end_submission(self) -> bool:
        delta_days = 90
        return datetime.datetime.fromisoformat(str(self.end)) >= (
            datetime.datetime.today() - datetime.timedelta(days=delta_days)
        )

    class Meta:
        verbose_name = "Процедуру"
        verbose_name_plural = "Архив"
