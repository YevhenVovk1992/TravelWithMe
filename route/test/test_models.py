from django.test import TestCase

from route.test.setup_file import Setting
from route import models


class PlaceTestCase(Setting):

    def test_name(self):
        place = self.test_place
        self.assertEqual(place.name, 'test_place')

    def test_info(self):
        place = self.test_place
        self.assertEqual(place.info, 'test_info')


class EventTestCase(Setting):
    def test_event_admin(self):
        event = self.test_event
        self.assertEqual(event.event_admin, 1)

    def test_validator_duration(self):
        limit_value = self.test_route._meta.get_field('duration').validators[0].limit_value
        message = self.test_route._meta.get_field('duration').validators[0].message
        self.assertEqual(limit_value, 1)
        self.assertEqual(message, 'Duration cannot be less than 1')

    def test_event_route(self):
        event = self.test_event
        self.assertEqual(event.id_route.country, 'test')
        self.assertEqual(event.id_route.start_point.name, 'test_place')
        self.assertEqual(event.id_route.duration, 1)
        self.assertEqual(event.id_route.route_type, 'Car')

    def test_to_dict(self):
        event = self.test_event
        event_dict = event.to_dict()
        self.assertEqual(event_dict.get('id route'), 'Route №1 Car-test-test_location-test_place-test_place')
        self.assertEqual(event_dict.get('price'), 10)