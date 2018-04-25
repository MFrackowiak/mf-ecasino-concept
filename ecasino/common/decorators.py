from django.contrib.auth.decorators import user_passes_test


def player_required(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_player(),
    )
    if func:
        return actual_decorator(func)
    return actual_decorator
