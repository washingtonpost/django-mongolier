from tastypie import fields
from tastypie.authorization import Authorization
from mongolier import api
from django.db import settings


class MongolierTestResource(api.MongoResource):

    my_field = fields.DictField()

    class Meta:

        connection = settings.MONGO_TEST_CONN
        resource_name = "mongo"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'patch', 'put', 'delete']

    def dehydrate_my_field(self, bundle_or_obj):
        return(bundle_or_obj.obj)


class MongoClientTestResource(api.MongoResource):

    my_field = fields.DictField()

    class Meta:

        connection = settings.TEST_PYMONGO_CLIENT_OBJ
        resource_name = "test_pymongo_client_obj"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'patch', 'put', 'delete']

    def dehydrate_my_field(self, bundle_or_obj):
        return(bundle_or_obj.obj)
