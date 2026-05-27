from django.contrib import admin
from .models import Category, Post, Location


# Декоратор регистрирует модель Category в админке
# Теперь она появится на главной странице админ-панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Какие поля показывать в таблице со списком всех категорий
    list_display = ('title', 'slug', 'is_published', 'created_at')
    # Поля, которые можно редактировать прямо из списка (не заходя в карточку)
    list_editable = ('is_published',)
    # По каким полям работает строка поиска в админке
    search_fields = ('title', 'slug')


# Регистрируем модель Location (геометка) в админке
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # В списке геометок показываем название, статус публикации и дату создания
    list_display = ('name', 'is_published', 'created_at')
    # Статус публикации можно менять прямо из списка
    list_editable = ('is_published',)
    # Поиск работает по названию геометки
    search_fields = ('name',)


# Регистрируем модель Post (пост) в админке
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Какие поля отображаются в таблице со списком всех постов
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'pub_date',
        'is_published',
    )
    # Поля, которые можно менять прямо из списка (без открытия каждого поста)
    list_editable = ('is_published', 'category', 'location', 'pub_date')
    # Фильтры в правой боковой панели — удобно отсеивать посты по категории, локации и статусу
    list_filter = ('category', 'location', 'is_published')
    # Поиск по заголовку и тексту поста
    search_fields = ('title', 'text')
