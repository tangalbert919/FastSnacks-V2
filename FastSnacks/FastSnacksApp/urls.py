from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('favorites', views.FavoritesView.as_view(), name="favorites"),
    path('list-items', views.ListItemsView.as_view(), name="list-items"),
    path('rewards', views.RewardsView.as_view(), name="rewards"),
    path('payment-methods', views.PaymentView.as_view(), name="payment-methods"),
    path('transaction-history', views.TransactionView.as_view(), name="transaction-history"),
    path('support-submit', views.SupportView.as_view(), name="support-submit"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('search', views.QueryView.as_view(), name="search"),
    path('cart', views.CartView.as_view(), name="cart"),
]
