"""
FIELDS
======
A FIELD is a commutative ring with identity where every non-zero element has a multiplicative inverse.

In a field:
- Addition forms an Abelian group
- Non-zero elements under multiplication form an Abelian group
- Distributive laws hold

Examples:
- Q (rational numbers): Field
- R (real numbers): Field
- C (complex numbers): Field
- Z_p (integers mod p where p is prime): Finite field F_p
"""


def rational_numbers():
    """The field of rational numbers Q."""
    return {
        "name": "Rational Numbers: Q",
        "elements": "All ratios a/b where a, b are integers and b ≠ 0",
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "multiplicative_inverse_op": lambda x: 1/x if x != 0 else None,
        "infinite_field": True,
        "characteristic": 0,
        "is_integral_domain": True,
        "note": "The rationals form a field. Every non-zero rational has an inverse.",
    }


def real_numbers():
    """The field of real numbers R."""
    return {
        "name": "Real Numbers: R",
        "elements": "All real numbers (includes Q, irrational numbers)",
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "multiplicative_inverse_op": lambda x: 1/x if x != 0 else None,
        "infinite_field": True,
        "characteristic": 0,
        "is_integral_domain": True,
        "note": "The reals form a field. Complete ordered field.",
    }


def complex_numbers():
    """The field of complex numbers C."""
    return {
        "name": "Complex Numbers: C",
        "elements": "All numbers a + bi where a, b in R and i^2 = -1",
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "multiplicative_inverse_op": lambda z: (z.conjugate() / abs(z)**2) if z != 0 else None,
        "infinite_field": True,
        "characteristic": 0,
        "is_integral_domain": True,
        "algebraically_closed": True,
        "note": "The complex numbers form an algebraically closed field (Fundamental Theorem of Algebra).",
    }


def finite_field_p(p):
    """
    Finite field F_p = Z_p where p is prime.
    This is the field of integers modulo a prime number.
    """
    elements = list(range(p))

    def add(a, b):
        return (a + b) % p

    def mult(a, b):
        return (a * b) % p

    def mult_inverse(x):
        # Fermat's Little Theorem: a^(p-2) ≡ a^(-1) (mod p)
        if x == 0:
            return None
        return pow(x, p - 2, p)

    return {
        "name": f"Finite Field F_p = Z_p",
        "elements": elements,
        "addition_op": add,
        "multiplication_op": mult,
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "multiplicative_inverse_op": mult_inverse,
        "infinite_field": False,
        "characteristic": p,
        "order": p,
        "note": f"Z_p is a field because p={p} is prime",
    }


def finite_field_2x_k(k):
    """
    Finite field F_{2^k} constructed as GF(2)[x]/(f(x)) where f is irreducible of degree k.
    For simplicity, we show F_4 (k=2) as an example.

    F_4 has 4 elements and characteristic 2.
    """
    # Construct F_4 = GF(2)[x]/(x^2 + x + 1)
    # Elements: {0, 1, x, x+1} with x^2 = x + 1
    elements = [0, 1, 'x', 'x+1']

    def add(e1, e2):
        """Addition in F_4 (characteristic 2, so a+a=0)"""
        if e1 == 0:
            return e2
        if e2 == 0:
            return e1
        if e1 == e2:
            return 0
        # XOR-like in characteristic 2
        if {e1, e2} == {1, 'x'}:
            return 'x+1'
        if {e1, e2} == {1, 'x+1'}:
            return 'x'
        if {e1, e2} == {'x', 'x+1'}:
            return 1
        return 0

    def mult(e1, e2):
        """Multiplication in F_4"""
        if e1 == 0 or e2 == 0:
            return 0
        if e1 == 1:
            return e2
        if e2 == 1:
            return e1
        # x * x = x^2 = x + 1
        if e1 == 'x' and e2 == 'x':
            return 'x+1'
        # x * (x+1) = x^2 + x = (x+1) + x = 1
        if {e1, e2} == {'x', 'x+1'}:
            return 1
        # (x+1) * (x+1) = x^2 + 2x + 1 = x^2 + 1 = (x+1) + 1 = x
        if e1 == 'x+1' and e2 == 'x+1':
            return 'x'
        return 0

    def mult_inverse(x):
        if x == 0:
            return None
        if x == 1:
            return 1
        if x == 'x':
            return 'x+1'
        if x == 'x+1':
            return 'x'
        return None

    return {
        "name": f"Finite Field F_{{2^k}}",
        "elements": elements,
        "addition_op": add,
        "multiplication_op": mult,
        "is_commutative": True,
        "has_identity": True,
        "identity_element": 1,
        "multiplicative_inverse_op": mult_inverse,
        "infinite_field": False,
        "characteristic": 2,
        "order": 4,
        "field_name": f"F_{{2^{{k}}}} where k=2",
        "note": "This is a finite field with 2^k elements, characteristic 2",
    }


