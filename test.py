#!/usr/bin/env python3
"""
Lanceur de test pour vérifier que tout fonctionne
"""

import sys
import os

def test_imports():
    """Tester que tous les modules s'importent correctement"""
    print("🧪 Test des imports...")
    
    try:
        from core.block import PQBlock
        print("✅ core.block OK")
    except Exception as e:
        print(f"❌ core.block: {e}")
    
    try:
        from core.transaction import PQTransaction, PQTxOutput
        print("✅ core.transaction OK")
    except Exception as e:
        print(f"❌ core.transaction: {e}")
    
    try:
        from core.proof_of_work import SimpleMiner
        print("✅ core.proof_of_work OK")
    except Exception as e:
        print(f"❌ core.proof_of_work: {e}")
    
    try:
        from core.blockchain import QuantumBlockchain
        print("✅ core.blockchain OK")
    except Exception as e:
        print(f"❌ core.blockchain: {e}")

def test_basic_functionality():
    """Tester les fonctionnalités de base"""
    print("\n🔧 Test des fonctionnalités de base...")
    
    # Test de minage simple
    from core.proof_of_work import SimpleMiner
    nonce, hash = SimpleMiner.quick_mine("test_header", 2)
    
    if hash:
        print(f"✅ Minage test réussi! Nonce: {nonce}, Hash: {hash[:16]}...")
    else:
        print("❌ Échec du minage test")

def main():
    print("🧪 TEST COMPLET QUANTUM BLOCKCHAIN")
    print("=" * 50)
    
    test_imports()
    test_basic_functionality()
    
    print("\n🎯 CHOIX DU MODE:")
    print("1. Mode DEBUG (recommandé pour tester)")
    print("2. Mode COMPLET (blockchain avancée)")
    
    choix = input("Votre choix (1 ou 2): ").strip()
    
    if choix == "1":
        print("\n🚀 Lancement du mode DEBUG...")
        from debug_blockchain import main as debug_main
        import asyncio
        asyncio.run(debug_main())
    else:
        print("\n🚀 Lancement du mode COMPLET...")
        from main import main as full_main
        import asyncio
        asyncio.run(full_main())

if __name__ == "__main__":
    main()