from django.test import TestCase

from . import country


class TestCountry(TestCase):

    def test_activate_deactivate_country(self):
        self.assertIsNone(country.get_country())
        country.activate('us')
        self.assertEqual(country.get_country(), 'us')
        country.activate('ca')
        self.assertEqual(country.get_country(), 'ca')
        country.deactivate()
        self.assertIsNone(country.get_country())

    def test_activate_checks_country(self):
        with self.assertRaises(ValueError):
            country.activate(None)
        with self.assertRaises(ValueError):
            country.activate('br')
        self.assertIsNone(country.get_country())

    def test_override_country(self):
        self.assertIsNone(country.get_country())
        with country.override('us'):
            self.assertEqual(country.get_country(), 'us')
            with country.override('ca'):
                self.assertEqual(country.get_country(), 'ca')
            self.assertEqual(country.get_country(), 'us')
        self.assertIsNone(country.get_country())
