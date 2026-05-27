from django.apps import AppConfig


# Класс-конфигурация приложения
class BlogConfig(AppConfig):
    # Тип поля для автоматических primary key (BigAutoField = большое число)
    default_auto_field = 'django.db.models.BigAutoField'
    # Внутреннее имя приложения — должно совпадать с именем папки приложения
    name = 'blog'
    # перевод имя, которое отображается в админке и других местах
    verbose_name = 'Блог'
