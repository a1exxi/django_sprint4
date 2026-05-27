# pathlib — модуль для удобной работы с путями файлов/папок
from pathlib import Path


# BASE_DIR — корневая папка проекта (blogicum/).
# __file__ — путь к этому файлу (settings.py)
# .resolve() — превращает в абсолютный путь
# .parent.parent — поднимаемся на две папки вверх: из blogicum/settings.py → blogicum/ → корень
BASE_DIR = Path(__file__).resolve().parent.parent

# Папка, в которой лежат HTML-шаблоны (templates/)
TEMPLATES_DIR = BASE_DIR / 'templates'


# SECRET KEY — секретный ключ проекта. Используется для шифрования сессий, токенов и т.д.
# В реальном проекте его НЕ хранят в коде, а берут из переменных окружения.
SECRET_KEY = 'django-insecure-_1ot$=9^7u_n-pl7cm2h3&+r#-&htjcqo!q6ll=' \
    'snfa4k5m+%5'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True — показывать подробные ошибки (ТОЛЬКО для разработки!)
DEBUG = True

# ALLOWED_HOSTS — список доменов, на которых разрешён запуск сайта
# В продакшне сюда пишут домен (например, ['moyblog.ru'])
ALLOWED_HOSTS = []

# INSTALLED_APPS — список всех приложений, подключённых к проекту
INSTALLED_APPS = [
    # Наши собственные приложения
    'pages.apps.PagesConfig',           # приложение для статических страниц (главная, about и т.д.)
    'blog.apps.BlogConfig',             # приложение блога (посты, комментарии, категории)
    # Сторонние пакеты
    'django_bootstrap5',                # библиотека для Bootstrap 5 (стили)
    # Встроенные приложения Django
    'django.contrib.admin',             # админ-панель
    'django.contrib.auth',              # система авторизации (пользователи, группы)
    'django.contrib.contenttypes',      # фреймворк для работы с разными типами моделей
    'django.contrib.sessions',          # работа с сессиями пользователей
    'django.contrib.messages',          # система всплывающих сообщений
    'django.contrib.staticfiles'        # раздача статических файлов (CSS, JS, картинки)
]

# MIDDLEWARE — цепочка обработчиков, через которые проходит каждый запрос
# Каждый middleware делает что-то своё: проверяет безопасность, управляет сессией и т.д.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',              # безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',       # сессии (чтобы помнить пользователя)
    'django.middleware.common.CommonMiddleware',                  # общие вещи (например, чтение заголовков)
    'django.middleware.csrf.CsrfViewMiddleware',                  # защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # привязывает пользователя к запросу
    'django.contrib.messages.middleware.MessageMiddleware',       # поддержка flash-сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',     # защита от clickjacking
]

# ROOT_URLCONF — какой файл urls.py Django должен использовать как корневой
ROOT_URLCONF = 'blogicum.urls'

# TEMPLATES — настройки шаблонизатора (переменные в HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # движок шаблонов (штатный)
        'DIRS': [TEMPLATES_DIR],        # где лежат шаблоны (папка templates/)
        'APP_DIRS': True,               # искать шаблоны ещё и внутри каждого приложения (blog/templates/)
        'OPTIONS': {
            'context_processors': [     # функции, которые добавляют переменные ВО ВСЕ шаблоны
                'django.template.context_processors.request',      # добавляет переменную {{ request }}
                'django.contrib.auth.context_processors.auth',     # добавляет {{ user }}
                'django.contrib.messages.context_processors.messages',  # добавляет {{ messages }}
            ],
        },
    },
]

# WSGI_APPLICATION — какой объект использовать для запуска сайта на сервере
WSGI_APPLICATION = 'blogicum.wsgi.application'


# Database — настройки подключения к базе данных
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # тип БД: SQLite (файловая, для разработки)
        'NAME': BASE_DIR / 'db.sqlite3',          # путь к файлу базы данных
    }
}


# Password validation — правила для паролей пользователей
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # пароль не должен быть слишком похож на имя/фамилию пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
        # минимальная длина пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
        # пароль не должен быть слишком простым (123456, qwerty и т.д.)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
        # пароль не должен состоять только из цифр
    },
]


# Internationalization — язык, время, формат дат
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'              # язык сайта (русский)

TIME_ZONE = 'Asia/Yekaterinburg'     # часовой пояс (Екатеринбург)

USE_I18N = True                      # включить переводы

USE_TZ = True                        # хранить время в UTC, а показывать в локальном часовом поясе


# Static files (CSS, JavaScript, Images) — настройки для статических файлов
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# STATIC_URL — префикс URL для статических файлов (http://site.ru/static/...)
STATIC_URL = 'static/'

# Default primary key field type — тип поля для первичного ключа (id) по умолчанию
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# BigAutoField — большое целое число (до 9223372036854775807)

# STATICFILES_DIRS — дополнительные папки со статикой (помимо static/ внутри приложений)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# CSRF_FAILURE_VIEW — своя страница для ошибки CSRF (вместо стандартной)
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

# MEDIA_URL / MEDIA_ROOT — для загруженных пользователями файлов (картинки постов)
MEDIA_URL = '/media/'                       # URL-префикс для медиа-файлов
MEDIA_ROOT = BASE_DIR / 'media'             # папка, куда сохраняются файлы

# EMAIL — настройки отправки писем (для тестирования: сохраняем в файлы, а не отправляем по-настоящему)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'  # сохранять письма в файлы
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'                           # папка для писем

# Auth redirects — куда перенаправлять неавторизованного пользователя
LOGIN_URL = 'login'
