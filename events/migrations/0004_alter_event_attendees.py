# Generated by Django 4.2.6 on 2023-10-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, to='events.myclubuser'),
        ),
    ]
