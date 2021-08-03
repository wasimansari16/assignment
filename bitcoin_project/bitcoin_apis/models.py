# Create your models here.
from django.db import models

class BitCoinExchangeRate(models.Model):
    from_currency_name = models.CharField(max_length=20)
    to_currency_name = models.CharField(max_length=20)
    exchange_rate = models.FloatField()
    last_updates_ts = models.DateTimeField()
    time_zone = models.CharField(max_length=8)