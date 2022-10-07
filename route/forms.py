from django import forms
from route import models
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    duration = forms.IntegerField()

    class Meta:
        model = models.Event
        fields = ('start_point', 'destination', 'route_type', 'country', 'location', 'description', 'duration')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class UserLogin(forms.Form):
    username = forms.CharField(max_length=120, label='Name')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
