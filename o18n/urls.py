import re

from django.core.urlresolvers import RegexURLResolver
from django.conf.urls import patterns

from . import monkey
from .util import get_country_language_prefix


def o18n_patterns(prefix, *args):
    """
    Variant of django.conf.urls.i18n.i18_patterns.
    """
    return [CountryLanguageURLResolver(patterns(prefix, *args))]


class CountryLanguageURLResolver(RegexURLResolver):
    """
    Variant of django.core.urlresolvers.LocaleRegexURLResolver.
    """
    def __init__(self, urlconf_name, default_kwargs=None,
                 app_name=None, namespace=None):
        monkey.patch()          # Latest possible point for monkey patching.
        super(CountryLanguageURLResolver, self).__init__(
            None, urlconf_name, default_kwargs, app_name, namespace)

    @property
    def regex(self):
        prefix = get_country_language_prefix()
        if prefix not in self._regex_dict:
            if prefix is None:  # Regex that cannot be matched (hack).
                compiled_regex = re.compile('$/^'.format(prefix), re.UNICODE)
            else:
                compiled_regex = re.compile('^{}/'.format(prefix), re.UNICODE)
            self._regex_dict[prefix] = compiled_regex
        return self._regex_dict[prefix]
