"""Tests for discounts and surcharges (R4, R5, R6)."""

from decimal import Decimal

from gym_quote.discounts import (
    apply_group_discount,
    apply_special_offer,
    apply_premium_surcharge,
)


def test_apply_group_discount_two_members():
    """10% discount for 2 members."""
    assert apply_group_discount(Decimal("90"), 2) == Decimal("81.0")


def test_apply_group_discount_three_members_no_rounding():
    """10% discount for 3 members without rounding."""
    assert apply_group_discount(Decimal("135"), 3) == Decimal("121.5")


def test_apply_group_discount_one_member():
    """No discount for 1 member."""
    assert apply_group_discount(Decimal("45"), 1) == Decimal("45")