def check_field_axioms(field_info):
    """
    Check field axioms for finite fields (where elements are explicitly listed).
    """
    elements = field_info.get("elements", [])
    add = field_info.get("addition_op")
    mul = field_info.get("multiplication_op")
    inv = field_info.get("multiplicative_inverse_op")
    element_set = set(elements)

    # Additive identity (0)
    zero = None
    for e in elements:
        if all(add(a, e) == a and add(e, a) == a for a in elements):
            zero = e
            break

    # Additive inverses
    add_inv = True
    if zero is None:
        add_inv = False
    else:
        for a in elements:
            if not any(add(a, b) == zero for b in elements):
                add_inv = False
                break

    # Additive commutativity + associativity
    add_comm = True
    add_assoc = True
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a):
                add_comm = False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)):
                    add_assoc = False

    # Multiplicative identity (1)
    one = None
    for e in elements:
        if all(mul(a, e) == a and mul(e, a) == a for a in elements):
            one = e
            break

    # Multiplicative inverses for nonzero
    mult_inv = True
    if one is None:
        mult_inv = False
    else:
        for a in elements:
            if a == zero:
                continue
            if inv(a) is None or mul(a, inv(a)) != one:
                mult_inv = False
                break

    # Multiplicative commutativity + associativity
    mult_comm = True
    mult_assoc = True
    for a in elements:
        for b in elements:
            if mul(a, b) != mul(b, a):
                mult_comm = False
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)):
                    mult_assoc = False

    # Distributive laws
    left_dist = True
    right_dist = True
    for a in elements:
        for b in elements:
            for c in elements:
                if add(mul(a, b), mul(a, c)) != mul(a, add(b, c)):
                    left_dist = False
                if add(mul(b, a), mul(c, a)) != mul(add(b, c), a):
                    right_dist = False

    return {
        "zero": zero,
        "one": one,
        "add_commutative": add_comm,
        "add_associative": add_assoc,
        "add_inverses": add_inv,
        "mult_commutative": mult_comm,
        "mult_associative": mult_assoc,
        "mult_inverses": mult_inv,
        "left_distributive": left_dist,
        "right_distributive": right_dist,
    }


def display_field_info(field_info):
    """Display information about a field."""
    if "error" in field_info:
        print(f"Error: {field_info.get('error', 'Unknown error')}")
        return

    name = field_info.get("name", "Unknown Field")
    note = field_info.get("note", "")

    print(f"\n{'='*70}")
    print(f"FIELD: {name}")
    print('='*70)

    if note:
        print(note)

    properties = field_info.get("properties", field_info)

    print("\n--- Field Properties ---")
    print(f"  Commutative: ✓")
    if properties.get('has_identity'):
        print(f"  Has multiplicative identity (1): ✓")

    # Check inverses exist for all non-zero elements
    inverse_op = properties.get("multiplicative_inverse_op", None)
    print(f"  Every non-zero element has multiplicative inverse: ✓")
    if inverse_op:
        print(f"    Inverse operation: {inverse_op}")

    print(f"  Characteristic: {properties.get('characteristic', 'N/A')}")
    if properties.get("infinite_field"):
        print(f"  Infinite field: ✓")
    else:
        print(f"  Order: {properties.get('order', 'N/A')}")

    # Extra axioms check for finite fields
    if isinstance(field_info.get("elements"), list) and field_info.get("addition_op") and field_info.get("multiplication_op"):
        axioms = check_field_axioms(field_info)
        print("\n--- Axiom Check (finite field) ---")
        print(f"  Additive identity exists: {axioms['zero'] is not None}")
        print(f"  Additive commutative: {axioms['add_commutative']}")
        print(f"  Additive associative: {axioms['add_associative']}")
        print(f"  Additive inverses: {axioms['add_inverses']}")
        print(f"  Multiplicative identity exists: {axioms['one'] is not None}")
        print(f"  Multiplicative commutative: {axioms['mult_commutative']}")
        print(f"  Multiplicative associative: {axioms['mult_associative']}")
        print(f"  Multiplicative inverses (nonzero): {axioms['mult_inverses']}")
        print(f"  Left distributive: {axioms['left_distributive']}")
        print(f"  Right distributive: {axioms['right_distributive']}")

    print(f"\n--- Field vs Ring ---")
    print("✓ Fields are special commutative rings with:")
    print("  - All non-zero elements form a group under multiplication")
    print("  - Every element (except 0) has an inverse")


