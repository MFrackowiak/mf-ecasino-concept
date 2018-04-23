from django.db import models


class GamePlayed(models.Model):
    player = models.ForeignKey('player.Player', on_delete=models.PROTECT)
    funded_with_wallet = models.ForeignKey('wallet.Wallet', null=True,
                                           on_delete=models.PROTECT)
    funded_with_bonus = models.ForeignKey('bonus.AwardedBonus', null=True,
                                          on_delete=models.PROTECT)
    won = models.BooleanField(default=False)
