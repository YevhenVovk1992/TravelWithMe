from django.urls import path

from . import views

app_name = 'route'

urlpatterns = [
    path('', views.route_filter, name='route_all'),
    path('add_route', views.add_route, name='add_route'),
    path('<int:id_route>', views.route_detail, name='route_detail'),
    path('<int:id_route>/review', views.route_review, name='route_review'),
    path('<int:id_route>/add_event', views.route_add_event, name='add_event'),

    path('type-<str:route_type>', views.route_filter, name='route_type'),
    path('type-<str:route_type>/country-<str:country>', views.route_filter, name='route_country'),
    path(
        'type-<str:route_type>/country-<str:country>/location-<str:location>',
        views.route_filter, name='route_location')
]
