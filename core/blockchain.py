import time
import json
from typing import List, Dict, Optional, Any  # ← AJOUTEZ Optional ici
import asyncio
from .block import PQBlock
from .transaction import PQTransaction, PQTxOutput
from .proof_of_work import CPUOnlyMiner
from .smart_contracts import ContractVM, StandardContracts
from config.genesis_block import create_genesis_block, generate_genesis_hash

class QuantumBlockchain:
    """Blockchain finale avec minage CPU, genesis auto et contrats"""
    
    def __init__(self, network_id="quantum_mainnet_cpu"):
        self.network_id = network_id
        self.chain: List[PQBlock] = []
        self.pending_transactions: List[PQTransaction] = []
        self.contract_vm = ContractVM()
        self.miner = CPUOnlyMiner()
        
        # Création automatique du genesis block
        self._create_auto_genesis()
        
        # Déployer les contrats standards
        self._deploy_standard_contracts()
    
    def _create_auto_genesis(self):
        """Créer automatiquement le genesis block à la date actuelle"""
        genesis_config = create_genesis_block()
        
        genesis_block = PQBlock(
            index=0,
            timestamp=genesis_config["timestamp"],
            transactions=[],
            previous_hash="0" * 128,
            nonce=0,
            difficulty=genesis_config["difficulty"]
        )
        
        # Forcer le hash du genesis
        genesis_block.hash = generate_genesis_hash(genesis_config)
        
        self.chain.append(genesis_block)
        print(f"✅ Genesis block créé le {time.ctime(genesis_config['timestamp'])}")
        print(f"📦 Hash: {genesis_block.hash[:64]}...")
    
    def _deploy_standard_contracts(self):
        """Déployer les contrats intelligents standards"""
        try:
            # Contrat de token standard
            token_contract_code = StandardContracts.create_token_contract()
            token_address = self.contract_vm.deploy_contract(
                "GENESIS", token_contract_code
            )
            
            # Contrat multi-signatures
            multisig_code = StandardContracts.create_multisig_wallet()
            multisig_address = self.contract_vm.deploy_contract(
                "GENESIS", multisig_code
            )
            
            print(f"✅ Contrats standards déployés:")
            print(f"   Token: {token_address[:40]}...")
            print(f"   Multisig: {multisig_address[:40]}...")
        except Exception as e:
            print(f"⚠️  Contrats non déployés: {e}")
    
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
    
    def add_transaction(self, from_addr: str, to_addr: str, amount: float) -> bool:
        """Ajouter une transaction simple"""
        try:
            # Créer une transaction basique
            transaction = PQTransaction(
                inputs=[from_addr],
                outputs=[PQTxOutput(to_addr, amount, b"public_key_placeholder")],
                signature=b"signature_placeholder",
                timestamp=time.time()
            )
            
            self.pending_transactions.append(transaction)
            print(f"✅ Transaction ajoutée: {from_addr[:16]}... → {to_addr[:16]}... ({amount} QC)")
            return True
        except Exception as e:
            print(f"❌ Erreur transaction: {e}")
            return False
    
    def execute_smart_contract(self, contract_address: str, function: str, 
                             args: List[Any], caller: str, value: float = 0):
        """Exécuter un contrat intelligent"""
        try:
            result = self.contract_vm.call_contract(
                contract_address, function, args, caller, value
            )
            
            # Créer une transaction pour l'exécution
            if result['success']:
                contract_tx = PQTransaction(
                    inputs=[caller],
                    outputs=[PQTxOutput(contract_address, value, b"contract_public_key")],
                    signature=f"CONTRACT_EXEC_{function}".encode(),
                    timestamp=time.time(),
                    contract_data=result
                )
                self.pending_transactions.append(contract_tx)
            
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_block_header(self, block: PQBlock) -> str:
        """Créer l'en-tête de bloc pour le minage"""
        return json.dumps({
            'index': block.index,
            'timestamp': block.timestamp,
            'merkle_root': block.merkle_root,
            'previous_hash': block.previous_hash,
            'difficulty': block.difficulty
        }, sort_keys=True)
    
    def _calculate_difficulty(self) -> int:
        """Ajustement automatique de la difficulté pour CPU"""
        if len(self.chain) <= 1:
            return 2  # Difficulté très basse pour débuter
        
        if len(self.chain) % 5 == 0:  # Ajuster tous les 5 blocs pour les tests
            return self._adjust_difficulty()
        return self.chain[-1].difficulty
    
    def _adjust_difficulty(self) -> int:
        """Ajuster la difficulté basée sur le temps de minage"""
        if len(self.chain) < 5:
            return 2
        
        # Temps cible: 30 secondes par bloc pour les tests
        target_time = 30 * 5
        actual_time = self.chain[-1].timestamp - self.chain[-5].timestamp
        
        ratio = actual_time / target_time
        
        # Ajustement progressif
        if ratio > 2.0:
            ratio = 2.0
        elif ratio < 0.5:
            ratio = 0.5
        
        new_difficulty = int(self.chain[-1].difficulty * ratio)
        return max(1, min(new_difficulty, 4))  # Limites pour tests
    
    def _create_mining_reward(self, miner_address: str, block_height: int) -> PQTransaction:
        """Créer la transaction de récompense de minage"""
        reward = 50.0  # Récompense fixe pour les tests
        
        return PQTransaction(
            inputs=["0" * 64],  # Input spécial pour récompense
            outputs=[PQTxOutput(miner_address, reward, b"mining_reward")],
            signature=b"mining_reward",
            timestamp=time.time()
        )
    
    def get_blockchain_info(self) -> Dict[str, Any]:
        """Obtenir les informations de la blockchain"""
        return {
            'block_height': len(self.chain),
            'difficulty': self.chain[-1].difficulty if self.chain else 0,
            'pending_transactions': len(self.pending_transactions),
            'network_id': self.network_id
        }