from contextlib import contextmanager
from threading import local

from . import util


_country = local()


def get_country():
    """Return the currently selected country or None."""
    try:
        return _country.value
    except AttributeError:
        return None


def activate(country):
    """Select the country for the current thread."""
    # get_language_maps() returns a cached dict keyed by country code.
    if country not in util.get_language_maps():
        raise ValueError("Unsupported country '{}'.".format(country))
    _country.value = country


def deactivate():
    """Remove the country for the current thread."""
    try:
        del _country.value
    except AttributeError:
        pass


@contextmanager
def override(country):
    """Context manager that selects the country."""
    old_country = getattr(_country, 'value', None)
    activate(country)
    try:
        yield
    finally:
        if old_country is None:
            deactivate()
        else:
            activate(old_country)
