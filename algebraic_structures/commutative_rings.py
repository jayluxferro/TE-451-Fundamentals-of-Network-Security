"""
COMMUTATIVE RINGS
=================
A commutative ring is a ring where multiplication is commutative:
  a * b = b * a for all a, b.

A ring has:
- (R, +) an Abelian group
- multiplication associative
- distributive laws

Some commutative rings have identity (1), some do not.
"""


def integers_mod_n(n):
    """Z_n is a commutative ring with identity for all n >= 2."""
    elements = list(range(n))

    def add(a, b):
        return (a + b) % n

    def mul(a, b):
        return (a * b) % n

    return {
        "name": f"Z_{n}",
        "elements": elements,
        "add": add,
        "mul": mul,
        "has_identity": True,
        "identity": 1,
    }


def zero_divisors_in_zn(n):
    """Return example zero divisors in Z_n, if any."""
    if n < 2:
        return []
    pairs = []
    for a in range(1, n):
        for b in range(1, n):
            if (a * b) % n == 0:
                pairs.append((a, b))
    return pairs


def show_tables(ring):
    elements = ring["elements"]
    add = ring["add"]
    mul = ring["mul"]

    print(f"\n{'='*60}")
    print(f"COMMUTATIVE RING: {ring['name']}")
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

    print("\nAxiom summary:")
    print("  (R, +) is an Abelian group:")
    print("    - closed, associative, identity 0, inverses, commutative")
    print("  Multiplication is associative")
    print("  Distributive laws hold")
    print("  Multiplication is commutative (this makes it a commutative ring)")
    # Concrete distributive example
    a, b, c = elements[1], elements[2], elements[3]
    left = mul(a, add(b, c))
    right = add(mul(a, b), mul(a, c))
    print(f"  Example: {a}*({b}+{c}) = {left}, {a}*{b}+{a}*{c} = {right}")


if __name__ == "__main__":
    print("COMMUTATIVE RINGS - ALGEBRAIC STRUCTURE")
    print("Commutative ring: ring with a*b = b*a.")

    z4 = integers_mod_n(4)
    z6 = integers_mod_n(6)
    show_tables(z4)

    print("\nZero divisors in Z_4:")
    print("  Examples:", zero_divisors_in_zn(4)[:4])

    show_tables(z6)
    print("\nZero divisors in Z_6:")
    print("  Examples:", zero_divisors_in_zn(6)[:6])

    print("\nNote: Z_p (p prime) has no zero divisors and is a field.")
