from django.conf.urls.defaults import *
from tastypie.api import Api
from api import TestResource

api = Api('test')

api.register(TestResource())

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),
)