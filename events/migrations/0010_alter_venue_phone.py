# Generated by Django 3.2.7 on 2022-01-13 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_venue_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.IntegerField(verbose_name='Contact Phone'),
        ),
    ]