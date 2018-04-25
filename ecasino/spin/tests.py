from django.test import TestCase

from player.tests import TestWithPlayerMixin
from .consts import SPIN_SINGLE_GAME_COST, SPIN_SINGLE_GAME_WIN
from .models import GamePlayed
from .service import play_spin


class SpinTestCase(TestCase, TestWithPlayerMixin):
    def test_counting_money_spent(self):
        player = self.create_player()
        wallet = player.wallet_set.first()
        wallet.amount = 500
        wallet.save()

        for _ in range(250):
            play_spin(player)

        player.refresh_from_db()
        wallet.refresh_from_db()
        self.assertEqual(player.money_spent_toward_bonus, 500)
        self.assertEqual(
            wallet.amount,
            GamePlayed.objects.filter(
                won=True,
            ).count() * (SPIN_SINGLE_GAME_COST + SPIN_SINGLE_GAME_WIN))
