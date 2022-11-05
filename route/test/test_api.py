from django.test import TestCase
from django.urls import reverse

from route import views


class RouteApiTestCase(TestCase):
    def test_get(self):
        url = reverse('/route/add_route')
        print(url)
        responce = self.client.get(url)
