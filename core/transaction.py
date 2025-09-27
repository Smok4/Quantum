import hashlib
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional  # ← AJOUTEZ Optional ici

@dataclass
class PQTxOutput:
    address: str
    amount: float
    public_key: bytes
    
    def to_dict(self):
        return {
            'address': self.address,
            'amount': self.amount
        }

@dataclass
class PQTransaction:
    inputs: List[str]
    outputs: List[PQTxOutput]
    signature: bytes
    timestamp: float
    tx_hash: Optional[str] = None  # ← ET ici
    contract_data: Optional[Dict[str, Any]] = None  # ← ET ici
    
    def __post_init__(self):
        if self.tx_hash is None:
            self.tx_hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        data = f"{'-'.join(self.inputs)}-{'-'.join([out.address for out in self.outputs])}-{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'hash': self.tx_hash,
            'inputs': self.inputs,
            'outputs': [out.to_dict() for out in self.outputs],
            'timestamp': self.timestamp
        }