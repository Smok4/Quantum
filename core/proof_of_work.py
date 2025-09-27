import hashlib
import time
import threading

class CPUOnlyMiner:
    """Mineur CPU simple et stable"""
    
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.hash_rate = 0
        self.is_mining = False
        self.found_nonce = None
        self.found_hash = None
    
    def mine_block(self, block_header, max_threads=1):
        """Minage simple mono-thread pour stabilité"""
        self.is_mining = True
        self.found_nonce = None
        self.found_hash = None
        
        target = "0" * self.difficulty
        nonce = 0
        start_time = time.time()
        hashes_calculated = 0
        
        print(f"⛏️  Début du minage - Difficulté: {self.difficulty} (cible: {target})")
        
        while self.is_mining and nonce < 10000000:  # Limite de sécurité
            # Calcul du hash
            data = f"{block_header}{nonce}"
            block_hash = hashlib.sha256(data.encode()).hexdigest()
            hashes_calculated += 1
            
            # Vérification de la cible
            if block_hash.startswith(target):
                self.found_nonce = nonce
                self.found_hash = block_hash
                mining_time = time.time() - start_time
                self.hash_rate = hashes_calculated / mining_time if mining_time > 0 else 0
                
                print(f"✅ Hash trouvé après {nonce} tentatives!")
                print(f"⚡ Hash rate: {self.hash_rate:.2f} H/s")
                print(f"⏱️  Temps: {mining_time:.2f} secondes")
                print(f"🔑 Nonce: {nonce}")
                print(f"📦 Hash: {block_hash}")
                
                self.is_mining = False
                return nonce, block_hash
            
            nonce += 1
            
            # Affichage de progression
            if nonce % 100000 == 0:
                elapsed = time.time() - start_time
                current_rate = nonce / elapsed if elapsed > 0 else 0
                print(f"🔄 {nonce:,} hashes calculés - {current_rate:.0f} H/s")
        
        # Timeout ou arrêt
        self.is_mining = False
        print("⏹️  Minage arrêté")
        return None, None
    
    def stop_mining(self):
        """Arrêter le minage"""
        self.is_mining = False

class SimpleMiner:
    """Version ultra-simplifiée pour debug"""
    
    @staticmethod
    def quick_mine(block_header, difficulty=4):
        """Minage rapide pour tests"""
        target = "0" * difficulty
        nonce = 0
        
        print(f"🔍 Recherche de hash commençant par: {target}")
        
        while nonce < 1000000:  # Limite raisonnable pour tests
            data = f"{block_header}{nonce}"
            block_hash = hashlib.sha256(data.encode()).hexdigest()
            
            if block_hash.startswith(target):
                print(f"✅ Hash trouvé au nonce {nonce}: {block_hash}")
                return nonce, block_hash
            
            nonce += 1
            
            if nonce % 50000 == 0:
                print(f"🔄 Testé {nonce} nonces...")
        
        print("❌ Hash non trouvé dans la limite")
        return None, None