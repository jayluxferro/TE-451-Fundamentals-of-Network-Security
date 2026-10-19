"""
Textbook RSA -- key generation, encryption, decryption from first principles.

Ties together Lecture 2 (primes, modular inverse, Euler's phi) and Lecture 4
(RSA).  Everything here is plain Python so you can see every step; the prime
test is the same Miller-Rabin as number_theory/miller_rabin_algorithm.py.

    !!  EDUCATIONAL ONLY  !!
    This is *textbook* RSA with no padding (no OAEP), small-ish keys and a
    deterministic worked example.  Real systems must use a vetted library
    (e.g. `cryptography`) with OAEP/PSS -- never hand-rolled RSA.  The point
    here is to make the maths visible, not to be secure.

Run:   python3 rsa_textbook.py
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import random
import sys


# --- Primality (Miller-Rabin) --------------------------------------------
# Same idea as number_theory/miller_rabin_algorithm.py: a fast probabilistic
# test.  We need it because we cannot *factor* to check primality at crypto
# sizes -- we can only test.
def is_probable_prime(n: int, k: int = 40) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    """Draw random odd numbers of the given bit length until one is prime."""
    while True:
        # force top bit (size) and bottom bit (odd)
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


# --- Key generation -------------------------------------------------------
def generate_keypair(bits: int = 512, e: int = 65537):
    """Return ((e, n), (d, n)) -- public and private keys.

    Steps mirror the lecture slide exactly:
      1. pick primes p, q           4. d = e^-1 (mod phi)
      2. n = p*q
      3. phi = (p-1)(q-1)
    """
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while q == p:
        q = generate_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    # e must be coprime to phi; 65537 usually is, but verify and bump if not.
    from math import gcd
    while gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)          # modular inverse (extended Euclid, Lecture 2)
    return (e, n), (d, n)


def encrypt(public_key, m: int) -> int:
    e, n = public_key
    if m >= n:
        raise ValueError("message integer must be < n; real RSA chunks/pads it")
    return pow(m, e, n)          # c = m^e mod n


def decrypt(private_key, c: int) -> int:
    d, n = private_key
    return pow(c, d, n)          # m = c^d mod n


# --- Tiny demo ------------------------------------------------------------
def _text_to_int(s: str) -> int:
    return int.from_bytes(s.encode("utf-8"), "big")


def _int_to_text(i: int) -> str:
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, "big").decode("utf-8", errors="replace")


def main() -> None:
    print("=== Textbook RSA (educational) ===\n")

    # 1) The worked example from the Lecture 4 slide (tiny, hand-checkable).
    print("Worked example (slide):  p=17, q=11")
    p, q = 17, 11
    n, phi = p * q, (17 - 1) * (11 - 1)
    e = 7
    d = pow(e, -1, phi)
    print(f"  n={n}, phi={phi}, e={e}, d={d}")
    m = 88
    c = pow(m, e, n)
    print(f"  encrypt(88) = {c};  decrypt({c}) = {pow(c, d, n)}\n")

    # 2) A realistic-shape key pair, encrypting a short string.
    bits = 512
    print(f"Generating a {bits}-bit demo key (this is small -- real RSA >= 2048)...")
    public, private = generate_keypair(bits)
    e, n = public
    print(f"  public  (e, n): e={e}, n has {n.bit_length()} bits")
    print(f"  private (d, n): d has {private[0].bit_length()} bits\n")

    message = "TE451"
    m = _text_to_int(message)
    c = encrypt(public, m)
    back = _int_to_text(decrypt(private, c))
    print(f"  message : {message!r}  -> int {m}")
    print(f"  cipher  : {c}")
    print(f"  decrypt : {back!r}  {'OK' if back == message else 'MISMATCH'}")


if __name__ == "__main__":
    sys.exit(main())
