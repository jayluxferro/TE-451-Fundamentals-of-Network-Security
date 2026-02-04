def gcd(a, b):
    """
    Calculates the Greatest Common Divisor (GCD) of two numbers using the Euclidean algorithm.

    Parameters:
    a (int): The first number.
    b (int): The second number.

    Returns:
    int: The GCD of 'a' and 'b'.
    """
    while b != 0:
        # Use the remainder as the new divisor
        a, b = b, a % b
    return abs(a)


def main():
    # Test cases for the Euclidean algorithm

    print("Test case 1:")
    print(gcd(48, 18))  # Output: 6

    print("\nTest case 2:")
    print(gcd(-12, -15))  # Output: 3
    print(gcd(0, 5))  # Output: 5
    print(gcd(5, 0))  # Output: 5


if __name__ == "__main__":
    main()