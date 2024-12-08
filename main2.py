import random
import hashlib

# Setup phase
def setup():
    """
    Generate the parameters for the protocol.
    Returns:
        n (int): Product of two primes.
        y_squared (int): Public key derived from the secret 'x'.
        x (int): Secret key.
    """
    p = 11  # Use a larger prime in real applications
    q = 13
    n = p * q
    x = random.randint(1, n - 1)  # Secret key
    y_squared = (x ** 2) % n  # Public key

    print(f"Setup:\n  p = {p}, q = {q}, n = {n}, x = {x}, y^2 = {y_squared}")
    return n, y_squared, x

# Prover's steps
def prover(n):
    """
    Prover generates a commitment.
    Args:
        n (int): Public modulus.
    Returns:
        t (int): Commitment.
        r (int): Random value used to compute 't'.
    """
    r = random.randint(1, n - 1)
    t = (r ** 2) % n
    print(f"Prover:\n  r = {r}, t = {t}")
    return t, r

# Fiat-Shamir Challenge
def fiat_shamir_challenge(t, n, y_squared):
    """
    Generate a challenge using the Fiat-Shamir heuristic.
    Args:
        t (int): Commitment from the prover.
        n (int): Public modulus.
        y_squared (int): Public key.
    Returns:
        c (int): Challenge (0 or 1).
    """
    # Concatenate the inputs and hash them
    hash_input = f"{t}{n}{y_squared}".encode()
    hash_value = hashlib.sha256(hash_input).hexdigest()
    c = int(hash_value, 16) % 2  # Get a bit (0 or 1) from the hash
    print(f"Fiat-Shamir Challenge:\n  Hash input = {hash_input}, c = {c}")
    return c

# Prover's response
def prover_response(r, x, c, n):
    """
    Prover computes the response to the challenge.
    Args:
        r (int): Random value used to compute 't'.
        x (int): Secret key.
        c (int): Challenge from the verifier.
        n (int): Public modulus.
    Returns:
        s (int): Response.
    """
    s = (r * (x ** c)) % n
    print(f"Prover Response:\n  s = {s}")
    return s

# Verifier's final verification
def verifier_verification(s, t, y_squared, n):
    """
    Verifier checks the prover's response.
    Args:
        s (int): Response from the prover.
        t (int): Commitment from the prover.
        y_squared (int): Public key.
        c (int): Challenge from the verifier.
        n (int): Public modulus.
    Returns:
        bool: True if the verification is successful, False otherwise.
    """
    hash_input = f"{t}{n}{y_squared}".encode()
    hash_value = hashlib.sha256(hash_input).hexdigest()
    c = int(hash_value, 16) % 2  # Get a bit (0 or 1) from the hash
    lhs = (s ** 2) % n
    rhs = (t * (y_squared ** c)) % n
    print(f"Verifier Verification:\n  LHS = {lhs}, RHS = {rhs}")
    return lhs == rhs

# Main protocol execution
def main():
    n, y_squared, x = setup()          # Setup public and secret parameters
    t, r = prover(n)                  # Prover generates a commitment
    c = fiat_shamir_challenge(t, n, y_squared)  # Fiat-Shamir generates challenge
    s = prover_response(r, x, c, n)   # Prover computes response
    verification_result = verifier_verification(s, t, y_squared, n)  # Verify

    if verification_result:
        print("Verification successful: The prover knows 'x'.")
    else:
        print("Verification failed: The prover does not know 'x'.")

# Entry point
if __name__ == "__main__":
    main()
