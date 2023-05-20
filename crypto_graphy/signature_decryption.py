from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64, os

def decrypt_signature(encrypted_data, private_key_path = "crypto_graphy/private_key.pem"):

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

text = "IDivPFVgTKcEMBWLZvf4wRtN4zSo9C5N4JcLSUj0NwOsaxTgz5yLPeMA4rbwnYA0noQC87o+SrUXfA2BgqYLVtI3TnU7yD10102lzvSpciu/qO4wQ88NzwEMbaKBdiysU20SkUOBAA8JtoLL5VQ64MwXMqf1kH/wWcG2b0XnnvCmYTRP6VgcgxCKgQrxqYgjloD06TmRPjQECX/kmxijUzK8nWGbJs+EkTk118PW16XbzKXrJ8aRKFyrAhZyDo/+h5PAOo15WLVY4pMDVtMmxqy188JkDGSelMKYGbK/1ARZNqwsBuvH7WDGtnh9xkXTHsfIp61zXfTiXlzsNomIFA=="

x=decrypt_signature(text)
print(x)
