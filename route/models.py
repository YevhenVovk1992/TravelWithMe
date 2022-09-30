from django.db import models
from django.utils.translation import gettext_lazy


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
    stop_point = models.JSONField()
    destination = models.ForeignKey(Place, null=False, related_name='stop_route', on_delete=models.RESTRICT)
    route_type = models.CharField(max_length=50, choices=RouteType.choices, default=RouteType.ByFoot, null=False)
    country = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=120, null=False)
    description = models.TextField(null=True)
    duration = models.IntegerField(null=False, default=7)



class Event(models.Model):
    id_route = models.ForeignKey(Route, null=False, related_name='route', on_delete=models.RESTRICT)
    event_admin = models.IntegerField()
    approved_users = models.TextField(null=True)
    pending_users = models.TextField(null=True)
    start_date = models.DateField(null=False)
    price = models.IntegerField(null=True)
