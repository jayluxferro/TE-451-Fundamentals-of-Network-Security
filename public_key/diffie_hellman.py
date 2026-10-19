"""
Diffie-Hellman key exchange -- two parties agree a secret over a public channel.

Supports Lecture 4.  Watch the key point: Alice and Bob exchange g^a and g^b in
the clear, yet both end up holding g^(ab) -- which never crossed the wire.  An
eavesdropper who sees g, p, A, B still faces the *discrete logarithm* problem.

    !!  EDUCATIONAL ONLY  !!
    Plain DH has NO authentication, so it is vulnerable to a
    man-in-the-middle (demonstrated below).  Real protocols authenticate the
    exchange with signatures/certificates (see Lectures 5-6, 8) and use large,
    standardised groups.

Run:   python3 diffie_hellman.py
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import secrets
import sys


# A small, well-known safe-ish prime and generator for a *readable* demo.
# Real deployments use >= 2048-bit standardised groups (RFC 3526) or ECDH.
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF
G = 2


def public_share(private: int, g: int = G, p: int = P) -> int:
    """A = g^a mod p  -- safe to send in the clear."""
    return pow(g, private, p)


def shared_secret(their_public: int, my_private: int, p: int = P) -> int:
    """s = (their_public)^(my_private) mod p  -- never transmitted."""
    return pow(their_public, my_private, p)


def _short(x: int) -> str:
    h = f"{x:x}"
    return f"{h[:16]}...{h[-8:]} ({x.bit_length()} bits)"


def honest_exchange() -> None:
    print("=== Honest Diffie-Hellman exchange ===")
    a = secrets.randbelow(P - 2) + 2          # Alice's private
    b = secrets.randbelow(P - 2) + 2          # Bob's private

    A = public_share(a)                        # Alice -> Bob
    B = public_share(b)                        # Bob   -> Alice
    print(f"  Alice sends A = {_short(A)}")
    print(f"  Bob   sends B = {_short(B)}")

    alice_secret = shared_secret(B, a)
    bob_secret = shared_secret(A, b)
    print(f"  Alice computes s = {_short(alice_secret)}")
    print(f"  Bob   computes s = {_short(bob_secret)}")
    print(f"  Secrets match: {alice_secret == bob_secret}\n")


def mitm_exchange() -> None:
    """Show why unauthenticated DH is dangerous: Mallory sits in the middle and
    runs a separate exchange with each side, reading everything."""
    print("=== Man-in-the-middle (why DH needs authentication) ===")
    a = secrets.randbelow(P - 2) + 2           # Alice
    b = secrets.randbelow(P - 2) + 2           # Bob
    m = secrets.randbelow(P - 2) + 2           # Mallory

    A, B, M = public_share(a), public_share(b), public_share(m)

    # Mallory intercepts and substitutes her own public value both ways.
    alice_secret = shared_secret(M, a)         # Alice thinks she talks to Bob
    bob_secret = shared_secret(M, b)           # Bob thinks he talks to Alice
    mallory_with_alice = shared_secret(A, m)
    mallory_with_bob = shared_secret(B, m)

    print(f"  Alice<->Mallory secret agrees: {alice_secret == mallory_with_alice}")
    print(f"  Bob  <->Mallory secret agrees: {bob_secret == mallory_with_bob}")
    print(f"  Alice and Bob share a key:     {alice_secret == bob_secret}  <- they DON'T")
    print("  => Mallory relays/reads both sides. Authenticate the exchange!\n")


def main() -> None:
    honest_exchange()
    mitm_exchange()


if __name__ == "__main__":
    sys.exit(main())
