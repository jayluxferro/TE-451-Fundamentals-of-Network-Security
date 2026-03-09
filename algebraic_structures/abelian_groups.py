# -*- coding: utf-8 -*-
"""
ABELIAN GROUPS
==============
An Abelian (or commutative) group is a group where the operation is commutative:
a * b = b * a for all a, b in G.

All cyclic groups are Abelian. Z_n under addition mod n is always Abelian.
"""

from groups import cyclic_group_zn, Klein_four_group
import itertools


def check_abelian(operation, set_elements, identity=None):
    """
    Check if a group is Abelian (commutative).

    Args:
        operation: A function that takes two elements and returns their product
        set_elements: A list of elements in the set
        identity: The identity element

    Returns:
        Dictionary with results
    """
    if identity is None:
        for e in set_elements:
            is_identity = all(operation(a, e) == a and operation(e, a) == a for a in set_elements)
            if is_identity:
                identity = e
                break

    # Check commutativity: a * b = b * a for all pairs
    is_commutative = True
    non_commutative_pairs = []
    for a in set_elements:
        for b in set_elements:
            if operation(a, b) != operation(b, a):
                is_commutative = False
                non_commutative_pairs.append((a, b))

    return {
        "is_abelian": is_commutative,
        "identity": identity,
        "non_commutative_pairs": non_commutative_pairs if not is_commutative else []
    }


def direct_product_of_groups(groups):
    """
    Create a direct product of groups: G1 × G2 × ... × Gn.

    The operation is performed component-wise:
    (a1, a2, ...) * (b1, b2, ...) = (a1*b1, a2*b2, ...)

    Direct products of Abelian groups are always Abelian.
    """
    # Get sizes of each group
    sizes = [len(g['elements']) for g in groups]

    # Generate all combinations
    cartesian_product = itertools.product(*[g['elements'] for g in groups])
    elements = list(cartesian_product)

    # Function to check which group operation to use for each component
    def get_component_op(group, i):
        if isinstance(group['operation'], dict):  # Use table lookup
            return lambda a, b: group['operation'][(a[i], b[i])]
        else:
            return group['operation']

    # Create operation for direct product
    def operation(elem1, elem2):
        result = []
        for i, g in enumerate(groups):
            if isinstance(g['operation'], dict):
                comp_op = lambda a, b, g=g, i=i: g['operation'][(a[i], b[i])]
            else:
                comp_op = g['operation']
            result.append(comp_op(elem1[i], elem2[i]))
        return tuple(result)

    # Find identity (tuple of each group's identity)
    identities = [g['check']['identity'] for g in groups]
    identity = tuple(identities)

    results = check_abelian(operation, elements, identity)

    # Create operation for display
    def product_operation(elem1, elem2):
        result = []
        for i, g in enumerate(groups):
            if isinstance(g['operation'], dict):
                comp_op = lambda a, b, g=g, i=i: g['operation'][(a[i], b[i])]
            else:
                comp_op = g['operation']
            result.append(comp_op(elem1[i], elem2[i]))
        return tuple(result)

    return {
        "name": "Direct Product: {}".format(' x '.join(g['name'] for g in groups)),
        "elements": elements,
        "order": len(elements),
        "is_abelian": results["is_abelian"],
        "identity": identity,
        "groups": groups,
        "operation": product_operation
    }


def elementary_abelian_group(p, n):
    """
    Elementary Abelian p-group: (Z_p)^n under component-wise addition.

    Example: (Z_2)^2 = Klein four-group V4
    """
    # Create Z_p group info for direct product
    z_p_group_info = {
        'name': f'Z_{p}',
        'elements': list(range(p)),
        'operation': lambda a, b: (a + b) % p,
        'check': {'identity': 0}
    }

    result = direct_product_of_groups([z_p_group_info] * n)

    return {
        "name": f"Elementary Abelian Group (Z_{{p}})^{n}",
        "elements": result["elements"],
        "order": p ** n,
        "is_abelian": True,
        "identity": result["identity"],
        "base_group": f'Z_{p}',
        "dimension": n,
        "operation": result["operation"]
    }


