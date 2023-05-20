from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64, os

file_name = "private_key.pem"
absolute_path = os.path.abspath(file_name)
print(absolute_path)

def decrypt_signature(encrypted_data, private_key_path = absolute_path):

    # Decode the Base64-encoded encrypted data
    encrypted_data = base64.b64decode(encrypted_data)

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return decrypted_data.decode("utf-8")
