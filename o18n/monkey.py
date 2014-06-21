# coding: utf-8

from django.core import urlresolvers

from .util import get_country_language_prefix

# In `django.core.urlresolvers`, `reverse` loads the root resolver with
# `get_resolver` or `get_ns_resolver`. Both return a `RegexURLResolver`.

# Then `reverse` calls that resolver's `_reverse_with_prefix` method, which
# triggers `_populate`. This loads all URL patterns through a depth-first
# search. The recursion goes through `pattern.reverse_dict`, which triggers
# `_populate` on each included `RegexURLResolver`.

# Once this process completes, all URL patterns are stored in the root
# resolver's `reverse_dict` attribute. `reverse` simply looks up the view in
# that dict, gets the corresponding URL pattern and substitutes parameters.

# In fact, `reverse_dict` isn't a single dict. It's a property that returns a
# per-language dict. The current language is obtained through `get_language`.

# Unfortunately, this isn't sufficient for reversing in our case. With our
# localization scheme, the URL for a given view depends not only on the
# current language, but also on the current view.

# All this is a direct consequence of using `reverse`. There's no provision
# for customizing this behavior. We resort to monkey-patching `get_language`
# so that `reverse_dict` returns a per-country-and-language dict.


def patch():
    """🙈 🙉 🙊"""
    urlresolvers.get_language = get_country_language_prefix
