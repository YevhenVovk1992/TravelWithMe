from django.test import TestCase

from django.contrib.auth.models import User
from route import models


class Setting(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_place = models.Place(
                id=1,
                name='test_place',
                info='test_info'
            )
        cls.test_route = models.Route(
            id=1,
            start_point=cls.test_place,
            stop_point='test_stop_point',
            destination=cls.test_place,
            route_type='Car',
            country='test',
            location='test_location',
            description='test',
            duration=1
        )
        cls.test_event = models.Event(
            id=1,
            id_route=cls.test_route,
            event_admin=1,
            event_users='test',
            start_date='2022-03-02',
            price=10
        )
        cls.event_admin = User(
            id=1,
            username='test',
            email='test@test.com',
            password='test',
            first_name='test',
            last_name='test'
        )
        cls.event_admin.save()
        cls.test_place.save()
        cls.test_route.save()
        cls.test_route.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        models.Place.objects.filter(id=1).delete()
        models.Route.objects.filter(id=1).delete()
        models.User.objects.filter(id=1).delete()
        models.Event.objects.filter(id=1).delete()