# Generated by Django 3.0.3 on 2020-07-18 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_auto_20200717_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='precio',
            name='Antimonio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='precio',
            name='Arsenico',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='precio',
            name='Hierro',
            field=models.FloatField(blank=True, null=True),
        ),
    ]