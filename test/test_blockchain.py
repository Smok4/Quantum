import unittest
from src.core.blockchain import QuantumBlockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = QuantumBlockchain()
    
    def test_genesis_block(self):
        """Test que le bloc genesis est créé correctement"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
    
    def test_add_transaction(self):
        """Test l'ajout de transactions"""
        # Implémentation des tests
        pass

if __name__ == '__main__':
    unittest.main()