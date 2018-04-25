from player.models import Player


class TestWithPlayerMixin:
    PLAYER_USERNAME = 'test_1'
    PLAYER_PASSWORD = 'test1234'

    def create_player(self):
        return Player.objects.create_user(
            username=self.PLAYER_USERNAME,
            password=self.PLAYER_PASSWORD,
        )
