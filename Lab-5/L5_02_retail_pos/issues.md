# Lab 5: Issue Table: Retail POS (`pos_system.py`)

Line numbers refer to the **original** file. Tool IDs are in the Description column.
Scores: Pylint **5.65 -> 10.00**, Bandit **3 issues -> 0**, Flake8 **12 issues -> 0**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user promo input | Security (Bandit B307, Medium; Pylint W0123) | 27 | `apply_promo_code` runs whatever the user types, so `__import__('os').system(...)` executes arbitrary code. | Replaced with an `ast`-based evaluator that only allows numbers, `total` and `+ - * /`; anything else raises `ValueError`. |
| Mutable default argument | Bug (Pylint W0102) | 10 | `receipts=[]` is created once and shared across every call. | Default is `None`; a new list is created inside the function. |
| Bare `except` hides errors | Bug (Pylint W0702, Flake8 E722) | 16-17 | Any error (unknown item, string quantity) silently adds 0, so `("pen", "2")` gives a bill of 0 with no message. | Removed; explicit validation raises `ValueError`, unknown items are skipped with a logged warning. |
| `try/except Exception: pass` | Security/Quality (Bandit B110, Low; Pylint W0718) | 33-34 | `update_stock` swallows every error and prints a misleading "Stock updated" path; the body is also a no-op assignment. | Replaced with an explicit `if item in PRICE_LIST` check and a clear message for unknown items. |
| Negative quantity accepted | Logic bug (no tool flagged it) | 15, 47 | `("bottle", -4)` produced a bill of **-630** and reduced `sales_total`. | Quantity must be a positive `int`, otherwise `ValueError` (bill rejected in `main`). |
| Invalid tax rate accepted | Logic bug (no tool flagged it) | 18, 48 | `tax_rate=-1` zeroed the bill. | Tax rate must be between 0 and 1, otherwise `ValueError`. |
| File never closed | Resource leak (Pylint R1732, W1514) | 37 | `open()` without `with` or `encoding`; handle leaks if a write fails. | `with open(file, "a", encoding="utf-8")`. Receipts are cleared after writing so a second save does not duplicate them. |
| Weak RNG for receipt numbers | Security (Bandit B311, Low) | 21 | `random.randint` is not cryptographically secure. | Switched to `secrets.randbelow`. |
| `global` state | Design (Pylint W0603, C0103) | 7, 11 | Mutable global `sales_total` modified via `global`; name not UPPER_CASE. | State held in a module-level dict; constants renamed `PRICE_LIST`, `RECEIPT_LINES`. |
| Unused imports/variable | Quality (Pylint W0611, W0612; Flake8 F401, F841) | 1, 3, 26 | `json`, `logging` imported but unused; `total` assigned but unused. | Removed `json`; `logging` is now used for warnings; dead variable removed. |
| Missing docstrings, bad name, `%` format | Style (Pylint C0114, C0116, C0103, C0209) | 1, 10-44 | No docstrings, `printSales` is not snake_case, old `%` formatting. | Added docstrings, renamed to `print_sales`, used f-strings. |
| Formatting | Style (Flake8 E302, E305, E501) | 10-56 | One blank line between functions, an 88-char line, `main()` called on import. | Two blank lines, wrapped the long line, added `if __name__ == "__main__":`. |
| Floating-point noise in output | Output bug (no tool flagged it) | 18, 50 | Prints `301.45500000000004`. | Money rounded to 2 decimals. |
| Promo applies to day total, not to a bill | Design note (not changed) | 26 | The promo discounts the cumulative `sales_total`, not a single bill. | Left as is (behaviour of the original); worth confirming with the lab instructor. |
