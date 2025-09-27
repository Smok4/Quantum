import hashlib
import secrets

class TorLikeRouting:
    """Routage de type Tor pour l'anonymat"""
    
    def __init__(self, relay_nodes):
        self.relay_nodes = relay_nodes
        self.circuits = {}
    
    def create_circuit(self, num_hops=3):
        """Créer un circuit de relais"""
        circuit_id = secrets.token_hex(16)
        selected_relays = random.sample(self.relay_nodes, min(num_hops, len(self.relay_nodes)))
        
        self.circuits[circuit_id] = {
            'relays': selected_relays,
            'created_at': time.time(),
            'active': True
        }
        
        return circuit_id
    
    def route_through_circuit(self, circuit_id, data):
        """Router des données through un circuit"""
        if circuit_id not in self.circuits:
            return None
        
        circuit = self.circuits[circuit_id]
        encrypted_data = data
        
        # Chiffrement en couches (oignon)
        for relay in reversed(circuit['relays']):
            key = hashlib.sha256(relay.encode()).digest()[:32]
            encrypted_data = self.encrypt_layer(encrypted_data, key)
        
        return encrypted_data
    
    def encrypt_layer(self, data, key):
        """Chiffrer une couche de l'oignon"""
        # Implémentation simplifiée
        return hashlib.sha256(data + key).digest()