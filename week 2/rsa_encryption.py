-
public_key = private_key.public_key()

# Step 2: Define the Message to Encrypt
message = b"Hello Blockchain RSA!"

# Step 3: Encrypt the Message using the Public Key
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask Generation Function
        algorithm=hashes.SHA256(),                    # Hash Algorithm
        label=None                                    # Optional label
    )
)

# Step 4: Decrypt the Ciphertext using the Private Key
decrypted_message = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Step 5: Display the Results
print("Original Message: ", message.decode())
print("Encrypted Message:", ciphertext)  # Ciphertext will appear as unreadable bytes
print("Decrypted Message:", decrypted_message.decode())
