def chinese_remainder(n, a):
    """
    Chinese Remainder Theorem solver.

    Args:
        n: A list of pairwise coprime integers.
        a: A list of integers corresponding to each modulus in `n`.

    Returns:
        x: The solution to the system of congruences.
    """

    # Compute LCM of all moduli
    N = 1
    for ni in n:
        N *= ni

    # Compute partial products and inverses
    x = 0
    for ai, ni in zip(a, n):
        Ni = pow(N // ni, -1, ni)  # Inverse is already reduced modulo ni
        xi = (ai * Ni) % N
        x += xi
    x %= N

    return x, N


# Example usage:
n = [2, 3, 5]
a = [1, 2, 0]  # Congruences: x ≡ 1 (mod 2), x ≡ 2 (mod 3), x ≡ 0 (mod 5)
x, N = chinese_remainder(n, a)
print(f"Solution to system of congruences: x ≡ {x} (mod {N})")