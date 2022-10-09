from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Sum, Count, Avg
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User, Group


from route import forms
from route import models


# Create your views here.

def index(request):
    top_routes = models.RouteReview.objects.order_by('rating')[:3]
    countries = models.Route.objects.raw(
        """SELECT route_route.id, route_route.country as country, route_place.name as place
        FROM route_route join route_place
        ON route_route.start_point_id = route_place.id
        GROUP BY route_route.country"""
    )
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


@login_required(login_url='login')
def add_route(request):
    if request.user.has_perm('route.add_route'):
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
    else:
        data = {
            'title': 'Add New Route',
            'operation_status': 'No access'
        }
        return render(request, 'route/error.html', data)


def route_detail(request, id_route):
    get_route = models.Route.objects.filter(pk=id_route).first()
    get_events = models.Event.objects.filter(id_route=id_route).all()
    get_review = models.RouteReview.objects.filter(id_route=id_route).all()
    avg_rating = int(models.RouteReview.objects.values('id_route').filter(id_route=id_route).annotate(avg=Avg('rating'))[0]['avg'])
    data = {
        'title': 'Info',
        'route': get_route,
        'events': get_events,
        'get_review': get_review,
        'avg_rating': avg_rating
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


@login_required(login_url='login')
def route_add_event(request, id_route):
    if request.user.has_perm('route.add_event'):
        if request.method == 'GET':
            form = forms.EventForm(initial={'id_route': id_route})
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
    else:
        data = {
            'title': 'Error',
            'operation_status': 'No access'
        }
        return render(request, 'route/error.html', data)


@login_required(login_url='login')
def event_handler(request, event_id):
    if request.user.has_perm('route.view_event'):
        get_event = models.Event.objects.filter(pk=event_id).first()
        data = {
            'title': 'Event Info',
            'event': get_event
        }
        return render(request, 'route/event_handler.html', data)
    else:
        data = {
            'title': 'Error',
            'operation_status': 'No access'
        }
        return render(request, 'route/error.html', data)


def event_all(request):
    all_event = models.Event.objects.all()
    data = {
        'title': 'All Events',
        'all_event': [itm.to_dict() for itm in all_event]
    }
    return render(request, 'route/all_events.html', data)


def user_login(request):
    if request.method == 'GET':
        form = forms.UserLogin()
        data = {
            'title': 'User Login',
            'form': form
        }
        return render(request, 'route/login.html', data)
    if request.method == 'POST':
        form = forms.UserLogin(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if request.user.is_authenticated:
                    data = {
                        'title': 'Already log',
                        'operation_status': 'You are already logged in'
                    }
                    return render(request, 'route/error.html', data)
                if user.is_active:
                    login(request, user)

                    return redirect('index')
                else:
                    data = {
                        'title': 'User Error',
                        'operation_status': 'Disable account'
                    }
                    render(request, 'route/error.html', data)
            else:
                return redirect('registration')


def user_logout(request):
    logout(request)
    return redirect('index')


def registration(request):
    if request.method == 'GET':
        form = forms.RegisterForm()
        data = {
            'title': 'Registration',
            'form': form
        }
        return render(request, 'route/registration.html', data)
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        data = {
            'title': 'Registration',
            'operation_status': 'User registered successfully.'

        }
        if form.is_valid():
            form.save()
            User.objects.get(username=request.POST.get('username')).groups.add(request.POST.get('account_type'))
            return render(request, 'route/successful.html', data)
        else:
            data['operation_status'] = 'Incorrectly completed form'
            return render(request, 'route/error.html', data)


def user_info(request, username):
    try:
        active_user = request.session['_auth_user_id']
    except KeyError:
        return redirect('login')
    get_user_info = User.objects.get(username=username)
    if get_user_info.pk == int(active_user):
        data = {
            'title': 'User info',
            'user_info': get_user_info
        }
        return render(request, 'route/user_info.html', data)
    else:
        return HttpResponseNotFound('<h1>No user info</h1>')