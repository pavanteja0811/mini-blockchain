import hashlib  # Import the hashlib library for SHA-256 hashing

# Simple SHA-256 hash function
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()  # Encode string to bytes, hash it, and return hex string

# Recursive function to build one layer of the Merkle tree at a time
def build_merkle_layer(layer):
    if len(layer) == 1:
        return [layer]  # Base case: only one hash left, return as root layer

    # If the number of nodes is odd, duplicate the last node to make it even
    if len(layer) % 2 == 1:
        layer.append(layer[-1])

    next_layer = []  # This will hold the parent nodes of the current layer

    # Iterate over the layer two elements at a time
    for i in range(0, len(layer), 2):
        combined = layer[i] + layer[i + 1]  # Concatenate two sibling hashes
        next_layer.append(sha256(combined))  # Hash the concatenated string and add to the next layer

    # Recursively build the next layer and prepend the current layer to the result
    return [layer] + build_merkle_layer(next_layer)

# Build full Merkle tree from list of transactions and return all layers (bottom-up)
def build_merkle_tree(transactions):
    leaf_hashes = [sha256(tx) for tx in transactions]  # Hash each transaction (leaf nodes)
    return build_merkle_layer(leaf_hashes)  # Build the full Merkle tree using the leaf hashes

# Generate Merkle proof for a specific transaction (by index)
def get_merkle_proof(transactions, index):
    tree_layers = build_merkle_tree(transactions)  # Build the full tree
    proof = []  # Will store the proof: list of (sibling_hash, is_left) tuples
    pos = index  # Current index at each level

    # Loop through each layer except the top (root)
    for layer in tree_layers[:-1]:
        # If the number of nodes is odd, duplicate the last node to make even
        if len(layer) % 2 == 1:
            layer.append(layer[-1])

        # Determine if current node is a right child (odd index)
        is_left = pos % 2 == 1

        # Find the sibling index
        sibling_index = pos - 1 if is_left else pos + 1

        # Add sibling hash and whether sibling is on the left to the proof
        proof.append((layer[sibling_index], is_left))

        # Move up to the parent node in the next layer
        pos = pos // 2

    return proof  # Return the Merkle proof list

# Function to verify a transaction using its Merkle proof and root
def verify_transaction(tx, proof, merkle_root):
    current_hash = sha256(tx)  # Start by hashing the transaction data

    # Loop through the proof steps to reconstruct the path to the root
    for sibling_hash, is_left in proof:
        if is_left:
            # If sibling is on the left, concatenate it before current hash
            current_hash = sha256(sibling_hash + current_hash)
        else:
            # If sibling is on the right, concatenate after current hash
            current_hash = sha256(current_hash + sibling_hash)

    # After applying all proof steps, current_hash should equal the Merkle root
    return current_hash == merkle_root


# --- MAIN TEST SECTION ---

# Sample transactions (leaves of the Merkle tree)
transactions = [
    "Alice pays Bob 10 BTC",
    "Bob pays Charlie 5 BTC",
    "Charlie pays Dave 2 BTC",
    "Dave pays Eve 1 BTC"
]

# Build the Merkle tree and extract all layers
layers = build_merkle_tree(transactions)

# The Merkle root is the only hash in the final layer
merkle_root = layers[-1][0]
print("Merkle Root:", merkle_root)

# Choose transaction index 0 for proof generation (Alice pays Bob)
tx_index = 0

# Generate the Merkle proof for the selected transaction
proof = get_merkle_proof(transactions, tx_index)
print("Generated Merkle Proof for Tx0:", proof)

# Use the Merkle proof to verify the transaction's inclusion
is_verified = verify_transaction(transactions[tx_index], proof, merkle_root)
print("Tx0 Verified?", is_verified)