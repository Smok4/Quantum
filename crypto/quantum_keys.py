import hashlib
import base64

class QuantumKeyManager:
    def __init__(self):
        self.keys = {}
    
    def generate_quantum_address(self, public_key):
        hash1 = hashlib.sha3_512(public_key).digest()
        hash2 = hashlib.sha3_512(hash1).digest()
        return "Q" + base64.b64encode(hash2[:20]).decode()[:31]
    
    def create_stealth_address(self, public_key):
        ephemeral = hashlib.sha3_512(public_key + str(time.time()).encode()).digest()
        return "S" + base64.b64encode(ephemeral[:25]).decode()[:36]