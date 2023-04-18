from django.http import HttpResponse
from django.shortcuts import render


# Главная страница
def index(request):    
    return HttpResponse('Главная страница')