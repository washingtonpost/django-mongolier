"""
api.py

A lightweight implementation of pymongo and django-tastypie

"""
import json

from django.db.models.sql.constants import LOOKUP_SEP
from django.core.urlresolvers import NoReverseMatch
from tastypie.resources import Resource, DeclarativeMetaclass
from tastypie.bundle import Bundle
from bson.objectid import ObjectId


class MongoStorageObject(dict):
    """
    An object that stores information for data before it is transferred
    to Mongo.  It's a placeholder so that information can be properly passed
    through tastypie's methods.

    """
    pk = None

    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value


class MongoDeclarativeMetaclass(DeclarativeMetaclass):
    """
    A Metaclass to set the ``object_class`` for
    :class:`MongoResource <MongoResource>` so that tastypie works smoothly.
    """

    def __new__(cls, name, bases, attrs):
        """
        Create new class object
        """
        # get meta attrs, set ``object_class`` to MongoStorageObject
        meta = attrs.get('Meta')
        setattr(meta, 'object_class', MongoStorageObject)

        new_class = super(MongoDeclarativeMetaclass, cls).__new__(cls, name, bases, attrs)

        return new_class


class MongoResource(Resource):
    """
    A class that can be subclassed in order to plug a mongo document
        resource directly into an API
    """
    __metaclass__ = MongoDeclarativeMetaclass

    invalid_filter_types = ['format', 'callback']

    query_terms = ['all',
                   'exists',
                   'mod',
                   'ne',
                   'in',
                   'nin',
                   'size',
                   'type']

    unsupported_query_terms = ['and', 'or', 'nor']

    class Meta:
        connection = None

    def apply_filters(self, request, applicable_filters):

        mongo_list_cursor = self._meta.connection.find(applicable_filters)
        results = []

        for mongo_obj in mongo_list_cursor:
            results.append(mongo_obj)

        return(results)

    def filter_query_to_mongo(self, value, field_name, filters, filter_expr,
            filter_type):
        """
        Turn the string ``value`` into a python object.
        """
        # Simple values
        if value in ['true', 'True', True]:
            value = True
        elif value in ['false', 'False', False]:
            value = False
        elif value in ('nil', 'none', 'None', None):
            value = None

        # Split on ',' if not empty string and has attr ``getlist``

        if filter_type == 'exact':
            return {field_name: value}

        elif len(value):
            if hasattr(filters, 'getlist'):
                value = []

                for part in filters.getlist(filter_expr):
                    value.extend(part.split(','))

            return({field_name: {'$%s' % filter_type: value}})

    def build_filters(self, filters=None):
        """
        Deconstructs a GET request to create filter params
        """
        # If the filter includes a query parameter, assume the user is
        # passing a JSON query to thye URL string and ignore any other parameters

        if filters.get('query'):
            qs_filters = json.loads(filters['query'])
            return(qs_filters)

        # Otherwise, construct a query from the parameters passed.

        try:
            [filters.pop(filter_type) for filter_type in self.invalid_filter_types]
        except KeyError:
            pass

        qs_filters = {}

        for filter_expr, value in filters.items():
            filter_bits = filter_expr.split(LOOKUP_SEP)
            field_name = filter_bits.pop(0)
            filter_type = 'exact'

            if len(filter_bits) and filter_bits[-1] in self.query_terms:
                filter_type = filter_bits.pop()

            query = self.filter_query_to_mongo(value, field_name,
                filters, filter_expr, filter_type)

            qs_filters.update(query)
            return(qs_filters)

    def build_bundle(self, obj=None, data=None, request=None):
        """
        Given either an object, a data dictionary or both, builds a ``Bundle``
        for use throughout the ``dehydrate/hydrate`` cycle.

        If no object is provided, an empty object from
        ``Resource._meta.object_class`` is created so that attempts to access
        ``bundle.obj`` do not fail.
        """
        if obj is None:
            obj = self._meta.object_class()

        else:
            obj = self._meta.object_class(obj)
            if '_id' in obj:
                if isinstance(obj.get('_id'), ObjectId):
                    obj.pk = obj['_id'].__str__()
                else:
                    obj.pk = obj['_id']

            if data:
                obj.update(data)

        return Bundle(obj=obj, data=data, request=request)

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        """
        A method that returns the URI for an indvidual object. Uses the
        ``ObjectID`` as the id in the URI
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        if bundle_or_obj is not None:
            url_name = 'api_dispatch_detail'
            kwargs['pk'] = bundle_or_obj.obj.get('_id').__str__()

        try:
            return self._build_reverse_url(url_name, kwargs=self.resource_uri_kwargs(bundle_or_obj))
        except NoReverseMatch:
            return ''

    def get_object_list(self, request):
        """
        A method to return a list of objects.
        """
        mongo_list_cursor = self._meta.connection.find()

        results = []

        for mongo_obj in mongo_list_cursor:
            results.append(mongo_obj)
        return(results)

    def obj_get_list(self, request=None, **kwargs):
        """
        A method to to enable filtering on a list
        """
        filters = {}

        if hasattr(request, 'GET'):
            # Grab a mutable copy.
            filters = request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)

        applicable_filters = self.build_filters(filters=filters)

        return(self.apply_filters(request, applicable_filters))

    def obj_get(self, request=None, **kwargs):
        """
        A method required to get a single object
        """
        return(self._meta.connection.find_one(ObjectId(kwargs['pk'])))

    def obj_create(self, bundle, request=None, **kwargs):
        """
        A method to create an object
        """
        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        self._meta.connection.save(bundle.obj, safe=True)

        return(bundle)

    def obj_update(self, bundle, request=None, **kwargs):
        """
        A method to update an object
        """
        return(self.obj_create(bundle, request, **kwargs))

    def obj_delete(self, request=None, **kwargs):
        """
        A method to delete a single object.

        Does not return a success or failure statement, MongoDB does not have
        that output.

        """
        self._meta.connection.remove(**kwargs)

    def obj_delete_list(self, request=None, **kwargs):
        """
        A method to delete an entire list of objects

        Same pattern as :meth:`obj_delete <obj_delete>`
        """
        self.obj_delete(request, **kwargs)

    def rollback(self, bundles):
        """
        UNUSED
        """
        raise NotImplemented("Rollback is not used with MongoDB.")
