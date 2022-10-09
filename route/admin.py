from django.contrib import admin
from route.models import Place, Route, Event, RouteReview


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_route', 'event_admin', 'start_date', 'price']
    list_display_links = ['id', 'id_route']
    list_filter = ['id_route', 'event_admin']


admin.site.register(Place)
admin.site.register(Route)
admin.site.register(Event, EventAdmin)
admin.site.register(RouteReview)
