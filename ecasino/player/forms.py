from django.contrib.auth.forms import UserCreationForm
from .models import Player


class CasinoPlayerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Player
