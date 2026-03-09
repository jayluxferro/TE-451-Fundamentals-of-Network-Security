"""
RINGS AND COMMUTATIVE RINGS
===========================
A ring is a set equipped with two binary operations (+ and *):
1. (G, +) forms an Abelian group
2. Multiplication is associative
3. Distributive laws hold: a*(b+c) = a*b + a*c and (b+c)*a = b*a + c*a

A COMMUTATIVE RING additionally satisfies:
a * b = b * a for all a, b in G

Rings don't necessarily have multiplicative identity (1)
Commutative rings with identity are called "commutative rings with 1"
"""

import math


def check_ring_properties(set_elements, addition_op, multiplication_op, has_zero=True):
    """
    Check if a set with operations forms a ring.

    Args:
        set_elements: List of elements in the ring
        addition_op: Function for addition
        multiplication_op: Function for multiplication
        has_zero: Whether there should be a zero element

    Returns:
        Dictionary with properties and whether it's a ring/commutative
    """
    element_set = set(set_elements)

    # Closure checks
    def is_closed(op):
        for a in set_elements:
            for b in set_elements:
                if op(a, b) not in element_set:
                    return False
        return True

    closure_add = is_closed(addition_op)
    closure_mul = is_closed(multiplication_op)

    # Find additive identity (0)
    zero = None
    if has_zero:
        for e in set_elements:
            if all(addition_op(a, e) == a and addition_op(e, a) == a for a in set_elements):
                zero = e
                break

    # Check additive inverse: For each a, there exists b such that a + b = 0
    def has_additive_inverses():
        if zero is None:
            return False
        for a in set_elements:
            found_inverse = False
            for b in set_elements:
                if addition_op(a, b) == zero:
                    found_inverse = True
                    break
            if not found_inverse:
                return False
        return True

    additive_inverses = has_additive_inverses()

    # Check associativity of addition
    assoc_add = True
    for a in set_elements:
        for b in set_elements:
            for c in set_elements:
                if addition_op(addition_op(a, b), c) != addition_op(a, addition_op(b, c)):
                    assoc_add = False
                    break
            if not assoc_add:
                break
        if not assoc_add:
            break

    # Check associativity of multiplication
    assoc_mult = True
    for a in set_elements:
        for b in set_elements:
            for c in set_elements:
                if multiplication_op(multiplication_op(a, b), c) != multiplication_op(a, multiplication_op(b, c)):
                    assoc_mult = False
                    break
            if not assoc_mult:
                break
        if not assoc_mult:
            break

    # Check distributive laws
    def left_distributive():
        for a in set_elements:
            for b in set_elements:
                for c in set_elements:
                    if addition_op(multiplication_op(a, b), multiplication_op(a, c)) != multiplication_op(a, addition_op(b, c)):
                        return False
        return True

    def right_distributive():
        for a in set_elements:
            for b in set_elements:
                for c in set_elements:
                    if addition_op(multiplication_op(b, a), multiplication_op(c, a)) != multiplication_op(addition_op(b, c), a):
                        return False
        return True

    left_dist = left_distributive()
    right_dist = right_distributive()

    # Check commutativity of multiplication
    def mult_commutative():
        for a in set_elements:
            for b in set_elements:
                if multiplication_op(a, b) != multiplication_op(b, a):
                    return False
        return True

    is_commutative = mult_commutative()

    # Check multiplicative identity (1)
    one = None
    for e in set_elements:
        is_one = all(multiplication_op(e, a) == a and multiplication_op(a, e) == a for a in set_elements)
        if is_one:
            one = e
            break

    # Check additive commutativity (Abelian under +)
    additive_commutative = True
    for a in set_elements:
        for b in set_elements:
            if addition_op(a, b) != addition_op(b, a):
                additive_commutative = False
                break
        if not additive_commutative:
            break

    # Determine if it's a ring
    is_ring = (
        closure_add
        and closure_mul
        and (zero is not None)
        and additive_inverses
        and assoc_add
        and assoc_mult
        and left_dist
        and right_dist
        and additive_commutative
    )

    has_one = one is not None
    return {
        "is_ring": is_ring,
        "closure_addition": closure_add,
        "closure_multiplication": closure_mul,
        "has_zero": zero is not None,
        "zero": zero,
        "additive_inverses": additive_inverses,
        "additive_commutative": additive_commutative,
        "associative_addition": assoc_add,
        "associative_multiplication": assoc_mult,
        "left_distributive": left_dist,
        "right_distributive": right_dist,
        "is_commutative": is_commutative and is_ring,
        "has_one": one is not None,
        "one": one,
        "commutative_with_identity": is_ring and is_commutative and has_one
    }


def integers_mod_n(n):
    """
    The ring of integers modulo n: Z_n = {0, 1, ..., n-1}.
    This is a commutative ring with identity for all n ≥ 2.

    For prime p, Z_p is a field (special case).
    """
    elements = list(range(n))

    def add(a, b):
        return (a + b) % n

    def mult(a, b):
        return (a * b) % n

    properties = check_ring_properties(elements, add, mult)

    return {
        "name": f"Ring of Integers Modulo n: Z_{{n}}",
        "elements": elements,
        "addition_op": add,
        "multiplication_op": mult,
        "properties": properties
    }


