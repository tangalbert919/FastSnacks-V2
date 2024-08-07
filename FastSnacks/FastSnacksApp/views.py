from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
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

@login_required
def delete_user(request):
    user = User.objects.get(username=request.user.get_username())
    logout(request)
    user.delete()
    return HttpResponseRedirect("/")

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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["price"] = cart.price
        return context

@login_required
def add_to_cart(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = Item.objects.get(id=form.data['itemID'])
        cart.items.add(item)
        return HttpResponseRedirect("cart")
    return HttpResponseRedirect("cart")

@login_required
def remove_from_cart(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = Item.objects.get(id=form.data['itemID'])
        cart.items.remove(item)
        return HttpResponseRedirect("cart")
    return HttpResponseRedirect("cart")

class RewardsView(LoginRequiredMixin, BaseView, ListView):
    template_name = "rewards.html"
    model = Reward
    queryset = Reward.objects.all()

class PaymentView(LoginRequiredMixin, BaseView, ListView, FormView):
    template_name = "payment-methods.html"
    form_class = PaymentMethodForm
    success_url = "/payment-methods"

    def get_queryset(self) -> QuerySet[Any]:
        return PaymentMethod.objects.all().filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context["cart"] = cart.items.all()
        context["cart_price"] = cart.price
        return context

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

@login_required
def remove_payment_method(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        item = PaymentMethod.objects.get(id=form.data['itemID']).delete()
        return HttpResponseRedirect("payment-methods")
    return HttpResponseRedirect("payment-methods")

class TransactionView(LoginRequiredMixin, BaseView, ListView):
    template_name = "transaction-history.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.all().filter(user=self.request.user)

class SupportView(LoginRequiredMixin, BaseView, FormView):
    template_name = "support-submit.html"
    form_class = SupportTicketForm
    success_url = "/support"

    def form_valid(self, form):
        title = form.cleaned_data["title"]
        message = form.cleaned_data["message"]
        SupportTicket.objects.create(user=self.request.user, title=title, info=message, \
                                     date=datetime.datetime.now()).save()
        return super().form_valid(form)

class SupportTicketView(LoginRequiredMixin, BaseView, TemplateView):
    template_name = "support-ticket.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        print(kwargs)
        context = super().get_context_data(**kwargs)
        ticket = get_object_or_404(SupportTicket, id=self.kwargs['pk'])
        context["ticket"] = ticket
        return context

class ProfileView(LoginRequiredMixin, BaseView, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["rewardPoints"] = Customer.objects.get(user=self.request.user).reward_points
        context["searches"] = SearchHistory.objects.all().filter(user=self.request.user).order_by('-timestamp')
        context["support"] = SupportTicket.objects.all().filter(user=self.request.user).order_by('-date')
        return context

class QueryView(LoginRequiredMixin, BaseView, TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context["snacks"] = Item.objects.all().filter(name__contains=query)
        if self.request.user.is_authenticated:
            SearchHistory.objects.create(user=self.request.user, query=query).save()
        return context

@login_required
def delete_search_history(request):
    search_history = SearchHistory.objects.all().filter(user=request.user)
    search_history.delete()
    return HttpResponseRedirect("/profile")

class CheckoutView(LoginRequiredMixin, BaseView, ListView, FormView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = "/"

    def get_queryset(self) -> QuerySet[Any]:
        return PaymentMethod.objects.all().filter(user=self.request.user)