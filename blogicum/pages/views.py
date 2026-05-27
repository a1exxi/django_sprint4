# views.py — функции и классы-представления для приложения pages

from django.shortcuts import render                              # render — рендерит HTML-шаблон
from django.views.generic import TemplateView                    # TemplateView — готовый класс для статических страниц


# Классовые представления (Class-Based Views) для статических страниц.
# TemplateView просто показывает указанный HTML-шаблон — никакой логики не нужно.
class AboutView(TemplateView):
    # Какой шаблон показывать на странице /pages/about/
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    # Какой шаблон показывать на странице /pages/rules/
    template_name = 'pages/rules.html'


# Функции-обработчики для страниц ошибок.
# Они не привязаны к конкретному URL — Django вызывает их автоматически при ошибках.

def page_not_found(request, exception):
    """Страница 404 — «не найдено»."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Страница 500 — «ошибка сервера»."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Страница 403 — ошибка CSRF (подделка межсайтового запроса)."""
    return render(request, 'pages/403csrf.html', status=403)
