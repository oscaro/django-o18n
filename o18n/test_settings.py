# coding: utf-8

COUNTRIES = [
    ('us', 'en', ['es']),
    ('ca', None, ['en', 'fr']),
    ('mx', 'es', []),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', "English"),
    ('es', "Español"),
    ('fr', "Français"),
    ('es-mx', "Español de Mexico")
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'o18n.middleware.CountryLanguageMiddleware',
]

ROOT_URLCONF = 'o18n.test_urls'

SECRET_KEY = 'whatever'
