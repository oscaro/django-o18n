from setuptools import setup
import os

# Avoid polluting the .tar.gz with ._* files under Mac OS X
os.putenv('COPYFILE_DISABLE', 'true')

# Prevent distutils from complaining that a standard file wasn't found
README = os.path.join(os.path.dirname(__file__), 'README')
if not os.path.exists(README):
    os.symlink(README + '.md', README)

description = "/<country>/<language>/ URL scheme, like Django's i18n_patterns."

with open(README) as f:
    long_description = '\n\n'.join(f.read().split('\n\n')[1:11])

setup(
    name='django-o18n',
    version='1.0',

    description=description,
    long_description=long_description,

    url='https://github.com/oscaro/o18n',

    author='Aymeric Augustin',
    author_email='aymeric.augustin@oscaro.com',

    license='BSD',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=['o18n'],
)
