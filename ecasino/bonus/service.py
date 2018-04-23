from .models import AwardedBonus
from django.db.models import Sum


def bonus_wallet_summary(player):
    return dict(
        amount=AwardedBonus.objects.filter(
            player=player,
            cashed_in=False,
        ).aggregate(
            s=Sum('amount'),
        )['s'] or '0.00',
    )
