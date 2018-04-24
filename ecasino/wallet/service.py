from .models import Wallet


def player_wallet_for_game(player, min_amount):
    return Wallet.objects.filter(
        amount__gte=min_amount,
        player=player,
    ).first()
