from django.contrib.auth.views import LoginView
from django.urls import path

from .views import LandingView, CasinoLogoutView

app_name = 'common'
urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', CasinoLogoutView.as_view(), name='logout'),
]
