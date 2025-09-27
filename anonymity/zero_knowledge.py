import hashlib
import secrets

class SimpleZKProof:
    """Preuve à divulgation nulle simplifiée"""
    
    @staticmethod
    def create_proof(secret, public_challenge):
        """Créer une preuve ZK"""
        # Implémentation simplifiée
        proof_hash = hashlib.sha3_512(secret + public_challenge).digest()
        return proof_hash
    
    @staticmethod
    def verify_proof(proof, public_challenge, expected_result):
        """Vérifier une preuve ZK"""
        # Vérification simplifiée
        return proof == expected_result