"""
MACs vs bare hashes -- why integrity needs a key (Lecture 5).

A plain hash only detects *accidental* change: an attacker who rewrites the
message can just recompute the digest.  A MAC mixes in a shared secret, so only
a key-holder can produce a valid tag.  We also show why you must compare tags in
*constant time*.

Uses only the standard library (`hmac`, `hashlib`, `secrets`).

Run:   python3 hmac_demo.py
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import hashlib
import hmac
import secrets
import sys


def tag(key: bytes, message: bytes, algo: str = "sha256") -> str:
    """HMAC tag as hex.  `hmac`/`hashlib` implement the construction from the
    slide: H((k^opad) || H((k^ipad) || m))."""
    return hmac.new(key, message, algo).hexdigest()


def verify(key: bytes, message: bytes, received_tag: str, algo: str = "sha256") -> bool:
    """Recompute and compare.  `hmac.compare_digest` is constant-time, so an
    attacker can't learn the tag byte-by-byte from timing."""
    expected = tag(key, message, algo)
    return hmac.compare_digest(expected, received_tag)


def main() -> None:
    key = secrets.token_bytes(32)              # the shared secret
    message = b"transfer 100 GHS to account 42"

    t = tag(key, message)
    print("=== HMAC (authenticated integrity) ===")
    print(f"  message : {message.decode()}")
    print(f"  HMAC    : {t}")
    print(f"  verify(original)        -> {verify(key, message, t)}")

    # Attacker tampers with the message but cannot forge the tag (no key).
    tampered = b"transfer 900 GHS to account 99"
    print(f"\n  tampered: {tampered.decode()}")
    print(f"  verify(tampered, old tag) -> {verify(key, tampered, t)}  <- rejected")

    # Contrast: a bare hash offers no such protection -- the attacker simply
    # recomputes it, and the receiver has no way to tell.
    forged = hashlib.sha256(tampered).hexdigest()
    print("\n=== Bare hash (NO key) ===")
    print(f"  attacker ships tampered message + its own SHA-256 = {forged[:24]}...")
    print("  receiver recomputes the same hash -> looks 'valid'. Integrity broken.")
    print("\n  Lesson: use a MAC (or AEAD) whenever data crosses untrusted ground.")


if __name__ == "__main__":
    sys.exit(main())
