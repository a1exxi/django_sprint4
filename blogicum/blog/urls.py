# urls.py — файл, в котором мы описываем, по каким адресам (URL) какие страницы показывать
from django.urls import path
from . import views                     # импортируем функции-представления из views.py




app_name = 'blog'

urlpatterns = [
    # path(путь, какая_функция_из_views, name=имя_для_ссылок)
    # '' — пустая строка, значит главная страница блога
    path('', views.index, name='index'),
    # Страница регистрации нового пользователя
    path('auth/registration/', views.registration, name='registration'),
    # Редактирование профиля текущего пользователя
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # <str:username> — динамическая часть URL; вместо <str:username> подставляется имя пользователя
    # Например: /profile/ivanov/
    path('profile/<str:username>/', views.profile, name='profile'),
    # Страница со списком постов определённой категории
    # <slug:category_slug> — захват часть URL как переменную "category_slug, которая должна соответствовать slug
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    # Создание нового поста
    path('posts/create/', views.post_create, name='post_create'),
    # Добавление комментария к посту
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    # Редактирование комментария
    # <int:post_id> — число (id поста), <int:comment_id> — число (id комментария)
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # Удаление комментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    # Удаление поста
    path('posts/<int:post_id>/delete/', views.post_delete, name='delete_post'),
    # Редактирование поста
    path('posts/<int:post_id>/edit/', views.post_edit, name='edit_post'),
    # Детальная страница одного поста
    path('posts/<int:post_id>/',
         views.post_detail,
         name='post_detail'),
]
