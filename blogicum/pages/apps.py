# apps.py — конфигурация приложения pages
from django.apps import AppConfig


# Класс-конфигурация для приложения pages (статические страницы)
class PagesConfig(AppConfig):
    # Тип поля для автоматических primary key (id) по умолчанию
    default_auto_field = 'django.db.models.BigAutoField'
    # Внутреннее имя приложения — совпадает с именем папки приложения
    name = 'pages'
