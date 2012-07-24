from tastypie import fields
from tastypie.authorization import Authorization
from mongolier import api
from django.db import settings


class TestResource(api.MongoResource):

    my_field = fields.DictField()

    class Meta:

        connection = settings.MONGO_TEST_CONN
        resource_name = "mongo"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'patch', 'put', 'delete']

    def dehydrate_my_field(self, bundle_or_obj):
        return(bundle_or_obj.obj)
