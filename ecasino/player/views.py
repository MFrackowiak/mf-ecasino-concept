from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CasinoPlayerCreationForm


class RegisterView(FormView):
    form_class = CasinoPlayerCreationForm
    success_url = reverse_lazy('common:landing')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        login(request=self.request, user=form.instance)
        return super().form_valid(form)
