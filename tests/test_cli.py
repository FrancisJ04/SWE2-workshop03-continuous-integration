"""Tests for the command-line interface (R8)."""
import pytest

from gym_quote.cli import main, parse_extras, parse_members


def fake_input(answers):
    """Return an input function that replays the given answers."""
    replies = iter(answers)
    return lambda _prompt: next(replies)


def run(answers):
    """Run the CLI with the answers and return the result and the printed lines."""
    lines = []
    result = main(input_fn=fake_input(answers), print_fn=lines.append)
    return result, lines


@pytest.mark.parametrize(
    "answers, expected",
    [
        (["BASIC", "", "1", "y"], 30),
        (["PREMIUM", "GROUP_CLASSES, SPA", "2", "y"], 215),
        (["premium", "spa, specialized_program", "3", "Y"], 412),
    ],
)
def test_confirmed_quote_returns_total(answers, expected):
    """Answering y returns the total."""
    assert run(answers)[0] == expected


def test_cancelled_quote_returns_minus_one():
    """R8: answering n cancels and returns -1."""
    result, lines = run(["PREMIUM", "GROUP_CLASSES, SPA", "2", "n"])
    assert result == -1
    assert "Cancelled" in lines


@pytest.mark.parametrize(
    "answers",
    [
        ["GOLD", "", "1"],
        ["BASIC", "SPA", "1"],
        ["BASIC", "", "abc"],
        ["BASIC", "", "0"],
    ],
)
def test_invalid_selection_returns_minus_one_without_confirmation(answers):
    """An invalid selection returns -1 and does not ask for confirmation."""
    result, lines = run(answers)
    assert result == -1
    assert lines == ["Invalid selection"]


def test_breakdown_is_shown():
    """R8: the subtotal, each discount, the surcharge and the total are shown."""
    _, lines = run(["PREMIUM", "GROUP_CLASSES, SPA", "2", "y"])
    shown = "\n".join(lines)
    for label in ("Subtotal", "Group discount", "Special offer", "Premium surcharge", "Total"):
        assert label in shown
    assert "28.05" in shown


def test_parse_extras_and_members():
    """Extras are comma separated and members must be an integer."""
    assert parse_extras("SPA, ,GROUP_CLASSES") == ["SPA", "GROUP_CLASSES"]
    assert not parse_extras("")
    assert parse_members(" 3 ") == 3
    assert parse_members("tres") is None
