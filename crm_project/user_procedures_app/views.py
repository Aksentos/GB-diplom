from django.shortcuts import redirect, render
from procedures_app.models import Archive, NewProcedures
from .forms import ContractForm, ProcedureForUserForm
from .models import Contract, ProcedureForUser, ManagerProcedure


# страница с процедурами пользователя
def my_procedures(request):
    # Получаем список процедур пользователя, отсортированы по дате окночания подачи заявки по возрастанию
    procedures = ManagerProcedure.objects.filter(user=request.user).order_by(
        "procedure__end"
    )
    context = {
        "title": "Мои закупки",
        "staff": request.user,
        "procedures": procedures,
    }
    return render(request, "user_procedures_app/my_procedures.html", context)


def add_new_procedure(request):
    if request.method == "POST":
        form = ProcedureForUserForm(request.POST)
        if form.is_valid():
            new_procedure = form.save()
            ManagerProcedure.objects.create(user=request.user, procedure=new_procedure)
            return redirect("user_procedures_app:my_procedures")

    else:
        form = ProcedureForUserForm()
    context = {"title": "Добавить процедуру", "form": form}
    return render(request, "user_procedures_app/new_procedure.html", context)


def add_procedure_to_user(request, procedure_id):
    # првоерка с какой страницы нам пришел запрос
    if request.META.get("HTTP_REFERER").endswith("archive/"):
        procedure = Archive.objects.get(pk=procedure_id)
    else:
        procedure = NewProcedures.objects.get(pk=procedure_id)

    user = request.user
    if procedure.number not in [item.number for item in ProcedureForUser.objects.all()]:
        new_procedure_for_user = ProcedureForUser(
            method=procedure.method,
            number=procedure.number,
            purchase_name=procedure.purchase_name,
            customer=procedure.customer,
            price=procedure.price,
            start=procedure.start,
            update=procedure.update,
            end=procedure.end,
            purchase_link=procedure.purchase_link,
            status="at_work",  # Устанавливаем статус "В работе"
        )
        # Сохранение нового экземпляра в базе данных
        new_procedure_for_user.save()

        # Закрепляем закупку за авторизованным менеджером
        ManagerProcedure.objects.create(user=user, procedure=new_procedure_for_user)

    return redirect("procedures_app:new")


def contracts(request):
    all_contracts = Contract.objects.all().order_by("start")
    context = {
        "title": "Контракты",
        "all_contracts": all_contracts,
    }
    return render(request, "user_procedures_app/contracts.html", context)


def add_new_contract(request):

    if request.method == "POST":
        procedure_id = request.POST.get("procedure_id")
        if procedure_id:  # Обработка из заявок в контракты
            procedure = ProcedureForUser.objects.get(pk=procedure_id)
            if procedure.number not in [item.number for item in Contract.objects.all()]:
                Contract.objects.create(
                    method=procedure.method,
                    number=procedure.number,
                    purchase_name=procedure.purchase_name,
                    customer=procedure.customer,
                    purchase_link=procedure.purchase_link,
                    status="at_signing",  # Устанавливаем статус "На подписании"
                )
                return redirect("user_procedures_app:contracts")

        else:  # Обработка формы создания нового контракта
            form = ContractForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("user_procedures_app:contracts")
    else:
        form = ContractForm()  # Пустая форма для добавления нового контракта
    context = {"title": "Добавить Контракт", "form": form}
    return render(request, "user_procedures_app/new_contract.html", context)


#  Изменеие статуса заявок
def update_procedure_status(request):
    if request.method == "POST":
        procedure_id = request.POST.get("procedure_id")
        new_status = request.POST.get("status")

        user_procedure = ManagerProcedure.objects.get(procedure_id=procedure_id)
        user_procedure.procedure.status = new_status
        user_procedure.procedure.save()

        return redirect("user_procedures_app:my_procedures")


def delete_procedure(request):
    if request.method == "POST":
        procedure_id = request.POST.get("procedure_id")

        user_procedure = ManagerProcedure.objects.get(procedure_id=procedure_id)
        user_procedure.delete()

        return redirect("user_procedures_app:my_procedures")


def update_contract(request):
    if request.method == "POST":
        contract_id = request.POST.get("contract_id")
        new_status = request.POST.get("status")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        new_price = request.POST.get("price")

        contract = Contract.objects.get(id=contract_id)
        if new_status:
            contract.status = new_status
        if start_date:
            contract.start = start_date
        if end_date:
            contract.end = end_date
        if new_price:
            contract.price = new_price

        contract.save()

        return redirect("user_procedures_app:contracts")
