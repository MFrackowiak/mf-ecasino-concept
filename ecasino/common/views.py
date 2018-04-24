from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy


class LandingView(TemplateView):
    template_name = 'common/landing.html'


class CasinoLogoutView(LogoutView):
    next_page = reverse_lazy('common:landing')


class CasinoLoginView(LoginView):
    redirect_authenticated_user = True
