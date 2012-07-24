Utilities
=========

Management Commands
-------------------

Mongolier includes a management commands that emulate Django's load and dump data.
Keep in mind, this are not a replacement for ``mongoexport`` or ``mongoimport`` (utilities
that are included with MongoDB), as those tools are more powerful. This is simply
a tool that is designed to replicate Django's management commands so that it tightens
the link between your data.

Available options
^^^^^^^^^^^

**-d --database**

MongoDB database name

**-c, --collection**

MongoDB collection name

**-a, --auth**

MongoDB auth

**-o, --respect_id**

When exporting, leave the ``_id`` of the original object.  Probably not a good idea
for ObjectId, because those rely on system information to create. (Though ObjectId is
supported)

**-g, --gridfs**

Use GridFS instead of a standard connection

mongolier_dumpdata
^^^^^^^^^^^^^^^^^^

Very nearly the same behavior as Django's dumpdata, except you must specify
the database, collection, auth, etc.

Outputs data to stdout.

::

    $ django-admin.py mongolier_dumpdata -d my_db -c my_col --respect_id > /tmp/my_file.json

mongolier_loaddata
^^^^^^^^^^^^^^^^^^

Similar to mongolier_dumpdata, except the argument must specify a file to load from.

::

    $ django-admin.py mongolier_dumpdata -d my_db -c my_col --respect_id /tmp/my_file.json


Convert
-------

Mongolier also includes a few conversion utilities that help with Object (``python``)
-> Document(``MongoDB``) manipulation.

With pymongo, this is done via the ``json`` module, however, that is not always ideal.

Sometimes, you'd like to transform data and push it directly into MongoDB without going
through a JSON intermediary.

Convert decimals
^^^^^^^^^^^^^^^^

Convert Python Decimal objects to either floats or strings

::

    from mongolier.utils import ConvertDecimal

    converter = ConvertDecimal()

    converter.convert(['a', 'b', 'c', Decimal('5')])

By default, it converts to strings.  To use floats instead, pass ``to_float`` into the
instantiation.

::

    converter = ConvertDecimal(to_float=True)

Deserializer
^^^^^^^^^^^^

Remove the python bits that MongoDB doesn't like.

Currently converts:

* unicode
* decimal
* date
* datetime

::

    from mongolier.utils import Deserializer

    deserializer = Deserializer()

    converter.convert(['a', 'b', u'c', Decimal('5')], datetime.date(5, 1, 2012))


Extending the converter
-----------------------

You can extend the Converter class in order to change behavior and add additional
conversion functionality.

For example, to convert all datetimes to date strings:

* Add an object to compare against and a method to ``__init__``
* Add that method and do your conversion

::

    ```converter.py```

    from mongolier.utils import BaseConvert


    class DateConverter(BaseConvert):


        def __init__(self, **kwargs):

            super(Deserializer, self).__init__(**kwargs)

            self.other_input = {
                datetime.datetime: self.to_date,
            }

        def to_date(self, datetime_obj):

            return(datetime.datetime.strftime(date_obj, '%Y-%m-%d'))



