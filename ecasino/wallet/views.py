from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from bonus.service import bonus_wallet_summary, \
    awarded_bonuses_available_for_cash_in
from common.decorators import player_required
from .forms import DepositForm
from .models import Wallet


@method_decorator(player_required, name='dispatch')
class WalletsList(TemplateView):
    template_name = 'wallet/wallets.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_player():
            return HttpResponseBadRequest('Only players can access this view.')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return dict(
            super().get_context_data(**kwargs),
            wallets=self.request.user.player.wallet_set.all(),
            bonus_wallet=bonus_wallet_summary(self.request.user),
            can_cash_in_bonus=awarded_bonuses_available_for_cash_in(
                self.request.user.player).exists(),
        )


@method_decorator(player_required, name='dispatch')
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
