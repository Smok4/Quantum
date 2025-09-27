from aiohttp import web
import json

class QuantumAPI:
    def __init__(self, blockchain, p2p_network):
        self.blockchain = blockchain
        self.p2p_network = p2p_network
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Configurer les routes API"""
        self.app.router.add_get('/api/blockchain/info', self.get_blockchain_info)
        self.app.router.add_get('/api/blocks/{block_index}', self.get_block)
        self.app.router.add_post('/api/transactions', self.create_transaction)
        self.app.router.add_get('/api/peers', self.get_peers)
    
    async def get_blockchain_info(self, request):
        """Obtenir les infos de la blockchain"""
        info = {
            'block_height': len(self.blockchain.chain),
            'difficulty': self.blockchain.chain[-1].difficulty if self.blockchain.chain else 0,
            'peers_count': len(self.p2p_network.peers),
            'pending_transactions': len(self.blockchain.pending_transactions)
        }
        return web.json_response(info)
    
    async def get_block(self, request):
        """Obtenir un bloc par index"""
        block_index = int(request.match_info['block_index'])
        if block_index < len(self.blockchain.chain):
            block = self.blockchain.chain[block_index]
            return web.json_response(block.to_dict())
        return web.json_response({'error': 'Bloc non trouvé'}, status=404)
    
    async def create_transaction(self, request):
        """Créer une nouvelle transaction"""
        try:
            data = await request.json()
            # Logique de création de transaction
            return web.json_response({'status': 'success'})
        except Exception as e:
            return web.json_response({'error': str(e)}, status=400)
    
    async def get_peers(self, request):
        """Obtenir la liste des pairs"""
        return web.json_response({'peers': list(self.p2p_network.peers)})
    
    async def start(self, host='localhost', port=8334):
        """Démarrer l'API"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        print(f"🌐 API REST démarrée sur http://{host}:{port}")