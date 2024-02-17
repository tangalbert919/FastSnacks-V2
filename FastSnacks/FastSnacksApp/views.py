from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import datetime

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

@login_required
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

class FavoritesView(LoginRequiredMixin, BaseView, ListView):
    template_name = "favorites.html"
    model = Item

    def get_queryset(self):
        favorites, _ = Favorites.objects.get_or_create(user=self.request.user)
        return favorites.items.all()

@login_required
def add_favorites(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        favorites, _ = Favorites.objects.get_or_create(user=request.user)
        item = Item.objects.get(id=form.data['itemID'])
        favorites.items.add(item)
        return HttpResponseRedirect("favorites")
    return HttpResponseRedirect("favorites")

@login_required
def remove_favorites(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        favorites, _ = Favorites.objects.get_or_create(user=request.user)
        item = Item.objects.get(id=form.data['itemID'])
        favorites.items.remove(item)
        return HttpResponseRedirect("favorites")
    return HttpResponseRedirect("favorites")

class ListItemsView(LoginRequiredMixin, BaseView, ListView):
    template_name = "list-items.html"
    model = Item
    queryset = Item.objects.all()
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["vending"] = VendingMachine.objects.all()
        return context

class CartView(LoginRequiredMixin, BaseView, ListView):
    template_name = "cart.html"
    model = Item

    def get_queryset(self) -> QuerySet[Any]:
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

@login_required
def add_to_cart(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = Item.objects.get(id=form.data['itemID'])
        cart.items.add(item)
        return HttpResponseRedirect("cart")
    return HttpResponseRedirect("cart")

class RewardsView(LoginRequiredMixin, BaseView, ListView):
    template_name = "rewards.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Item.objects.all()

class PaymentView(LoginRequiredMixin, BaseView, ListView, FormView):
    template_name = "payment-methods.html"
    form_class = PaymentMethodForm
    success_url = "/payment-methods"

    def get_queryset(self) -> QuerySet[Any]:
        return PaymentMethod.objects.all().filter(user=self.request.user)

@login_required
def add_payment_method(request):
    form = PaymentMethodForm(request.POST)
    if form.is_valid():
        card_no = form.cleaned_data["ccnum"]
        expmonth = form.cleaned_data["expmonth"]
        expyear = form.cleaned_data["expyear"]
        cvv = form.cleaned_data["cvv"]
        PaymentMethod.objects.create(user=request.user, card_no=card_no, \
                                     exp_month=expmonth, exp_year=expyear, 
                                     security_code=cvv, account_bal=0.00).save()
        return HttpResponseRedirect("payment-methods")
    return HttpResponseRedirect("payment-methods")

class TransactionView(LoginRequiredMixin, BaseView, ListView):
    template_name = "transaction-history.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.all()

class SupportView(LoginRequiredMixin, BaseView, FormView):
    template_name = "support-submit.html"
    form_class = SupportTicketForm
    success_url = "/support"

@login_required
def submit_support_ticket(request):
    form = SupportTicketForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        message = form.cleaned_data["message"]
        SupportTicket.objects.create(user=request.user, title=title, info=message, \
                                     date=datetime.datetime.now()).save()
        return HttpResponseRedirect("support-submit")
    return HttpResponseRedirect("support-submit")

class ProfileView(LoginRequiredMixin, BaseView, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["rewardPoints"] = Customer.objects.get(user=self.request.user).reward_points
        return context

class QueryView(LoginRequiredMixin, BaseView, TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context["snacks"] = Item.objects.all().filter(name__contains=query)
        return context
