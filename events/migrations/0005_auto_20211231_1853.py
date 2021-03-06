# Generated by Django 3.2.7 on 2021-12-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Event Name'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Venue Name'),
        ),
    ]