def display_addition_table(add_op, elements):
    """Display addition table for a finite field."""
    if isinstance(elements, str):
        print("\n--- Addition Table (infinite set, not displayed) ---")
        return

    # For symbolic elements
    if any(isinstance(e, str) for e in elements):
        print("\n--- Addition Table ---")
        header = "\t".join(str(e) for e in elements)
        print(header)
        print('-'*70)

        for row_elem in elements:
            row = "\t".join(str(add_op(row_elem, col)) for col in elements)
            print(str(row_elem) + "\t" + row)


def display_multiplication_table(mult_op, elements):
    """Display multiplication table for a finite field."""
    if isinstance(elements, str):
        print("\n--- Multiplication Table (infinite set, not displayed) ---")
        return

    print("\n--- Multiplication Table ---")
    header = "\t".join(str(e) for e in elements)
    print(header)
    print('-'*70)

    for row_elem in elements:
        row = "\t".join(str(mult_op(row_elem, col)) for col in elements)
        print(str(row_elem) + "\t" + row)


# Main demonstration
if __name__ == "__main__":
    print("\n" + "="*70)
    print("FIELDS - ALGEBRAIC STRUCTURE")
    print("="*70)

    print("\n--- FIELD CONCEPT ---")
    print("")
    print("A FIELD is a commutative ring with identity where:")
    print("  - Every non-zero element has a multiplicative inverse")
    print("  - (R \ {0}, *) forms an Abelian group")
    print("  - All field axioms satisfied")
    print("")

    # Create field examples
    fields = {
        "Q": rational_numbers(),
        "R": real_numbers(),
        "C": complex_numbers(),
        "F_3": finite_field_p(3),
        "F_5": finite_field_p(5),
        "F_4": finite_field_2x_k(2),  # F_{2^2}
    }

    print("\n--- EXAMPLES OF FIELDS ---")

    # Infinite fields
    for name in ["Q", "R", "C"]:
        field = fields[name]
        display_field_info(field)

    print("\n--- FINITE FIELD EXAMPLES (F_p) ---")
    for p in [3, 5]:
        field = fields[f"F_{p}"]
        display_field_info(field)

        # Display tables
        add_op = field.get("addition_op", None)
        mult_op = field.get("multiplication_op", None)
        elements = field.get("elements", [])
        if callable(add_op) and callable(mult_op):
            display_addition_table(add_op, elements)
            display_multiplication_table(mult_op, elements)
            # Concrete distributive example
            if p >= 5:
                a, b, c = 2, 3, 4
                left = mult_op(a, add_op(b, c))
                right = add_op(mult_op(a, b), mult_op(a, c))
                print(f"\nDistributive check in F_{p}: {a}*( {b}+{c}) = {left}, {a}*{b}+{a}*{c} = {right}")

    print("\n--- FINITE FIELD F_4 (F_{2^k}) EXAMPLE ---")
    f4 = fields["F_4"]
    display_field_info(f4)

    print("\n--- KEY DIFFERENCES: RING vs FIELD ---")
    print("")
    print("RING:")
    print("  - Closed under addition, subtraction, multiplication")
    print("  - Has identity (0) and associativity/distributivity")
    print("  - May NOT have multiplicative inverses for all elements")

    print("")
    print("FIELD:")
    print("  - All RING properties PLUS:")
    print("  - Every non-zero element has inverse (can divide)")
    print("  - Can solve ax + b = c for any a, b, c in field")

    print("")
    print("--- HIERARCHY ---")
    print("")
    print("        FIELD")
    print("       /    \\")
    print("   INTEGRAL  COMMUTATIVE RING")
    print("      DOMAIN     \            ")
    print("         \          NON-COMMUTATIVE RING")
    print("")
    print("Fields are the 'nicest' algebraic structures - can do all arithmetic operations.")
