
# Import necessary modules from the 'cryptography' library
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils

# ----------------------------------------
# 1. Generate RSA Key Pair (Private and Public Keys)
# ----------------------------------------

# Generate private key (this should be kept secret)
private_key = rsa.generate_private_key(
    public_exponent=65537,  # Commonly used value
    key_size=2048  # Key size (bits) — secure and standard
)

# Derive public key from the private key (can be shared publicly)
public_key = private_key.public_key()

# ----------------------------------------
# 2. Original Message to be Sent
# ----------------------------------------

message = b"Blockchain Transaction: Alice pays Bob 10 BTC"  # Must be bytes

# ----------------------------------------
# 3. Sign the Message Using the Sender's Private Key
# ----------------------------------------

# Digital signature provides authenticity and integrity
signature = private_key.sign(
    message,
    padding.PSS(  # Probabilistic Signature Scheme (PSS) for padding
        mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()  # Hash function used in signature
)

# ----------------------------------------
# 4. Encrypt the Message Using Receiver's Public Key
# ----------------------------------------

# Encrypting with the public key ensures only the private key can decrypt
cipher_text = public_key.encrypt(
    message,
    padding.OAEP(  # Optimal Asymmetric Encryption Padding
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# ----------------------------------------
# 5. Receiver Verifies Signature Using Sender's Public Key
# ----------------------------------------

try:
    public_key.verify(
        signature,  # Digital signature from sender
        message,    # Original message
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ Signature is valid! Sender is authentic.")
except Exception as e:
    print("❌ Signature is NOT valid! Data might be tampered.")
    print("Error:", e)

# ----------------------------------------
# 6. Receiver Decrypts Message Using Private Key
# ----------------------------------------

plain_text = private_key.decrypt(
    cipher_text,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# ----------------------------------------
# 7. Print Final Results
# ----------------------------------------

print("\n🔒 Original Message:     ", message.decode())
print("🧾 Encrypted Message:    ", cipher_text)  # Still in bytes
print("🔓 Decrypted Message:    ", plain_text.decode())