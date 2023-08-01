#!/usr/bin/python3
"""Tests for the module api.v1.app"""

import unittest
from werkzeug.test import Client
from api.v1 import app


class AppTestCase(unittest.TestCase):
    """Class for Testing the module app"""

    def setUp(self):
        """Set up for the tests"""
        self.c = Client(app.app)
    def test_app_application(self):
        """Tests the app using Client"""
        response = self.c.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)

    def test_app_response_content_type(self):
        """Tests the response content type of the
        route /api/v1/status"""
        response = self.c.get('/api/v1/status')
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'application/json')
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_cities_view(self):
        """Tests the routes from the states view"""
        response = self.c.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.get_json()), list)
        
        response = self.c.get('/api/v1/states/not_a_state')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

        response = self.c.delete('/api/v1/states/123')
        self.assertEqual(response.status_code, 404)
        
        state = {"name": "Colorado"}
        response = self.c.post('/api/v1/states', json=state)
        self.assertEqual(response.status_code, 201)
        state_id = response.get_json()["id"]

