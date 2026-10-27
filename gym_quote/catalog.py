"""Plan and extra catalog with selection validation (R1, R2)."""

PLANS = {"BASIC": 30, "STANDARD": 45, "PREMIUM": 70}
EXTRAS = {
    "GROUP_CLASSES": 15,
    "PERSONAL_TRAINING": 25,
    "SPA": 30,
    "SPECIALIZED_PROGRAM": 40,
}
PREMIUM_EXTRAS = frozenset({"SPA", "SPECIALIZED_PROGRAM"})
PREMIUM_PLAN = "PREMIUM"


def normalize(names):
    """Return the names stripped and upper-cased, without duplicates, keeping their order."""
    return list(dict.fromkeys(name.strip().upper() for name in names))


def has_premium_extra(extras):
    """Return True if at least one of the extras is a premium extra."""
    return any(extra in PREMIUM_EXTRAS for extra in extras)


def is_valid_selection(plan, extras, members):
    """Return True if the plan, the extras and the number of members form a valid selection.

    R1: the plan must be in the catalog.
    R2: every extra must be in the catalog, and premium extras need the PREMIUM plan.
    R3: the number of members is an integer of at least 1.
    """
    if plan not in PLANS:
        return False
    if any(extra not in EXTRAS for extra in extras):
        return False
    if has_premium_extra(extras) and plan != PREMIUM_PLAN:
        return False
    return isinstance(members, int) and not isinstance(members, bool) and members >= 1
