from django.urls import path

from .views import RegisterView

app_name = 'player'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
]
