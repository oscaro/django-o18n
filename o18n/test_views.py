import json

# JsonResponse is available in Django 1.7+
from django.http import HttpResponse


UNSERIALIZABLE_ATTRS = {'environ', 'META', 'resolver_match'}


def info(request):
    skip = lambda attr: attr.startswith('_') or attr in UNSERIALIZABLE_ATTRS
    request = {k: v for k, v in request.__dict__.items() if not skip(k)}
    return HttpResponse(json.dumps(request), content_type='application/json')
