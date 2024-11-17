import hashlib
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Merkle tree creation based on transactions
def build_merkle_tree(transactions):
    if len(transactions) == 0:
        return []
    if len(transactions) == 1:
        print(1)
        return [hashlib.sha256(transactions[0].encode()).hexdigest()]


    new_transactions = []
    for i in range(0, len(transactions), 2):
        print(2)
        if i + 1 < len(transactions):
            combined = transactions[i] + transactions[i + 1]
        else:
            combined = transactions[i]
        new_transactions.append(hashlib.sha256(combined.encode()).hexdigest())

    return build_merkle_tree(new_transactions)

class Block:
    def __init__(self, index, previous_hash, timestamp, merkle_root, nonce, data, hash, signature, public_key):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.data = data
        self.hash = hash
        self.signature = signature
        self.public_key = public_key

def calculate_hash(index, previous_hash, timestamp, merkle_root, nonce, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(merkle_root) + str(nonce) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()

# Function to sign data with private key
def sign_data(private_key, data):
    return private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# Function to create RSA key pair (private and public)
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def create_genesis_block():
    private_key, public_key = generate_key_pair()
    data = "Genesis Block"
    block_hash = calculate_hash(0, "0", int(time.time()), "", 0, data)
    signature = sign_data(private_key, block_hash)
    return Block(0, "0", int(time.time()), "", 0, data, block_hash, signature, public_key)

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    merkle_tree = build_merkle_tree(data)
    merkle_root = merkle_tree[-1] if merkle_tree else ""
    nonce = 0

    private_key, public_key = generate_key_pair()  # Generate key pair for each block

    while True:
        nonce += 1
        hash_attempt = calculate_hash(index, previous_block.hash, timestamp, merkle_root, nonce, data)
        if hash_attempt.startswith("0000"):  # PoW condition: first four bytes must be zeros
            signature = sign_data(private_key, hash_attempt)  # Sign the block hash
            break

    return Block(index, previous_block.hash, timestamp, merkle_root, nonce, data, hash_attempt, signature, public_key)

# Testing the blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_blocks_to_add = 3
transactions = []

for i in range(num_blocks_to_add):
    new_data = [f"Tranzakció #{i+1} - Befizető: Alice, Kedvezményezett: Bob, Összeg: 10 BTC"]
    transactions.extend(new_data)
    new_block = create_new_block(previous_block, new_data)
    blockchain.append(new_block)
    previous_block = new_block
    print(f"Block #{new_block.index} added to the blockchain.")
    print(f"Hash: {new_block.hash}\n")

# Blockchain details
print("Blockchain verification:")
for block in blockchain:
    print(f"Block #{block.index}")
    print(f"Hash: {block.hash}")
    print(f"Previous hash: {block.previous_hash}")
    print(f"Merkle root: {block.merkle_root}")
    print(f"Nonce: {block.nonce}")
    print(f"Data: {block.data}")
    print(f"Signature: {block.signature}")
    print()
