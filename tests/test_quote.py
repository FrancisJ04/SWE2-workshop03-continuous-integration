"""Tests for the quote pipeline and its breakdown (R7)."""
from decimal import Decimal

from gym_quote.quote import Breakdown, calculate, quote


def test_breakdown_of_premium_group_quote():
    """Each step is reported, and only the total is rounded."""
    assert calculate("PREMIUM", ["GROUP_CLASSES", "SPA"], 2) == Breakdown(
        subtotal=Decimal(230),
        group_discount=Decimal(23),
        special_offer=Decimal(20),
        surcharge=Decimal("28.05"),
        total=215,
    )


def test_invalid_selection_has_no_breakdown():
    """An invalid selection returns None instead of a breakdown."""
    assert calculate("BASIC", ["SPA"], 1) is None


def test_invalid_selection_quotes_minus_one():
    """R7: an invalid selection gives -1."""
    assert quote("GOLD", [], 1) == -1


def test_names_are_case_and_space_insensitive():
    """Plan and extras are normalised before validating."""
    assert quote("basic", [" group_classes "], 2) == 81


def test_repeated_extra_counts_once():
    """A repeated extra is charged once: (70 + 30) x 1.15 = 115."""
    assert quote("PREMIUM", ["SPA", "SPA"], 1) == 115
