import os
import pkcs11

# --- HSM Configuration ---
lib_path = '/path/to/your/pkcs11_library'
slot_id = 0
hsm_pin = os.environ.get("HSM_PIN")
lib = pkcs11.lib(lib_path)
token = lib.get_token(slot=slot_id)

def encrypt_with_hsm(data):
    """
    Encrypts data using the HSM.
    """
    with token.open(user_pin=hsm_pin) as session:
        key = session.get_key(label='my_encryption_key')
        encrypted_data = key.encrypt(data.encode())
    return encrypted_data
