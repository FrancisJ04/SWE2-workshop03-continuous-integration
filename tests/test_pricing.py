"""Tests for the subtotal (R3) and the half-up rounding (R7)."""
from decimal import Decimal

import pytest

from gym_quote.pricing import round_half_up, subtotal


@pytest.mark.parametrize(
    "plan, extras, members, expected",
    [
        ("BASIC", [], 1, Decimal(30)),
        ("BASIC", ["GROUP_CLASSES"], 3, Decimal(135)),
        ("STANDARD", ["GROUP_CLASSES", "PERSONAL_TRAINING"], 4, Decimal(340)),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, Decimal(420)),
    ],
)
def test_subtotal(plan, extras, members, expected):
    """R3: subtotal = (plan price + price of the extras) x number of members."""
    assert subtotal(plan, extras, members) == expected


@pytest.mark.parametrize(
    "amount, expected",
    [
        (Decimal("121.5"), 122),
        (Decimal("2.5"), 3),
        (Decimal("215.05"), 215),
        (Decimal("411.7"), 412),
        (Decimal("625.6"), 626),
        (Decimal("0.49"), 0),
    ],
)
def test_round_half_up(amount, expected):
    """R7: the total is rounded half up to a whole number."""
    assert round_half_up(amount) == expected


def test_round_half_up_differs_from_builtin_round():
    """Python's round() rounds 2.5 to 2 (banker's rounding); R7 needs 3."""
    assert round(2.5) == 2
    assert round_half_up(Decimal("2.5")) == 3
