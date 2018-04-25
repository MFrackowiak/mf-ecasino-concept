from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

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
    awards_real_money = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, default='EUR')

    def can_be_awarded_to(self, user):
        return not (
                self.min_time_between_award and
                AwardedBonus.objects.filter(
                    player=user,
                    bonus=self,
                    awarded__gte=timezone.now() -
                                 self.min_time_between_award
                ).exists()
        )


class AwardedBonus(models.Model):
    bonus = models.ForeignKey(Bonus, on_delete=models.PROTECT)
    player = models.ForeignKey('player.Player', on_delete=models.PROTECT)
    awarded = models.DateTimeField(default=timezone.now)
    amount = MoneyField()
    awarded_for = models.ForeignKey('wallet.Deposit', null=True,
                                    on_delete=models.PROTECT)
    cashed_in = models.BooleanField(default=False)

    def can_be_cashed_in(self):
        if self.cashed_in or self.bonus.awards_real_money:
            return False
        return self.amount * self.bonus.wagering_requirement <= \
               self.player.money_spent_toward_bonus
