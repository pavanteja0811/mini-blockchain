import hashlib

# Function to calculate SHA-256 hash
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Recursive function to build one level at a time using for loop
def build_merkle_layer(layer):
    if len(layer) == 1:
        return layer  # Final root reached

    # If odd number of elements, duplicate last one
    if len(layer) % 2 == 1:
        layer.append(layer[-1])

    next_layer = []
    for i in range(0, len(layer), 2):
        combined = layer[i] + layer[i + 1]
        next_layer.append(sha256(combined))

    # Recursively build next level
    return build_merkle_layer(next_layer)

# Function to build Merkle Tree and return root hash
def build_merkle_tree(transactions):
    # Initial layer: hash of each transaction
    initial_layer = [sha256(tx) for tx in transactions]
    root_layer = build_merkle_layer(initial_layer)
    return root_layer[0]

# Test data
transactions = ["Alice pays Bob 10", "Bob pays Charlie 5", "Charlie pays Dave 2"]

# Build Merkle Tree and print root hash
merkle_root = build_merkle_tree(transactions)
print("Merkle Root Hash:", merkle_root)
