"""Specification table from the workshop statement (R9)."""
import pytest

from gym_quote.quote import quote


@pytest.mark.parametrize(
    "plan, extras, members, expected",
    [
        ("BASIC", [], 1, 31),
        ("STANDARD", ["PERSONAL_TRAINING"], 1, 70),
        ("BASIC", ["GROUP_CLASSES"], 2, 81),
        ("BASIC", ["GROUP_CLASSES"], 3, 122),
        ("STANDARD", ["GROUP_CLASSES", "PERSONAL_TRAINING"], 4, 286),
        ("PREMIUM", ["GROUP_CLASSES", "SPA"], 2, 215),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, 412),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM", "PERSONAL_TRAINING"], 4, 626),
        ("BASIC", ["SPA"], 1, -1),
        ("GOLD", [], 1, -1),
        ("BASIC", [], 0, -1),
    ],
)
def test_specification_table(plan, extras, members, expected):
    """Every row of the table in the statement gives the expected result."""
    assert quote(plan, extras, members) == expected
