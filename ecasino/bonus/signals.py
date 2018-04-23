from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from .models import Bonus, AwardedBonus, BONUS_ON_LOGIN


@receiver(user_logged_in)
def award_log_in_bonus(sender, request, user, **_):
    if user.is_player():
        for login_bonus in Bonus.objects.filter(
                is_active=True,
                bonus_type=BONUS_ON_LOGIN,
        ):
            if login_bonus.min_time_between_award and \
                    AwardedBonus.objects.filter(
                        player=user,
                        bonus=login_bonus,
                        awarded__gte=timezone.now() -
                                     login_bonus.min_time_between_award
                    ):
                # bonus cannot be awarded yet
                continue
            AwardedBonus.objects.create(
                player=user,
                bonus=login_bonus,
                amount=login_bonus.bonus_amount,
            )
