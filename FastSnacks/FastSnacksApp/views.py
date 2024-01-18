from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Favorites

# Create your views here.
# TODO: Have all views inherit this class
class BaseView(View):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.get_username()
        return context

class HomeView(BaseView, TemplateView):
    template_name = "index.html"

# Handle login/logout/registration
class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super().get(request)

    def post(self, request):
        username = request.POST["username"]
        if not username:
            return render(request, "login.html", context={'error': '1'})
        password = request.POST["password"]
        if not password:
            return render(request, "login.html", context={'error': '2'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", context={'error': '3'})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

class RegisterView(TemplateView):
    template_name = "register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super().get(request)

    def post(self, request):
        username = request.POST["username"]
        if not username:
            return render(request, "register.html", context={'error': '1'})
        password = request.POST["password"]
        password_repeat = request.POST["password-repeat"]
        if not password or not password_repeat:
            return render(request, "register.html", context={'error': '2'})
        if password != password_repeat:
            return render(request, "register.html", context={'error': '3'})
        try:
            User.objects.create_user(username=username, password=password)
            return render(request, "login.html", context={'isRegistrationSuccessful': True})
        except:
            return render(request, "register.html", context={'error': '4'})

class FavoritesView(BaseView, ListView):
    queryset = Favorites.objects.all()
    template_name = "favorites.html"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("authenticated")
        else:
            return HttpResponse("not authenticated")