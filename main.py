#!/usr/bin/env python3
"""
QUANTUM BLOCKCHAIN - VERSION COMPLÈTE FINALE
Blockchain post-quantique avec hébergement web P2P, minage CPU et contrats intelligents
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Any

# Configuration des chemins
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

class QuantumBlockchainFullNode:
    """Nœud complet Quantum Blockchain avec toutes les fonctionnalités"""
    
    def __init__(self):
        self.blockchain = None
        self.p2p_network = None
        self.web_server = None
        self.is_running = False
        
    async def initialize(self):
        """Initialiser tous les modules"""
        print("🚀 INITIALISATION QUANTUM BLOCKCHAIN")
        print("=" * 60)
        
        # 1. Initialiser la blockchain
        try:
            from core.blockchain import QuantumBlockchain
            self.blockchain = QuantumBlockchain()
            print("✅ Blockchain initialisée")
        except Exception as e:
            print(f"❌ Erreur blockchain: {e}")
            return False
        
        # 2. Initialiser le réseau P2P
        try:
            from network.p2p_network import QuantumP2PNetwork
            self.p2p_network = QuantumP2PNetwork(port=8333)
            await self.p2p_network.start()
            print("✅ Réseau P2P initialisé")
        except Exception as e:
            print(f"⚠️  Réseau P2P non disponible: {e}")
        
        # 3. Initialiser le serveur web P2P
        try:
            from p2p_web_hosting.p2p_web_server import P2PWebServer
            self.web_server = P2PWebServer(port=8080)
            await self.web_server.start()
            print("✅ Serveur web P2P initialisé")
        except Exception as e:
            print(f"⚠️  Serveur web P2P non disponible: {e}")
        
        # 4. Initialiser l'API REST
        try:
            from api.rest_api import QuantumAPI
            self.api = QuantumAPI(self.blockchain, self.p2p_network)
            await self.api.start(port=8334)
            print("✅ API REST initialisée")
        except Exception as e:
            print(f"⚠️  API REST non disponible: {e}")
        
        self.is_running = True
        return True
    
    async def start_mining(self, miner_address=None, max_threads=2):
        """Démarrer le minage CPU"""
        if miner_address is None:
            miner_address = f"QmMINER_{int(time.time())}"
        
        print(f"⛏️  DÉMARRAGE MINAGE CPU")
        print(f"👷 Mineur: {miner_address}")
        print(f"💻 Threads: {max_threads}")
        
        mining_round = 0
        while self.is_running:
            try:
                mining_round += 1
                print(f"\n🔄 Round de minage #{mining_round}")
                
                # Minage d'un bloc
                new_block = self.blockchain.mine_new_block(miner_address, max_threads)
                
                if new_block:
                    print(f"💰 BLOC #{new_block.index} MINÉ AVEC SUCCÈS!")
                    
                    # Diffuser le bloc sur le réseau P2P
                    if self.p2p_network:
                        await self.p2p_network.broadcast_block(new_block)
                    
                    # Statistiques
                    info = self.blockchain.get_blockchain_info()
                    print(f"📊 Chaîne: {info['block_height']} blocs | TX en attente: {info['pending_transactions']}")
                
                # Ajouter des transactions automatiques périodiquement
                if mining_round % 3 == 0:
                    self._add_test_transaction(miner_address)
                
                # Pause entre les blocs
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ Erreur minage: {e}")
                await asyncio.sleep(5)
    
    def _add_test_transaction(self, miner_address):
        """Ajouter une transaction test"""
        test_address = f"QmTEST_{int(time.time())}"
        amount = 0.1 + (time.time() % 1.0)  # Montant aléatoire
        self.blockchain.add_transaction(miner_address, test_address, amount)
    
    async def start_web_services(self):
        """Démarrer les services web"""
        print("🌐 DÉMARRAGE DES SERVICES WEB")
        
        urls = []
        if self.web_server:
            urls.append(f"http://localhost:8080")
        if hasattr(self, 'api'):
            urls.append(f"http://localhost:8334/api")
        
        if urls:
            print("📍 URLs accessibles:")
            for url in urls:
                print(f"   • {url}")
        else:
            print("⚠️  Aucun service web démarré")
    
    async def monitor_system(self):
        """Surveillance du système"""
        import psutil
        import os
        
        print("📊 SURVEILLANCE SYSTÈME ACTIVÉE")
        
        while self.is_running:
            try:
                # Mémoire
                memory = psutil.virtual_memory()
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                # Processus
                process = psutil.Process(os.getpid())
                
                print(f"📈 CPU: {cpu_percent}% | RAM: {memory.percent}% | Threads: {process.num_threads()}")
                
                await asyncio.sleep(30)  # Toutes les 30 secondes
                
            except Exception as e:
                print(f"⚠️  Erreur monitoring: {e}")
                await asyncio.sleep(60)
    
    async def run(self, enable_mining=True, enable_web=True):
        """Exécuter le nœud complet"""
        if not await self.initialize():
            print("❌ Échec de l'initialisation")
            return
        
        # Afficher les informations de démarrage
        print("\n🎯 QUANTUM BLOCKCHAIN - PRÊT")
        print("=" * 50)
        
        info = self.blockchain.get_blockchain_info()
        print(f"📦 Bloc genesis: {self.blockchain.chain[0].hash[:32]}...")
        print(f"🔗 Difficulté actuelle: {info['difficulty']}")
        print(f"🌐 Network ID: {info['network_id']}")
        
        # Démarrer les services
        tasks = []
        
        if enable_web:
            await self.start_web_services()
        
        # Surveillance système
        tasks.append(asyncio.create_task(self.monitor_system()))
        
        # Minage
        if enable_mining:
            tasks.append(asyncio.create_task(self.start_mining()))
        
        # Attendre que tout soit terminé
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé...")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Arrêt gracieux"""
        print("\n🔴 ARRÊT DU NŒUD QUANTUM BLOCKCHAIN")
        self.is_running = False
        
        if self.p2p_network:
            await self.p2p_network.stop()
            print("✅ Réseau P2P arrêté")
        
        if self.web_server:
            await self.web_server.stop()
            print("✅ Serveur web arrêté")
        
        print("👋 Quantum Blockchain arrêté avec succès")

async def main():
    """Fonction principale"""
    print("🌐 QUANTUM BLOCKCHAIN - VERSION COMPLÈTE")
    print("🔒 Post-quantique | 🌐 P2P Web | ⛏️ CPU Mining | 🤖 Smart Contracts")
    print("=" * 70)
    
    # Configuration
    import argparse
    parser = argparse.ArgumentParser(description="Quantum Blockchain Full Node")
    parser.add_argument("--no-mining", action="store_true", help="Désactiver le minage")
    parser.add_argument("--no-web", action="store_true", help="Désactiver les services web")
    parser.add_argument("--threads", type=int, default=2, help="Threads de minage")
    
    args = parser.parse_args()
    
    # Créer et lancer le nœud
    node = QuantumBlockchainFullNode()
    
    try:
        await node.run(
            enable_mining=not args.no_mining,
            enable_web=not args.no_web
        )
    except KeyboardInterrupt:
        print("\n🛑 Arrêt par l'utilisateur")
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Configuration Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())