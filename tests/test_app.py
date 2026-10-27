"""Skeleton test that proves the CI pipeline runs."""
from gym_quote.app import GymQuoteApp


def test_title():
    """The application reports its title."""
    assert GymQuoteApp().title() == "Gym Membership Quote"
