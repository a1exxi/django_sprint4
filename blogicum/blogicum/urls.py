# Импорты
from django.contrib import admin
from django.urls import path, include                          #  include — подключить файл urls.py другого приложения
from blog import views as blog_views                           # представления из приложения blog (нужны для алиасов)
from django.conf import settings
from django.conf.urls.static import static                     # раздача медиа-файлов в режиме разработки


urlpatterns = [
    # Админ-панель доступна по адресу /admin/
    path('admin/', admin.site.urls),

    # Алиасы, то есть дополнительные имена для некоторых страниц — нужны для тестов и проверок
    # Чтобы работали name='registration' и name='create_post' без указания namespace
    path('auth/registration/', blog_views.registration, name='registration'),
    path('posts/create/', blog_views.post_create, name='create_post'),

    # Подключаем файлы urls.py из наших приложений:
    path('', include('blog.urls', namespace='blog')),         # все URL блога (главная, посты, профили...)
    path('pages/', include('pages.urls', namespace='pages')), # статические страницы (about, rules...)

    # Встроенные URL для авторизации (login, logout, reset password...)
    path('auth/', include('django.contrib.auth.urls')),
]

# Кастомные страницы для ошибок 404 и 500
handler404 = 'pages.views.page_not_found'      # страница «не найдено»
handler500 = 'pages.views.server_error'        # страница «ошибка сервера»

# В речжиме разработки (DEBUG=True) раздаём медиа-файлы (картинки) через static()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)