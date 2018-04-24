from django.views.generic import TemplateView

from .models import AwardedBonus
from .service import cash_in_bonus, awarded_bonuses_available_for_cash_in


class BonusCashInView(TemplateView):
    template_name = 'bonus/cash_in.html'

    def post(self, request, *args, **kwargs):
        context = {}
        bonus_id = request.POST.get('bonus')
        if bonus_id:
            bonus = AwardedBonus.objects.get(id=bonus_id)

            if bonus.can_be_cashed_in():
                cash_in_bonus(request.user.player, bonus)
                context['bonus'] = bonus

        context.update(self.get_context_data(**kwargs))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['awarded_cashable_wallets'] = \
            awarded_bonuses_available_for_cash_in(self.request.user.player)

        return context