def infinite_cyclic_group():
    """
    Infinite cyclic group: Z = {..., -2, -1, 0, 1, 2, ...} under addition.
    This is the prototypical Abelian group.
    """
    # Represent as integers
    elements = list(range(-5, 6))  # Show a finite subset

    def operation(a, b):
        return a + b

    identity = 0

    check = check_abelian(operation, elements, identity)

    return {
        "name": "Infinite Cyclic Group (Z, +)",
        "elements": elements,
        "order": "infinite",
        "is_abelian": True,
        "identity": identity,
        "inverse_op": lambda x: -x,
        "note": "The full group is infinite; we show a finite subset for display",
        "operation": operation
    }


def dihedral_group_d4():
    """
    Dihedral group D_4: symmetries of a square (order 8).
    This is non-abelian.

    Elements: {e, r, r², r³, s, sr, sr², sr³}
    where r = rotation by 90°, s = reflection
    """
    elements = ['e', 'r', 'r^2', 'r^3', 's', 'sr', 'sr^2', 'sr^3']

    operation_table = {
        ('e', 'e'): 'e', ('e', 'r'): 'r', ('e', 'r^2'): 'r^2', ('e', 'r^3'): 'r^3',
        ('e', 's'): 's', ('e', 'sr'): 'sr', ('e', 'sr^2'): 'sr^2', ('e', 'sr^3'): 'sr^3',
        ('r', 'e'): 'r', ('r', 'r'): 'r^2', ('r', 'r^2'): 'r^3', ('r', 'r^3'): 'e',
        ('r', 's'): 'sr', ('r', 'sr'): 'sr^2', ('r', 'sr^2'): 'sr^3', ('r', 'sr^3'): 's',
        ('r^2', 'e'): 'r^2', ('r^2', 'r'): 'r^3', ('r^2', 'r^2'): 'e', ('r^2', 'r^3'): 'r',
        ('r^2', 's'): 'sr^2', ('r^2', 'sr'): 'sr^3', ('r^2', 'sr^2'): 's', ('r^2', 'sr^3'): 'sr',
        ('r^3', 'e'): 'r^3', ('r^3', 'r'): 'e', ('r^3', 'r^2'): 'r', ('r^3', 'r^3'): 'r^2',
        ('r^3', 's'): 'sr^3', ('r^3', 'sr'): 's', ('r^3', 'sr^2'): 'sr', ('r^3', 'sr^3'): 'sr^2',
        ('s', 'e'): 's', ('s', 'r'): 'sr^3', ('s', 'r^2'): 'sr^2', ('s', 'r^3'): 'sr',
        ('s', 's'): 'e', ('s', 'sr'): 'r^3', ('s', 'sr^2'): 'r^2', ('s', 'sr^3'): 'r',
        ('sr', 'e'): 'sr', ('sr', 'r'): 's', ('sr', 'r^2'): 'sr^3', ('sr', 'r^3'): 'sr^2',
        ('sr', 's'): 'r^2', ('sr', 'sr'): 'r', ('sr', 'sr^2'): 'r^3', ('sr', 'sr^3'): 'e',
        ('sr^2', 'e'): 'sr^2', ('sr^2', 'r'): 'sr', ('sr^2', 'r^2'): 's', ('sr^2', 'r^3'): 'sr^3',
        ('sr^2', 's'): 'r', ('sr^2', 'sr'): 'r^3', ('sr^2', 'sr^2'): 'r^2', ('sr^2', 'sr^3'): 'e',
        ('sr^3', 'e'): 'sr^3', ('sr^3', 'r'): 'sr^2', ('sr^3', 'r^2'): 'sr', ('sr^3', 'r^3'): 's',
        ('sr^3', 's'): 'r^3', ('sr^3', 'sr'): 'r', ('sr^3', 'sr^2'): 'r^2', ('sr^3', 'sr^3'): 'e'
    }

    def operation(x, y):
        return operation_table[(x, y)]

    identity = 'e'

    # This group is non-abelian (e.g., r * s ≠ s * r)
    result = check_abelian(operation, elements, identity)
    result["is_non_abelian"] = not result["is_abelian"]

    return {
        "name": "Dihedral Group D_4",
        "elements": elements,
        "order": 8,
        "is_abelian": False,
        "identity": identity,
        "geometric_meaning": "Symmetries of a square",
        "operation": operation
    }


