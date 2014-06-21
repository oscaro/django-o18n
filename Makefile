export PYTHONPATH:=.:$(PYTHONPATH)
export DJANGO_SETTINGS_MODULE:=o18n.test_settings

test:
	django-admin.py test o18n

coverage:
	coverage erase
	coverage run --branch --source=o18n `which django-admin.py` test o18n
	coverage html

clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist htmlcov MANIFEST
