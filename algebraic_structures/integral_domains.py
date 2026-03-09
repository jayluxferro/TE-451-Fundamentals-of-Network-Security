"""
INTEGRAL DOMAINS
===============
An INTEGRAL DOMAIN is a commutative ring with identity (1) that has no zero divisors.

A ZERO DIVIDER is a pair of non-zero elements a, b such that a * b = 0.

Examples:
- Z (integers): Integral domain
- Q, R, C (rational/real/complex numbers): Fields, hence integral domains
- Z_n where n is prime: Fields (special case), hence integral domains
- Z_n where n is composite: NOT an integral domain (has zero divisors)
"""

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def check_zero_divisors(set_elements, multiplication_op):
    """
    Check if there are zero divisors in the set.
    Zero divisor: non-zero a, b where a * b = 0
    """
    has_zero_divisor = False
    zero_divisor_pairs = []

    for a in set_elements:
        for b in set_elements:
            if a != 0 and b != 0 and multiplication_op(a, b) == 0:
                has_zero_divisor = True
                zero_divisor_pairs.append((a, b))

    return {
        "has_zero_divisor": has_zero_divisor,
        "zero_divisor_pairs": zero_divisor_pairs[:10] if zero_divisor_pairs else []  # Limit display
    }


def integers_mod_n(n):
    """
    The ring Z_n = {0, 1, ..., n-1} with addition and multiplication mod n.

    This is an INTEGRAL DOMAIN if and only if n is prime.
    If n is composite, there are zero divisors (e.g., in Z_6: 2*3=0).
    """
    elements = list(range(n))

    def add(a, b):
        return (a + b) % n

    def mult(a, b):
        return (a * b) % n

    # Check integral domain properties
    zero_divisors = check_zero_divisors(elements, mult)

    # Z_n is an integral domain iff n is prime
    n_is_prime = is_prime(n)

    return {
        "name": f"Ring of Integers Modulo n: Z_{{n}}",
        "elements": elements,
        "addition_op": add,
        "multiplication_op": mult,
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "has_zero_divisor": zero_divisors["has_zero_divisor"],
        "n_is_prime": n_is_prime,
        "is_integral_domain": n_is_prime and not zero_divisors["has_zero_divisor"]
    }


def integers_z():
    """
    The ring of integers Z.
    This is the prototypical integral domain.

    Note: We'll show a finite subset for display purposes,
    but note that Z itself is infinite.
    """
    elements = list(range(-5, 6))

    def add(a, b):
        return a + b

    def mult(a, b):
        result = a * b
        if -10 <= result < 10:
            return result
        return "(outside displayed range)"

    zero_divisors = check_zero_divisors(elements, mult)

    is_integral_domain = True

    return {
        "name": "Ring of Integers: Z",
        "elements": elements,
        "addition_op": add,
        "multiplication_op": mult,
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "has_zero_divisor": False,
        "infinite_ring": True,
        "is_integral_domain": is_integral_domain
    }


def integers_mod_6():
    """
    Special case showing Z_6 which is NOT an integral domain.
    Zero divisors: 2*3 = 6 = 0 (mod 6)
    """
    return integers_mod_n(6)


def display_integral_domain_info(ring_info):
    """
    Display information about a ring, highlighting integral domain properties.
    """
    if "error" in ring_info:
        print(f"Error: {ring_info.get('error', 'Unknown error')}")
        return

    name = ring_info.get("name", "Unknown")
    note = ring_info.get("note", "")

    print(f"\n{'='*70}")
    print(f"INTEGRAL DOMAIN (or related ring): {name}")
    print('='*70)

    if note:
        print(note)

    properties = ring_info.get("properties", ring_info)

    print("\n--- Properties ---")
    print(f"  Commutative: {properties.get('is_commutative', 'N/A')}")
    if properties.get('has_identity'):
        print(f"  Has multiplicative identity (1): {properties['has_identity']}")

    zero_divisors = check_zero_divisors(ring_info.get("elements", []), ring_info.get("multiplication_op", None))
    print(f"  Has zero divisors: {zero_divisors['has_zero_divisor']}")
    if zero_divisors["zero_divisor_pairs"]:
        print(f"    Examples: {zero_divisors['zero_divisor_pairs'][:3]}")

    is_id = properties.get("is_integral_domain", True)
    n_prime = properties.get("n_is_prime", True)

    print(f"\n--- Integral Domain Check ---")
    if not is_id:
        print("  ✗ NOT an integral domain!")
        reason = []
        if not properties.get("is_commutative"):
            reason.append("Not commutative")
        if not properties.get("has_identity"):
            reason.append("No identity")
        if zero_divisors["has_zero_divisor"]:
            reason.append("Has zero divisors")
        print(f"    Reason: {', '.join(reason)}")
        if zero_divisors["zero_divisor_pairs"]:
            a, b = zero_divisors["zero_divisor_pairs"][0]
            print(f"    Concrete: {a} * {b} = 0 (zero divisor)")
    else:
        print("  ✓ IS an integral domain!")

    print("\n--- Axiom summary ---")
    print("  (R, +) is an Abelian group")
    print("  Multiplication is associative")
    print("  Commutative: a*b = b*a")
    print("  Has identity: 1")
    print("  No zero divisors")

    if n_prime and is_id:
        print("")
        print("--- Note ---")
        print("Z_n where n is PRIME is a FIELD (special case of integral domain)")


