import unittest
from src.crypto.post_quantum import PostQuantumCrypto

class TestCrypto(unittest.TestCase):
    def test_key_generation(self):
        """Test la génération de clés"""
        crypto = PostQuantumCrypto()
        pub, priv = crypto.generate_keypair()
        self.assertEqual(len(pub), 64)
        self.assertEqual(len(priv), 64)

if __name__ == '__main__':
    unittest.main()