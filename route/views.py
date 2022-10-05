from django.shortcuts import render, redirect
from django.http import HttpResponse

from route import forms
from route import models


# Create your views here.

def index(request):
    top_routes = models.RouteReview.objects.order_by('rating')[:3]
    countries = models.Route.objects.raw('SELECT id, country FROM route_route GROUP BY country')
    data = {
        'title': 'TravelWithMe',
        'top_routes': top_routes,
        'countries': countries
    }
    return render(request, 'route/index.html', data)


def route_filter(request, **kwargs):
    route_list = models.Route.objects.all().filter(**kwargs)
    data = {
        'title': 'Routes',
        'route_list': [itm.to_dict() for itm in route_list]
    }
    return render(request, 'route/route_filter.html', data)


def add_route(request):
    form = forms.RouteForm()
    if request.method == 'GET':
        data = {
            'title': 'Add New Route',
            'form': form,
            'anchor': 'signup'
        }
        return render(request, 'route/add_route.html', data)
    if request.method == 'POST':
        data = {
            'title': 'Add New Route',
            'anchor': '#signup',
            'operation_status': 'Operation successful'
        }
        try:
            new_route = models.Route(
                start_point=models.Place.objects.filter(id=request.POST.get('start_point'))[0],
                destination=models.Place.objects.filter(id=request.POST.get('destination'))[0],
                route_type=request.POST.get('route_type'),
                country=request.POST.get('country'),
                location=request.POST.get('location'),
                description=request.POST.get('description'),
                duration=request.POST.get('duration')
            )
            new_route.save()
        except Exception as error:
            data['operation_status'] = error
            return render(request, 'route/error.html', data)
        else:
            return render(request, 'route/successful.html', data)


def route_detail(request, id_route):
    get_route = models.Route.objects.filter(pk=id_route).first()
    get_events = models.Event.objects.filter(id_route=id_route).all()
    data = {
        'title': 'Info',
        'route': get_route,
        'events': get_events
    }
    return render(request, 'route/route_detail.html', data)


def route_review(request, id_route):
    if request.method == 'GET':
        get_reviews = models.RouteReview.objects.filter(id_route=id_route).all()
        data = {
            'title': 'Reviews',
            'reviews': get_reviews
        }
        return render(request, 'route/route_review.html', data)


def route_add_event(request, id_route):
    if request.method == 'GET':
        form = forms.EventForm()
        data = {
            'title': 'Add New Event',
            'form': form
        }
        return render(request, 'route/add_event.html', data)
    if request.method == 'POST':
        data = {
            'title': 'Add New Event',
            'anchor': '#signup',
            'operation_status': 'Operation successful'
        }
        try:
            new_event = models.Event(
                id_route=models.Route.objects.filter(id=request.POST.get('id_route'))[0],
                event_admin=request.POST.get('event_admin'),
                start_date=request.POST.get('start_date'),
                price=request.POST.get('price')
            )
            new_event.save()
        except Exception as error:
            data['operation_status'] = error
            return render(request, 'route/error.html', data)
        else:
            return render(request, 'route/successful.html', data)


def event_handler(request, event_id):
    get_event = models.Event.objects.filter(pk=event_id).first()
    print(get_event)
    data = {
        'title': 'Event Info',
        'event': get_event
    }
    return render(request, 'route/event_detail.html', data)
