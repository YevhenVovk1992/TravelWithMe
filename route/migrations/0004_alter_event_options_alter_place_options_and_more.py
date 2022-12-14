# Generated by Django 4.1.1 on 2022-10-23 08:42

import django.core.validators
from django.db import migrations, models
import utils.Validators


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0003_rename_approved_users_event_event_users_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date'], 'verbose_name': 'Event', 'verbose_name_plural': 'Travel event'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ['name'], 'verbose_name': 'Route place', 'verbose_name_plural': 'Route place'},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['id'], 'verbose_name': 'Route', 'verbose_name_plural': 'Travel route'},
        ),
        migrations.AlterModelOptions(
            name='routereview',
            options={'ordering': ['id', 'rating'], 'verbose_name': 'Route review', 'verbose_name_plural': 'Route review'},
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Price must be greater then 0')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(validators=[utils.Validators.DateValidator.data_validate]),
        ),
    ]
