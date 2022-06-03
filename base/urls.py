from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("logout", views.logout),
    path("dashboard", views.dashboard),
    path("signup", views.signup),
    path("categories", views.categories),
    path("cart", views.cart),
    path("verify/<str:token>", views.verify),
]
