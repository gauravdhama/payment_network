from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.encoding.pem import PEMEncoder
import secrets
import base64

# Generate ECC key pair (do this once and store the keys securely)
private_key, public_key = keys.gen_keypair(curve.P256)

# Store the public key in PEM format
with open('public_key.pem', 'w') as f:
    f.write(PEMEncoder.encode_public_key(public_key))

def generate_token(pan):
    """
    Generates a token for the given PAN using ECC.
    """
    # Generate a random nonce
    nonce = secrets.token_bytes(32)

    # Sign the PAN with the private key
    r, s = ecdsa.sign(pan.encode(), private_key)
    signature = DEREncoder.encode_signature(r, s)

    # Concatenate the nonce and signature
    token_bytes = nonce + signature

    # Encode the token as a Base64 string
    token = base64.b64encode(token_bytes).decode()
    return token

def detokenize(token):
    """
    Detokenizes the given token to retrieve the PAN using ECC.
    """
    try:
        # Decode the Base64 token
        token_bytes = base64.b64decode(token.encode())

        # Extract nonce and signature
        nonce = token_bytes[:32]
        signature = token_bytes[32:]

        # Verify the signature with the public key
        with open('public_key.pem', 'r') as f:
            public_key = PEMEncoder.decode_public_key(f.read())

        r, s = DEREncoder.decode_signature(signature)
        valid = ecdsa.verify((r, s), nonce, public_key)
        if not valid:
            raise ValueError("Invalid token signature")

        # If the signature is valid, return the nonce as the PAN
        return nonce.decode()

    except Exception as e:
        print(f"Error detokenizing: {e}")
        return None
