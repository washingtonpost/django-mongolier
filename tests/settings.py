"""
settings.py

A generic settings for testing.
"""
from mongolier import Connection

MONGO_TEST_CONN = Connection(db='test', collection='mongolier_test')

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'mongolier.sqlite'
TEST_DATABASE_NAME = 'mongolier-test.sqlite'

# for forwards compatibility
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'TEST_NAME': TEST_DATABASE_NAME,
    }
}

ROOT_URLCONF = 'tests.testapp.urls'

SECRET_KEY = 'TEST'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'tests.testapp',
)
