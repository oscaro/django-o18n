o18n
====

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

o18n is designed for Django ≥ 1.6 and Python ≥ 3.2. (Python 2.7 may work too.)

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
because outputting text in the wrong language is usually better than crashing

Limitations
-----------

Like `i18n_patterns`, `o18n_patterns` may only be used in the root URLconf.

The currenty implementation assumes but does not check that `APPEND_SLASH` and
`USE_I18N` are `True`.

There are no `{% get_current_coutry %}` and `{% get_country_info %}` template
tags at this time, but they could be implemented if there's a use case.

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

o18n is released under the BSD license, like Django itself.
