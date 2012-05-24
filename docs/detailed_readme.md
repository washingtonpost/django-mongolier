# django-mongolier detailed readme

## MongoConnection

`db.py` includes a MongoConnection class. MongoConnection is a base class for connecting to the WaPo MongoDB server hosted on Amazon EC2 at http://data.washingtonpost.com/

###Usage
    
    mongo_object = connect.MongoConnection(port=222, host='myhost')
    mongo_connection = mongo_object.connect()

## Class-based Mongo views

`views.py` includes a generic list and detail view for mapping MongoDB document objects from PyMongo to template context objects.

###ListView usage

    class LogList(ListView):
        """
        A simple list view.
        """
        db_name                 = 'sports'  # The database name
        collection_name         = 'log'     # The collection name
        query_filter            = { 'kwargs': { 'mongo_field': 'script', 'url_kwarg':'script_name' } }
        query_sort              = { 'field': '$natural', 'direction': DESCENDING }
        context_object_name     = 'logs'    # The context object that the main query should be returned to.
        
####Using `query_filter`

`query_filter` is a dict containing information for how the list view should structure a MongoDB query.

`query_filter` should contain a dict with the keyword argument `kwargs`.

The keyword argument `kwargs` should have a value with another dict. This dict should contain two keyword args:

*   `mongo_field` -- The field name for PyMongo to filter on.
*   `url_kwarg` -- The URL kwarg from `urls.py` for PyMongo to match on.

Please see https://github.com/WPMedia/wapo-sports-pkg/blob/master/wapo\_sports\_proj/apps/log/views.py for examples.

####Using `query_sort`

`query_sort` is a dict containing information for how the class-based views should sort a MongoDB query.

The `query_sort` dict should have two keyword arguments:

*   `field` -- The name of the field for PyMongo to sort on.
*   `direction` -- The direction for PyMongo to sort in.

Please see https://github.com/WPMedia/wapo-sports-pkg/blob/master/wapo\_sports\_proj/apps/log/views.py for examples.

###DetailView

    class LogDetail(DetailView):
        """
        A simple detail view.
        """
        db_name                 = 'sports'  # The database name
        collection_name         = 'log'     # The collection name
        query_filter            = { 'kwargs': { 'url_kwarg':'log_id' } }
        context_object_name     = 'log'     # The context object that the main query should be returned to.

####Using `query_filter`

`query_filter` is a dict containing information for how the detail view should find an object.

`query_filter` should contain a dict with the keyword argument `kwargs`.

The keyword argument `kwargs` should have a value with another dict. This dict should contain one keyword arg:

*   `url_kwarg` -- The URL kwarg from `urls.py` for PyMongo to match on.

