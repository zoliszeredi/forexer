# Generated by Django 2.2.1 on 2019-05-13 21:27

from django.db import migrations, models
import django.utils.timezone
import forexer.trade.models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trade',
            options={'ordering': ['-date_booked']},
        ),
        migrations.AlterField(
            model_name='trade',
            name='buy_currency',
            field=models.CharField(default='USD', max_length=3),
        ),
        migrations.AlterField(
            model_name='trade',
            name='date_booked',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='trade',
            name='id',
            field=models.CharField(default=forexer.trade.models.create_unique_pk, editable=False, max_length=9, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='trade',
            name='rate',
            field=models.DecimalField(decimal_places=4, default=0, editable=False, max_digits=12),
        ),
    ]
