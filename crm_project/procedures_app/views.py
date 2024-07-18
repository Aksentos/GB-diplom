import datetime as dt
import requests as req
from bs4 import BeautifulSoup as bs
from django.shortcuts import redirect, render

from .models import Archive, NewProcedures
from user_app.models import User
from user_procedures_app.models import Contract, ProcedureForUser, ManagerProcedure


# Стартовая странциа
def index(request):
    managers = User.objects.all()
    user_procedures = ManagerProcedure.objects.all()
    contracts = Contract.objects.all().count()
    context = {
        "title": "CRM 44 FZ",
        "content": "Главная страница CRM",
        "managers": managers,
        "user_procedures": user_procedures,
        "contracts": contracts,
    }
    return render(request, "main/index.html", context)


# страница с новыми закупками
def new(request):
    context = {
        "title": "Новые закупки",
        "procedures": NewProcedures.objects.order_by(
            "end"
        ),  # Сортировка по возрастанию даты
    }
    return render(request, "main/new.html", context)


# страница со всеми закупками
def archive(request):
    arch = Archive.objects.all()
    for item in arch:
        if not item.end_submission():
            item.delete()
    context = {
        "title": "Архив процедур",
        "procedures": Archive.objects.order_by("-end"),  # Сортировка по убыванию даты
    }
    return render(request, "main/archive.html", context)


# страница инфо
def about(request):
    return render(request, "main/about.html")


# функция собирает данные для обработки с сайта закупок
def get_data():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    }
    # сайт с настроенными фильтрами
    URL = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=%D0%94%D0%B0%' \
        'D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false' \
        '&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&af=on&currencyIdGeneral=' \
        '-1&okpd2IdsWithNested=on&okpd2Ids=8874055&okpd2IdsCodes=26.2&gws=' \
        %D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+' \
        %D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=' \
        on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0"

    try:
        page = req.get(URL, headers=HEADERS)
    except Exception as e:
        return None

    if page:  # возвращает True если page.status_code == 200
        soup = bs(
            page.text, "lxml"
        )  # "lxml" установлен вместо "html.parser" для улучшения обработки
        data = soup.find_all("div", class_="row no-gutters registry-entry__form mr-0")
        return data
    return None


# Обрабатка данных и формирует словарь
def add_data_dict(data) -> dict:
    bd = {}
    id = 1
    for item in data:
        # Способ определния поставщика
        method = " ".join(
            item.find(
                "div",
                class_="col-9 p-0 registry-entry__header-top__title text-truncate",
            )
            .text.replace("\n", "")
            .split()
        )
        # номер процедуры
        number = (
            item.find("div", class_="registry-entry__header-mid__number")
            .text.replace("\n", "")
            .replace("№", "")
            .strip()
        )
        # предмет закупки
        purchase_name = (
            item.find("div", class_="registry-entry__body-value")
            .text.replace("\n", "")
            .strip()
        )
        # заказчик
        customer = (
            item.find("div", class_="registry-entry__body-href")
            .text.replace("\n", "")
            .strip()
        )
        # начальная цена
        price = (
            item.find("div", class_="price-block__value").text.replace("\n", "").strip()
        )
        # Даты
        start, update, end = item.find_all("div", class_="data-block__value")
        # Размещено
        start = dt.datetime.strptime(start.text, "%d.%m.%Y").date()
        # Обновлено
        update = dt.datetime.strptime(update.text, "%d.%m.%Y").date()
        # Окончание подачи заявок
        end = dt.datetime.strptime(end.text, "%d.%m.%Y").date()
        # получаем ссылку на закупку по номеру
        url_data = item.find("div", class_="registry-entry__header-mid__number")
        purchase_link = "https://zakupki.gov.ru" + url_data.find(
            "a", target="_blank"
        ).get("href")

        bd[id] = {
            "method": method,
            "number": number,
            "purchase_name": purchase_name,
            "customer": customer,
            "price": price,
            "start": start,
            "update": update,
            "end": end,
            "purchase_link": purchase_link,
        }

        id += 1
    return bd


# добавление новых закупок на страницу
def update_procedures(request):
    bd = add_data_dict(get_data())  # формируем новый словарь с закупками
    NewProcedures.objects.all().delete()  # убираем закупки из БД
    if request.method == "POST":
        for k, v in bd.items():
            _, created = NewProcedures.objects.get_or_create(
                id=k,
                method=v["method"],
                number=v["number"],
                purchase_name=v["purchase_name"],
                customer=v["customer"],
                price=v["price"],
                start=v["start"],
                update=v["update"],
                end=v["end"],
                purchase_link=v["purchase_link"],
            )
    update_archive()  # добавляем все новые закупки в общий архив
    return redirect("main:new")


# для добавления закупок в архив
def update_archive():
    procedures = NewProcedures.objects.all()
    for item in procedures:
        if item.number not in Archive.objects.all():
            Archive.objects.get_or_create(
                method=item.method,
                number=item.number,
                purchase_name=item.purchase_name,
                customer=item.customer,
                price=item.price,
                start=item.start,
                update=item.update,
                end=item.end,
                purchase_link=item.purchase_link,
            )
