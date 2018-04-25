from decimal import Decimal

from django.test import TestCase

from player.tests import TestWithPlayerMixin
from wallet.models import Deposit
from .models import Bonus, BONUS_ON_LOGIN, BONUS_ON_DEPOSIT, \
    AwardedBonus
from .service import bonus_wallet_summary, cash_in_bonus, \
    awarded_bonuses_available_for_cash_in


class BonusTestCase(TestCase, TestWithPlayerMixin):
    def test_login_bonus(self):
        login_bonus = Bonus.objects.create(
            bonus_type=BONUS_ON_LOGIN,
            awards_real_money=True,
            bonus_amount=20,
            wagering_requirement=10,
            is_active=True
        )

        player = self.create_player()

        self.client.login(username=self.PLAYER_USERNAME,
                          password=self.PLAYER_PASSWORD)

        self.assertEqual(player.wallet_set.first().amount, 20)
        self.assertEqual(login_bonus.awardedbonus_set.all().count(), 1)
        self.assertEqual(bonus_wallet_summary(player)['amount'],
                         Decimal('0.00'))

    def test_deposit_bonus(self):
        deposit_bonus = Bonus.objects.create(
            bonus_type=BONUS_ON_DEPOSIT,
            awards_real_money=False,
            bonus_amount=40,
            wagering_requirement=10,
            is_active=True,
            min_deposit_amount=100,
        )

        player = self.create_player()
        wallet = player.wallet_set.first()

        Deposit.objects.create(
            wallet=wallet,
            amount=50,
        )

        self.assertEqual(deposit_bonus.awardedbonus_set.count(), 0)

        Deposit.objects.create(
            wallet=wallet,
            amount=100,
        )

        self.assertEqual(deposit_bonus.awardedbonus_set.count(), 1)

        awarded_bonus = AwardedBonus.objects.filter(
            bonus=deposit_bonus,
        ).first()

        self.assertEqual(awarded_bonus.player, player)
        self.assertEqual(awarded_bonus.amount, 40)
        self.assertEqual(bonus_wallet_summary(player)['amount'], 40)

        Deposit.objects.create(
            wallet=wallet,
            amount=100,
        )

        self.assertEqual(bonus_wallet_summary(player)['amount'], 80.00)

    def test_awarded_bonus_list(self):
        deposit_bonus = Bonus.objects.create(
            bonus_type=BONUS_ON_DEPOSIT,
            awards_real_money=False,
            bonus_amount=40,
            wagering_requirement=20,
            is_active=True,
            min_deposit_amount=100,
        )
        player = self.create_player()
        wallet = player.wallet_set.first()

        for _ in range(3):
            AwardedBonus.objects.create(
                bonus=deposit_bonus,
                amount=deposit_bonus.bonus_amount,
                player=player,
            )

        self.assertEqual(awarded_bonuses_available_for_cash_in(player).count(),
                         0)

        player.money_spent_toward_bonus += 800
        player.save()

        self.assertEqual(awarded_bonuses_available_for_cash_in(player).count(),
                         3)

        player.money_spent_toward_bonus += 1200
        player.save()

        self.assertEqual(awarded_bonuses_available_for_cash_in(player).count(),
                         3)

        for i in range(2):
            cash_in_bonus(player, AwardedBonus.objects.filter(
                player=player).first())
            wallet.refresh_from_db()
            self.assertEqual(wallet.amount, (i + 1) * 40)

        self.assertEqual(awarded_bonuses_available_for_cash_in(player).count(),
                         0)
        player.refresh_from_db()
        self.assertEqual(player.money_spent_toward_bonus, 400)
