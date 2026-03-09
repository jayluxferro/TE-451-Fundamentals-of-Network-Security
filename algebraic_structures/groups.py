"""
GROUPS
======
A group is a set G equipped with a binary operation * that satisfies:
1. Closure: For all a, b in G, a * b is in G
2. Associativity: (a * b) * c = a * (b * c) for all a, b, c in G
3. Identity: There exists e in G such that a * e = e * a = a for all a in G
4. Inverse: For each a in G, there exists a⁻¹ in G such that a * a⁻¹ = a⁻¹ * a = e
"""


def check_group_properties(operation, set_elements, identity=None):
    """
    Check if a given set with operation forms a group.

    Args:
        operation: A function that takes two elements and returns their product
        set_elements: A list of elements in the set
        identity: The identity element (if known)

    Returns:
        Dictionary with properties and whether it's a group
    """
    if identity is None:
        # Find identity element by checking which element acts as identity
        for e in set_elements:
            is_identity = True
            for a in set_elements:
                if operation(a, e) != a or operation(e, a) != a:
                    is_identity = False
                    break
            if is_identity:
                identity = e
                break

    if identity is None:
        return {
            "is_group": False,
            "closure": True,  # Assume closure for finite sets with well-defined operation
            "associativity": False,  # Can't verify without associativity check
            "identity": None,
            "inverse": False,
            "reason": "Identity element not found"
        }

    # Check closure: a * b is in the set for all a, b
    element_set = set(set_elements)
    closure = True
    for a in set_elements:
        for b in set_elements:
            if operation(a, b) not in element_set:
                closure = False
                break
        if not closure:
            break

    # Check inverse: For each a, there exists b such that a * b = identity and b * a = identity
    def has_inverses():
        for a in set_elements:
            found_inverse = False
            for b in set_elements:
                if operation(a, b) == identity and operation(b, a) == identity:
                    found_inverse = True
                    break
            if not found_inverse:
                return False
        return True

    inverse = has_inverses()

    # Check associativity: (a*b)*c == a*(b*c)
    associativity = True
    for a in set_elements:
        for b in set_elements:
            for c in set_elements:
                if operation(operation(a, b), c) != operation(a, operation(b, c)):
                    associativity = False
                    break
            if not associativity:
                break
        if not associativity:
            break

    return {
        "is_group": closure and associativity and (identity is not None) and inverse,
        "closure": closure,
        "associativity": associativity,
        "identity": identity,
        "inverse": inverse
    }


def cyclic_group_zn(n):
    """
    Create a cyclic group of order n: Z_n = {0, 1, ..., n-1} under addition mod n.

    Example:
    - Cyclic group of order 4: {0, 1, 2, 3} with addition mod 4
    """
    elements = list(range(n))
    def operation(a, b):
        return (a + b) % n

    return {
        "name": f"Cyclic Group Z_{{n}}",
        "order": n,
        "elements": elements,
        "operation": operation,
        "is_abelian": True,
        "check": check_group_properties(operation, elements)
    }


def symmetric_group_sn(n):
    """
    The symmetric group S_n: all permutations of n elements under composition.
    For educational purposes, we'll show S_3 (order 6) as an example.
    """
    if n < 2:
        return {"error": f"Symmetric group S_n requires n >= 2. Created S_{n} which has no non-trivial permutations."}

    # Represent permutations as tuples
    from itertools import permutations
    elements = list(permutations(range(n)))

    def operation(a, b):
        """Composition of permutations: apply b first, then a"""
        return tuple(a[i] for i in b)

    # Find identity (which should be (0, 1, ..., n-1))
    identity = tuple(range(n))

    return {
        "name": f"Symmetric Group S_{{n}}",
        "order": len(elements),
        "elements": elements,
        "operation": operation,
        "is_abelian": False,
        "check": check_group_properties(operation, elements, identity)
    }


