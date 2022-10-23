from django.utils import timezone
from django.core import exceptions


class DateValidator:

    @staticmethod
    def data_validate(date: str):
        now_date = timezone.now().date()
        if date <= now_date:
            raise exceptions.ValidationError('Enter correct date')

