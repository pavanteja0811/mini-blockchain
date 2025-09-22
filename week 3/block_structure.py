import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()  # Current time
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Combine block data into one string using f-string
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        # Return SHA-256 hash
        return hashlib.sha256(block_string.encode()).hexdigest()

# ---- Test Code ----
block1 = Block(1, "Tx1: Alice -> Bob", "0")  # First block

# Print block data using f-strings
print(f"Block Index: {block1.index}")
print(f"Transactions: {block1.transactions}")
print(f"Previous Hash: {block1.previous_hash}")
print(f"Current Hash: {block1.hash}")
