"""
How key length defeats brute force (Lecture 3).

Each extra *bit* of key doubles the number of possibilities, so brute-force cost
grows exponentially.  This script measures how fast your machine can enumerate
keys, then extrapolates to real key sizes -- showing why a 56-bit DES key is
crackable but a 128-bit AES key is not.

    NOTE: the original version of this file tried to `print()` every one of
    2**word_size values.  For word_size=64 that is ~1.8e19 lines -- it would
    never finish.  We now *measure a small sample* and extrapolate instead.

Run:   python3 compute_time_per_word_size.py
"""

__author__ = "TE 451 - Fundamentals of Network Security"

import sys
from time import perf_counter

# Interesting key sizes to reason about.
KEY_SIZES = {
    8: "toy",
    40: "old 'export-grade' crypto",
    56: "DES (broken by brute force)",
    112: "3DES (effective)",
    128: "AES-128",
    256: "AES-256",
}


def measure_rate(sample_bits: int = 24) -> float:
    """Enumerate 2**sample_bits keys (no printing) and return keys/second."""
    n = 1 << sample_bits
    start = perf_counter()
    total = 0
    for i in range(n):
        total ^= i            # touch each key cheaply so the loop isn't optimised away
    elapsed = perf_counter() - start
    return n / elapsed if elapsed > 0 else float("inf")


def human_time(seconds: float) -> str:
    """Render a (possibly astronomical) duration readably."""
    if seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    minute, hour, day, year = 60, 3600, 86400, 31_557_600
    for unit, name in ((year, "years"), (day, "days"), (hour, "hours"),
                       (minute, "minutes"), (1, "seconds")):
        if seconds >= unit:
            value = seconds / unit
            if name == "years" and value > 1e6:
                age_of_universe = 1.38e10
                return f"{value:.2e} years ({value / age_of_universe:.1e}x the age of the universe)"
            return f"{value:,.1f} {name}"
    return f"{seconds:.1f} seconds"


def main() -> None:
    print("Measuring this machine's raw key-enumeration rate...")
    rate = measure_rate()
    print(f"  ~{rate:,.0f} keys/second (single-threaded Python)\n")

    print(f"{'bits':>5}  {'keyspace':>12}  {'brute-force time':>22}   note")
    print("-" * 70)
    for bits, note in KEY_SIZES.items():
        keyspace = 1 << bits
        # average case: expect to find the key after half the space
        seconds = (keyspace / 2) / rate
        print(f"{bits:>5}  {f'2^{bits}':>12}  {human_time(seconds):>22}   {note}")

    print("\nLesson: adding one bit DOUBLES the attacker's work. 56 bits falls;")
    print("128 bits is out of reach for brute force -- so attacks target keys,")
    print("implementations and people instead (Lectures 5-7, 11).")


if __name__ == "__main__":
    sys.exit(main())
