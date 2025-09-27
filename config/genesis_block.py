import time
from datetime import datetime

def create_genesis_block():
    """Créer automatiquement le genesis block à la date actuelle"""
    current_timestamp = int(time.time())
    
    return {
        "timestamp": current_timestamp,
        "difficulty": 4,  # Difficulté initiale faible
        "mining_reward": 50.0,
        "message": f"Quantum Blockchain Genesis - {datetime.utcfromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "cpu_only": True
    }

def generate_genesis_hash(genesis_data):
    """Générer le hash du genesis block"""
    import hashlib
    genesis_string = f"{genesis_data['timestamp']}{genesis_data['message']}"
    return hashlib.sha3_512(genesis_string.encode()).hexdigest()