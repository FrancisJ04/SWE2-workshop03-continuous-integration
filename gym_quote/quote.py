"""Quote calculation pipeline (R7): validation, R3 to R6 in order, and the final rounding.

This module does no input or output.
"""
from dataclasses import dataclass
from decimal import Decimal

from gym_quote import catalog, discounts, pricing

INVALID = -1


@dataclass(frozen=True)
class Breakdown:
    """Amounts of each step of a quote; discounts and surcharge are positive amounts."""

    subtotal: Decimal
    group_discount: Decimal
    special_offer: Decimal
    surcharge: Decimal
    total: int


def calculate(plan, extras, members):
    """Return the Breakdown of the quote, or None if the selection is invalid."""
    plan = plan.strip().upper()
    extras = catalog.normalize(extras)
    if not catalog.is_valid_selection(plan, extras, members):
        return None

    base = pricing.subtotal(plan, extras, members)
    after_group = discounts.apply_group_discount(base, members)
    after_offer = discounts.apply_special_offer(after_group)
    after_surcharge = discounts.apply_premium_surcharge(
        after_offer, catalog.has_premium_extra(extras)
    )
    return Breakdown(
        subtotal=base,
        group_discount=base - after_group,
        special_offer=after_group - after_offer,
        surcharge=after_surcharge - after_offer,
        total=pricing.round_half_up(after_surcharge),
    )


def quote(plan, extras, members):
    """Return the monthly total as a whole number, or -1 if the selection is invalid."""
    breakdown = calculate(plan, extras, members)
    if breakdown is None:
        return INVALID
    return breakdown.total
