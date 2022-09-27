from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.route_filter, name='index'),
    path('add_route', views.add_route, name='add_route'),
    path('<int:id>', views.index, name='index'),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
]
