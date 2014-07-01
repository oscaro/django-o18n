django-o18n
===========

Use case
--------

Django's [i18n_patterns][] prefixes URLs with a language code which may
contain a variant e.g. `/en`, `/fr`, `/fr-ca`.

o18n_patterns is similar but it prefixes URLs with a country code and a
language code e.g. `/us`, `/ca/en`, `/ca/fr`.

This is useful for websites that are mainly segmented by country rather than
by language.

[i18n_patterns]: https://docs.djangoproject.com/en/stable/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns

Features
--------

Some countries have a main language. In that case, the URL for the main
language only contains the country e.g. `/us`. URLs for other languages
contain the country and the language e.g. `/us/es`.

Some countries don't have a main language — and it may be a sensitive topic!
In that case, all URLs contain the country and the language e.g. `/ca/en` and
`/ca/fr`.

Unlike i18_patterns, o18n_patterns doesn't attempt to determine the country
and language and automatically redirect the user to the appropriate URL.

If an URL doesn't match a valid country and language combination, it doesn't
resolve with o18n_patterns and no country is activated. Vice-versa, if no
country is active, reversing an URL raises an exception.

Setup
-----

django-o18n is designed for Django ≥ 1.6 and Python ≥ 3.2 or 2.7.

It relies on a list of supported countries and languages declared in the
`COUNTRIES` setting. For example:

    COUNTRIES = [
        ('us', 'en', ['es']),
        ('ca', None, ['en', 'fr']),
        ('mx', 'es', []),
    ]

Each entry is a 3-uple containing:

* A two-letter country code,
* The two-letter language code of the main language, if there is one,
* A list of two-letter language codes of other languages, possibly empty.

With the example above, o18n_patterns matches the following URL prefixes:

* `us/`: country = USA, language = English
* `us/es/`: country = USA, language = Spanish
* `ca/en/`: country = Canada, language = English
* `ca/fr/`: country = Canada, language = French
* `mx/`: country = Mexico, language = Spanish

(If `COUNTRIES` clashes with another setting, set `O18N_COUNTRIES` instead.)

Add `'o18n.middleware.CountryLanguageMiddleware'` to `MIDDLEWARE_CLASSES`
instead of `'django.middleware.locale.LocaleMiddleware'`.

Ensure that all languages also exist in `LANGUAGES` and `USE_I18N` is `True`.

Finally use `o18n.urls.o18n_patterns` in your URLconf instead of
`django.conf.urls.i18n.i18_patterns`.

APIs
----

If an o18n pattern matches:

- `request.COUNTRY` and `request.LANGUAGE` contain the two-letter country and
  language codes.
- `request.LANGUAGE_CODE` contains the language code, including a variant if
  there is one.

Otherwise:

- `request.COUNTRY` and `request.LANGUAGE` are `None`.
- `request.LANGUAGE_CODE` defaults to `settings.LANGUAGE_CODE`.

`request.LANGUAGE_CODE` provides compatibility with software designed to
integrate with `django.middleware.locale.LocaleMiddleware`.

If you need to manipulate the current country, the `o18n.country` module
provides `get_country()`, `activate(country)` and `deactivate()` functions as
well as an `override(country)` context manager.

They behave like their equivalents for manipulating the current language in
`django.utils.translation`, with one difference: if there's no active country,
`get_country()` returns `None`. If a project is bothering with per-country
logic, that may be related to local regulations, making it a bad choice to
fall back silently to a default country. This argument is weaker for languages
because outputting text in the wrong language is usually better than crashing.

Limitations
-----------

Like `i18n_patterns`, `o18n_patterns` may only be used in the root URLconf.

The currenty implementation assumes but does not check that `APPEND_SLASH` and
`USE_I18N` are `True`.

There are no `{% get_current_coutry %}` and `{% get_country_info %}` template
tags at this time, but they could be implemented if there's a use case.

FAQ
---

### Why does the root URL return a 404 Not Found error?

Since django-o18n doesn't attempt to guess the user's country, it cannot
handle the root URL (`/`). It's up to you to implement the logic you need
in a Django view and add it to your root URLconf outside of o18n_patterns:

    from django.conf.urls import patterns, url
    from o18n.urls import o18n_patterns
    from myproject.views import root

    urlpatterns = patterns('',
        url(r'^$', root, name='root'),
    ) + o18n_patterns('',
        # ...
    )

For instance, you can guess the user's country with [GeoIP][] and offer a link
to the corresponding site or the option to choose another one. Note that it's
hard to determine reliably a user's country over the Internet. If you want to
redirect the user automatically, you should provide the option to select
another country in case you guessed wrong.

[GeoIP]: https://docs.djangoproject.com/en/stable/ref/contrib/gis/geoip/

### Why do my tests fail with a `NoReverseMatch` exception?

Since django-o18n doesn't have a default country, it cannot reverse o18n
patterns when no country is active. This doesn't play nice with the pattern of
reversing an URL and then making a request to this URL with the test client.
In contrast, it isn't an issue in regular code because a country is usually
activated by `CountryLanguageMiddleware` before the request reaches the view.

If you want to activate a default country and language in your tests, you can
implement a mixin and add it to your test cases:


    from django.utils import translation
    from o18n import country

    class O18nMixin(object):
        country_code = 'us'
        language_code = 'en'

        def setUp(self):
            country.activate(self.country_code)
            translation.activate(self.language_code)
            super(O18nMixin, self).setUp()

        def tearDown(self):
            super(O18nMixin, self).tearDown()
            translation.deactivate()
            country.deactivate()

Hacking
-------

Install Django in a virtualenv.

Run the tests with:

    make test

Run the tests under coverage with:

    make coverage

If you want to suggest changes, please submit a pull request!

License
-------

django-o18n is released under the BSD license, like Django itself.
