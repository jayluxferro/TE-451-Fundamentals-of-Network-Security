"""
FINITE FIELDS
=============
A finite field (also called a Galois field) is a field with finitely many elements.
All finite fields have size p^k for some prime p and integer k >= 1.

Key facts:
- F_p (integers mod p) is a field iff p is prime.
- For each p^k there is a finite field with exactly p^k elements.
"""


def finite_field_p(p):
    """Finite field F_p = Z_p for prime p."""
    elements = list(range(p))

    def add(a, b):
        return (a + b) % p

    def mul(a, b):
        return (a * b) % p

    def inv(a):
        if a == 0:
            return None
        # Fermat's little theorem: a^(p-2) = a^-1 (mod p)
        return pow(a, p - 2, p)

    return {
        "name": f"F_{p}",
        "order": p,
        "elements": elements,
        "add": add,
        "mul": mul,
        "inv": inv,
    }


def finite_field_f4():
    """
    Example of F_4 = GF(2)[x]/(x^2 + x + 1).
    Elements: {0, 1, x, x+1} with x^2 = x + 1.
    This is a finite field of order 4.
    """
    elements = ["0", "1", "x", "x+1"]

    def add(a, b):
        if a == "0":
            return b
        if b == "0":
            return a
        if a == b:
            return "0"
        # XOR-like in characteristic 2
        if {a, b} == {"1", "x"}:
            return "x+1"
        if {a, b} == {"1", "x+1"}:
            return "x"
        if {a, b} == {"x", "x+1"}:
            return "1"
        return "0"

    def mul(a, b):
        if a == "0" or b == "0":
            return "0"
        if a == "1":
            return b
        if b == "1":
            return a
        # x * x = x^2 = x + 1
        if a == "x" and b == "x":
            return "x+1"
        # x * (x+1) = x^2 + x = (x+1) + x = 1
        if {a, b} == {"x", "x+1"}:
            return "1"
        # (x+1) * (x+1) = x^2 + 2x + 1 = x^2 + 1 = (x+1) + 1 = x
        if a == "x+1" and b == "x+1":
            return "x"
        return "0"

    def inv(a):
        if a == "0":
            return None
        # In F_4, every nonzero element has order 3
        if a == "1":
            return "1"
        if a == "x":
            return "x+1"
        if a == "x+1":
            return "x"
        return None

    return {
        "name": "F_4",
        "order": 4,
        "elements": elements,
        "add": add,
        "mul": mul,
        "inv": inv,
    }


def show_tables(field):
    elements = field["elements"]
    add = field["add"]
    mul = field["mul"]

    print(f"\n{'='*60}")
    print(f"FINITE FIELD: {field['name']} (order {field['order']})")
    print('='*60)

    print("\nAddition table:")
    header = "\t".join(str(e) for e in elements)
    print(header)
    print('-'*60)
    for a in elements:
        row = "\t".join(str(add(a, b)) for b in elements)
        print(f"{a}\t{row}")

    print("\nMultiplication table:")
    header = "\t".join(str(e) for e in elements)
    print(header)
    print('-'*60)
    for a in elements:
        row = "\t".join(str(mul(a, b)) for b in elements)
        print(f"{a}\t{row}")

    print("\nMultiplicative inverses (nonzero):")
    for a in elements:
        if a == 0 or a == "0":
            continue
        print(f"  {a}^-1 = {field['inv'](a)}")

    # Axiom summary for clarity
    print("\nAxiom summary:")
    print("  Additive identity: 0")
    print("  Multiplicative identity: 1")
    print("  Additive inverses: all elements have an inverse under +")
    print("  Multiplicative inverses: all nonzero elements have an inverse under *")
    print("  Distributive laws: a*(b+c) = a*b + a*c and (b+c)*a = b*a + c*a")
    # Concrete distributive example
    a = field["elements"][1]
    b = field["elements"][2]
    c = field["elements"][3] if len(field["elements"]) > 3 else field["elements"][0]
    left = field["mul"](a, field["add"](b, c))
    right = field["add"](field["mul"](a, b), field["mul"](a, c))
    print(f"  Example: {a}*({b}+{c}) = {left}, {a}*{b}+{a}*{c} = {right}")


if __name__ == "__main__":
    print("FINITE FIELDS - ALGEBRAIC STRUCTURE")
    print("A finite field has p^k elements for prime p and integer k >= 1.")

    f5 = finite_field_p(5)
    show_tables(f5)

    f4 = finite_field_f4()
    show_tables(f4)
