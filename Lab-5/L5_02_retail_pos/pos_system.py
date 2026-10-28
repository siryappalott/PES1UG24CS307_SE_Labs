"""Retail point-of-sale script: checkout totals, promo codes and receipts."""
import ast
import logging
import operator
import secrets

# Module-level state (a dict avoids the `global` statement)
PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
RECEIPT_LINES = []
_STATE = {"sales_total": 0.0}

# Operators allowed in promo codes (replaces eval)
_PROMO_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Total a cart of (item, quantity) pairs with tax and record the sale.

    Raises ValueError for a bad tax rate or a non-positive/non-integer
    quantity. Items missing from PRICE_LIST are skipped with a warning.
    """
    if receipts is None:
        receipts = []
    if not 0 <= tax_rate <= 1:
        raise ValueError(f"tax rate must be between 0 and 1, got {tax_rate}")
    subtotal = 0
    for name, qty in cart_items:
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValueError(f"invalid quantity for {name}: {qty!r}")
        if name not in PRICE_LIST:
            logging.warning("Unknown item skipped: %s", name)
            continue
        subtotal += PRICE_LIST[name] * qty
    total = round(subtotal * (1 + tax_rate), 2)
    receipts.append(total)
    _STATE["sales_total"] += total
    receipt_no = secrets.randbelow(9000) + 1000
    RECEIPT_LINES.append(f"Receipt #{receipt_no} total={total:.2f}")
    return total


def _eval_promo(node, total):
    """Evaluate only numbers, the name 'total' and + - * / (no eval)."""
    if isinstance(node, ast.Expression):
        return _eval_promo(node.body, total)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "total":
        return total
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_promo(node.operand, total)
    if isinstance(node, ast.BinOp) and type(node.op) in _PROMO_OPS:
        return _PROMO_OPS[type(node.op)](
            _eval_promo(node.left, total), _eval_promo(node.right, total))
    raise ValueError("invalid promo code")


def apply_promo_code(code_str):
    """Apply a promo such as 'total * 0.9' to the sales total (never < 0)."""
    try:
        tree = ast.parse(code_str.strip(), mode="eval")
        result = _eval_promo(tree, _STATE["sales_total"])
    except (SyntaxError, ZeroDivisionError) as exc:
        raise ValueError("invalid promo code") from exc
    return round(max(result, 0), 2)


def update_stock(item, qty):
    """Report a stock update for a known item."""
    if item in PRICE_LIST:
        print("Stock updated for", item, "by", qty)
    else:
        print("Unknown item, stock not updated:", item)


def save_receipt_log(file="pos_log.txt"):
    """Append pending receipt lines to the log file, then clear them."""
    with open(file, "a", encoding="utf-8") as log_file:
        for line in RECEIPT_LINES:
            log_file.write(line + "\n")
    RECEIPT_LINES.clear()


def print_sales():
    """Print the running sales total."""
    print(f"Sales so far: {_STATE['sales_total']:.2f}")


def main():
    """Run the demo checkouts, promo codes and receipt logging."""
    bills = [
        ([("pen", 3), ("notebook", 2)], 0.05),
        ([("bag", 1), ("laptop", 1)], 0.05),
        ([("bottle", -4)], 0.05),
        ([("pen", "2")], -1),
    ]
    for number, (cart, rate) in enumerate(bills, start=1):
        try:
            print(f"Bill {number}:", process_checkout(cart, tax_rate=rate))
        except ValueError as exc:
            print(f"Bill {number}: rejected ({exc})")
    update_stock("laptop", 5)
    print("After promo:", apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    try:
        print("After your promo:", apply_promo_code(code))
    except ValueError as exc:
        print("Promo rejected:", exc)
    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()
