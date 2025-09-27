#!/usr/bin/env python3
import asyncio
from src.network.p2p_network import QuantumP2PNetwork

async def bootstrap_network():
    """Script de bootstrap du réseau"""
    network = QuantumP2PNetwork()
    await network.start()
    
    print("✅ Réseau bootstrapé avec succès!")
    print(f"🔗 Pairs découverts: {len(network.peers)}")

if __name__ == "__main__":
    asyncio.run(bootstrap_network())