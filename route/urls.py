from django.contrib import admin
from django.urls import path

from . import views

app_name = 'route'

urlpatterns = [
    path('', views.route_filter, name='route_all'),
    path('<str:route_type>', views.route_filter, name='route_type'),
    path('<str:route_type>/<str:country>', views.route_filter, name='route_country'),
    path('<str:route_type>/<str:country>/<str:location>', views.route_filter, name='route_location'),
    path('<int:id>', views.route_detail, name='route_detail'),
    path('<int:id>/review', views.route_review, name='route_review'),
    path('add_route', views.add_route, name='add_route'),
    path('<int:id>/add_event', views.route_add_event, name='add_event'),
]
