MAINNET_CONFIG = {
    "network_id": "quantum_mainnet_v1",
    "version": "1.0.0",
    "port": 8333,
    "rpc_port": 8334,
    "web_port": 8080,
    
    # Consensus
    "block_time_target": 120,
    "initial_difficulty": 4,
    "mining_reward": 50.0,
    
    # Réseau
    "max_connections": 50,
    "bootstrap_nodes": [
        "localhost:8333"
    ],
    
    # Sécurité
    "pq_algorithm": "DILITHIUM3",
    "hash_algorithm": "SHA3-512"
}