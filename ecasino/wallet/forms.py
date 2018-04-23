from django import forms
from django.db import transaction

from .models import Deposit


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        exclude = ('timestamp', 'wallet')

    def __init__(self, *args, wallet, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    @transaction.atomic
    def save(self, commit=True):
        self.instance.wallet = self.wallet
        deposit = super().save(commit=commit)
        if commit:
            self.wallet.amount += deposit.amount
            self.wallet.save()
        return deposit
