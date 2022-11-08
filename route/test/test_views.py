from django.contrib.auth.models import Permission, Group, User, AnonymousUser
from django.test import TestCase, RequestFactory, Client

from route import views, models
from route.test.setup_file import Setting


# Create your tests here.
class IndexTestCase(TestCase):

    def test_url_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_get(self):
        response = self.client.get('')
        self.assertEqual(response.context['countries'].columns, ['id', 'country', 'place'])


class AddRouteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.place = models.Place(
            id=1,
            name='test_place',
            info='test_info'
        )
        self.place.save()

        class UserMock:

            def has_perm(self, *args, **kwargs):
                return True

        self.user = UserMock()

    def test_for_anonymous_user(self):
        request = self.factory.get('/route/add_route')
        request.user = AnonymousUser()
        response = views.add_route(request)
        self.assertEqual(response.status_code, 302)

    def test_for_login_user(self):
        request = self.factory.get('/route/add_route')
        request.user = self.user
        response = views.add_route(request)
        self.assertEqual(response.status_code, 200)

    def test_add_route_post(self):
        stop_point = """
                    [{
                        "name": "point1", 
                        "lat": "000.0000", 
                        "lon": "000.0000"
                    }, {
                        "name": "point2", 
                        "lat": "000.0000", 
                        "lon": "000.0000"
                    }]"""

        form_data = {
            'stop_points': stop_point,
            'start_point': 1,
            'destination': 1,
            'stop_point': stop_point,
            'route_type': 'Car',
            'country': 'UK',
            'location': 'UK',
            'description': 'test',
            'duration': 4
        }
        self.assertEqual(models.Route.objects.count(), 0)
        request = self.factory.post('/route/add_route', data=form_data)
        request.user = self.user
        response = views.add_route(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Route.objects.count(), 1)


class RouteFilterApiTestCase(TestCase):
    def test_url_route_filter(self):
        client = Client()
        response = client.get('/route/')
        self.assertEqual(response.status_code, 200)


class EventAllTestCase(Setting):

    def setUp(self) -> None:
        self.client = Client()
        for i in range(10):
            event = models.Event(
                id=i,
                id_route=self.test_route,
                event_admin=1,
                event_users='test',
                start_date='2022-03-02',
                price=10
            )
            event.save()

    def tearDown(self) -> None:
        for i in range(10):
            event = models.Event.objects.get(id=i)
            event.delete()

    def test_url_event_all(self):
        response = self.client.get('/event')
        self.assertEqual(response.status_code, 200)

    def test_paginator(self):
        response = self.client.get('/event')
        self.assertEqual(response.context['paginator'].get('all'), 2)
        self.assertEqual(len(models.Event.objects.all()), 10)
