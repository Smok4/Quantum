<<<<<<< HEAD
#!/usr/bin/env python3
"""
Point d'entrée principal Quantum Blockchain
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Configuration du chemin
SRC_PATH = Path(__file__).parent / 'src'
sys.path.append(str(SRC_PATH))

from scripts.deploy_mainnet import MainnetDeployer

async def main():
    parser = argparse.ArgumentParser(description="Quantum Blockchain Mainnet")
    parser.add_argument("--mainnet", action="store_true", help="Démarrer en mode mainnet")
    parser.add_argument("--testnet", action="store_true", help="Démarrer en mode testnet")
    parser.add_argument("--type", choices=["full", "mining", "api"], default="full")
    parser.add_argument("--port", type=int, help="Port personnalisé")
    
    args = parser.parse_args()
    
    if not (args.mainnet or args.testnet):
        print("❌ Spécifiez --mainnet ou --testnet")
        return
    
    network_mode = "mainnet" if args.mainnet else "testnet"
    print(f"🌐 Démarrage Quantum Blockchain en mode {network_mode.upper()}...")
    
    deployer = MainnetDeployer(node_type=args.type)
    
    try:
        if args.type == "full":
            await deployer.deploy_full_node()
        elif args.type == "mining":
            await deployer.deploy_mining_node()
        elif args.type == "api":
            await deployer.deploy_api_node()
            
        # Maintenir en fonctionnement
        await asyncio.Future()  # Couroutine infinie
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt gracieux du nœud...")
    except Exception as e:
        print(f"❌ Erreur critique: {e}")

if __name__ == "__main__":
    asyncio.run(main())
=======
#!/usr/bin/env python3
"""
Point d'entrée principal Quantum Blockchain - Windows
"""

import asyncio
import sys
import os
from pathlib import Path

# Configuration du chemin
current_dir = Path(__file__).parent
src_path = current_dir
sys.path.insert(0, str(src_path))

async def main():
    print("🚀 Quantum Blockchain pour Windows")
    print("=" * 50)
    
    try:
        # Importer et démarrer le déployeur
        from scripts.deploy_mainnet import SimpleDeployer
        
        deployer = SimpleDeployer()
        await deployer.deploy("mining", 2)  # Minage avec 2 threads par défaut
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("\n📦 Vérifiez que tous les fichiers sont présents:")
        print("   - core/blockchain.py")
        print("   - core/block.py") 
        print("   - core/transaction.py")
        print("   - config/genesis_block.py")
        print("   - scripts/deploy_mainnet.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    # Configuration Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de Quantum Blockchain")
>>>>>>> aabbdd6 (Quantum)
