from django.db.models.fields import DecimalField


class MoneyField(DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=10,
                 decimal_places=2, **kwargs):
        super().__init__(verbose_name, name, max_digits, decimal_places,
                         **kwargs)
