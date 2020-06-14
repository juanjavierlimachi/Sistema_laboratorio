# Generated by Django 3.0.3 on 2020-03-19 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0006_auto_20200318_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='Precio',
        ),
        migrations.AlterField(
            model_name='resultado',
            name='Resultado',
            field=models.FloatField(help_text='Engrese el resultado Ejem. 2.25'),
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Precio', models.FloatField()),
                ('estado', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('Cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente')),
                ('Elemento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Elemento')),
            ],
        ),
    ]
