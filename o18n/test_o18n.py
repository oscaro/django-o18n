import json
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import translation

from . import country


class FakeRequest(object):

    def __init__(self, attrs):
        self.__dict__.update(attrs)


class TestRequests(TestCase):

    def tearDown(self):
        country.deactivate()
        translation.deactivate()

    def get_data_for_url(self, url):
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        return FakeRequest(json.loads(response.content.decode()))

    def test_slash(self):
        self.assertEqual(404, self.client.get('/').status_code)

    def test_us(self):
        request = self.get_data_for_url('/us/')
        self.assertEqual(request.COUNTRY, 'us')
        self.assertEqual(request.LANGUAGE, 'en')
        self.assertEqual(request.LANGUAGE_CODE, 'en')

    def test_us_en(self):
        self.assertEqual(404, self.client.get('/us/en/').status_code)

    def test_us_es(self):
        request = self.get_data_for_url('/us/es/')
        self.assertEqual(request.COUNTRY, 'us')
        self.assertEqual(request.LANGUAGE, 'es')
        self.assertEqual(request.LANGUAGE_CODE, 'es')

    def test_us_fr(self):
        self.assertEqual(404, self.client.get('/us/fr/').status_code)

    def test_ca(self):
        self.assertEqual(404, self.client.get('/ca/').status_code)

    def test_ca_en(self):
        request = self.get_data_for_url('/ca/en/')
        self.assertEqual(request.COUNTRY, 'ca')
        self.assertEqual(request.LANGUAGE, 'en')
        self.assertEqual(request.LANGUAGE_CODE, 'en')

    def test_ca_es(self):
        self.assertEqual(404, self.client.get('/ca/es/').status_code)

    def test_ca_fr(self):
        request = self.get_data_for_url('/ca/fr/')
        self.assertEqual(request.COUNTRY, 'ca')
        self.assertEqual(request.LANGUAGE, 'fr')
        self.assertEqual(request.LANGUAGE_CODE, 'fr')

    def test_mx(self):
        request = self.get_data_for_url('/mx/')
        self.assertEqual(request.COUNTRY, 'mx')
        self.assertEqual(request.LANGUAGE, 'es')
        self.assertEqual(request.LANGUAGE_CODE, 'es-mx')

    def test_mx_es(self):
        self.assertEqual(404, self.client.get('/mx/es/').status_code)

    def test_subpath(self):
        self.assertEqual(404, self.client.get('/subpath/').status_code)

    def test_us_subpath(self):
        request = self.get_data_for_url('/us/subpath/')
        self.assertEqual(request.COUNTRY, 'us')
        self.assertEqual(request.LANGUAGE, 'en')
        self.assertEqual(request.LANGUAGE_CODE, 'en')

    def test_us_en_subpath(self):
        self.assertEqual(404, self.client.get('/us/en/subpath/').status_code)

    @override_settings(COUNTRIES=[('us', 'en', [])])
    def test_unsupported_country(self):
        self.assertEqual(404, self.client.get('/mx/').status_code)

    @override_settings(LANGUAGES=[('en', "English")])
    def test_unsupported_language(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.get('/mx/')

    @override_settings(COUNTRIES=[('us', 'en', ['en'])])
    def test_redundant_language(self):
        with warnings.catch_warnings(record=True) as warning:
            self.client.get('/us/')
        warning = warning[0]
        self.assertEqual(
            warning.message.args[0],
            "Main language 'en' needs not be in other languages "
            "for country 'us'.")

    def test_non_o18n_urls(self):
        request = self.get_data_for_url('/xx/')
        self.assertEqual(request.COUNTRY, None)
        self.assertEqual(request.LANGUAGE, None)
        self.assertEqual(request.LANGUAGE_CODE, 'en')
        self.assertEqual(request.path_info, '/xx/')

        request = self.get_data_for_url('/yy/zz/')
        self.assertEqual(request.COUNTRY, None)
        self.assertEqual(request.LANGUAGE, None)
        self.assertEqual(request.LANGUAGE_CODE, 'en')
        self.assertEqual(request.path_info, '/yy/zz/')


class TestReverse(TestCase):

    def test_none(self):
        # Reversing raises an exception when no country is active.
        with self.assertRaises(NoReverseMatch):
            reverse('default')

    def test_us(self):
        with country.override('us'):
            self.assertEqual(reverse('default'), '/us/')

    def test_us_es(self):
        with country.override('us'):
            with translation.override('es'):
                self.assertEqual(reverse('default'), '/us/es/')

    def test_ca(self):
        with country.override('ca'):
            self.assertEqual(reverse('default'), '/ca/en/')

    def test_ca_fr(self):
        with country.override('ca'):
            with translation.override('fr'):
                self.assertEqual(reverse('default'), '/ca/fr/')

    def test_mx_es_mx(self):
        with country.override('mx'):
            with translation.override('es-mx'):
                self.assertEqual(reverse('default'), '/mx/')

    def test_subpath(self):
        with country.override('us'):
            self.assertEqual(reverse('subpath'), '/us/subpath/')

    def test_unsupported_language_in_country_with_a_main_language(self):
        with country.override('us'):
            with translation.override('fr'):
                with self.assertRaises(NoReverseMatch):
                    reverse('default')

    def test_unsupported_language_in_country_without_a_main_language(self):
        with country.override('ca'):
            with translation.override('es'):
                with self.assertRaises(NoReverseMatch):
                    reverse('default')
