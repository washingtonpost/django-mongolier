Using Views
===========

``views.py`` includes a generic list and detail view for mapping MongoDB document objects from PyMongo to template context objects.

ListView usage
-----------------

::

    class LogList(ListView):
        """
        A simple list view.
        """
        db_name                 = 'sports'  # The database name
        collection_name         = 'log'     # The collection name
        query_filter            = { 'kwargs': { 'mongo_field': 'script', 'url_kwarg':'script_name' } }
        query_sort              = { 'field': '$natural', 'direction': DESCENDING }
        context_object_name     = 'logs'    # The context object that the main query should be returned to.

Using `query_filter`
--------------------

``query_filter`` is a dict containing information for how the list view should structure a MongoDB query.

``query_filter`` should contain a dict with the keyword argument ``kwargs``.

The keyword argument ``kwargs`` should have a value with another dict. This dict should contain two keyword args:

*   ``mongo_field`` -- The field name for PyMongo to filter on.
*   ``url_kwarg`` -- The URL kwarg from ``urls.py`` for PyMongo to match on.

Using `query_sort`
------------------

``query_sort`` is a dict containing information for how the class-based views should sort a MongoDB query.

The `query_sort` dict should have two keyword arguments:

*   ``field`` -- The name of the field for PyMongo to sort on.
*   ``direction`` -- The direction for PyMongo to sort in.

DetailView
----------

::

    class LogDetail(DetailView):
        """
        A simple detail view.
        """
        db_name                 = 'sports'  # The database name
        collection_name         = 'log'     # The collection name
        query_filter            = { 'kwargs': { 'url_kwarg':'log_id' } }
        context_object_name     = 'log'     # The context object that the main query should be returned to.
