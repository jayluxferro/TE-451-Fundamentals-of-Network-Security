# TE 451 — Fundamentals of Network Security · code

Runnable Python examples that accompany the TE 451 lectures (KNUST, Dept. of
Telecommunication Engineering). Each script is small, heavily commented, and
tied to a specific lecture so you can *see* the idea, not just read about it.

> **Ethics.** Everything here is for learning and for systems you own or are
> authorised to test. The hash-cracking example in particular is lawful only
> against your own hashes.

## Setup

Pure standard library for the crypto examples; `pandas` is only needed for the
Wireshark one.

```bash
# with uv (recommended)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# or plain pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Run any script directly, e.g. `python3 public_key/rsa_textbook.py`.

## Modules → lectures

| Module | What's inside | Lecture |
|---|---|---|
| `number_theory/` | divisibility, Euclidean GCD, Miller–Rabin primality, CRT | L2 |
| `algebraic_structures/` | groups, (commutative) rings, integral domains, fields, finite fields | L2 |
| `symmetric_ciphers/` | one-time pad + the key-reuse pitfall (Shannon) | L3 |
| `cryptographic_algorithms/` | single-key concept, factoring, key-size vs brute-force | L2–L3 |
| `public_key/` | textbook RSA, Diffie–Hellman (+ MITM demo) | L4 |
| `data_integrity/` | HMAC vs a bare hash | L5 |
| `crack_the_hash/` | dictionary cracker (salt/slow-hash motivation) | L5, L7 |
| `wireshark_analysis/` | extract domains/DNS from a capture (CSV) | L8 |

## The demos

```text
number_theory/divisibility.py            properties of  a | b
number_theory/gcd_algorithm.py           Euclidean algorithm
number_theory/miller_rabin_algorithm.py  probabilistic primality test
number_theory/chinese_remainder_theorem.py   solve congruence systems
algebraic_structures/*.py                groups → rings → fields (with tables)
cryptographic_algorithms/compute_time_per_word_size.py   why 128-bit keys resist brute force
symmetric_ciphers/one_time_pad.py        perfect secrecy; two-time-pad break
public_key/rsa_textbook.py               RSA keygen / encrypt / decrypt from scratch
public_key/diffie_hellman.py             key agreement over a public channel; MITM
data_integrity/hmac_demo.py              keyed integrity vs forgeable bare hash
crack_the_hash/crack.py                  dictionary attack: --algo, --mutate, --target
wireshark_analysis/test_traffic_analysis.py   pull domains out of a DNS capture
```

### crack_the_hash quick start

```bash
cd crack_the_hash
python3 crack.py wordlist_crack_test.txt            # default demo target
python3 crack.py wordlist_crack_test.txt --mutate   # + case/suffix variants
python3 crack.py words.txt --target <hex> --algo md5
```

## Conventions

- Every script guards its demo under `if __name__ == "__main__":`, so you can
  also `import` the functions.
- Crypto examples that are **teaching toys** (textbook RSA, the single-key
  concept) say so in their docstring — never use them for real protection; use a
  vetted library (`cryptography`, `pyca`).
