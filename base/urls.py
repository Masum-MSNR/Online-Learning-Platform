from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("logout", views.logout),
    path("dashboard", views.dashboard),
    path("signup", views.signup),
    path("categories", views.categories),
    path("cart", views.cart),
    path("verify/<str:token>", views.verify),
    path("view_course/<str:id>", views.view_course),
    path("add_course", views.add_course),
    path("edit_course/<str:id>", views.edit_course),
    path("open_course/<str:id>", views.open_course),
    path("category/<str:category>", views.category),
    path("search/<str:text>", views.search),
]
