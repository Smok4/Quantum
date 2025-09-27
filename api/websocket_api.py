import asyncio
import websockets
import json

class WebSocketAPI:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.connections = set()
    
    async def handler(self, websocket, path):
        """Gérer les connexions WebSocket"""
        self.connections.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(message, websocket)
        finally:
            self.connections.remove(websocket)
    
    async def handle_message(self, message, websocket):
        """Traiter un message WebSocket"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'subscribe_blocks':
                await self.send_block_updates(websocket)
            elif msg_type == 'get_blockchain_info':
                await self.send_blockchain_info(websocket)
        except Exception as e:
            print(f"Erreur WebSocket: {e}")
    
    async def send_block_updates(self, websocket):
        """Envoyer les mises à jour de blocs"""
        # Implémentation simplifiée
        pass
    
    async def send_blockchain_info(self, websocket):
        """Envoyer les infos de la blockchain"""
        info = {
            'type': 'blockchain_info',
            'block_height': len(self.blockchain.chain),
            'difficulty': self.blockchain.chain[-1].difficulty if self.blockchain.chain else 0
        }
        await websocket.send(json.dumps(info))
    
    async def start(self, host='localhost', port=8335):
        """Démarrer le serveur WebSocket"""
        server = await websockets.serve(self.handler, host, port)
        print(f"🔌 WebSocket API démarrée sur ws://{host}:{port}")
        return server