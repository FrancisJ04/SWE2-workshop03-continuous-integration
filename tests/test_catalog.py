"""Tests for the catalog and the selection validation (R1, R2, R3)."""
import pytest

from gym_quote.catalog import has_premium_extra, is_valid_selection, normalize


@pytest.mark.parametrize(
    "plan, extras, members",
    [
        ("BASIC", [], 1),
        ("STANDARD", ["GROUP_CLASSES", "PERSONAL_TRAINING"], 4),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3),
    ],
)
def test_valid_selection(plan, extras, members):
    """A known plan with allowed extras and at least one member is valid."""
    assert is_valid_selection(plan, extras, members)


def test_unknown_plan_is_invalid():
    """R1: a plan that is not in the catalog is invalid."""
    assert not is_valid_selection("GOLD", [], 1)


def test_unknown_extra_is_invalid():
    """R2: an extra that is not in the catalog is invalid."""
    assert not is_valid_selection("BASIC", ["YOGA"], 1)


@pytest.mark.parametrize(
    "plan, extras",
    [
        ("BASIC", ["SPA"]),
        ("STANDARD", ["SPECIALIZED_PROGRAM"]),
    ],
)
def test_premium_extra_needs_premium_plan(plan, extras):
    """R2: a premium extra with a plan other than PREMIUM is invalid."""
    assert not is_valid_selection(plan, extras, 1)


@pytest.mark.parametrize("members", [0, -2, 1.5, "2", True])
def test_members_must_be_a_positive_integer(members):
    """R3: the number of members is an integer of at least 1."""
    assert not is_valid_selection("BASIC", [], members)


def test_normalize_strips_uppercases_and_removes_duplicates():
    """Names are trimmed, upper-cased and a repeated extra counts once."""
    assert normalize([" spa ", "Spa", "group_classes"]) == ["SPA", "GROUP_CLASSES"]


def test_has_premium_extra():
    """Only SPA and SPECIALIZED_PROGRAM are premium extras."""
    assert not has_premium_extra(["GROUP_CLASSES", "PERSONAL_TRAINING"])
    assert has_premium_extra(["GROUP_CLASSES", "SPA"])
