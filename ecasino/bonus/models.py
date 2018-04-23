from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from common.fields import MoneyField


BONUS_ON_LOGIN = 1
BONUS_ON_DEPOSIT = 2


BONUS_TYPE_CHOICES = (
    (BONUS_ON_LOGIN, 'Bonus awarded on login to the application.'),
    (BONUS_ON_DEPOSIT, 'Bonus awarded when user deposits money on account.'),
)


class Bonus(models.Model):
    bonus_type = models.IntegerField(choices=BONUS_TYPE_CHOICES)
    bonus_amount = MoneyField()
    is_active = models.BooleanField()
    wagering_requirement = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(100)),
    )
    min_time_between_award = models.DurationField(null=True)
    min_deposit_amount = MoneyField(default=0)


class AwardedBonus(models.Model):
    bonus = models.ForeignKey(Bonus, on_delete=models.PROTECT)
    player = models.ForeignKey('player.Player', on_delete=models.PROTECT)
    awarded = models.DateTimeField(default=timezone.now)
    money_spent = MoneyField(default=0)
    amount = MoneyField()
