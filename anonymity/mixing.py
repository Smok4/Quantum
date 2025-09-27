import random
import time
from typing import List, Dict

class CoinMixer:
    def __init__(self, pool_size=10):
        self.mixing_pool = []
        self.pool_size = pool_size
    
    def add_transaction_to_mix(self, transaction):
        """Ajouter une transaction au pool de mixage"""
        self.mixing_pool.append({
            'transaction': transaction,
            'timestamp': time.time(),
            'mixed': False
        })
        
        # Garder seulement les N dernières transactions
        if len(self.mixing_pool) > self.pool_size:
            self.mixing_pool.pop(0)
    
    def mix_transactions(self):
        """Mélanger les transactions du pool"""
        if len(self.mixing_pool) < 3:  # Minimum 3 transactions pour le mixage
            return []
        
        # Mélanger aléatoirement
        random.shuffle(self.mixing_pool)
        
        # Marquer comme mélangées
        for item in self.mixing_pool:
            item['mixed'] = True
        
        return [item['transaction'] for item in self.mixing_pool]