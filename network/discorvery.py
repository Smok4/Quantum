import asyncio
import aiohttp
from typing import List

class PeerDiscovery:
    def __init__(self, bootstrap_nodes: List[str]):
        self.bootstrap_nodes = bootstrap_nodes
        self.discovered_peers = set()
    
    async def discover_peers(self):
        """Découvrir des pairs via les nœuds bootstrap"""
        tasks = []
        for node in self.bootstrap_nodes:
            task = asyncio.create_task(self.query_bootstrap_node(node))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        return list(self.discovered_peers)
    
    async def query_bootstrap_node(self, node_url):
        """Interroger un nœud bootstrap pour découvrir des pairs"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{node_url}/peers", timeout=5) as response:
                    if response.status == 200:
                        peers = await response.json()
                        self.discovered_peers.update(peers)
        except Exception as e:
            print(f"Erreur avec {node_url}: {e}")