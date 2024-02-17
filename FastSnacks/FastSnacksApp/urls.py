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
    path('payment-methods-add', views.add_payment_method, name="payment-methods-add"),
    path('transaction-history', views.TransactionView.as_view(), name="transaction-history"),
    path('support', views.SupportView.as_view(), name="support"),
    path('support-submit', views.submit_support_ticket, name="support-submit"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('search', views.QueryView.as_view(), name="search"),
    path('cart', views.CartView.as_view(), name="cart"),
    path('add-to-cart', views.add_to_cart, name="add-to-cart"),
    path('favorites-add', views.add_favorites, name="favorites-add"),
    path('favorites-remove', views.remove_favorites, name="favorites-remove"),
    path('user-delete', views.delete_user, name="user-delete"),
]
