import os
import hvac

# --- Vault Configuration ---
vault_addr = os.environ.get("VAULT_ADDR")
vault_token = os.environ.get("VAULT_TOKEN")
client = hvac.Client(url=vault_addr, token=vault_token)

# Function to read secrets from Vault
def get_secret(secret_path):
    """
    Reads a secret from HashiCorp Vault.
    """
    try:
        response = client.read(secret_path)
        if response and 'data' in response:
            return response['data']
        else:
            print(f"Failed to read secret from Vault: {secret_path}")
            return None
    except Exception as e:
        print(f"Error reading secret from Vault: {e}")
        return None
