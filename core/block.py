import hashlib
import json
from dataclasses import dataclass
from typing import List, Optional  # ← AJOUTEZ Optional ici
from .transaction import PQTransaction

@dataclass
class PQBlock:
    index: int
    timestamp: float
    transactions: List[PQTransaction]
    previous_hash: str
    nonce: int
    difficulty: int
    merkle_root: Optional[str] = None  # ← ET ici
    hash: Optional[str] = None  # ← ET ici
    
    def __post_init__(self):
        if self.merkle_root is None:
            self.merkle_root = self.calculate_merkle_root()
        if self.hash is None:
            self.hash = self.calculate_hash()
    
    def calculate_merkle_root(self) -> str:
        if not self.transactions:
            return "0" * 64
            
        tx_hashes = [tx.tx_hash for tx in self.transactions]
        while len(tx_hashes) > 1:
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                if i + 1 < len(tx_hashes):
                    combined = tx_hashes[i] + tx_hashes[i + 1]
                    new_hash = hashlib.sha256(combined.encode()).hexdigest()
                else:
                    new_hash = tx_hashes[i]
                new_hashes.append(new_hash)
            tx_hashes = new_hashes
        return tx_hashes[0]
    
    def calculate_hash(self) -> str:
        data = f"{self.index}{self.timestamp}{self.merkle_root}{self.previous_hash}{self.nonce}{self.difficulty}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'transactions_count': len(self.transactions)
        }