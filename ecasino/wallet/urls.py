from django.urls import path
from .views import WalletsList, DepositToWallet


app_name = 'wallet'
urlpatterns = [
    path('', WalletsList.as_view(), name='list'),
    path('<int:wallet>/deposit/', DepositToWallet.as_view(), name='deposit'),
]