def display_operation_table(group_info, show_abelian_check=False):
    """
    Display the Cayley table for an Abelian group.
    """
    if "error" in group_info:
        print(f"Error: {group_info.get('error', 'Unknown error')}")
        return

    name = group_info.get("name", "Unknown")
    elements = group_info.get("elements", [])
    identity = group_info.get("identity", None)
    is_abelian = group_info.get("is_abelian", False)

    print(f"\n{'='*70}")
    print(f"ABELIAN GROUP: {name}")
    print('='*70)

    if identity is not None:
        print(f"Identity element: {identity}")

    print(f"Is Abelian (commutative): {'Yes ✓' if is_abelian else 'No ✗'}")
    print(f"Order: {group_info.get('order', len(elements))}")

    if "groups" in group_info:
        print(f"Base groups: {', '.join(g['name'] for g in group_info['groups'])}")

    # Show only first few elements for display (to avoid very long tables)
    display_elements = elements[:min(len(elements), 9)] if len(elements) > 9 else elements

    print(f"\nElements shown: {display_elements}")

    # Cayley table header
    header = "\t".join(str(e) for e in display_elements)
    print(header)
    print('-'*70)

    # Operation rows - handle both callable operations and table-based operations
    operation_func = group_info.get('operation')
    if callable(operation_func):
        for row_elem in display_elements:
            if isinstance(row_elem, tuple):
                row_str = f"({', '.join(str(x) for x in row_elem)})"
            else:
                row_str = str(row_elem)
            row = "\t".join(str(operation_func(row_elem, col)) for col in display_elements)
            print(f"{row_str}\t{row}")
    elif isinstance(operation_func, dict):
        # Table-based operation (dict mapping tuples to results)
        table = operation_func
        for row_elem in display_elements:
            if isinstance(row_elem, tuple):
                row_str = f"({', '.join(str(x) for x in row_elem)})"
            else:
                row_str = str(row_elem)
            try:
                row = "\t".join(table[(row_elem, col)] for col in display_elements)
                print(f"{row_str}\t{row}")
            except KeyError:
                print(f"{row_str}\t???")
    elif 'operation_table' in group_info:
        # Alternative table-based (non-callable) operation
        table = group_info['operation_table']
        for row_elem in display_elements:
            if isinstance(row_elem, tuple):
                row_str = f"({', '.join(str(x) for x in row_elem)})"
            else:
                row_str = str(row_elem)
            row = "\t".join(table[(row_elem, col)] for col in display_elements)
            print(f"{row_str}\t{row}")
    else:
        print("No operation available for this group.")

    # If group is Abelian, highlight commutativity
    if is_abelian:
        print("\n✓ This group satisfies a * b = b * a (commutative)")

    print(f"\nGroup Properties:")
    check = group_info.get("check", {})
    for prop, value in check.items():
        if isinstance(value, bool):
            status = "✓" if value else "✗"
            print(f"  {prop.capitalize()}: {status}")


# Main demonstration
if __name__ == "__main__":
    print("\n" + "="*70)
    print("ABELIAN GROUPS - ALGEBRAIC STRUCTURE")
    print("="*70)

    print("\n--- ABELIAN GROUP CONCEPT ---")
    print("")
    print("An ABELIAN (commutative) group is a group where:")
    print("  - All group axioms are satisfied")
    print("  - Commutativity: a * b = b * a for all a, b in G")
    print("")
    print("Concrete example in Z_4: 1 + 3 = 3 + 1 = 0 (mod 4)")

    # Create Abelian groups
    abelian_groups_info = {
        "Z_3": cyclic_group_zn(3),
        "V4": Klein_four_group(),
        "D_4": dihedral_group_d4()  # Non-abelian example for contrast
    }

    print("\n--- EXAMPLE 1: Klein Four-Group V4 ---")
    print("V4 = {e, a, b, c} with each non-identity element having order 2")
    v4_info = Klein_four_group()
    display_operation_table(v4_info)

    print("\n--- EXAMPLE 2: (Z_2)^2 Direct Product ---")
    # (Z_2 × Z_2) is isomorphic to V4 but constructed differently
    direct_product_info = elementary_abelian_group(2, 2)
    display_operation_table(direct_product_info)

    print("\n--- EXAMPLE 3: Infinite Cyclic Group (Z, +) ---")
    z_inf = infinite_cyclic_group()
    display_operation_table(z_inf)

    print("\n--- CONTRAST: D_4 (Non-Abelian Example) ---")
    d4_info = dihedral_group_d4()
    display_operation_table(d4_info, show_abelian_check=True)

    print(f"\nNotice: {d4_info['name']} is NOT Abelian!")
    print("  - r * s ≠ s * r (rotation then reflection ≠ reflection then rotation)")
