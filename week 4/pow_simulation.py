import hashlib  # Import hashlib for SHA-256 hashing
import time     # Import time to measure duration

def proof_of_work(data, difficulty, max_nonce=10**7):
    nonce = 0  # Start nonce at 0
    start_time = time.time()  # Record start time
    
    # Loop over nonce values from 0 up to max_nonce (to prevent infinite loop)
    for nonce in range(max_nonce):
        text = f"{data}{nonce}"  # Concatenate data and current nonce
        hash_result = hashlib.sha256(text.encode()).hexdigest()  
        # Compute SHA-256 hash of the concatenated string
        
        # Check if hash starts with required number of zeros for difficulty
        if hash_result.startswith("0" * difficulty):
            end_time = time.time()  # Record end time on success
            return nonce, hash_result, end_time - start_time  # Return results
    
    # If loop finishes without finding valid nonce, raise error or return None
    return None, None, None

# Difficulty of 4 means hash must start with '0000'
difficulty = 4

# Run proof of work with a max nonce limit (to avoid infinite running)
nonce, hash_val, duration = proof_of_work("Block Data", difficulty)

if nonce is not None:
    print("Proof of Work successful!")
    print("Nonce:", nonce)
    print("Hash:", hash_val)
    print("Time taken:", duration, "seconds")
else:
    print("Failed to find a valid nonce within max attempts.")
