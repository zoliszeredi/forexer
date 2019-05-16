import hashlib

import django.utils.timezone
from django.db import models


def create_unique_pk(when=None, algo='md5', digits=7):
    "Attempts to unique string by hashing the datetime"
    now = when or django.utils.timezone.now()
    data = bytes(now.isoformat(), 'utf-8')
    hashval = hashlib.new(name=algo, data=data).hexdigest()
    output_fmt = 'TR{}'
    result = output_fmt.format(hashval[:digits]).upper()
    return result


class Trade(models.Model):
    id = models.CharField(max_length=9,
                          default=create_unique_pk,
                          primary_key=True,
                          editable=False)
    sell_currency = models.CharField(max_length=3,
                                     default='EUR', null=False)
    sell_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                      default=0, null=False)
    buy_currency = models.CharField(max_length=3,
                                    default='USD', null=False)
    buy_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                     default=0, null=False, editable=False)
    rate = models.DecimalField(max_digits=12, decimal_places=4,
                               default=0, null=False, editable=False)
    date_booked = models.DateTimeField(default=django.utils.timezone.now,
                                       editable=False)

    class Meta:
        ordering = ['-date_booked']
