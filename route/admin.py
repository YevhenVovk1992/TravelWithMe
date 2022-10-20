from django.contrib import admin
from route.models import Place, Route, Event, RouteReview


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_route', 'event_admin', 'start_date', 'price']
    list_display_links = ['id', 'id_route']
    list_filter = ['id_route', 'event_admin']


class RouteAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_point',
        'stop_point',
        'destination',
        'route_type',
        'country',
        'location',
        'description',
        'duration']
    list_display_links = ['id', 'country', 'location', 'description',]
    list_filter = ['route_type', 'country', 'location', 'duration']


class RouteReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_route', 'rating', 'comment']
    list_display_links = ['id', 'id_route', 'rating']
    list_filter = ['id_route', 'rating']


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'info']
    list_display_links = ['id', 'name', 'info']


admin.site.register(Place, PlaceAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RouteReview, RouteReviewAdmin)
