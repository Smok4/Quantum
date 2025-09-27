#!/usr/bin/env python3
"""
Version DEBUG ultra-simplifiée pour tester rapidement
"""

import hashlib
import time
import asyncio
from dataclasses import dataclass
from typing import List

@dataclass
class DebugTransaction:
    from_addr: str
    to_addr: str
    amount: float
    timestamp: float
    tx_hash: str = None
    
    def __post_init__(self):
        if self.tx_hash is None:
            data = f"{self.from_addr}{self.to_addr}{self.amount}{self.timestamp}"
            self.tx_hash = hashlib.sha256(data.encode()).hexdigest()

@dataclass
class DebugBlock:
    index: int
    timestamp: float
    transactions: List[DebugTransaction]
    previous_hash: str
    nonce: int = 0
    hash: str = None
    
    def mine(self, difficulty=2):
        """Minage très simple"""
        target = "0" * difficulty
        nonce = 0
        
        print(f"⛏️  Minage du bloc #{self.index} - Cible: {target}")
        
        while nonce < 100000:  # Limite basse pour tests rapides
            data = f"{self.index}{self.timestamp}{self.previous_hash}{nonce}"
            block_hash = hashlib.sha256(data.encode()).hexdigest()
            
            if block_hash.startswith(target):
                self.nonce = nonce
                self.hash = block_hash
                print(f"✅ Bloc #{self.index} miné! Nonce: {nonce}, Hash: {block_hash}")
                return True
            
            nonce += 1
        
        print(f"❌ Minage échoué pour le bloc #{self.index}")
        return False

class DebugBlockchain:
    """Blockchain de debug ultra-simple"""
    
    def __init__(self):
        self.chain: List[DebugBlock] = []
        self.pending_transactions: List[DebugTransaction] = []
        self._create_genesis()
    
    def _create_genesis(self):
        """Créer le bloc genesis"""
        genesis = DebugBlock(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64
        )
        genesis.hash = hashlib.sha256(b"genesis").hexdigest()
        self.chain.append(genesis)
        print("✅ Bloc Genesis créé!")
    
    def add_transaction(self, from_addr, to_addr, amount):
        """Ajouter une transaction"""
        tx = DebugTransaction(from_addr, to_addr, amount, time.time())
        self.pending_transactions.append(tx)
        print(f"💸 Transaction: {from_addr[:8]} -> {to_addr[:8]} ({amount} QC)")
        return True
    
    def mine_block(self, miner_address):
        """Minage d'un nouveau bloc"""
        if not self.pending_transactions:
            print("➕ Ajout d'une transaction test...")
            self.add_transaction(miner_address, "test_addr", 1.0)
        
        last_block = self.chain[-1]
        new_block = DebugBlock(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=last_block.hash
        )
        
        if new_block.mine(difficulty=2):  # Difficulté très basse pour tests
            # Ajouter récompense
            reward_tx = DebugTransaction(
                "network", miner_address, 50.0, time.time()
            )
            new_block.transactions.insert(0, reward_tx)
            
            self.chain.append(new_block)
            self.pending_transactions = []
            
            print(f"🎉 Bloc #{new_block.index} ajouté à la blockchain!")
            print(f"📊 Taille de la chaîne: {len(self.chain)} blocs")
            return True
        
        return False

async def main():
    """Fonction principale de debug"""
    print("🐛 DEBUG Blockchain - Version Ultra-Simple")
    print("=" * 50)
    
    blockchain = DebugBlockchain()
    miner_address = "miner_" + str(int(time.time()))[-6:]
    
    print(f"👷 Mineur: {miner_address}")
    print("🚀 Démarrage du minage... (Ctrl+C pour arrêter)")
    
    try:
        block_count = 0
        while block_count < 10:  # Limiter à 10 blocs pour le test
            if blockchain.mine_block(miner_address):
                block_count += 1
                print(f"📈 Progression: {block_count}/10 blocs")
            
            # Ajouter une transaction aléatoire
            if block_count % 2 == 0:
                blockchain.add_transaction(
                    f"addr_{block_count}",
                    f"addr_{block_count + 1}",
                    block_count * 0.5
                )
            
            await asyncio.sleep(2)  # Pause entre les blocs
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    
    print("\n📊 RAPPORT FINAL:")
    print(f"📦 Blocs minés: {len(blockchain.chain)}")
    print(f"💸 Transactions en attente: {len(blockchain.pending_transactions)}")
    print(f"🔗 Dernier hash: {blockchain.chain[-1].hash[:32]}...")

if __name__ == "__main__":
    asyncio.run(main())