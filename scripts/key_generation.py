#!/usr/bin/env python3
from src.crypto.post_quantum import PostQuantumCrypto
from src.crypto.quantum_keys import QuantumKeyManager

def main():
    crypto = PostQuantumCrypto()
    key_manager = QuantumKeyManager()
    
    public_key, private_key = crypto.generate_keypair()
    address = key_manager.generate_quantum_address(public_key)
    
    print("🔑 Clés générées:")
    print(f"Adresse: {address}")
    print(f"Clé publique: {public_key.hex()[:64]}...")
    print(f"Clé privée: {private_key.hex()[:64]}...")

if __name__ == "__main__":
    main()