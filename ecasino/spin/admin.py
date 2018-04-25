from django.contrib import admin

from .models import GamePlayed


@admin.register(GamePlayed)
class GamePlayedAdmin(admin.ModelAdmin):
    pass
