"""Command-line interface (R8): asks for the selection, shows the breakdown and confirms.

Run it with: python -m gym_quote.cli
"""
from gym_quote.quote import INVALID, calculate


def parse_extras(text):
    """Split a comma-separated list of extras; an empty text means no extras."""
    return [name.strip() for name in text.split(",") if name.strip()]


def parse_members(text):
    """Return the number of members as an integer, or None if the text is not an integer."""
    try:
        return int(text.strip())
    except ValueError:
        return None


def row(label, value):
    """Format one line of the breakdown with the label on the left and the value on the right."""
    return f"{label:<20}{value:>10}"


def main(input_fn=input, print_fn=print):
    """Run the quote dialogue and return the total, or -1 if invalid or cancelled."""
    plan = input_fn("Plan (BASIC, STANDARD, PREMIUM): ")
    extras = parse_extras(
        input_fn("Extras (GROUP_CLASSES, PERSONAL_TRAINING, SPA, SPECIALIZED_PROGRAM), "
                 "comma separated, empty for none: ")
    )
    members = parse_members(input_fn("Members: "))

    breakdown = None if members is None else calculate(plan, extras, members)
    if breakdown is None:
        print_fn("Invalid selection")
        return INVALID

    print_fn(row("Subtotal:", f"{breakdown.subtotal:.2f}"))
    print_fn(row("Group discount:", f"-{breakdown.group_discount:.2f}"))
    print_fn(row("Special offer:", f"-{breakdown.special_offer:.2f}"))
    print_fn(row("Premium surcharge:", f"+{breakdown.surcharge:.2f}"))
    print_fn(row("Total:", str(breakdown.total)))

    if input_fn("Confirm (y/n): ").strip().lower() != "y":
        print_fn("Cancelled")
        return INVALID
    print_fn(f"Confirmed. Total: {breakdown.total}")
    return breakdown.total


if __name__ == "__main__":
    main()