def display_operations(ring_info, title="Operations"):
    """
    Display operation tables for a ring.
    """
    print(f"\n{title}")
    print("="*50)

    elements = ring_info.get("elements", [])

    if all(isinstance(e, int) for e in elements) and len(elements) <= 8:
        display = ring_info.get("multiplication_op")
        if display:
            print(f"\nMultiplication Table for {ring_info['name']}")
            header = "\t".join(str(e) for e in elements)
            print(header)
            print('-'*50)

            for row_elem in elements:
                row = "\t".join(display(row_elem, col) for col in elements)
                print(str(row_elem) + "\t" + row)


def show_zero_divisor_explanation(n):
    """
    Explain zero divisors in Z_n.
    """
    print(f"\n--- Zero Divisors in Z_{{n}} where n = {n} ---")

    zero_divs = []
    for a in range(1, n):
        for b in range(1, n):
            if (a * b) % n == 0:
                zero_divs.append((a, b))

    if zero_divs:
        print(f"Zero divisors in Z_{n}:")
        pairs = [(str(a), str(b)) for a, b in zero_divs[:6]]
        print(f"  Pairs whose product is 0 (mod {n}):")
        for pair in pairs:
            print(f"    {pair[0]} * {pair[1]} = {(int(pair[0]) * int(pair[1])) % n} (mod {n})")
    else:
        print(f"No zero divisors in Z_{n}")


# Main demonstration
if __name__ == "__main__":
    print("\n" + "="*70)
    print("INTEGRAL DOMAINS - ALGEBRAIC STRUCTURE")
    print("="*70)

    print("\n--- INTEGRAL DOMAIN CONCEPT ---")
    print("")
    print("An INTEGRAL DOMAIN is a ring that satisfies:")
    print("  1. (R, +) is an Abelian group")
    print("  2. Multiplication is associative")
    print("  3. Distributive laws hold")
    print("  4. COMMUTATIVE: a * b = b * a")
    print("  5. HAS IDENTITY: There exists 1 ≠ 0")
    print("  6. NO ZERO DIVIDERS: If a * b = 0, then a = 0 or b = 0")
    print("")

    id_examples = {
        "Z": integers_z(),
        "Z_3 (prime)": integers_mod_n(3),
        "Z_5 (prime)": integers_mod_n(5),
        "Z_7 (prime)": integers_mod_n(7),
        "Z_6 (composite)": integers_mod_6(),
    }

    print("\n--- INTEGRAL DOMAINS (Examples) ---")

    for name in ["Z", "Z_3 (prime)", "Z_5 (prime)"]:
        example = id_examples[name]
        display_integral_domain_info(example)

    print("\n--- NON-INTEGRAL DOMAIN EXAMPLE ---")
    composite_ring = id_examples["Z_6 (composite)"]
    display_integral_domain_info(composite_ring)

    print("\n--- ZERO DIVISOR EXPLANATION ---")
    show_zero_divisor_explanation(6)

    print("\n--- COMPARISON: Z_5 vs Z_6 ---")
    print("")
    z5 = id_examples["Z_5 (prime)"]
    z6 = id_examples["Z_6 (composite)"]

    print(f"Z_5 (p=5, prime):")
    print(f"  - Commutative: ✓")
    print(f"  - Has identity: ✓")
    print(f"  - No zero divisors: ✓")
    print(f"  - Integral domain: ✓")
    print(f"  - Actually a FIELD!")

    print("")
    print(f"Z_6 (n=6, composite):")
    print(f"  - Commutative: ✓")
    print(f"  - Has identity: ✓")
    print(f"  - No zero divisors: ✗")
    print(f"  - Is integral domain: ✗")

    show_zero_divisor_explanation(6)

    print("\n--- RELATIONSHIPS ---")
    print("")
    print("Hierarchy of algebraic structures:")
    print("")
    print("  FIELD      ")
    print("   ↑         "  "(fields are integral domains)")
    print("  /           "  "  ")
    print(" INTEGRAL DOMAIN")
    print("   ↑          "  "(integral domains are commutative rings with 1, no zero divisors)")
    print(" COMMUTATIVE RING WITH 1 AND NO ZERO DIVISORS")
    print("   ↑          "  "(same as integral domain by definition)")
    print("  /           ")
    print(" COMMUTATIVE RING")
    print("   ↑         "  "(commutative rings may or may not have identity/zero divisors)")
    print("   \               ")
    print("    NON-COMMUTATIVE RING")

    print("\n--- SPECIAL CASES ---")
    print("")
    print("- Z (integers): Integral domain, not a field")
    print("- Q (rationals): Field, hence integral domain")
    print("- R (reals): Field, hence integral domain")
    print("- C (complex numbers): Field, hence integral domain")
    print("- Z_p (p prime): Field, hence integral domain")
    print("- Z_n (n composite): Commutative ring, NOT an integral domain")
