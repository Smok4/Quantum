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