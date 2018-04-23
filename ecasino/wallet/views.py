from django.views.generic import TemplateView, FormView
from .forms import DepositForm
from .models import Wallet
from django.urls import reverse_lazy
from bonus.service import bonus_wallet_summary


class WalletsList(TemplateView):
    template_name = 'wallet/wallets.html'

    def get_context_data(self, **kwargs):
        return dict(
            super().get_context_data(**kwargs),
            wallets=self.request.user.player.wallet_set.all(),
            bonus_wallet=bonus_wallet_summary(self.request.user),
        )


class DepositToWallet(FormView):
    form_class = DepositForm
    template_name = 'wallet/deposit.html'
    success_url = reverse_lazy('wallet:list')

    def get_form_kwargs(self):
        return dict(
            super().get_form_kwargs(),
            wallet=Wallet.objects.get(
                player_id=self.request.user.id,
                id=self.kwargs['wallet'],
            ),
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
