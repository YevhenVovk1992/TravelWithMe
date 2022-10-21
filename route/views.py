import json

from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User, Group


from route import forms
from route import models
from utils.MongoDBConnect import MongoConnect, CONNECTION_STRING, CONNECTION_DB


# Create your views here.

def index(request):
    if request.method == 'GET':
        form = forms.RouteFilter()
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
            'countries': countries,
            'form': form
        }
        return render(request, 'route/index.html', data)
    else:
        form = forms.RouteFilter(request.POST)
        if form.is_valid():
            route_type = form.cleaned_data['route_type']
            country = form.cleaned_data['country']
            location = form.cleaned_data['location']
            return redirect('route:route_filter', route_type=route_type, country=country, location=location)


def route_filter(request, **kwargs):
    route_list = models.Route.objects.filter(**kwargs).all()
    data = {
        'title': 'Routes',
        'route_list': [itm.to_dict() for itm in route_list]
    }
    return render(request, 'route/route_filter.html', data)


@login_required(login_url='login')
def add_route(request):
    """
        Function to add route if the user is registered and has permissions
    :param request:
    :return: HTML with Django form
    """
    if request.user.has_perm('route.add_route'):
        if request.method == 'GET':
            form = forms.RouteForm()
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
            stop_point_data = json.loads(request.POST.get('stop_points'))
            try:
                with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
                    id_stop_points = db['stop_points'].insert_one({'points': stop_point_data}).inserted_id
                new_route = models.Route(
                    start_point=models.Place.objects.filter(id=request.POST.get('start_point'))[0],
                    destination=models.Place.objects.filter(id=request.POST.get('destination'))[0],
                    stop_point=id_stop_points,
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


def route_detail(request, id_route: int):
    """
        Show detail information about route
    :param request:
    :param id_route: id route from DB
    :return: HTML page
    """
    get_route = models.Route.objects.filter(pk=id_route).first()
    get_events = models.Event.objects.filter(id_route=id_route).all()
    get_review = models.RouteReview.objects.filter(id_route=id_route).all()

    # Get an average rating
    get_avg_rating = models.RouteReview.objects.values('id_route').filter(id_route=id_route).annotate(avg=Avg('rating'))
    avg_rating = get_avg_rating[0]['avg'] if len(get_avg_rating) > 0 else 'No rating'

    # With stop points id get info about stop points from MongoDB
    with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
        get_collection = db['stop_points']
        stop_points = get_collection.find_one({'_id': ObjectId(get_route.stop_point)}).get('points')
    data = {
        'title': 'Info',
        'route': get_route,
        'events': get_events,
        'get_review': get_review,
        'avg_rating': avg_rating,
        'stop_points': stop_points
    }
    return render(request, 'route/route_detail.html', data)


def route_review(request, id_route: int):
    """
        Reviews and evaluation of the route
    :param request:
    :param id_route: id route from DB
    :return: HTML page
    """
    if request.method == 'GET':
        get_reviews = models.RouteReview.objects.filter(id_route=id_route).all()
        data = {
            'title': 'Reviews',
            'reviews': get_reviews
        }
        return render(request, 'route/route_review.html', data)


@login_required(login_url='login')
def route_add_event(request, id_route: int):
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
def event_handler(request, event_id: int):
    """
        Output information about the event if the user is logged in
    :param request:
    :param event_id: event id from DB
    :return: HTML page
    """
    if request.user.has_perm('route.view_event'):
        get_event = models.Event.objects.filter(pk=event_id).annotate(
            guide=Subquery(User.objects.filter(pk=OuterRef('event_admin')).values('username'))
        ).first()

        # Get id users from MongoDB use id of the string from event table
        with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
            get_collection = db['event_users']
            id_event_users = get_collection.find_one({'_id': ObjectId(get_event.event_users)})

            # Add to the event model new parameters
            if id_event_users is None:
                get_event.approved_users = ['No approved users']
                get_event.pending_users = ['No pending users']
            else:
                approved_users = User.objects.filter(pk__in=id_event_users.get('approved_users')).all()
                pending_users = User.objects.filter(pk__in=id_event_users.get('pending_users')).all()
                get_event.approved_users = [itm.username for itm in approved_users]
                get_event.pending_users = [itm.username for itm in pending_users]
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


@login_required(login_url='login')
def add_me_to_event(request, event_id: int):
    """
        Adding users to the event
    :param request:
    :param event_id: id event
    :return: HTTP page
    """
    if request.user.has_perm('route.view_event'):
        id_user = request.user.pk
        event = models.Event.objects.filter(pk=event_id).first()
        with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
            get_collection = db['event_users']
            event_users = get_collection.find_one({'_id': ObjectId(event.event_users)})
            pending_users = event_users.get('pending_users') if event_users is not None else []
            approved_users = event_users.get('approved_users') if event_users is not None else []

            # Checking if the user has applied
            if id_user in approved_users or id_user in pending_users:
                data = {
                    'title': 'New pending user',
                    'operation_status': 'You have already applied!'
                }
                return render(request, 'route/error.html', data)
            else:
                pending_users.append(id_user)

                # Update the record if it exists in the database. If not, create a new one
                if event_users is not None:
                    get_collection.update_one(
                        {'_id': ObjectId(event.event_users)}, {'$set': {'pending_users': pending_users}}
                    )
                else:
                    id_collection = get_collection.insert_one(
                        {'approved_users': approved_users, 'pending_users': pending_users}
                    ).inserted_id
                    event.event_users = id_collection
                    event.save()
        data = {
            'title': 'New pending user',
            'operation_status': f'You have applied for participation in the tour along the route {event.id_route.pk}'
        }
        return render(request, 'route/successful.html', data)


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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def user_to_approved(request, event_id: int):
    if request.user.is_superuser:
        event = models.Event.objects.filter(pk=event_id).first()
        with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
            get_collection = db['event_users']
            event_users = get_collection.find_one({'_id': ObjectId(event.event_users)})
            id_pending_users = event_users.get('pending_users') if event_users is not None else []
            id_approved_users = event_users.get('approved_users') if event_users is not None else []
        pending_users = User.objects.in_bulk(id_pending_users)
        approved_users = User.objects.in_bulk(id_approved_users)
        if request.method == 'GET':
            form_pending = forms.ChangeUserToApproved(users_dict=pending_users)
            form_approved = forms.ChangeUserToPending(users_dict=approved_users)
            data = {
                'title': 'Event users',
                'approved_users': approved_users,
                'form_pending': form_pending,
                'form_approved': form_approved
            }
            return render(request, 'route/pending_user_to_approved.html', data)
        if request.method == 'POST':
            users_to_approved = request.POST.get('users_to_approved')
            users_to_approved_status = request.POST.get('users_to_approved_status')
            users_to_pending = request.POST.get('users_to_pending')
            users_to_pending_status = request.POST.get('users_to_pending_status')

            # Perform operations according to the condition
            if users_to_approved and users_to_approved_status[0] == '1':
                id_pending_users.remove(int(users_to_approved))
                id_approved_users.append(int(users_to_approved))
            elif users_to_pending and users_to_pending_status[0] == '1':
                id_pending_users.append(int(users_to_pending))
                id_approved_users.remove(int(users_to_pending))
            elif users_to_approved and users_to_approved_status[0] == '2':
                id_pending_users.remove(int(users_to_approved))
            elif users_to_pending and users_to_pending_status[0] == '2':
                id_approved_users.remove(int(users_to_pending))
            with MongoConnect(CONNECTION_STRING, CONNECTION_DB) as db:
                get_collection = db['event_users']
                get_collection.update_one(
                    {'_id': ObjectId(event.event_users)}, {'$set': {'pending_users': id_pending_users, 'approved_users': id_approved_users}}
                )
            return redirect(user_to_approved, event_id=event_id)
    else:
        return HttpResponseNotFound('<h1>No access</h1>')
