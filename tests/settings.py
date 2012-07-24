"""
settings.py

A generic settings for testing.
"""
from mongolier import Connection, MongoConnection

# MONGO_TEST_CONN = Connection(db='test', collection='test')

MONGO_TEST_DB = MongoConnection(db='test', collection='test')
MONGO_TEST_CONN = MONGO_TEST_DB.connect()

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'mongolier.db'
TEST_DATABASE_NAME = 'mongolier-test.db'

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
