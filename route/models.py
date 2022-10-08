from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User, Group


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=120, null=False)
    info = models.TextField(null=True)

    def __str__(self):
        return f'{self.name}'


class Route(models.Model):
    class RouteType(models.TextChoices):
        Car = 'Car', gettext_lazy('Car')
        ByFoot = 'Foot', gettext_lazy('Foot')
        Motor = 'Motor', gettext_lazy('Motor')

    start_point = models.ForeignKey(Place, null=False, related_name='start_route', on_delete=models.RESTRICT)
    stop_point = models.JSONField(null=True)
    destination = models.ForeignKey(Place, null=False, related_name='stop_route', on_delete=models.RESTRICT)
    route_type = models.CharField(max_length=50, choices=RouteType.choices, default=RouteType.ByFoot, null=False)
    country = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=120, null=False)
    description = models.TextField(null=True)
    duration = models.IntegerField(null=False, default=7)

    def __str__(self):
        return f'Route №{self.pk} {self.route_type}-{self.country}-{self.location}-{self.start_point}-{self.destination}'

    def to_dict(self):
        return {
            'id': self.pk,
            'start point': str(self.start_point),
            'stop point': self.stop_point,
            'destination': str(self.destination),
            'route type': self.route_type,
            'country': self.country,
            'location': self.location,
            'description': self.description,
            'duration': self.duration
        }


class Event(models.Model):
    id_route = models.ForeignKey(Route, null=False, related_name='route', on_delete=models.RESTRICT)
    event_admin = models.IntegerField()
    approved_users = models.TextField(null=True)
    pending_users = models.TextField(null=True)
    start_date = models.DateField(null=False)
    price = models.IntegerField(null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'id route': str(self.id_route),
            'event_admin': self.event_admin,
            'approved_users': self.approved_users,
            'pending_users': self.pending_users,
            'start_date': self.start_date,
            'price': self.price
        }


class RouteReview(models.Model):
    id_route = models.ForeignKey(Route, null=False, related_name='route_review', on_delete=models.RESTRICT)
    rating = models.IntegerField(null=False)
    comment = models.TextField(null=True)


class ChoiceTypeAccount:
    _CHOICES_LIST = [(itm.pk, itm.name) for itm in Group.objects.all()]

    @classmethod
    def choices_type(cls):
        return cls._CHOICES_LIST
