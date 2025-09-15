import hashlib

# Function to generate SHA-256 hash
def generate_hash(data):
    # Encode the data to bytes because hashlib works on bytes
    return hashlib.sha256(data.encode()).hexdigest()

# Example data
data1 = "Blockchain"
data2 = "blockchain"  # Notice: Only 'B' vs 'b'

# Generate hashes
hash1 = generate_hash(data1)
hash2 = generate_hash(data2)

# Print results
print(f"Data 1: {data1}")
print(f"Hash 1: {hash1}\n")
print(f"Data 2: {data2}")
print(f"Hash 2: {hash2}\n")

# Check if hashes are same or different
if hash1 == hash2:
    print("Both hashes are same → No Avalanche Effect")
else:
    print("Hashes are different → Avalanche Effect Observed!")