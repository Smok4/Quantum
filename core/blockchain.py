def mine_new_block(self, miner_address: str, max_threads=None) -> Optional[PQBlock]:
    """Minage d'un nouveau bloc (CPU uniquement)"""
    if not self.pending_transactions:
        print("⏭️  Aucune transaction en attente - création d'une transaction test")
        # Ajouter une transaction test
        self.add_transaction(miner_address, "QmTEST_" + str(int(time.time()))[-6:], 0.5)
    
    previous_block = self.chain[-1]
    difficulty = self._calculate_difficulty()
    
    print(f"📦 Création du bloc #{len(self.chain)} - Difficulté: {difficulty}")
    
    # Créer le bloc
    new_block = PQBlock(
        index=len(self.chain),
        timestamp=time.time(),
        transactions=self.pending_transactions.copy(),
        previous_hash=previous_block.hash,
        nonce=0,
        difficulty=difficulty
    )
    
    # Minage CPU - version simplifiée
    block_header = self._create_block_header(new_block)
    print(f"🔍 Début du minage de l'en-tête: {block_header[:50]}...")
    
    # Utiliser le mineur simple
    from .proof_of_work import SimpleMiner
    nonce, block_hash = SimpleMiner.quick_mine(block_header, difficulty)
    
    if nonce is not None:
        new_block.nonce = nonce
        new_block.hash = block_hash
        
        # Ajouter la récompense de minage
        reward_tx = self._create_mining_reward(miner_address, new_block.index)
        new_block.transactions.insert(0, reward_tx)
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        print(f"✅ Bloc #{new_block.index} miné avec succès!")
        print(f"📊 Transactions: {len(new_block.transactions)}")
        print(f"🔗 Hash précédent: {new_block.previous_hash[:16]}...")
        print(f"🔑 Nonce: {new_block.nonce}")
        print(f"📦 Hash: {new_block.hash}")
        
        return new_block
    
    print("❌ Échec du minage du bloc")
    return None