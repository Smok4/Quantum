import hashlib
import secrets

class StealthAddress:
    @staticmethod
    def generate_stealth_address(public_key):
        # Génération d'adresse furtive
        nonce = secrets.token_bytes(32)
        stealth_pub = hashlib.sha3_512(public_key + nonce).digest()
        return "STEALTH_" + stealth_pub.hex()[:56]
    
    @staticmethod
    def create_mixing_transaction(transactions, dummy_count=3):
        # Ajouter des transactions factices
        dummies = []
        for i in range(dummy_count):
            dummies.append({
                'from': '0' * 64,
                'to': '0' * 64,
                'amount': 0,
                'is_dummy': True
            })
        return transactions + dummies