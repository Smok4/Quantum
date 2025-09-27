class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def validate_block(self, block):
        """Valider un bloc selon les règles de consensus"""
        if block.index != len(self.blockchain.chain):
            return False, "Index incorrect"
        
        if block.previous_hash != self.blockchain.chain[-1].hash:
            return False, "Hash précédent invalide"
        
        if not self.validate_proof_of_work(block):
            return False, "Preuve de travail invalide"
        
        return True, "Bloc valide"
    
    def validate_proof_of_work(self, block):
        """Valider la preuve de travail"""
        target = "0" * block.difficulty
        return block.hash.startswith(target)