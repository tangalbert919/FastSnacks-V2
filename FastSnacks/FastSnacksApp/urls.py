from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('favorites', views.FavoritesView.as_view(), name="favorites"),
]
