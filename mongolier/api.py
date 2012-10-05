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

    invalid_filter_types = ['format', 'callback', 'limit', 'offset', 'key']

    query_terms = ['all',
                   'exists',
                   'mod',
                   'ne',
                   'in',
                   'nin',
                   'size',
                   'type']

    query_terms_list_input = ['in', 'nin']
    unsupported_query_terms = ['and', 'or', 'nor']

    class Meta:
        connection = None

    def apply_filters(self, request, applicable_filters):

        mongo_list_cursor = self._meta.connection.api.find(applicable_filters)
        results = []

        for mongo_obj in mongo_list_cursor:
            results.append(mongo_obj)

        return(results)

    def filter_query_to_mongo(self, value, field_name, filters, filter_expr,
            filter_type):
        """
        Turn the string ``value`` into a python-mongo object.

        In order to filter in MongoDB, one must pass a dictionary with a modifier,
        this is basically an exact representation of the Javascript objects
        that MongoDB uses internally.

        For example, an ``in`` query would look like:

        ::

            filter_dict = {"my_field": {"$in": ["list","of","values"]}}

        """
        # Simple values
        if value in ['true', 'True', True]:
            value = True
        elif value in ['false', 'False', False]:
            value = False
        elif value in ('nil', 'none', 'None', None):
            value = None

        # If filter_type is exact, return a dictionary without any modifiers
        if filter_type == 'exact':
            return {field_name: value}

        # Otherwise, find the appropriate modifier and return a dictionary that
        # contains that modifier.
        # Split on ',' if not empty string and has attr ``getlist`` and has
        # not already been created as a list or bool
        if value and hasattr(filters, 'getlist') \
            and not isinstance(value, (list, bool))\
            and filter_type in self.query_terms_list_input:
            value = []

            for part in filters.getlist(filter_expr):
                value.extend(part.split(','))

        return({field_name: {'$%s' % filter_type: value}})

    def get_query_bits_from_dict(self, dictionary, keys_list=[], value=None):
        """
        A special method that examines dictionaries and extracts keys and values.

        ``keys_list`` and ``value`` are required for the ``filter_bits`` list,
        and ``value``, respectively, in  in ``::meth::<build_filters> build_filters``.
        """
        # If dictionary contains a query parameter, build the filter_bits
        # based on that parameter
        if dictionary.keys()[0] in self.query_terms:
            # check to see if the values are a dict
            if isinstance(dictionary.values()[0], dict):
                # Add the key that represents the field
                keys_list.extend(dictionary.values()[0].keys())
                # Add the key that represents the filter
                keys_list.extend(dictionary.keys())
                value = dictionary.values()[0].values()[0]

            # If it's not a dictionary, then it is a direct key, value pair
            else:
                keys_list.extend(dictionary.keys())
                if not value:
                    value = dictionary.values()[0]

            return(keys_list, value)

        # Iterate over the dictionary and create a keys_list
        for key, expr in dictionary.items():
            # If this is a dict, extract the key and pass it back into this method
            if isinstance(expr, dict):
                keys_list.append(key)
                keys_list, value = self.get_query_bits_from_dict(expr,
                    keys_list=keys_list, value=value)
            # If this is just a key/value pair, it is the end of iteration,
            # add to keys_list, value
            else:
                keys_list.append(key)
                value = expr

        return(keys_list, value)

    def build_filters(self, filters=None):
        """
        Deconstructs a GET request to create filter params

        Queries with mongolier accept three different types of patterns:

        * standard django double underbar (__)
        * a single JSON object, passed with the ``query`` parameter
        * a JSON object attached to a parameter, which represents a field
        """
        # If the filter includes a query parameter, assume the user is
        # passing a JSON query to thye URL string and ignore any other parameters
        if filters.get('query'):
            qs_filters = json.loads(filters['query'])
            return(qs_filters)

        # Otherwise, construct a query from the parameters passed.
        # First, remove reserved filter keywords
        try:
            [filters.pop(filter_type) for filter_type in self.invalid_filter_types]
        except KeyError:
            pass

        # Create a blank dictionary to store a filter dictionary
        qs_filters = {}

        # Iterate over the filters passed by the client
        for filter_expr, value in filters.items():
            # Sets the default filter type.  If no other modifiers are passed
            # this will produce a standard dictionary to filter on
            filter_type = 'exact'

            # Check first to see if a value can be decoded as json
            try:
                value_dict = json.loads(value)
                # Because the python json module is not as strict as JSON standards
                # We must check to make sure that the value loaded is a dict
                if not isinstance(value_dict, dict):
                    value_dict = None
            except ValueError:
                value_dict = None
            # If a value is decoded, it passes that dict into a special method
            if value_dict:
                # Get the value and filter_bits from the method.
                filter_bits, value = self.get_query_bits_from_dict(value_dict,
                    keys_list=[], value=None)
                # Because the field_name and the filter_expr are backward,
                # we need to set the field name = to filter expr
                field_name = filter_expr
            else:
                # Split filters that use the lookup separator (__ by default)
                filter_bits = filter_expr.split(LOOKUP_SEP)

                # field_name is the first item in the list
                field_name = filter_bits.pop(0)

            # Checks to make sure the modifier is in self.query_terms
            # (Makes sure it's a valid modifier)
            # If it's valid, it changes the filter_type to the query_term
            if len(filter_bits) and filter_bits[-1] in self.query_terms:
                filter_type = filter_bits.pop()

            # Convert the filters passed in to valid python/mongo
            query = self.filter_query_to_mongo(value, field_name,
                filters, filter_expr, filter_type)

            # Add the filter to the dictionary
            qs_filters.update(query)

            return(qs_filters)

    def build_bundle(self, obj=None, data=None, request=None):
        """
        Given either an object, a data dictionary or both, builds a ``Bundle``
        for use throughout the ``dehydrate/hydrate`` cycle.

        If no object is provided, an empty object from
        ``Resource._meta.object_class`` is created so that attempts to access
        ``bundle.obj`` do not fail.

        In order to maintain consistency between Django and MongoDB documents,
        it turns the obj's '_id' value into a pk, and adds it as a property
        on the obj.
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
                obj.pop('_id')

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
            return self._build_reverse_url(url_name, kwargs=kwargs)
        except NoReverseMatch:
            return ''

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
        return(self._meta.connection.api.find_one(ObjectId(kwargs['pk'])))

    def obj_create(self, bundle, request=None, **kwargs):
        """
        A method to create an object
        """
        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        self._meta.connection.api.save(bundle.obj, safe=True)

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
        self._meta.connection.api.remove(**kwargs)

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
