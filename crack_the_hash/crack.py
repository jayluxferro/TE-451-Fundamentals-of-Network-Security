"""
Dictionary hash cracker -- the attacker's side of password storage (Lecture 5/7).

Given a target digest and a wordlist, compute the hash of each candidate (plus
simple mutations) and look for a match.  This is exactly why password stores
must use a *salt* and a *slow* hash (bcrypt/scrypt/Argon2): against a fast raw
hash like SHA-256, a laptop tries millions of guesses a second.

    Lawful use only: crack hashes you generated or are authorised to test.

Completes the exercise in the original starter (test1.py):
  - streams the wordlist (handles large files),
  - selectable algorithm (--algo sha256|md5|sha1|...),
  - optional mutations (--mutate): case variants + common suffixes.

Examples
--------
  # default demo target, bundled wordlist:
  python3 crack.py wordlist_crack_test.txt

  # explicit target + mutations + md5:
  python3 crack.py words.txt --target 5f4dcc3b5aa765d61d8327deb882cf99 --algo md5 --mutate
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import argparse
import hashlib
import sys

# Default target ships with the lab so `crack.py wordlist_crack_test.txt` works
# out of the box.  It is a SHA-256 digest of a word in the bundled list.
DEFAULT_TARGET = "cc58f07dd22a4663f112edfeeba4f72737d087b1b71db81937ef8bf6aa033d52"

COMMON_SUFFIXES = ("", "!", "1", "123", "2026", "@", "#")


def mutations(word: str):
    """Yield cheap, high-yield variants of a candidate word.

    These mirror how people actually mangle passwords -- capitalising, shouting,
    tacking on a year.  Kept small on purpose; real tools (hashcat, John) use
    rule engines, but the idea is identical."""
    bases = {word, word.lower(), word.upper(), word.capitalize()}
    for base in bases:
        for suffix in COMMON_SUFFIXES:
            yield base + suffix


def crack(dictionary_path: str, target: str, algo: str, mutate: bool) -> str | None:
    target = target.lower()
    try:
        hashlib.new(algo)
    except ValueError:
        sys.exit(f"[!] Unknown hash algorithm: {algo!r} "
                 f"(try: {', '.join(sorted(hashlib.algorithms_available))[:60]}...)")

    tried = 0
    with open(dictionary_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            candidates = mutations(word) if mutate else (word,)
            for cand in candidates:
                tried += 1
                digest = hashlib.new(algo, cand.encode("utf-8")).hexdigest()
                if digest == target:
                    print(f"[+] FOUND after {tried} guesses: {cand!r}")
                    return cand
    print(f"[-] Not found ({tried} candidates tried with {algo}).")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Dictionary hash cracker (educational).")
    ap.add_argument("dictionary", help="path to wordlist, one candidate per line")
    ap.add_argument("--target", default=DEFAULT_TARGET, help="target hash (hex)")
    ap.add_argument("--algo", default="sha256",
                    help="hash algorithm (sha256, md5, sha1, sha512, ...)")
    ap.add_argument("--mutate", action="store_true",
                    help="also try case variants and common suffixes")
    args = ap.parse_args()

    result = crack(args.dictionary, args.target, args.algo, args.mutate)
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
