from django.urls import path

# from django.conf import settings
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
]
