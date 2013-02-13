"""
views.py

A module that replicates django's class based views for mongodb

"""
try:
    from django.db.settings import DEFAULT_PAGINATION
except ImportError:
    DEFAULT_PAGINATION = 25
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.views.generic.list import ListView as GenericListView
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse


class BaseMongoMixin(object):
    """
    Base Mixin object.
    """
    connection = None
    sort = None
    query = None
    results = None
    context_object_name = None
    template_name = None
    class_type = None

    def get_context_data(self, *args, **kwargs):
        context = {'object_list': self.results}
        context.update(**kwargs)
        context[self.context_object_name] = self.results
        return context

    def get_template_name(self):
        if not self.template_name:
            return u'%s/%s_%s.html' % (self.connection.collection, self.connection.collection, self.class_type)
        else:
            return self.template_name

    def render_to_response(self, context):
        return TemplateResponse(request=self.request,
            template=self.get_template_name(),
            context=context,)


class BasePaginatedMongoMixin(BaseMongoMixin):
    pages = None
    page = None
    next_page_number = None
    previous_page_number = None
    offset = None
    pagination_limit = DEFAULT_PAGINATION
    page_range = None

    def get_context_data(self, *args, **kwargs):
        context = super(BasePaginatedMongoMixin, self).get_context_data(*args, **kwargs)
        context['page'] = self.page
        context['pages'] = self.pages
        context['page_range'] = self.page_range
        context['previous_page_number'] = self.previous_page_number
        context['next_page_number'] = self.next_page_number
        return context


class DetailView(BaseMongoMixin, View):
    """
    A Detail
    """
    class_type = 'detail'

    def get_object(self, *args, **kwargs):
        if self.query:
            kwargs.update(self.query)

        obj_query = self.connection.api.find_one(kwargs, sort=self.sort)

        if obj_query == None:
            raise Http404(u"List is empty.")
        else:
            return obj_query, 'query'

    def get(self, request, *args, **kwargs):
        """
        Overrides the built in get() function on the base View class.
        Gets the object and the context.
        Returns a redirect if there's an issue with the page number.
        """
        # If the type of response is a query:
        if self.get_object()[1] == 'query':

            # Set the results to the first part of the tuple.
            self.results = self.get_object(*args, **kwargs)[0]

            # If there are no results ...
            if not self.results:

                #... raise a 404.
                raise Http404(u"List is empty.")

            # If there are results, set the context data.
            context = self.get_context_data()

            # Return render_to_response with the context data.
            return self.render_to_response(context)

        # Otherwise, if the response is a redirect ...
        elif self.get_object()[1] == 'redirect':

            #... execute the redirect.
            return HttpResponseRedirect(self.get_object()[0])


class ListView(BaseMongoMixin, View):

    #: View type
    class_type = 'list'
    #: Determines whether or not to add the mongo `_id` param to output
    show_id = False

    def _get_query_list(self, mongo_iterable):
        """
        Iterates over a mongo iterable to provide a list for consumption in the
        view
        """
        query_list = []

        # Append each item to the query_list.
        for item in mongo_iterable:
            item_dict = dict(item)
            # If show id is set, adds the mongo `_id` to the key `id`
            if self.show_id:
                item_dict['id'] = str(item['_id'])

            # Remove this key always, it is very un-django
            item_dict.pop('_id')
            query_list.append(item_dict)

        return(query_list)

    def get_list(self, *args, **kwargs):
        """
        Provides a list of JSON objects from a MongoConnection class.
        """
        if self.query:
            kwargs.update(self.query)
        # Get the total count and the number of pages.
        mongo_iterable = self.connection.api.find(kwargs, sort=self.sort)

        query_list = self._get_query_list(mongo_iterable)

        # Return the query list, and set the type of return to query.
        return query_list, 'query'

    def get(self, request, *args, **kwargs):
        """
        Overrides the built in get() function on the base View class.
        Gets the object and the context.
        Returns a redirect if there's an issue with the page number.
        """

        query_list, query_type = self.get_list()
        # If the type of response is a query:
        if query_type == 'query':

            # Set the results to the first part of the tuple.
            results = self.get_list(*args, **kwargs)[0]

            # If there are no results raise a 404.
            if not results:
                raise Http404(u"List is empty.")

            # If there are results, set the context data.
            context = self.get_context_data(**kwargs)

            # Return render_to_response with the context data.
            return self.render_to_response(context)

        elif query_type == 'redirect':
            return HttpResponseRedirect(query_list)


class PaginatedListView(BasePaginatedMongoMixin, ListView, GenericListView):
    """
    Provides a generic list view for MongoDB.
    """

    def _redirect(self, page):
        # short circuit the process and return a redirect URL while setting the type as a redirect.
        redirect_url = '%s?page=%s' % (self.request.META['PATH_INFO'], page)
        return redirect_url, 'redirect'

    def get_list(self, *args, **kwargs):
        """
        Provides a list of JSON objects from a MongoConnection class.
        """
        import pdb;pdb.set_trace()
        # if self.query:
        #     kwargs.update(self.query)
        # # Get the total count and the number of pages.
        # total_count = self.connection.api.find(kwargs, sort=self.sort).count()

        # self.pages = total_count / self.pagination_limit

        # if total_count % self.pagination_limit:
        #     self.pages + 1

        # if self.pages == 1:
        #     self.page_range = [1]
        # else:
        #     self.page_range = range(1, self.pages + 1)

        # # Try to get the page from the URL.
        # if 'page' in self.request.GET:
        #     self.page = int(self.request.GET['page'])

        # # If there's no page in the URL, set the page to 1.
        # else:
        #     self.page = 1
        #     self.offset = 0

        # # Redirect invalid pages to their proper counterpart.
        # if self.page == 0:
        #     self._redirect(1)

        # elif self.page > self.pages:
        #     self._redirect(self.pages)

        # else:
        #     # If so, set the offset to the 1-indexed page number * the pagination limit.
        #     self.offset = (self.page - 1) * self.pagination_limit

        #     # Set the previous/next page numbers.
        #     if self.page == 1 and self.page == self.pages:
        #         pass

        #     elif self.page == 1:
        #         self.next_page_number = 2

        #     elif self.page == self.pages:
        #         self.previous_page_number = self.page - 1

        #     else:
        #         self.next_page_number = self.page + 1
        #         self.previous_page_number = self.page - 1

        # # Send along the connection query with the sort attached.
        # mongo_iterable = self.connection.api.find(kwargs,
        #                     limit=self.pagination_limit,
        #                     skip=self.offset,
        #                     sort=self.sort
        #                 )

        # query_list = self._get_query_list(mongo_iterable)

        # # Return the query list, and set the type of return to query.
        # return query_list, 'query'
