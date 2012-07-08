Tastypie API
=============

 The .. _Tastypie: https://github.com/toastdriven/django-tastypie module for mongolier
supports many of the basic functions of Tastypie.  Keep in mind, that not everything
is supported

**Currently Supported**

* CRUD (GET, POST, PATCH, PUT, DELETE)
* Top-level filtering

**Unsupported**

The following features are unsupported, but are on the roadmap for future
implementation

* Sorting
* More complex filtering


Setup
-----

* In your api.py, import a connection, and assign it to a resource.
* choose a field for your resource, name it, and dehydrate the bundle into that resource.

*(A future version will likely return the document into a standard field by default)*

**Example**

::

    ```api.py```

    from mongolier.api import MongoResource
    from tastypie import fields

    from my_settings import my_persistent_connection

    class MyResource(MongoResource):

        palms = fields.DictField()

        class Meta:

            connection = my_persistent_connection
            resource_name = 'my_resource'

        def dehydrate_palms(self, bundle_or_obj):
            return(bundle_or_obj.obj)



The rest of the Tastypie setup is standard.

Typical usage would be to create a collection for each resource.

Usage
-----

To query the example above, follow standard Tastypie patterns:

``http://my_site/api/v1/my_resource/format=json``

Let's say, one of your documents has a top-level parameter of "face" with
a value of 5, you can pass those into the URL and return only the documents
which match that parameter.

``http://my_site/api/v1/my_resource/format=json&face=5``

Extending
---------

By default, mongolier will assign your document's ``_id`` to be the ID available
at the ``resource_uri``. To change this behavior, override the method ::meth::`get_resource_uri <get_resource_uri`.

Any functionality that mongolier does not provide, you can override any of the typical tastypie methods,
as they are available.
