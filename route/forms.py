from django import forms
from django.db.models import Count

from route import models
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class ChoiceTypeAccount:
    try:
        _CHOICES_LIST = [(itm.pk, itm.name.capitalize) for itm in Group.objects.all()]
        _CHOICES_LIST_LOCATION = [(itm["location"], itm["location"].capitalize) for i, itm in enumerate(
            models.Route.objects.values('location').annotate(count=Count('location')).order_by()
        )]
        _CHOICES_LIST_COUNTRY = [(itm["country"], itm["country"].capitalize) for i, itm in enumerate(
            models.Route.objects.values('country').annotate(count=Count('country')).order_by()
        )]
    except:
        _CHOICES_LIST = []
        _CHOICES_LIST_LOCATION = []
        _CHOICES_LIST_COUNTRY = []

    @classmethod
    def choices_type(cls):
        return cls._CHOICES_LIST

    @classmethod
    def choices_location(cls):
        return cls._CHOICES_LIST_LOCATION

    @classmethod
    def choices_country(cls):
        return cls._CHOICES_LIST_COUNTRY


class EventForm(forms.ModelForm):
    id_route = forms.ModelMultipleChoiceField(queryset=models.Route.objects.all(), label='Route')
    event_admin = forms.IntegerField(label='Event admin')
    start_date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    price = forms.IntegerField(label='Price')

    class Meta:
        model = models.Event
        fields = ('id_route', 'event_admin', 'start_date', 'price')


class RouteForm(forms.ModelForm):
    start_point = forms.ModelChoiceField(queryset=models.Place.objects.all(), label='Start place')
    destination = forms.ModelChoiceField(queryset=models.Place.objects.all(), label='Finish place')
    route_type = forms.ChoiceField(choices=models.Route.RouteType.choices)
    country = forms.CharField(max_length=50, label='Country')
    location = forms.CharField(max_length=50, label='Location')
    description = forms.CharField(widget=forms.Textarea)
    stop_points = forms.CharField(
        widget=forms.Textarea,
        initial="""
            [{
                "name": "point1", 
                "lat": "000.0000", 
                "lon": "000.0000"
            }, {
                "name": "point2", 
                "lat": "000.0000", 
                "lon": "000.0000"
            }]"""
    )
    duration = forms.IntegerField()

    class Meta:
        model = models.Event
        fields = ('start_point', 'destination', 'route_type', 'country', 'location', 'description', 'duration')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    account_type = forms.ChoiceField(widget=forms.Select(), choices=ChoiceTypeAccount.choices_type())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class UserLogin(forms.Form):
    username = forms.CharField(max_length=120, label='Name')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class RouteFilter(forms.Form):
    route_type = forms.ChoiceField(choices=models.Route.RouteType.choices)
    location = forms.ChoiceField(choices=ChoiceTypeAccount.choices_location())
    country = forms.ChoiceField(widget=forms.Select(), choices=ChoiceTypeAccount.choices_country())


class ChangeUserToPending(forms.Form):
    users_to_pending = forms.MultipleChoiceField(label='Users', choices=[])
    users_to_pending_status = forms.MultipleChoiceField(
        label='Status', choices=[(0, 'to approved'), (1, 'to pending'), (2, 'delete')]
    )

    def __init__(self, users_dict=None, *args, **kwargs):
        super(ChangeUserToPending, self).__init__(*args, **kwargs)
        if users_dict:
            self.fields['users_to_pending'].choices = list(users_dict.items())


class ChangeUserToApproved(forms.Form):
    users_to_approved = forms.MultipleChoiceField(label='Users', choices=[])
    users_to_approved_status = forms.MultipleChoiceField(
        label='Status', choices=[(1, 'to approved'), (0, 'to pending'), (2, 'delete')]
    )

    def __init__(self, users_dict=None, *args, **kwargs):
        super(ChangeUserToApproved, self).__init__(*args, **kwargs)
        if users_dict:
            self.fields['users_to_approved'].choices = list(users_dict.items())