#!/usr/bin/env python3
"""
Script de déploiement simplifié pour Windows
"""

import asyncio
import argparse
import threading
import time
from core.blockchain import QuantumBlockchain

class SimpleDeployer:
    """Déployeur simplifié pour tests"""
    
    def __init__(self):
        self.blockchain = None
        self.mining = False
    
    async def deploy(self, node_type="full", max_threads=2):
        """Déployer le nœud"""
        print("🚀 Quantum Blockchain - Version Windows Simplifiée")
        print("=" * 60)
        
        # Initialiser la blockchain
        self.blockchain = QuantumBlockchain()
        print("✅ Blockchain initialisée")
        
        if node_type == "mining":
            await self.start_mining(max_threads)
        else:
            await self.start_full_node()
    
    async def start_mining(self, max_threads):
        """Démarrer le minage"""
        print(f"⛏️  Démarrage minage avec {max_threads} threads...")
        self.mining = True
        
        miner_address = "QmMINER_" + str(int(time.time()))[-6:]
        
        def mine_loop():
            while self.mining:
                try:
                    new_block = self.blockchain.mine_new_block(miner_address, 1)  # 1 thread pour stabilité
                    if new_block:
                        print(f"💰 Bloc #{new_block.index} miné! Hash: {new_block.hash[:16]}...")
                    
                    # Ajouter une transaction test périodiquement
                    if len(self.blockchain.pending_transactions) == 0:
                        self.blockchain.add_transaction(
                            miner_address, 
                            "QmTEST_" + str(int(time.time()))[-6:], 
                            1.0
                        )
                    
                    time.sleep(2)  # Pause entre les blocs
                    
                except Exception as e:
                    print(f"❌ Erreur minage: {e}")
                    time.sleep(5)
        
        # Démarrer le minage dans un thread séparé
        mining_thread = threading.Thread(target=mine_loop, daemon=True)
        mining_thread.start()
        
        print("🎯 Minage démarré. Ctrl+C pour arrêter.")
        await self.keep_alive()
    
    async def start_full_node(self):
        """Démarrer un nœud complet sans minage"""
        print("🌐 Nœud complet démarré (sans minage)")
        print("💡 Utilisez --type mining pour démarrer le minage")
        await self.keep_alive()
    
    async def keep_alive(self):
        """Maintenir le programme en vie"""
        try:
            while True:
                # Afficher les stats périodiquement
                info = self.blockchain.get_blockchain_info()
                print(f"📊 Blocs: {info['block_height']} | Transactions en attente: {info['pending_transactions']}")
                await asyncio.sleep(30)
        except KeyboardInterrupt:
            self.mining = False
            print("\n🛑 Arrêt du nœud...")

async def main():
    parser = argparse.ArgumentParser(description="Quantum Blockchain Windows")
    parser.add_argument("--type", choices=["full", "mining"], default="full")
    parser.add_argument("--threads", type=int, default=2)
    
    args = parser.parse_args()
    
    deployer = SimpleDeployer()
    
    try:
        await deployer.deploy(args.type, args.threads)
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé")
    except Exception as e:
        print(f"💥 Erreur critique: {e}")

if __name__ == "__main__":
    asyncio.run(main())