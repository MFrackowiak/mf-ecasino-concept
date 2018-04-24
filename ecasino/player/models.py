from common.fields import MoneyField
from common.models import CasinoUser


class Player(CasinoUser):
    money_spent_toward_bonus = MoneyField(default=0)
