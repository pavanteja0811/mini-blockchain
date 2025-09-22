import hashlib
import time

# Calculate SHA-256 hash of given data
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Recursively build Merkle Tree layers until root is reached
def build_merkle_layer(layer):
    if len(layer) == 1:
        return layer  # Root reached

    # Duplicate last element if odd number of nodes
    if len(layer) % 2 == 1:
        layer.append(layer[-1])

    next_layer = []
    for i in range(0, len(layer), 2):
        combined = layer[i] + layer[i + 1]
        next_layer.append(sha256(combined))

    # Recursive call for next layer
    return build_merkle_layer(next_layer)

# Compute Merkle root for a list of transactions
def build_merkle_root(transactions):
    if not transactions:
        return ""
    initial_layer = [sha256(tx) for tx in transactions]
    root_layer = build_merkle_layer(initial_layer)
    return root_layer[0]

# Block class representing each block in the blockchain
class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_root = build_merkle_root(transactions)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.merkle_root}{self.previous_hash}"
        return sha256(block_string)

# Blockchain class managing the chain of blocks
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), transactions, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Block {i} hash mismatch!")
                return False

            if current.previous_hash != previous.hash:
                print(f"Block {i} previous hash mismatch!")
                return False

        return True

# Example usage
if __name__ == "__main__":
    my_chain = Blockchain()
    my_chain.add_block(["Alice pays Bob 10", "Bob pays Charlie 5"])
    my_chain.add_block(["Charlie pays Dave 2", "Dave pays Eve 1"])

    print("Is Blockchain valid?", my_chain.is_chain_valid())

    for block in my_chain.chain:
        print(f"\nBlock {block.index}")
        print(f"Timestamp     : {block.timestamp}")
        print(f"Merkle Root   : {block.merkle_root}")
        print(f"Previous Hash : {block.previous_hash}")
        print(f"Current Hash  : {block.hash}")
        print(f"Transactions  : {block.transactions}")
