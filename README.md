# Gym Membership Quote

Workshop 03 — Continuous Integration (Software Engineering II, ESPOL 2026).

Command-line application that quotes the monthly cost of a gym membership.
Jenkins runs the tests on every push to `main`; GitHub Actions runs linting and tests on every pull request to `main`.

## Team

| Member | GitHub | Role | Responsible for |
|---|---|---|---|
| Francis Jiménez | `FrancisJ04` | Repository lead + Jenkins lead | Repository, branches, PR reviews and merges, Jenkins, tunnel, webhook, Jenkins job |
| Francisco Avendaño | `FranciscoAve` | GitHub Actions lead | `.github/workflows/ci.yml`, pylint, Actions runs |
| Marcia Torres | `marciatorresg` | Developer A | R1, R2, R3, R7 and their tests |
| Juan Ayala | `JuanAyala619` | Developer B | R4, R5, R6 and their tests |
| Gino Quinde | `LeonardoGino31` | CLI + test table lead | R8, R9 test table, report integration |

## Function contract

Amounts are `decimal.Decimal`. Plans and extras are uppercase strings.

```python
# gym_quote/catalog.py      — Developer A (R1, R2)
PLANS = {"BASIC": 30, "STANDARD": 45, "PREMIUM": 70}
EXTRAS = {"GROUP_CLASSES": 15, "PERSONAL_TRAINING": 25, "SPA": 30, "SPECIALIZED_PROGRAM": 40}
PREMIUM_EXTRAS = {"SPA", "SPECIALIZED_PROGRAM"}
def normalize(names: list[str]) -> list[str]: ...
def has_premium_extra(extras: list[str]) -> bool: ...
def is_valid_selection(plan: str, extras: list[str], members: int) -> bool: ...

# gym_quote/pricing.py      — Developer A (R3, R7)
def subtotal(plan: str, extras: list[str], members: int) -> Decimal: ...
def round_half_up(amount: Decimal) -> int: ...

# gym_quote/discounts.py    — Developer B (R4, R5, R6)
def apply_group_discount(amount: Decimal, members: int) -> Decimal: ...
def apply_special_offer(amount: Decimal) -> Decimal: ...
def apply_premium_surcharge(amount: Decimal, has_premium: bool) -> Decimal: ...

# gym_quote/quote.py        — Developer A (R7): no input/output
class Breakdown: subtotal, group_discount, special_offer, surcharge (Decimal), total (int)
def calculate(plan: str, extras: list[str], members: int) -> Breakdown | None: ...
def quote(plan: str, extras: list[str], members: int) -> int:  # -1 if invalid

# gym_quote/cli.py          — CLI lead (R8): input/print, confirmation y/n (n -> -1)
def main(input_fn=input, print_fn=print) -> int: ...
```

## Run

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install pytest pylint
pytest
pylint $(git ls-files '*.py')
python -m gym_quote.cli
```

## Assumptions

- Plan and extra names are case-insensitive and surrounding spaces are ignored.
- A repeated extra counts once.
- The number of members must be an integer of at least 1; anything else is invalid (-1).
- In the CLI, extras are comma separated; an empty answer means no extras.
- Discounts and surcharge are applied in the order R4, R5, R6; only the final total is rounded (half up).
- An invalid selection, or any confirmation answer other than `y`, returns -1.

## Continuous integration

- **Jenkins** (job `gym-membership-quote-ci`): runs `pytest` on every push to `main`, triggered by a GitHub webhook, and publishes the JUnit report.
- **GitHub Actions** (`.github/workflows/ci.yml`): runs `pytest` and `pylint` on every pull request to `main`.
