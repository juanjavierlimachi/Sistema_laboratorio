# Generated by Django 3.0.3 on 2020-03-16 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_elemento_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Precio',
            field=models.FloatField(default='1'),
            preserve_default=False,
        ),
    ]
