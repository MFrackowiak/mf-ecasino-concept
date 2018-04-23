from player.models import Player
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet


@receiver(post_save, sender=Player)
def create_default_wallet(sender, instance, created, **_):
    if created:
        Wallet.objects.create(
            player=instance,
        )
