from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!#f(mbh2_5x@@a3-eis(k2qp5xy6z*!&^jfu%*w^34eo0jub=k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-histor


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_cleanup.apps.CleanupConfig",

    'user',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def get_full_name(request):
    if request.user.is_authenticated:
        return request.user.get_full_name()
    return "Guest"


UNFOLD = {
    "SITE_TITLE": "Universal Bot",
    "SITE_HEADER": lambda request: get_full_name(request),
    "SITE_SUBHEADER": "Administrator",
    "SITE_URL": "/",

    "SITE_SYMBOL": "admin_panel_settings",

    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": True,  # show/hide "Back" button on changeform in header, default: False

    # "THEME": "dark", # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        "redirect_after": lambda request: reverse_lazy("admin:login"),
    },
    "BORDER_RADIUS": "10px",

    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Users"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Foydalanuvchilar"),
                        "icon": "person",
                        "link": reverse_lazy("admin:user_user_changelist"),
                    },
                    {
                        "title": _("Xodimlar"),
                        "icon": "assignment_ind",
                        "link": reverse_lazy("admin:user_employee_changelist"),
                    },
                    {
                        "title": _("Mijozlar"),
                        "icon": "patient_list",
                        "link": reverse_lazy("admin:user_client_changelist"),
                    },
                    {
                        "title": _("Rollar"),
                        "icon": "add_moderator",
                        "link": reverse_lazy("admin:user_role_changelist"),
                    },
                ],
            },
            {
                "title": _("Buildings"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Loyihalar"),
                        "icon": "apartment",
                        "link": reverse_lazy("admin:main_building_changelist"),
                    },
                    {
                        "title": _("Xonadonlar"),
                        "icon": "living",
                        "link": reverse_lazy("admin:main_flat_changelist"),
                    },
                    {
                        "title": _("Materiallar"),
                        "icon": "texture",
                        "link": reverse_lazy("admin:main_material_changelist"),
                    },
                ],
            },
        ],

    }
}
