from route import views, models, forms
from route.test.setup_file import Setting


class RouteFormTestCase(Setting):
    def test_forms_valid(self):
        form_data = {
            'id_route': self.test_route,
            'event_admin': 1,
            'start_date': '2023-05-10',
            'price': 5000
        }
        form = forms.EventForm(data=form_data)
        self.assertFalse(form.is_valid())


