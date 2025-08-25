from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm
from azure.keyvault.keys import KeyClient
import os

class AzureHSMClient:
    def __init__(self, vault_url: str = None, key_name: str = None, key_version: str = None, credential=None):
        self.vault_url = vault_url or os.environ.get('AZURE_KEY_VAULT_URL')
        self.key_name = key_name or os.environ.get('AZURE_KEY_NAME')
        self.key_version = key_version or os.environ.get('AZURE_KEY_VERSION', None)

        if not self.vault_url or not self.key_name:
            raise ValueError('AZURE_KEY_VAULT_URL and AZURE_KEY_NAME must be set')

        if credential is None:
            credential = DefaultAzureCredential()

        key_client = KeyClient(vault_url=self.vault_url, credential=credential)
        if self.key_version:
            key = key_client.get_key(self.key_name, self.key_version)
        else:
            key = key_client.get_key(self.key_name)

        self.crypto_client = CryptographyClient(key, credential=credential)

    def sign_data(self, data: bytes) -> bytes:
        result = self.crypto_client.sign(SignatureAlgorithm.rs256, data)
        return result.signature

    def close(self):
        pass
