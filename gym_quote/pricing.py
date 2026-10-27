"""Subtotal (R3) and final rounding (R7)."""
from decimal import Decimal, ROUND_HALF_UP

from gym_quote.catalog import EXTRAS, PLANS


def subtotal(plan, extras, members):
    """Return (plan price + price of the extras) x number of members.

    The selection must already be valid.
    """
    price_per_member = PLANS[plan] + sum(EXTRAS[extra] for extra in extras)
    return Decimal(price_per_member) * members


def round_half_up(amount):
    """Round the amount half up to a whole number (2.5 -> 3), unlike Python's round()."""
    return int(Decimal(amount).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
