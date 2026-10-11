# Pricing Module — Assignment 10

Small Python pricing module with taxes, member discounts, and receipt writing, plus a full pytest suite.

## Project structure

```
Assignment10/
├── pricing.py          # module under test (do not modify)
├── tests/
│   └── test_pricing.py # 14 test functions, 18 cases
├── pytest-output.txt   # passing run proof
└── README.md
```

## Prerequisites

- Python 3.8+
- pytest (`pip install pytest` or `pip install -r requirements.txt` if provided)

Check:

```bash
python3 --version
python3 -m pytest --version
```

## Run tests

```bash
cd /home/rzidinc/Projects/college/SDF/Assignment10
python3 -m pytest -v
```

Expected: `18 passed`.

Save proof output:

```bash
python3 -m pytest -v > pytest-output.txt 2>&1
```

## Use the module

```python
from pricing import calculate_subtotal, calculate_total, write_receipt

calculate_subtotal(100, 2)              # 200
calculate_total(10000, 2)               # 22200.0 (non-member)
calculate_total(10000, 2, is_member=True)  # 19980.0 (member)

write_receipt("receipt.txt", ["subtotal: 200", "total: 199.8"])
```

API:

| Function | Behavior |
|---|---|
| `calculate_subtotal(unit_price, quantity)` | `unit_price * quantity`. Raises `ValueError` on negative price or non-positive quantity. |
| `apply_member_discount(subtotal, is_member)` | 10% off if member, full price otherwise. |
| `add_tax(amount)` | Adds 11% tax. |
| `calculate_total(unit_price, quantity, is_member=False)` | Subtotal → discount → tax. |
| `write_receipt(path, lines)` | Writes each line with trailing newline, including last line. |

## Business rules covered

1. Subtotal = unit price × quantity.
2. Negative unit price rejected (`ValueError`).
3. Zero/negative quantity rejected (`ValueError`).
4. Members get 10% discount, non-members pay full.
5. 11% tax applied after discount.
6. Receipt file ends every line with newline, including last.

## Mutation testing

All three sample mutants are killed by the suite:

| Mutant | Failing tests | Verdict |
|---|---|---|
| Discount removed (`return subtotal`) | `test_apply_member_discount_member_gets_ten_percent`, `test_calculate_total_member` | Killed |
| Tax changed (`0.11` → `0.10`) | `test_add_tax_eleven_percent`, `test_calculate_total_nonmember`, `test_calculate_total_member` | Killed |
| Quantity validation removed | `test_subtotal_zero_quantity_raises`, `test_subtotal_negative_quantity_raises`, `test_calculate_total_propagates_input_validation` | Killed |
