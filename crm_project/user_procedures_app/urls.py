from django.urls import path
from . import views

app_name = "user_procedures_app"

urlpatterns = [
    path("my_procedures/", views.my_procedures, name="my_procedures"),
    path("add_new_procedure/", views.add_new_procedure, name="add_new_procedure"),
    path(
        "add_procedure_to_user/<int:procedure_id>",
        views.add_procedure_to_user,
        name="add_procedure_to_user",
    ),
    path("contracts/", views.contracts, name="contracts"),
    path("add_new_contract/", views.add_new_contract, name="add_new_contract"),
    path(
        "update_procedure_status/",
        views.update_procedure_status,
        name="update_procedure_status",
    ),
    path("delete_procedure/", views.delete_procedure, name="delete_procedure"),
    path("update_contract/", views.update_contract, name="update_contract"),
]
