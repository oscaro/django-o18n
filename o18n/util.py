import re
import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import receiver
from django.test.signals import setting_changed
from django.utils.translation import get_language
from django.utils.translation.trans_real import get_supported_language_variant


country_language_prefix_re = re.compile(r'^/([a-z]{2})/(?:([a-z]{2})/)?')

_language_maps = None


def get_countries_setting():
    """
    Return the O18N_COUNTRIES or COUNTRIES setting.

    The latter is more readable and more consistent with LANGUAGES.
    The former is less likely to clash with another application.
    """
    try:
        return settings.O18N_COUNTRIES
    except AttributeError:
        return settings.COUNTRIES


def _variant(country, language):
    language_code = '{}-{}'.format(language, country)
    try:
        return get_supported_language_variant(language_code)
    except LookupError:
        raise ImproperlyConfigured(
            "No matching locale found for '{}'. ".format(language_code) +
            "Check your COUNTRIES and LANGUAGES settings.")


def get_language_maps():
    """
    Create a mapping of country -> URL language -> (language, language code).

    This allows checking for countries and languages efficiently.
    """
    global _language_maps
    if _language_maps is None:
        outer = {}
        for country, main_language, other_languages in get_countries_setting():
            inner = {}
            if main_language is not None:
                inner[None] = main_language, _variant(country, main_language)
            for language in other_languages:
                if language == main_language:
                    warnings.warn(
                        "Main language '{}' needs not be in other languages "
                        "for country '{}'.".format(main_language, country))
                inner[language] = language, _variant(country, language)
            outer[country] = inner
        _language_maps = outer
    return _language_maps


@receiver(setting_changed)
def reset_caches(**kwargs):
    global _language_maps
    if kwargs['setting'] in {'COUNTRIES', 'O18N_COUNTRIES', 'LANGUAGES'}:
        _language_maps = None


def get_country_language(request):
    """
    Return the country and language information when found in the path.
    """
    regex_match = country_language_prefix_re.match(request.path_info)
    if not regex_match:
        return None, None, settings.LANGUAGE_CODE

    country, language = regex_match.groups()

    try:
        language, language_code = get_language_maps()[country][language]
    except KeyError:
        return None, None, settings.LANGUAGE_CODE

    return country, language, language_code


def get_country_language_prefix():
    """
    Return the URL prefix according to the current country and language.
    """
    from .country import get_country        # avoid import loop

    country = get_country()
    if country is None:
        return None

    language = get_language().split('-')[0]
    language_map = get_language_maps()[country]
    if language in language_map:
        # non-main language
        return '/'.join((country, language))
    elif None in language_map and language_map[None][0] == language:
        # main language
        return country
    else:
        # invalid language
        return None
