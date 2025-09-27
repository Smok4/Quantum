import asyncio
import json

class QuantumProtocol:
    """Protocole de communication P2P sécurisé"""
    
    def __init__(self):
        self.message_handlers = {}
    
    async def handle_message(self, message, peer):
        """Traiter un message reçu"""
        msg_type = message.get('type')
        if msg_type in self.message_handlers:
            await self.message_handlers[msg_type](message, peer)
    
    def register_handler(self, msg_type, handler):
        """Enregistrer un gestionnaire de message"""
        self.message_handlers[msg_type] = handler
    
    def create_message(self, msg_type, data):
        """Créer un message structuré"""
        return {
            'type': msg_type,
            'data': data,
            'timestamp': asyncio.get_event_loop().time(),
            'version': '1.0'
        }