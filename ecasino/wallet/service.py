from .models import Wallet


def player_wallet_for_game(player, min_amount):
    return Wallet.objects.filter(
        amount__gte=min_amount,
        player=player,
    ).first()


def add_to_wallet(player, currency, amount):
    wallet, _ = Wallet.objects.get_or_create(
        player=player,
        currency=currency,
    )
    wallet.amount += amount
    wallet.save()
    return wallet
