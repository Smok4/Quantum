import asyncio
import json
from typing import Dict, Any
from core.blockchain import QuantumBlockchain
from core.smart_contracts import QuantumSmartContract

class Web3BlockchainIntegration:
    """Intégration Web3 pour les sites décentralisés"""
    
    def __init__(self, blockchain: QuantumBlockchain):
        self.blockchain = blockchain
        self.dapp_registry = {}  # Registry des dApps hébergées
        
    async def register_dapp(self, site_hash: str, dapp_contract: Dict[str, Any]):
        """Enregistrer une dApp sur la blockchain"""
        # Créer un contrat pour la dApp
        contract_code = self.generate_dapp_contract_code(dapp_contract)
        
        contract_address = self.blockchain.contract_vm.deploy_contract(
            "DAPP_REGISTRY", contract_code
        )
        
        # Stocker les métadonnées
        self.dapp_registry[site_hash] = {
            'contract_address': contract_address,
            'site_hash': site_hash,
            'name': dapp_contract.get('name', 'Unnamed DApp'),
            'description': dapp_contract.get('description', ''),
            'version': dapp_contract.get('version', '1.0.0')
        }
        
        return contract_address
    
    def generate_dapp_contract_code(self, dapp_contract: Dict[str, Any]) -> str:
        """Générer le code de contrat pour une dApp"""
        return f"""
def getSiteInfo():
    return {{
        'name': '{dapp_contract.get('name', '')}',
        'description': '{dapp_contract.get('description', '')}',
        'version': '{dapp_contract.get('version', '1.0.0')}',
        'author': '{dapp_contract.get('author', '')}'
    }}

def getSiteHash():
    return '{dapp_contract.get('site_hash', '')}'

def verifyOwnership(owner_address):
    # Logique de vérification de propriété
    return storage.get('owner', '') == owner_address

def updateSite(new_site_hash, signature):
    require(verifyOwnership(caller), "Not owner")
    storage['site_hash'] = new_site_hash
    return True
"""
    
    async def serve_dapp(self, site_hash: str) -> Dict[str, Any]:
        """Servir une dApp via la blockchain"""
        if site_hash not in self.dapp_registry:
            return {'error': 'DApp non trouvée'}
        
        dapp_info = self.dapp_registry[site_hash]
        
        # Récupérer les infos depuis la blockchain
        result = self.blockchain.execute_smart_contract(
            dapp_info['contract_address'], 'getSiteInfo', [], 'WEB3_SERVER'
        )
        
        return {
            'dapp_info': result.get('result', {}),
            'contract_address': dapp_info['contract_address'],
            'blockchain_integrated': True
        }

class DecentralizedStorage:
    """Stockage décentralisé pour les sites web"""
    
    def __init__(self, p2p_web_server):
        self.p2p_web_server = p2p_web_server
        self.chunk_size = 1024 * 1024  # 1MB par chunk
        
    async def store_large_site(self, site_files: Dict[str, bytes]) -> str:
        """Stocker un grand site en chunks distribués"""
        site_hash = self.p2p_web_server.create_site_hash(site_files)
        
        # Diviser les gros fichiers en chunks
        chunks = await self.split_into_chunks(site_files)
        
        # Distribuer les chunks sur le réseau P2P
        await self.distribute_chunks(site_hash, chunks)
        
        return site_hash
    
    async def split_into_chunks(self, site_files: Dict[str, bytes]) -> Dict[str, List[bytes]]:
        """Diviser les fichiers en chunks"""
        chunks = {}
        
        for filename, content in site_files.items():
            if len(content) > self.chunk_size:
                # Diviser en chunks
                file_chunks = []
                for i in range(0, len(content), self.chunk_size):
                    chunk = content[i:i + self.chunk_size]
                    file_chunks.append(chunk)
                chunks[filename] = file_chunks
            else:
                chunks[filename] = [content]
        
        return chunks
    
    async def distribute_chunks(self, site_hash: str, chunks: Dict[str, List[bytes]]):
        """Distribuer les chunks sur le réseau P2P"""
        # Implémentation simplifiée de distribution
        # Dans une version complète, on utiliserait DHT ou IPFS-like
        
        for filename, file_chunks in chunks.items():
            for chunk_index, chunk_data in enumerate(file_chunks):
                chunk_id = f"{site_hash}_{filename}_{chunk_index}"
                
                # Stocker localement
                await self.p2p_web_server.store_file(site_hash, f"chunks/{chunk_id}", chunk_data)
                
                # Répliquer sur 3 pairs aléatoires
                await self.replicate_chunk(chunk_id, chunk_data)
    
    async def replicate_chunk(self, chunk_id: str, chunk_data: bytes):
        """Répliquer un chunk sur le réseau"""
        # Implémentation basique - à améliorer avec un vrai protocole P2P
        peers = self.p2p_web_server.peer_servers[:3]  # Premiers 3 pairs
        
        for peer in peers:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        f"http://{peer}/store_chunk",
                        json={'chunk_id': chunk_id, 'data': chunk_data.hex()}
                    )
            except:
                continue