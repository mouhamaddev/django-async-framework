import django

from django.conf import settings


def configure():
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DEFAULT_CHARSET='utf-8',
            ROOT_URLCONF=__name__,
            SECRET_KEY='dummy',
            ALLOWED_HOSTS=['*'],
            MIDDLEWARE=[],
            INSTALLED_APPS=[],
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:", # For tests
                }
            },
        )
    django.setup()