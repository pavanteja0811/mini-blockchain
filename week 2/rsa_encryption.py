# Import necessary cryptographic modules
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# STEP 1: Generate RSA Private Key
# Why: This private key will be used to both sign messages (for authentication) and derive the public key.
private_key = rsa.generate_private_key(
    public_exponent=65537,  # Standard value for RSA; a good balance of performance and security
    key_size=2048           # 2048-bit key size is widely used and considered secure for most applications
)

# STEP 2: Derive the Public Key from the Private Key
# Why: The public key is used by others to verify the signature created by the private key.
public_key = private_key.public_key()

# STEP 3: (Optional) Serialize the Keys to PEM format
# Why: PEM format is a widely-used text encoding for storing keys.
# This step is useful if you want to save or export the keys.

# Serialize (convert to bytes) the private key in PEM format
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,                        # Encode as PEM
    format=serialization.PrivateFormat.TraditionalOpenSSL,     # Standard private key format
    encryption_algorithm=serialization.NoEncryption()          # No encryption (for demo purposes; use password in real use)
)

# Serialize the public key in PEM format
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,                        # Encode as PEM
    format=serialization.PublicFormat.SubjectPublicKeyInfo      # Standard public key format
)

# Print the serialized keys for viewing or saving
print("Private Key:\n", pem_private.decode())  # Decode bytes to string for printing
print("Public Key:\n", pem_public.decode())

# STEP 4: Sign a Message with the Private Key
# Why: This generates a digital signature that proves the message was created by someone holding the private key.
message = b"Send 10 BTC to Bob"  # The message we want to sign

# Create the digital signature using RSA-PSS padding and SHA-256 hashing
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),      # Mask Generation Function using SHA-256
        salt_length=padding.PSS.MAX_LENGTH      # Use maximum salt length (recommended for security)
    ),
    hashes.SHA256()                              # Hashing algorithm used in signature
)

# STEP 5: Verify the Signature using the Public Key
# Why: This checks if the message was really signed by the holder of the private key and not modified.

try:
    # Attempt to verify the signature
    public_key.verify(
        signature,                               # The signature to verify
        message,                                 # The original message
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),   # Must match the padding used in signing
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()                          # Must match the hashing algorithm used in signing
    )
    print("Signature Verified. Data not tampered.")  # Verification successful
except:
    print(" Verification Failed. Data changed!")       # Verification failed — data was altered or signature invalid
