from django.urls import path
from . import views

app_name = "procedures_app"

urlpatterns = [
    path("", views.index, name="index"),  # домашняя страница
    path("about/", views.about, name="about"),  # о нас
    path("new/", views.new, name="new"),  # новые закупки
    path("update_procedures/", views.update_procedures, name="update_procedure"),  # обновление закупок
    path("archive/", views.archive, name="archive"),  # архив
]
