from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def route_filter(request, route_type=None, country=None, location=None):
    return HttpResponse(f'<h3>{route_type}-{country}-{location}</h3>')


def add_route(request):
    return HttpResponse('Create new route')


def route_detail(request, id_route):
    return HttpResponse(f'<h3>{id_route}</h3>')


def route_review(request, id_route):
    return HttpResponse(f'<h3>{id_route}</h3>')


def route_add_event(request, id_route):
    return HttpResponse(f'<h3>{id_route}</h3>')


def event_handler(request, event_id):
    return HttpResponse(f'<h3>{event_id}</h3>')
