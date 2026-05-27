# urls.py — какие URL обрабатывает приложение pages
from django.urls import path
from . import views                     # импортируем представления из views.py

# Пространство имён — чтобы обращаться к этим URL через {% url 'pages:about' %}
app_name = 'pages'

urlpatterns = [
    # Страница «О проекте» — доступна по адресу /pages/about/
    path('about/', views.AboutView.as_view(), name='about'),
    # Страница «Правила» — доступна по адресу /pages/rules/
    path('rules/', views.RulesView.as_view(), name='rules'),
]
