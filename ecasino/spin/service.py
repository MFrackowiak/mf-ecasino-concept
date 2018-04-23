from collections import namedtuple
from random import random
from django.db import transaction
from .consts import SPIN_WIN_CHANCE


GameResult = namedtuple(
    'GameResult',
    ['result', ]
)


class SpinGameError(Exception):
    pass


@transaction.atomic
def play_spin(player):
    won = random() > SPIN_WIN_CHANCE
    pass
