import hashlib
import time
from typing import Dict, List, Any

class QuantumSmartContract:
    """Contrat intelligent simplifié"""
    
    def __init__(self, contract_address: str, creator: str, code: str = ""):
        self.contract_address = contract_address
        self.creator = creator
        self.code = code
        self.storage: Dict[str, Any] = {}
        self.balance = 0.0
    
    def execute(self, function_name: str, args: List[Any], caller: str, value: float = 0):
        """Exécuter une fonction du contrat"""
        try:
            if function_name == "getBalance":
                return self.balance
            elif function_name == "deposit":
                self.balance += value
                return True
            elif function_name == "getStorage":
                key = args[0] if args else ""
                return self.storage.get(key)
            elif function_name == "setStorage":
                if len(args) >= 2:
                    self.storage[args[0]] = args[1]
                    return True
                return False
            else:
                return f"Fonction {function_name} exécutée avec args {args}"
        except Exception as e:
            return f"Erreur: {e}"

class ContractVM:
    """Machine virtuelle de contrats simplifiée"""
    
    def __init__(self):
        self.contracts: Dict[str, QuantumSmartContract] = {}
    
    def deploy_contract(self, creator: str, code: str = "", initial_funds: float = 0) -> str:
        """Déployer un nouveau contrat"""
        contract_address = self._generate_contract_address(creator)
        
        contract = QuantumSmartContract(
            contract_address=contract_address,
            creator=creator,
            code=code
        )
        contract.balance = initial_funds
        
        self.contracts[contract_address] = contract
        return contract_address
    
    def call_contract(self, contract_address: str, function: str, 
                     args: List[Any], caller: str, value: float = 0, gas: int = 100000):
        """Appeler une fonction de contrat"""
        if contract_address not in self.contracts:
            return {'success': False, 'error': 'Contract not found'}
        
        contract = self.contracts[contract_address]
        
        if value > 0:
            contract.balance += value
        
        try:
            result = contract.execute(function, args, caller, value)
            return {
                'success': True,
                'result': result,
                'gas_used': gas,
                'contract_address': contract_address
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'gas_used': gas // 2
            }
    
    def _generate_contract_address(self, creator: str) -> str:
        """Générer une adresse de contrat unique"""
        data = f"{creator}{time.time()}".encode()
        return "QC_" + hashlib.sha256(data).hexdigest()[:20]

class StandardContracts:
    """Contrats standards"""
    
    @staticmethod
    def create_token_contract():
        return "Token contract template"
    
    @staticmethod
    def create_multisig_wallet():
        return "Multisig wallet template"