from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth, messages


# Обработка Login
class UserLoginView(LoginView):

    template_name = "user_app/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user:
            auth.login(self.request, user)
        return redirect("procedures_app:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context


class UserRegistrationView(CreateView):
    template_name = "user_app/registration.html"
    form_class = UserRegistrationForm

    # Если форма заполнена верно, сразу сохраняем в БД и выполняем вход
    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

        return redirect("procedures_app:index")

    # добавляем в контекст название страницы "Регистрация"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect("procedures_app:index")
