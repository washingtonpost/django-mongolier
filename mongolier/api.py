"""
api.py

A lightweight implementation of pymongo and django-tastypie

"""
from tastypie.resources import Resource, DeclarativeMetaclass
from bson.objectid import ObjectId


class MongoStorageObject(dict):
    """
    An object that stores information for data before it is transferred
    to Mongo.  It's a placeholder so that information can be properly passed
    through tastypie's methods.

    """
    pk = None


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

    class Meta:
        connection = None

    def get_resource_uri(self, bundle_or_obj):
        """
        A method that returns the URI for an indvidual object. Uses the
        ``ObjectID`` as the id in the URI
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        kwargs['pk'] = bundle_or_obj.obj.get('_id').__str__()

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

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
        return(self.get_object_list(request))

    def obj_get(self, request=None, **kwargs):
        """
        A method required to get a single object
        """
        return(self._meta.connection.find_one(ObjectId(kwargs['pk'])))

    def obj_create(self, bundle, request=None, **kwargs):
        """
        A method to create an object
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        bundle.obj.pk = self._meta.connection.save(kwargs)

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