def integers_mod_p(p):
    """
    The field of integers modulo p where p is prime.
    Z_p is both a ring AND a field when p is prime.

    Note: For educational purposes, this shows it's also a COMMUTATIVE RING.
    """
    return integers_mod_n(p)


def integers_z_subset():
    """
    A subset of Z (integers) showing ring properties.
    We use {-3, -2, -1, 0, 1, 2, 3} under standard + and *.

    Note: This is actually the full ring Z restricted to a finite subset,
    which doesn't form a proper ring (no additive inverses for elements outside).
    For demonstration, we'll treat it as having "partial" operations.
    """
    elements = list(range(-3, 4))

    def add(a, b):
        # Only return if result is in our subset (closure check)
        result = a + b
        if -3 <= result < 4:
            return result
        else:
            return None  # Not closed

    def mult(a, b):
        result = a * b
        if -3 <= result < 4:
            return result
        else:
            return None

    properties = check_ring_properties(elements, add, mult)

    return {
        "name": "Ring Z (restricted subset demonstration)",
        "elements": elements,
        "note": "This is a subset of integers with standard operations. For true ring structure, use full Z or Z_n.",
        "properties": properties
    }


def polynomial_ring():
    """
    Polynomial ring R[x] over a field R (here we use real coefficients).
    We show a finite set of polynomials for demonstration.

    For simplicity, we work with coefficient-based representations.
    Example: x^2 + 1 represented as [1, 0, 1] (coefficients of 1, x, x^2)
    """
    # We'll represent small degree polynomials
    # Elements are tuples (a0, a1, ..., an) representing a0 + a1*x + ... + an*x^n
    elements = [
        (0, 0),           # 0
        (1, 0),           # 1
        (0, 1),           # x
        (1, 1),           # 1 + x
        (-1, 1, 1),       # -1 + x + x^2
    ]

    def add(p1, p2):
        max_len = max(len(p1), len(p2))
        return tuple(
            (p1[i] if i < len(p1) else 0) + (p2[i] if i < len(p2) else 0)
            for i in range(max_len)
        )[:max_len]

    def mult(p1, p2):
        if not p1 or not p2:
            return tuple()
        result = [0] * (len(p1) + len(p2) - 1)
        for i, a in enumerate(p1):
            for j, b in enumerate(p2):
                result[i+j] += a * b
        return tuple(result)

    properties = check_ring_properties(elements, add, mult)

    return {
        "name": "Polynomial Ring R[x]",
        "elements": elements,
        "note": "Polynomials represented by coefficient tuples",
        "properties": properties
    }


def matrix_ring_2x2():
    """
    The ring of 2×2 matrices over a field.
    Matrix addition and multiplication form a ring.

    Matrix ring M_n(F) is:
    - A ring
    - NOT commutative for n ≥ 2
    - Has identity (identity matrix)
    """
    # Full ring M_2(Z_3): all 2x2 matrices with entries in {0,1,2}
    vals = [0, 1, 2]
    elements = []
    for a in vals:
        for b in vals:
            for c in vals:
                for d in vals:
                    elements.append(((a, b), (c, d)))

    def add(m1, m2):
        return (
            ((m1[0][0] + m2[0][0]) % 3, (m1[0][1] + m2[0][1]) % 3),
            ((m1[1][0] + m2[1][0]) % 3, (m1[1][1] + m2[1][1]) % 3)
        )

    def mult(m1, m2):
        return (
            (
                (m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0]) % 3,
                (m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1]) % 3
            ),
            (
                (m1[1][0]*m2[0][0] + m1[1][1]*m2[1][0]) % 3,
                (m1[1][0]*m2[0][1] + m1[1][1]*m2[1][1]) % 3
            )
        )

    properties = check_ring_properties(elements, add, mult)

    return {
        "name": "Matrix Ring M_2(Z_3)",
        "elements": elements,
        "note": "Matrices with entries in Z_3. This is a non-commutative ring.",
        "properties": properties
    }


