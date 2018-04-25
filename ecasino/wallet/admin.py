from django.contrib import admin

from .models import Wallet, Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass
