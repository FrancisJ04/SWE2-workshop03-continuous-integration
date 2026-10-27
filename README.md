# Gym Membership Quote

Workshop 03 — Continuous Integration (Software Engineering II, ESPOL 2026).

Command-line application that quotes the monthly cost of a gym membership.
Jenkins runs the tests on every push to `main`; GitHub Actions runs linting and tests on every pull request to `main`.

## Team

| Member | Role | Responsible for |
|---|---|---|
| Francis Jiménez | Repository lead + Jenkins lead | Repository, branches, PR reviews and merges, Jenkins, tunnel, webhook, Jenkins job |
| Francisco Avendaño | GitHub Actions lead | `.github/workflows/ci.yml`, pylint, Actions runs |
| Marcia Torres | Developer A | R1, R2, R3, R7 and their tests |
| Juan Ayala | Developer B | R4, R5, R6 and their tests |
| Gino Quinde | CLI + test table lead | R8, R9 test table, report integration |

## Function contract (agree before coding)

Amounts are `decimal.Decimal`. Plans and extras are uppercase strings.

```python
# gym_quote/catalog.py      — Developer A (R1, R2)
PLANS = {"BASIC": 30, "STANDARD": 45, "PREMIUM": 70}
EXTRAS = {"GROUP_CLASSES": 15, "PERSONAL_TRAINING": 25, "SPA": 30, "SPECIALIZED_PROGRAM": 40}
PREMIUM_EXTRAS = {"SPA", "SPECIALIZED_PROGRAM"}
def is_valid_selection(plan: str, extras: list[str], members: int) -> bool: ...

# gym_quote/pricing.py      — Developer A (R3, R7)
def subtotal(plan: str, extras: list[str], members: int) -> Decimal: ...
def round_half_up(amount: Decimal) -> int: ...

# gym_quote/discounts.py    — Developer B (R4, R5, R6)
def apply_group_discount(amount: Decimal, members: int) -> Decimal: ...
def apply_special_offer(amount: Decimal) -> Decimal: ...
def apply_premium_surcharge(amount: Decimal, has_premium: bool) -> Decimal: ...

# gym_quote/quote.py        — Developer A + B (R7): no input/output
def quote(plan: str, extras: list[str], members: int) -> int:  # -1 if invalid

# gym_quote/cli.py          — CLI lead (R8): input/print, confirmation y/n (n -> -1)
def main() -> int: ...
```

## Run the tests

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install pytest pylint
pytest
pylint $(git ls-files '*.py')
```

## Assumptions

- Plan and extra names are case-insensitive and are normalised to uppercase.
- A repeated extra counts once.
