from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import Deposit
from wallet.service import add_to_wallet
from .models import Bonus, AwardedBonus, BONUS_ON_LOGIN, BONUS_ON_DEPOSIT


@receiver(user_logged_in)
def award_log_in_bonus(sender, request, user, **_):
    if user.is_player():
        for login_bonus in Bonus.objects.filter(
                is_active=True,
                bonus_type=BONUS_ON_LOGIN,
        ):
            if login_bonus.can_be_awarded_to(user):
                AwardedBonus.objects.create(
                    player=user.player,
                    bonus=login_bonus,
                    amount=login_bonus.bonus_amount,
                )
                if login_bonus.awards_real_money:
                    add_to_wallet(user.player, login_bonus.currency,
                                  login_bonus.bonus_amount)


@receiver(post_save, sender=Deposit)
def award_deposit_bonus(sender, instance, created, **_):
    player = instance.wallet.player
    if created:
        for deposit_bonus in Bonus.objects.filter(
                min_deposit_amount__lte=instance.amount,
                is_active=True,
                bonus_type=BONUS_ON_DEPOSIT,
        ):
            if deposit_bonus.can_be_awarded_to(player):
                AwardedBonus.objects.create(
                    player=player,
                    bonus=deposit_bonus,
                    amount=deposit_bonus.bonus_amount,
                    awarded_for=instance,
                )
                if deposit_bonus.awards_real_money:
                    add_to_wallet(player, deposit_bonus.currency,
                                  deposit_bonus.bonus_amount)
