from django.urls import path
from .views import BonusCashInView


app_name = 'bonus'
urlpatterns = [
    path('cash-in/', BonusCashInView.as_view(), name='cash_in'),
]
