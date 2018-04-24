from django.urls import path

from .views import PlaySpinsView

app_name = 'spin'
urlpatterns = [
    path('play/', PlaySpinsView.as_view(), name='game'),
]
