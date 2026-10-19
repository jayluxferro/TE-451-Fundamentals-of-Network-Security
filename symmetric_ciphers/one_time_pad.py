"""
The one-time pad: perfect secrecy, and why 'one-time' is the whole point.

Supports Lecture 3 (Shannon perfect secrecy).  The OTP is the only cipher with a
mathematical proof of unbreakability -- but only if the key is truly random, as
long as the message, and NEVER reused.  Reuse it once and the secrecy collapses,
as the 'two-time pad' demo shows.

Standard library only (`secrets`).

Run:   python3 one_time_pad.py
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import secrets
import sys


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def otp_encrypt(plaintext: bytes, key: bytes) -> bytes:
    if len(key) < len(plaintext):
        raise ValueError("OTP key must be at least as long as the message")
    return xor(plaintext, key)


def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return xor(ciphertext, key)      # XOR is its own inverse


def demo_perfect_secrecy() -> None:
    print("=== One-time pad (used correctly) ===")
    message = b"ATTACK AT DAWN"
    key = secrets.token_bytes(len(message))     # random, same length, fresh
    ct = otp_encrypt(message, key)
    print(f"  plaintext : {message!r}")
    print(f"  key       : {key.hex()}")
    print(f"  ciphertext: {ct.hex()}")
    print(f"  decrypt   : {otp_decrypt(ct, key)!r}")

    # Perfect secrecy intuition: for ANY other plaintext of the same length,
    # there exists a key that would yield this exact ciphertext.  So the
    # ciphertext alone tells an attacker nothing.
    other = b"RETREAT NOW!!!"
    would_be_key = xor(ct, other)
    print(f"\n  The same ciphertext decrypts to {other!r}")
    print(f"  under key {would_be_key.hex()} -- so ct reveals nothing.\n")


def demo_two_time_pad() -> None:
    print("=== Key REUSE breaks everything (two-time pad) ===")
    key = secrets.token_bytes(16)               # ONE key...
    m1 = b"SELL 500 SHARES!"
    m2 = b"HOLD YOUR SHARES"
    c1 = otp_encrypt(m1, key)
    c2 = otp_encrypt(m2, key)                    # ...reused: the fatal mistake

    # Attacker never needs the key: XOR the two ciphertexts and the key cancels.
    #   c1 ^ c2 = (m1 ^ k) ^ (m2 ^ k) = m1 ^ m2
    leak = xor(c1, c2)
    print(f"  c1 ^ c2 = m1 ^ m2 = {leak.hex()}")
    print(f"  recovered m1 ^ m2 as text vs (m1 ^ m2): {leak == xor(m1, m2)}")
    print("  With any crib/guess about one message, the other falls out.")
    print("  => reuse a pad once and 'perfect secrecy' becomes none.")


def main() -> None:
    demo_perfect_secrecy()
    demo_two_time_pad()


if __name__ == "__main__":
    sys.exit(main())
