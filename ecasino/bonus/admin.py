from django.contrib import admin
from .models import AwardedBonus, Bonus


@admin.register(AwardedBonus)
class AwardedBonusAdmin(admin.ModelAdmin):
    pass


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    pass
