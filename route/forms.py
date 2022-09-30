from django import forms
from route import models


class EventForm(forms.ModelForm):

    id_route = forms.ModelMultipleChoiceField(queryset=models.Route.objects.all())
    event_admin = forms.IntegerField(label='event_admin')
    start_date = forms.DateField()
    price = forms.IntegerField(label='Price')

    class Meta:
        model = models.Event
        fields = ('id_route', 'event_admin', 'start_date', 'price')


class RouteForm(forms.ModelForm):

    start_point = forms.ModelChoiceField(queryset=models.Place.objects.all(), label='start place')
    destination = forms.ModelChoiceField(queryset=models.Place.objects.all(), label='finish place')
    route_type = forms.ChoiceField(choices=models.Route.RouteType.choices)
    country = forms.CharField(max_length=50, label='country')
    location = forms.CharField(max_length=50, label='location')
    description = forms.CharField(widget=forms.Textarea)
    duration = forms.IntegerField()

    class Meta:
        model = models.Event
        fields = ('start_point', 'destination', 'route_type', 'country', 'location', 'description', 'duration')
