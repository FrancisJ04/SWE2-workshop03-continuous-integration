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


def test_apply_special_offer_above_400():
    """Amount > 400 subtracts 50."""
    assert apply_special_offer(Decimal("450")) == Decimal("400")


def test_apply_special_offer_exactly_401():
    """Boundary test: 401 subtracts 50."""
    assert apply_special_offer(Decimal("401")) == Decimal("351")


def test_apply_special_offer_exactly_400():
    """Boundary test: 400 is not > 400, so subtracts 20."""
    assert apply_special_offer(Decimal("400")) == Decimal("380")


def test_apply_special_offer_between_200_and_400():
    """Amount between 200 and 400 subtracts 20."""
    assert apply_special_offer(Decimal("300")) == Decimal("280")


def test_apply_special_offer_exactly_201():
    """Boundary test: 201 subtracts 20."""
    assert apply_special_offer(Decimal("201")) == Decimal("181")


def test_apply_special_offer_exactly_200():
    """Boundary test: 200 is not > 200, so no subtraction."""
    assert apply_special_offer(Decimal("200")) == Decimal("200")


def test_apply_special_offer_below_200():
    """Amount below 200 has no offer."""
    assert apply_special_offer(Decimal("150")) == Decimal("150")
