# Generated by Django 2.2.1 on 2019-05-13 21:13

from django.db import migrations, models
import django.utils.timezone
import forexer.trade.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.CharField(default=forexer.trade.models.create_unique_pk, max_length=9, primary_key=True, serialize=False)),
                ('sell_currency', models.CharField(default='USD', max_length=3)),
                ('sell_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('buy_currency', models.CharField(default=0, max_length=3)),
                ('buy_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=4, default=0, max_digits=12)),
                ('date_booked', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