def Klein_four_group():
    """
    Klein four-group V4 = {e, a, b, c} where every non-identity element has order 2.
    Isomorphic to Z_2 × Z_2.
    """
    elements = ['e', 'a', 'b', 'c']
    # Cayley table (Cayley product)
    operation_table = {
        ('e', 'e'): 'e', ('e', 'a'): 'a', ('e', 'b'): 'b', ('e', 'c'): 'c',
        ('a', 'e'): 'a', ('a', 'a'): 'e', ('a', 'b'): 'c', ('a', 'c'): 'b',
        ('b', 'e'): 'b', ('b', 'a'): 'c', ('b', 'b'): 'e', ('b', 'c'): 'a',
        ('c', 'e'): 'c', ('c', 'a'): 'b', ('c', 'b'): 'a', ('c', 'c'): 'e'
    }

    def operation(x, y):
        return operation_table[(x, y)]

    identity = 'e'

    return {
        "name": "Klein Four-Group V4",
        "order": 4,
        "elements": elements,
        "operation": operation_table,
        "is_abelian": True,
        "check": check_group_properties(operation, elements, identity)
    }


def show_operation_table(group_info):
    """
    Display the Cayley table (operation table) for a group.
    """
    if "error" in group_info:
        print(f"Error: {group_info['error']}")
        return

    name = group_info.get("name", "Unknown Group")
    elements = group_info.get("elements", [])
    operation_table = group_info.get("operation", None)
    is_abelian = group_info.get("is_abelian", False)

    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"Order: {group_info.get('order', len(elements))}")
    if is_abelian:
        print("Abelian: Yes")
    else:
        print("Abelian: No (non-commutative)")
    print('='*60)

    if isinstance(operation_table, dict):
        # Print Cayley table
        header = "\t".join(str(e) for e in elements)
        print(header)
        print('-'*60)

        for row_elem in elements:
            row = "\t".join(str(operation_table[(row_elem, col)]) for col in elements)
            print(str(row_elem) + "\t" + row)
    elif callable(operation_table):
        header = "\t".join(str(e) for e in elements)
        print(header)
        print('-'*60)

        for row_elem in elements:
            row = "\t".join(str(operation_table(row_elem, col)) for col in elements)
            print(str(row_elem) + "\t" + row)

    print("\nGroup Properties:")
    check = group_info.get("check", {})
    for prop, value in check.items():
        if isinstance(value, bool):
            status = "✓" if value else "✗"
            print(f"  {prop.capitalize()}: {status}")
        else:
            print(f"  {prop}: {value}")


# Main demonstration
if __name__ == "__main__":
    print("\n" + "="*60)
    print("GROUPS - ALGEBRAIC STRUCTURE")
    print("="*60)

    # Define all concepts
    groups_info = {
        "Z_3": cyclic_group_zn(3),  # {0,1,2} under addition mod 3
        "Z_4": cyclic_group_zn(4),  # {0,1,2,3} under addition mod 4
        "Z_5": cyclic_group_zn(5),  # {0,1,2,3,4} under addition mod 5
        "V4": Klein_four_group(),   # Non-cyclic group of order 4
        "S_3": symmetric_group_sn(3)  # Permutations of {0,1,2}
    }

    print("\n--- GROUP CONCEPT ---")
    print("")
    print("A GROUP consists of a set with a binary operation satisfying:")
    print("  1. Closure")
    print("  2. Associativity")
    print("  3. Identity element exists")
    print("  4. Every element has an inverse")
    print("")
    print("Concrete examples in Z_5 (addition mod 5):")
    print("  Identity: 0, since 3 + 0 = 3")
    print("  Inverse: 2 has inverse 3 because 2 + 3 = 0 (mod 5)")
    print("  Associativity: (1 + 2) + 3 = 1 + (2 + 3) = 1 (mod 5)")

    # Display each group
    for name in ["Z_3", "Z_4", "V4", "Z_5"]:
        show_operation_table(groups_info[name])

    print("\n--- S_3 (Symmetric Group) ---")
    # For S_3, elements are complex tuples, just show info
    s3 = groups_info["S_3"]
    if "error" not in s3:
        print(f"Elements ({len(s3['elements'])} total):")
        for elem in s3['elements']:
            print(f"  {elem}")
        print("")
        print("S_3 has 6 elements (permutations of 3 items)")
        print("It is non-abelian (not commutative): a * b ≠ b * a for some a, b")

    print("\n" + "="*60)
    print("SUMMARY: Types of Groups")
    print("="*60)
    print("- Cyclic groups (Z_n): Generated by one element")
    print("- Klein four-group (V4): Smallest non-cyclic group")
    print("- Symmetric groups (S_n): Permutation groups, non-abelian for n≥3")
