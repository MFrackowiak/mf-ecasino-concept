from django.contrib.auth.models import AbstractUser, UserManager


class CasinoUser(AbstractUser):
    objects = UserManager()

    def is_player(self):
        return hasattr(self, 'player')
