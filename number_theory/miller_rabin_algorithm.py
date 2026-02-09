import random

def miller_rabin(n, k=5):  # number of iterations (k)
    """
    Miller-Rabin primality test.

    Args:
        n: The number to be tested for primality.
        k: The number of iterations. Default is 5.

    Returns:
        True if n is probably prime, False otherwise.
    """

    # Corner cases
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    # Find r and s such that n = 2^s * r + 1, where r is odd.
    s = 0
    r = n - 1
    while r % 2 == 0:
        s += 1
        r //= 2

    # k iterations of the Miller-Rabin test
    for _ in range(k):
        a = random.randrange(2, n)
        x = pow(a, r, n)

        # If x is not a witness to compositeness, continue.
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1: return False
                j += 1

            # If n-1 is a power of 2, we need to check whether
            # x^(r/2) is equal to 1 or n-1.
            if x != n - 1:
                return False

    return True


# Example usage:
print(miller_rabin(25))   # Composite number: returns False
print(miller_rabin(23))   # Prime number: returns True