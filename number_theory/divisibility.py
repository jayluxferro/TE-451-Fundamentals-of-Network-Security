def is_divisible(a: int, b: int) -> bool:
    """
    Checks if 'a' is divisible by 'b'.

    Parameters:
    a (int): The dividend.
    b (int): The divisor.

    Returns:
    bool: True if 'a' is divisible by 'b', False otherwise.
    """
    return a % b == 0


# Test cases for properties of divisibility
print("Test case 1:")
print(is_divisible(10, 2))  # True
print(is_divisible(-5, 3))  # False (since -5 is not divisible by 3)

print("\nTest case 2: Any b ≠ 0 divides 0")
for b in range(1, 11):
    print(f"{b} | 0") if is_divisible(0, b) else print(f"{b} does not divide 0")

print("\nTest case 3: If a | b and b | a, then a = ±b")
pairs = [(10, 2), (5, -10), (-20, 4)]
for a, b in pairs:
    if is_divisible(a, b) and is_divisible(b, a):
        print(f"{a} = ±{b}")
