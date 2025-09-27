#!/usr/bin/env python3
"""
Point d'entrée principal avec hébergement web P2P
"""

import asyncio
import argparse
from core.blockchain import QuantumBlockchain
from p2p_web_hosting.p2p_web_server import P2PWebServer
from p2p_web_hosting.web3_integration import Web3BlockchainIntegration
from scripts.deploy_mainnet import CPUMainnetDeployer

class QuantumFullNode:
    """Nœud complet avec blockchain et hébergement web P2P"""
    
    def __init__(self, web_port=8080, p2p_port=8333):
        self.blockchain = QuantumBlockchain()
        self.web_server = P2PWebServer(port=web_port)
        self.web3_integration = Web3BlockchainIntegration(self.blockchain)
        self.p2p_port = p2p_port
        
    async def start(self, enable_mining=False, mining_threads=None):
        """Démarrer le nœud complet"""
        print("🚀 Démarrage Quantum Full Node...")
        print("⛓️  Blockchain + 🌐 Hébergement Web P2P")
        
        # Démarrer le serveur web P2P
        await self.web_server.start()
        
        # Démarrer la blockchain
        if enable_mining:
            await self.start_mining(mining_threads)
        
        # Intégration Web3
        await self.setup_web3_api()
        
        print(f"🌐 Interface web: http://localhost:{self.web_server.port}")
        print("✅ Nœud pleinement opérationnel!")
        
        # Maintenir en fonctionnement
        await asyncio.Future()
    
    async def start_mining(self, max_threads=None):
        """Démarrer le minage CPU"""
        import threading
        
        def mine_blocks():
            miner_address = "QmWEBMINER_" + str(hash(self))
            while True:
                try:
                    self.blockchain.mine_new_block(miner_address, max_threads)
                except Exception as e:
                    print(f"Erreur minage: {e}")
        
        mining_thread = threading.Thread(target=mine_blocks, daemon=True)
        mining_thread.start()
        print("⛏️  Minage CPU démarré en arrière-plan")
    
    async def setup_web3_api(self):
        """Configurer l'API Web3 pour les dApps"""
        # Ajouter des routes API supplémentaires
        @self.web_server.app.route('/api/blockchain')
        async def api_blockchain(request):
            return web.json_response({
                'network': 'quantum_mainnet',
                'block_height': len(self.blockchain.chain),
                'difficulty': self.blockchain.chain[-1].difficulty if self.blockchain.chain else 0,
                'peers': len(self.web_server.peer_servers)
            })
        
        @self.web_server.app.route('/api/dapps/{site_hash}')
        async def api_dapp(request):
            site_hash = request.match_info['site_hash']
            dapp_info = await self.web3_integration.serve_dapp(site_hash)
            return web.json_response(dapp_info)

async def main():
    parser = argparse.ArgumentParser(description="Quantum Full Node avec Web P2P")
    parser.add_argument("--web-port", type=int, default=8080, help="Port serveur web")
    parser.add_argument("--p2p-port", type=int, default=8333, help="Port P2P blockchain")
    parser.add_argument("--mine", action="store_true", help="Activer le minage")
    parser.add_argument("--threads", type=int, help="Threads de minage")
    
    args = parser.parse_args()
    
    # Démarrer le nœud complet
    node = QuantumFullNode(web_port=args.web_port, p2p_port=args.p2p_port)
    
    try:
        await node.start(enable_mining=args.mine, mining_threads=args.threads)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du nœud...")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())