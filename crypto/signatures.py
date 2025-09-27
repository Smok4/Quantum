import hashlib
from .post_quantum import PostQuantumCrypto

class SignatureManager:
    def __init__(self):
        self.crypto = PostQuantumCrypto()
    
    def sign_transaction(self, private_key, transaction_data):
        """Signer une transaction"""
        message = self._hash_transaction_data(transaction_data)
        return self.crypto.sign_message(private_key, message)
    
    def verify_transaction(self, public_key, transaction_data, signature):
        """Vérifier une signature de transaction"""
        message = self._hash_transaction_data(transaction_data)
        return self.crypto.verify_signature(public_key, message, signature)
    
    def _hash_transaction_data(self, data):
        """Hasher les données de transaction"""
        import json
        return hashlib.sha3_512(json.dumps(data, sort_keys=True).encode()).digest()