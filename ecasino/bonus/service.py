from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from wallet.service import add_to_wallet
from .models import AwardedBonus


def bonus_wallet_summary(player):
    return dict(
        amount=AwardedBonus.objects.filter(
            player=player,
            cashed_in=False,
            bonus__awards_real_money=False,
        ).aggregate(
            s=Sum('amount'),
        )['s'] or Decimal('0.00'),
    )


def bonus_wallet_first_bonus(player, min_amount):
    return AwardedBonus.objects.filter(
        player=player,
        cashed_in=False,
        amount__gte=min_amount,
        bonus__awards_real_money=False,
    ).first()


def awarded_bonuses_available_for_cash_in(player):
    return AwardedBonus.objects.filter(
        player=player,
        cashed_in=False,
        bonus__awards_real_money=False,
    ).annotate(
        wagering_amount=ExpressionWrapper(
            F('amount') * F('bonus__wagering_requirement'),
            output_field=DecimalField()),
    ).filter(
        wagering_amount__lte=player.money_spent_toward_bonus,
    )


@transaction.atomic
def cash_in_bonus(player, awarded_bonus):
    wagered_amount = awarded_bonus.amount * \
                     awarded_bonus.bonus.wagering_requirement
    if wagered_amount > player.money_spent_toward_bonus:
        raise ValueError('Cannot be cashed in.')

    player.money_spent_toward_bonus -= wagered_amount
    awarded_bonus.cashed_in = True
    add_to_wallet(player, awarded_bonus.bonus.currency, awarded_bonus.amount)

    player.save()
    awarded_bonus.save()

    return awarded_bonus
