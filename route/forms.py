from django import forms
from route import models


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
