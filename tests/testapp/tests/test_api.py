"""
test_api.py

A harness for testing API features
"""
import json
from django.test.client import Client, FakePayload, MULTIPART_CONTENT
from django.test import TestCase
from warnings import warn
from urlparse import urlparse
from django.db import settings


class TestClient(Client):
    """
    A test client with additional methods for tastypie that the 1.4 client does not
    currently support
    """
    def patch(self, path, data={}, content_type=MULTIPART_CONTENT,
             **extra):
        "Construct a PATCH request."
        warn("This custom patch method here is deprecated in Django 1.5 by the ``generic`` method.")
        post_data = self._encode_data(data, content_type)

        parsed = urlparse(path)
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      self._get_path(parsed),
            'QUERY_STRING':   parsed[4],
            'REQUEST_METHOD': 'PATCH',
            'wsgi.input':     FakePayload(post_data),
        }
        r.update(extra)
        return self.request(**r)


class TestAPI(TestCase):
    """
    A series of tests to make sure the API behavior is working correctly.
    """

    def setUp(self):

        self.client = TestClient()

    def test_object(self):
        """
        Test getting a URL
        """
        # Test a standard GET response
        get_response = self.client.get('/api/test/mongo/?format=json')
        self.assertEqual(get_response.status_code, 200)

        # Test a POST response
        post_response = self.client.post('/api/test/mongo/?format=json',
            json.dumps({'mongolier-api-test': 1}),
            content_type='application/json')
        self.assertEqual(post_response.status_code, 201)
        test_response = self.client.get('/api/test/mongo/?format=json')
        test_response_json = json.loads(test_response.content)
        self.assertNotEqual(test_response_json['meta']['total_count'], 0)

        # Test a PATCH response
        test_response = self.client.get('/api/test/mongo/?format=json')
        test_response_json = json.loads(test_response.content)
        # Find the Mongolier test object, and retrieve its id
        for value in test_response_json['objects']:
            if value['my_field']['mongolier-api-test'] == 1:
                mongolier_test_object = value['my_field']
        self.assertEqual(len(mongolier_test_object), 2)
        # Assemble data to update
        mongolier_test_object.update({'another_field': 1})
        patch_response = self.client.patch('/api/test/mongo/?format=json',
            json.dumps(mongolier_test_object),
            content_type='application/json')

        # Destroy data
        settings.MONGO_TEST_CONN.api.remove({'mongolier-api-test': 1})

    def test_list(self):
        """
        Test creating an object in Mongo
        """
