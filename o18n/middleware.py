from django.utils import translation

from . import country as country_mod
from . import util


class CountryLanguageMiddleware(object):
    """
    Variant of django.middleware.locale.LocaleMiddleware.

    Uses the /<country>/<language>/ format for URL prefixes.

    Sets request.COUNTRY and request.LANGUAGE.
    """

    def process_request(self, request):
        country, language, language_code = util.get_country_language(request)

        if country is None:
            country_mod.deactivate()
        else:
            country_mod.activate(country)
        translation.activate(language_code)

        request.COUNTRY = country
        request.LANGUAGE = language
        request.LANGUAGE_CODE = language_code

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        return response
