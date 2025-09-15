import hashlib  # built-in library for creating cryptographic hashes (SHA-256)
import time     # used to timestamp blocks when they are created

# -------------------------
# Block class: represents one block in the blockchain
# -------------------------
class Block:
    def __init__(self, index, data, previous_hash):
        """
        Initialize a block.
        index: integer position of the block in the chain (0 for genesis)
        data: the transactions or payload stored in this block
        previous_hash: the hash string of the previous block (links blocks together)
        """
        self.index = index
        # timestamp lets us know when this block was created; included in the hash so time affects block identity
        self.timestamp = time.time()
        self.data = data
        # previous_hash links this block to the chain; without it blocks wouldn't be chained
        self.previous_hash = previous_hash
        # calculate and save this block's hash immediately so we have a recorded fingerprint
        # (this is used later to detect tampering)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Combine the block's important fields into a single string and hash it.
        We include index, timestamp, data, and previous_hash so that any change to them changes the hash.
        """
        # create a string representation of the block contents that should be hashed
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        # compute SHA-256 hash of the string and return it as a readable hex string
        return hashlib.sha256(block_string.encode()).hexdigest()

# -------------------------
# Blockchain class: manages the chain of blocks
# -------------------------
class Blockchain:
    def __init__(self):
        # The chain is a list of Block objects. Start with the genesis block so chain is never empty.
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        Manually create the first block in the chain.
        Genesis block has no real previous block, so we set previous_hash to "0" by convention.
        """
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        """
        Return the most recent block in the chain.
        We'll need this when adding a new block so we can link to its hash.
        """
        return self.chain[-1]

    def add_block(self, data):
        """
        Create a new block with given data, link it to the previous block by previous_hash,
        and append it to the chain.
        - len(self.chain) is used as the new block index to reflect its position.
        """
        previous_block = self.get_latest_block()
        # pass previous_block.hash so the new block contains the link to the chain
        new_block = Block(len(self.chain), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validate the entire chain by checking two things for each non-genesis block:
        1) The stored hash equals the recalculated hash (detects data tampering inside a block).
        2) The stored previous_hash equals the actual hash of the previous block (detects broken links).
        If any check fails, the chain is invalid.
        """
        # start from 1 because block 0 (genesis) has no previous block to compare
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            # Recalculate the hash of the current block and compare to the stored hash.
            # If they differ, the block's contents (data/timestamp/etc.) were changed after its creation.
            if current.hash != current.calculate_hash():
                print(f"Block {i} hash mismatch! The block's stored hash does not match the recalculated hash.")
                return False

            # Check that the current block's previous_hash actually matches the previous block's hash.
            # If not, the chain linkage is broken (someone replaced or re-ordered blocks).
            if current.previous_hash != previous.hash:
                print(f"Block {i} previous hash mismatch! The chain link is broken between block {i-1} and block {i}.")
                return False

        # If all checks pass, the chain is valid
        return True

# -------------------------
# Example usage / test
# -------------------------
if __name__ == "__main__":
    # Create a new blockchain (contains genesis block automatically)
    my_chain = Blockchain()

    # Add some blocks with simple string "transactions"
    # Each added block stores the hash of the previous block to maintain the chain
    my_chain.add_block("Alice pays Bob 10 BTC")
    my_chain.add_block("Bob pays Charlie 5 BTC")

    # Validate the chain now: expected True because we haven't tampered with it
    print("Is blockchain valid?", my_chain.is_chain_valid())  # Expected output: True

    # Show hashes for clarity (optional, to observe the chain)
    for blk in my_chain.chain:
        print(f"Index: {blk.index}, Data: '{blk.data}', Hash: {blk.hash[:16]}..., Prev: {blk.previous_hash[:16]}...")

    # Now simulate tampering: change the data in block index 1
    # Note: changing data does NOT automatically update hash because hash was calculated at creation.
    # That mismatch is what validation detects.
    my_chain.chain[1].data = "Alice pays Bob 100 BTC"  # someone illegally modified the transaction

    # Re-run validation after tampering: expected False because data changed but hash stayed same
    print("Is blockchain valid after tampering?", my_chain.is_chain_valid())  # Expected output: False

    # Optional: To "fix" the chain after tampering (not secure), you would need to recalculate hashes
    # for the tampered block and every following block and also re-link them — but on a real decentralized
    # network this would require recomputing and outpacing the whole network (hence security).