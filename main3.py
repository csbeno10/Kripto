import random
import hashlib
import sympy


def setup():

    #p = 11
    #q = 13
    p = random_prime(10, 500)
    q = random_prime(10, 500)
    n = p * q
    x = random.randint(1, n - 1)
    y_squared = (x ** 2) % n

    print(f"Setup:\n  p = {p}, q = {q}, n = {n}, x = {x}, y^2 = {y_squared}")
    return n, y_squared, x

def random_prime(min_val, max_val):
    primes = list(sympy.primerange(min_val, max_val))
    return random.choice(primes)


def prover(n):

    r = random.randint(1, n - 1)
    t = (r ** 2) % n
    print(f"Prover:\n  r = {r}, t = {t}")
    return t, r


def fiat_shamir_challenge(t, n, y_squared, i):
    hash_input = f"{t}{n}{y_squared}{i}".encode()
    hash_value = hashlib.sha256(hash_input).hexdigest()
    c = int(hash_value, 16) % 2
    print(f"Fiat-Shamir Challenge:\n  Hash input = {hash_input}, c = {c}")
    return c


def prover_response(r, x, c, n):

    s = (r * (x ** c)) % n
    print(f"Prover Response:\n  s = {s}")
    return s


def verifier_verification(s, t, y_squared, n, c):

    lhs = (s ** 2) % n
    rhs = (t * (y_squared ** c)) % n
    print(f"Verifier Verification:\n  LHS = {lhs}, RHS = {rhs}")
    return lhs == rhs


def main():
    n, y_squared, x = setup()
    t, r = prover(n)
    for i in range(0,10):

        c = fiat_shamir_challenge(t, n, y_squared,i)
        s = prover_response(r, x, c, n)
        verification_result = verifier_verification(s, t, y_squared, n, c)

        if not verification_result:
            print("Verification failed: The prover does not know 'x'.")
            return

    print("Verification successful: The prover knows 'x'.")



if __name__ == "__main__":
    main()