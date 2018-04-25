from django.db import models

from common.fields import MoneyField


class Wallet(models.Model):
    player = models.ForeignKey('player.Player', on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, default='EUR')
    amount = MoneyField(default=0)


class Deposit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    amount = MoneyField()
