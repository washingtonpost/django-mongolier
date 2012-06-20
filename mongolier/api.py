"""
api.py

A lightweight implementation of pymongo and django-tastypie

"""
from tastypie.resources import Resource
from bson.objectid import ObjectId

from mongolier.exceptions import DoesNotExist

class MongoResource(Resource):
    """
    A class that can be subclassed in order to plug a mongo document
        resource directly into an API
    """

    class Meta:
        connection = None

    def get_resource_uri(self, bundle_or_obj):
        """
        A method that returns the URI for an indvidual object
    
        Uses the `ObjectID` as the id in the URI
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
    
    def obj_create(self, request=None, **kwargs):
        """
        A method to create an object
        """
        bundle.obj = self._meta.connection.save(kwargs)

        bundle = self.full_hydrate(bundle)

        return(bundle)

    def obj_update(self, request=None, **kwargs):
        """
        A method to update an object
        """
        return(self.obj_create(bundle, request, **kwargs))

    def obj_delete(self, request=None, **kwargs):
        """
        A method to delete a single object.
        """

        # First, find the object to make sure it exists
        object_to_be_deleted = self._meta.connection.find_one(**kwargs)

        # If it exists, delete it.
        if object_to_be_deleted:
            self._meta.connection.remove(**kwargs)

        # Otherwise, raise exception
        else:
            raise DoesNotExist("Item with parameters %s does not exist" % kwargs)

    def obj_delete_list(self, request=None, **kwargs):
        """
        A method to delete an entire list of objects

        Does not check to see if the objects exist.  
        Will not raise exception out if no objects are deleted.
        """
        self._meta.connection.remove(**kwargs)

    def rollback(self, bundles):
        """
        Unused. A method to rollback failed database transactions.

        """
        raise NotImplementedError("Not used for Mongodb")