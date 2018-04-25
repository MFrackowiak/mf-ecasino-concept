from django.contrib import admin

from .models import CasinoUser


@admin.register(CasinoUser)
class CasinoUserAdmin(admin.ModelAdmin):
    pass
