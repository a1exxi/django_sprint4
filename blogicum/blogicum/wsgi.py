# Модуль для запуска Django-приложения через WSGI-сервер (например, Gunicorn).
# WSGI — протокол, по которому веб-сервер общается с Django-приложением.

import os                              # работа с переменными окружения
from django.core.wsgi import get_wsgi_application  # функция, которая создаёт WSGI-приложение

# Указываем Django, какой файл настроек использовать (blogicum/settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

# Создаём WSGI-приложение — его будет использовать сервер (например, Gunicorn, uWSGI)
application = get_wsgi_application()
