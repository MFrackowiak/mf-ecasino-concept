from collections import namedtuple
from random import random

from django.db import transaction

from bonus.service import bonus_wallet_first_bonus
from wallet.service import player_wallet_for_game
from .consts import SPIN_WIN_CHANCE, SPIN_SINGLE_GAME_COST, SPIN_SINGLE_GAME_WIN
from .models import GamePlayed


class SpinGameError(Exception):
    pass


@transaction.atomic
def play_spin(player):
    funding_wallet = player_wallet_for_game(player, SPIN_SINGLE_GAME_COST)
    funding_bonus = None if funding_wallet else bonus_wallet_first_bonus(
        player, SPIN_SINGLE_GAME_COST)

    if not (funding_bonus or funding_wallet):
        raise SpinGameError('You don\'t have enough funds.')

    (funding_wallet or funding_bonus).amount -= SPIN_SINGLE_GAME_COST
    (funding_wallet or funding_bonus).save()
    player.money_spent_toward_bonus += SPIN_SINGLE_GAME_COST
    player.save()

    won = random() > SPIN_WIN_CHANCE

    game = GamePlayed.objects.create(
        won=won,
        funded_with_wallet=funding_wallet,
        funded_with_bonus=funding_bonus,
        player=player,
    )

    if won:
        (funding_wallet or funding_bonus).amount += SPIN_SINGLE_GAME_COST + \
                                                    SPIN_SINGLE_GAME_WIN
        (funding_wallet or funding_bonus).save()

    return game
