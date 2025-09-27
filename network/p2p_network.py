import asyncio
import aiohttp
from typing import List, Set

class QuantumP2PNetwork:
    def __init__(self, port=8333, bootstrap_nodes=None):
        self.port = port
        self.bootstrap_nodes = bootstrap_nodes or []
        self.peers: Set[str] = set()
        self.is_running = False
    
    async def start(self):
        self.is_running = True
        await self.discover_peers()
        print(f"🌐 Réseau P2P démarré sur le port {self.port}")
    
    async def discover_peers(self):
        for node in self.bootstrap_nodes:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{node}/peers", timeout=5) as resp:
                        if resp.status == 200:
                            peers = await resp.json()
                            self.peers.update(peers)
            except:
                continue
    
    async def broadcast_transaction(self, transaction):
        for peer in self.peers:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(f"http://{peer}/transaction", 
                                     json=transaction.to_dict())
            except:
                continue
    
    async def stop(self):
        self.is_running = False