def display_ring_info(ring_info):
    """
    Display information about a ring.
    """
    if "error" in ring_info:
        print(f"Error: {ring_info['error']}")
        return

    name = ring_info.get("name", "Unknown Ring")
    note = ring_info.get("note", "")

    print(f"\n{'='*70}")
    print(f"RING: {name}")
    print('='*70)

    if note:
        print(note)

    properties = ring_info.get("properties", {})

    print("\nRing Properties:")
    print(f"  Closed under addition: {properties.get('closure_addition', False)}")
    print(f"  Closed under multiplication: {properties.get('closure_multiplication', False)}")
    print(f"  Zero element exists: {properties['has_zero']}")
    if properties['has_zero']:
        print(f"    Zero ({'zero'}): {properties['zero']}")

    print(f"  Additive inverses: {properties['additive_inverses']}")
    print(f"  Additive commutativity: {properties.get('additive_commutative', False)}")
    print(f"  Associativity (addition): {properties['associative_addition']}")
    print(f"  Associativity (multiplication): {properties['associative_multiplication']}")
    print(f"  Left distributive: {properties['left_distributive']}")
    print(f"  Right distributive: {properties['right_distributive']}")

    print(f"\nCommutativity:")
    if properties.get('is_commutative'):
        print("  ✓ Multiplication is commutative")
    elif not properties.get('is_commutative', False) and 'commutative_with_identity' in ring_info:
        status = "Non-commutative ring"
        print(f"  ✗ {status}")

    print(f"\nIdentity:")
    if properties['has_one']:
        one = properties['one']
        name_str = str(one)
        if isinstance(one, tuple):
            # Matrix or polynomial - don't display full details here
            print(f"  One element: <display as matrix/polynomial>")
        else:
            print(f"  One: {one}")
    else:
        print("  No multiplicative identity (rng, not unital ring)")

    print(f"\nCommutative Ring with Identity: {properties.get('commutative_with_identity', 'N/A')}")

    # Extra: show a concrete non-commutative example for matrix rings
    if "Matrix Ring" in name:
        a = ((1, 1), (0, 1))
        b = ((1, 0), (1, 1))

        def add(m1, m2):
            return (
                ((m1[0][0] + m2[0][0]) % 3, (m1[0][1] + m2[0][1]) % 3),
                ((m1[1][0] + m2[1][0]) % 3, (m1[1][1] + m2[1][1]) % 3)
            )

        def mult(m1, m2):
            return (
                (
                    (m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0]) % 3,
                    (m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1]) % 3
                ),
                (
                    (m1[1][0]*m2[0][0] + m1[1][1]*m2[1][0]) % 3,
                    (m1[1][0]*m2[0][1] + m1[1][1]*m2[1][1]) % 3
                )
            )

        def mat_str(m):
            return f"[[{m[0][0]}, {m[0][1]}], [{m[1][0]}, {m[1][1]}]]"

        ab = mult(a, b)
        ba = mult(b, a)
        print("\nNon-commutative example (A*B != B*A):")
        print(f"  A = {mat_str(a)}")
        print(f"  B = {mat_str(b)}")
        print(f"  A*B = {mat_str(ab)}")
        print(f"  B*A = {mat_str(ba)}")


def display_addition_table(add_op, elements):
    """
    Display the addition table.
    """
    print("\n--- ADDITION TABLE ---")
    header = "\t".join(str(e) for e in elements)
    print(header)
    print('-'*70)

    for row_elem in elements:
        row = "\t".join(add_op(row_elem, col) for col in elements)
        print(str(row_elem) + "\t" + row)


def display_multiplication_table(mult_op, elements):
    """
    Display the multiplication table.
    """
    print("\n--- MULTIPLICATION TABLE ---")
    header = "\t".join(str(e) for e in elements)
    print(header)
    print('-'*70)

    for row_elem in elements:
        row = "\t".join(mult_op(row_elem, col) for col in elements)
        print(str(row_elem) + "\t" + row)


# Main demonstration
if __name__ == "__main__":
    print("\n" + "="*70)
    print("RINGS AND COMMUTATIVE RINGS - ALGEBRAIC STRUCTURE")
    print("="*70)

    print("\n--- RING CONCEPT ---")
    print("")
    print("A RING consists of a set with TWO binary operations (+ and *) satisfying:")
    print("  1. (G, +) is an Abelian group")
    print("     - Associativity, identity (0), inverses, commutativity")
    print("  2. Multiplication is associative")
    print("  3. Distributive laws hold")
    print("")
    print("A COMMUTATIVE RING additionally satisfies:")
    print("  a * b = b * a for all a, b in G")
    print("")

    # Create ring examples
    ring_examples = {
        "Z_3": integers_mod_n(3),   # Field (special commutative ring)
        "Z_4": integers_mod_n(4),   # Commutative ring with zero divisors
        "Z_6": integers_mod_n(6),   # Commutative ring with more structure
        "Matrix_2x2": matrix_ring_2x2(),  # Non-commutative ring
    }

    for name in ["Z_3", "Z_4", "Z_6"]:
        ring = ring_examples[name]
        display_ring_info(ring)

    print("\n--- COMMUTATIVE vs NON-COMMUTATIVE ---")
    matrix_ring = ring_examples["Matrix_2x2"]
    display_ring_info(matrix_ring)

    print(f"\nNotice: {matrix_ring['name']} is a RING but NOT a COMMUTATIVE RING!")
    print("  Matrix multiplication: AB ≠ BA in general")

    print("\n--- SPECIAL CASE: Z_n WHERE n IS PRIME ---")
    print("")
    z5 = integers_mod_n(5)
    display_ring_info(z5)

    print("")
    print("When n is prime, Z_p is a FIELD (a special type of commutative ring)")

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("")
    print("RING types:")
    print("  - Z_n (integers mod n): Commutative ring with identity")
    print("  - M_n(F) (matrices): Non-commutative ring with identity")
    print("")
    print("COMPUTATIVE RING: A ring where multiplication commutes")
    print("- All Z_n are commutative rings")
    print("- Matrix rings are NOT commutative")
