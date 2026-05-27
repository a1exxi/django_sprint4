# Модуль models содержит классы — описания таблиц в базе данных.
# Каждый класс = одна таблица, каждое поле = один столбец в таблице.
from django.db import models
from django.conf import settings


# Модель «Категория» — группирует посты по темам (например, «Путешествия», «Еда»)
class Category(models.Model):
    # CharField — строка ограниченной длины (max_length=256 символов максимум)
    title = models.CharField(
        'Заголовок',
        max_length=256,
        # blank=False — поле обязательно для заполнения (нельзя оставить пустым)
        blank=False,
    )
    # TextField — текст без ограничения длины
    description = models.TextField(
        'Описание',
        blank=False,
    )
    # SlugField — короткий уникальный идентификатор для URL (например, /category/travel/)
    slug = models.SlugField(
        'Идентификатор',
        # unique=True — значение должно быть уникальным (не может повторяться у других категорий)
        unique=True,
        blank=False,
        # help_text — подсказка, которая отображается в админке под полем
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )
    # BooleanField — галочка (True = опубликовано, False = скрыто)
    is_published = models.BooleanField(
        'Опубликовано',
        # default=True — новым категориям по умолчанию ставится галочка «опубликовано»
        default=True,
        blank=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    # DateTimeField — дата и время
    created_at = models.DateTimeField(
        'Добавлено',
        # auto_now_add=True — дата автоматически ставится один раз при создании записи
        auto_now_add=True,
        blank=False,
    )

    # Meta — внутренний класс с дополнительными настройками модели
    class Meta:
        verbose_name = 'категория'                          # имя в единственном числе (в админке)
        verbose_name_plural = 'Категории'                   # имя во множественном числе (в админке)

    # __str__ — что показывать при печати объекта (в админке, в консоли и т.д.)
    def __str__(self):
        return self.title                                   # показываем заголовок категории


# Модель «Местоположение» (геометка) — привязывает пост к месту
class Location(models.Model):
    name = models.CharField(
        'Название места',
        max_length=256,
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


# Модель «Пост» — основная сущность блога (статья/запись)
class Post(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=256,
    )
    text = models.TextField(
        'Текст',
    )
    # ImageField — загрузка изображения; upload_to='posts/' — картинки сохранятся в папку media/posts/
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        blank=True,     # blank=True — поле может быть пустым в форме
        null=True,      # null=True — в базе данных может хранить NULL (отсутствие значения)
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    # ForeignKey — связь «много к одному» (много постов могут принадлежать одному автору)
    # settings.AUTH_USER_MODEL — ссылка на модель пользователя (по умолчанию User)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,   # CASCADE — если пользователя удалят, удалятся и его посты
    )
    # Ещё одна внешняя связь — пост может относиться к одному местоположению
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        null=True,      # пост может быть без привязки к месту
        blank=True,
        on_delete=models.SET_NULL,  # SET_NULL — если место удалят, у поста останется пустое значение
    )
    # Категория поста — пост может быть только в одной категории
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)   # сортировка по умолчанию: от новых к старым (минус = обратный порядок)

    def __str__(self):
        return self.title


# Модель «Комментарий» — пользователи могут оставлять комментарии под постами
class Comment(models.Model):
    # Ссылка на пост, под которым написан комментарий
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,       # если пост удалят, удалятся и все его комментарии
        related_name='comments',        # related_name — как обращаться к комментариям из поста: post.comments.all()
        verbose_name='Публикация',
    )
    # Кто написал комментарий
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',        # user.comments.all() — все комментарии пользователя
        verbose_name='Автор комментария',
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        ordering = ('created_at',)      # сортировка: от старых к новым
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]           # показываем первые 30 символов текста
