# -*- coding: latin-1 -*-

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from geographics import PositionApi


class ControllerTestCase(TestCase):
    def test_http200_get_home(self):
        """
        Testa o retorno da homepage.
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)