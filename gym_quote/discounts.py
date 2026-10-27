"""Module for calculating discounts and surcharges (R4, R5, R6)."""

from decimal import Decimal

GROUP_DISCOUNT_RATE = Decimal("0.90")
PREMIUM_SURCHARGE_RATE = Decimal("1.15")


def apply_group_discount(amount: Decimal, members: int) -> Decimal:
    """Apply a 10% discount if there are 2 or more members (R4)."""
    if members >= 2:
        return amount * GROUP_DISCOUNT_RATE
    return amount


def apply_special_offer(amount: Decimal) -> Decimal:
    """Apply the exclusive special offer based on the amount (R5)."""
    if amount > Decimal("400"):
        return amount - Decimal("50")
    if amount > Decimal("200"):
        return amount - Decimal("20")
    return amount
