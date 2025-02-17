from config import Config
from pathlib import Path


def get_secret_key() -> str:
    """
    Возвращает секретный ключ из конфигурации.

    Возвращает:
        str: Секретный ключ.
    """
    return Config.SECRET_KEY


def get_base_dir() -> Path:
    """
    Возвращает базовую директорию проекта.

    Возвращает:
        Path: Базовая директория проекта.
    """
    return Path(__file__).resolve().parent.parent


SECRET_KEY: str = get_secret_key()
"""Секретный ключ для шифрования данных."""

DEBUG: bool = False
"""Режим отладки."""

BASE_DIR: Path = get_base_dir()
"""Базовая директория проекта."""

ALLOWED_HOSTS: list[str] = ['127.0.0.1', 'localhost']
"""Список разрешенных хостов."""

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'cafe_orders'
]
"""Список установленных приложений."""

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
"""Список middleware."""

ROOT_URLCONF: str = 'cafe_order_management.urls'
"""Корневой URLconf."""

TEMPLATES: list[dict[str, str]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
"""Список настроек шаблонов."""

WSGI_APPLICATION: str = 'cafe_order_management.wsgi.application'
"""Приложение WSGI."""

DATABASES: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""Настройки базы данных."""

LANGUAGE_CODE: str = 'en-us'
"""Код языка."""

TIME_ZONE: str = 'UTC'
"""Часовой пояс."""

USE_I18N: bool = True
"""Флаг использования интернационализации."""

USE_TZ: bool = True
"""Флаг использования часовых поясов."""

STATIC_URL: str = 'static/'
"""URL статических файлов."""

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
"""Поле по умолчанию для автоматических моделей."""