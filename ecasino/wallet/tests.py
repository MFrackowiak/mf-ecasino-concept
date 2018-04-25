from django.test import TestCase

from player.tests import TestWithPlayerMixin
from .service import add_to_wallet, player_wallet_for_game


class WalletTestCase(TestCase, TestWithPlayerMixin):
    def test_wallet_create_signal(self):
        player = self.create_player()

        self.assertEqual(player.wallet_set.all().count(), 1)

        wallet = player.wallet_set.first()
        self.assertEqual(wallet.currency, 'EUR')
        self.assertEqual(wallet.amount, 0)

    def test_add_to_wallet_eur(self):
        player = self.create_player()

        wallet = add_to_wallet(player, 'EUR', 100)

        self.assertEqual(player.wallet_set.all().count(), 1)
        self.assertEqual(wallet.amount, 100)

    def test_add_to_wallet_usd(self):
        player = self.create_player()

        wallet = add_to_wallet(player, 'USD', 100)

        self.assertEqual(player.wallet_set.all().count(), 2)
        self.assertEqual(wallet.amount, 100)
        self.assertEqual(
            player.wallet_set.filter(currency='EUR').first().amount, 0)

    def test_wallet_for_game(self):
        player = self.create_player()

        wallet = player_wallet_for_game(player, 2)

        self.assertIsNone(wallet)

        add_to_wallet(player, 'EUR', 100)

        wallet = player_wallet_for_game(player, 2)

        self.assertGreaterEqual(wallet.amount, 2)
