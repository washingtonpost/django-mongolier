from django.conf.urls import *
from tastypie.api import Api
from api import MongolierTestResource, MongoClientTestResource

api = Api('test')

api.register(MongolierTestResource())
api.register(MongoClientTestResource())


urlpatterns = patterns('',
    (r'^api/', include(api.urls)),
)