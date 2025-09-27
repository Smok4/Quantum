import asyncio
import aiohttp
from aiohttp import web
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import mimetypes
from datetime import datetime

class P2PWebServer:
    """Serveur web décentralisé P2P"""
    
    def __init__(self, port=8080, storage_path="./p2p_web_storage"):
        self.port = port
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        self.hosted_sites: Dict[str, Dict] = {}  # site_hash -> site_data
        self.peer_servers: List[str] = []  # Liste des pairs serveurs web
        
        # Créer l'application web
        self.app = web.Application()
        self.setup_routes()
        
    def setup_routes(self):
        """Configurer les routes HTTP"""
        self.app.router.add_get('/', self.handle_index)
        self.app.router.add_get('/{site_hash}/{path:.*}', self.handle_site_request)
        self.app.router.add_post('/upload', self.handle_upload)
        self.app.router.add_get('/discover', self.handle_discover)
        self.app.router.add_post('/register', self.handle_register)
        
    async def handle_index(self, request):
        """Page d'accueil du réseau web P2P"""
        sites_count = len(self.hosted_sites)
        peers_count = len(self.peer_servers)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🌐 Quantum Web P2P</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 10px; }}
                .stats {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .upload {{ border: 2px dashed #3498db; padding: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌐 Quantum Web P2P</h1>
                <p>Hébergement web décentralisé sur la blockchain</p>
            </div>
            
            <div class="stats">
                <h3>📊 Statistiques du réseau</h3>
                <p>🖥️ Sites hébergés: <strong>{sites_count}</strong></p>
                <p>🔗 Pairs connectés: <strong>{peers_count}</strong></p>
                <p>🌍 Votre nœud: <code>http://{request.host}</code></p>
            </div>
            
            <div class="upload">
                <h3>📤 Uploader un site web</h3>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="siteFiles" webkitdirectory directory multiple>
                    <button type="submit">Héberger sur le réseau P2P</button>
                </form>
                <div id="uploadStatus"></div>
            </div>
            
            <div>
                <h3>🕸️ Sites disponibles</h3>
                <div id="sitesList">
                    {self.generate_sites_list()}
                </div>
            </div>
            
            <script>
                document.getElementById('uploadForm').addEventListener('submit', async function(e) {{
                    e.preventDefault();
                    const files = document.getElementById('siteFiles').files;
                    const formData = new FormData();
                    
                    for (let file of files) {{
                        // Préserver la structure des dossiers
                        formData.append('files', file, file.webkitRelativePath || file.name);
                    }}
                    
                    try {{
                        const response = await fetch('/upload', {{
                            method: 'POST',
                            body: formData
                        }});
                        const result = await response.json();
                        document.getElementById('uploadStatus').innerHTML = 
                            '<p style="color: green;">✅ Site uploadé! Hash: ' + result.site_hash + '</p>';
                    }} catch (error) {{
                        document.getElementById('uploadStatus').innerHTML = 
                            '<p style="color: red;">❌ Erreur: ' + error + '</p>';
                    }}
                }});
            </script>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    
    def generate_sites_list(self):
        """Générer la liste des sites disponibles"""
        if not self.hosted_sites:
            return "<p>Aucun site hébergé pour le moment</p>"
        
        sites_html = ""
        for site_hash, site_data in self.hosted_sites.items():
            sites_html += f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0;">
                <h4>🌍 {site_data.get('name', 'Site sans nom')}</h4>
                <p>📁 Fichiers: {len(site_data.get('files', []))}</p>
                <p>🔗 <a href="/{site_hash}/">Accéder au site</a></p>
                <p>📏 Taille: {site_data.get('size', 0)} bytes</p>
            </div>
            """
        return sites_html
    
    async def handle_site_request(self, request):
        """Servir les fichiers d'un site hébergé"""
        site_hash = request.match_info['site_hash']
        path = request.match_info['path'] or 'index.html'
        
        # Chercher localement d'abord
        file_content = await self.get_local_file(site_hash, path)
        if file_content:
            return await self.serve_file(content=file_content, filename=path)
        
        # Si pas trouvé localement, chercher sur le réseau P2P
        file_content = await self.fetch_from_peers(site_hash, path)
        if file_content:
            # Stocker localement pour cache
            await self.store_file(site_hash, path, file_content)
            return await self.serve_file(content=file_content, filename=path)
        
        return web.Response(text="Fichier non trouvé", status=404)
    
    async def handle_upload(self, request):
        """Uploader un site web sur le réseau P2P"""
        reader = await request.multipart()
        site_files = {}
        
        async for field in reader:
            if field.name == 'files':
                filename = field.filename
                file_content = await field.read()
                
                # Préserver la structure des dossiers
                site_files[filename] = file_content
        
        if not site_files:
            return web.json_response({'error': 'Aucun fichier uploadé'}, status=400)
        
        # Créer le hash du site
        site_hash = self.create_site_hash(site_files)
        
        # Stocker les fichiers localement
        await self.store_site(site_hash, site_files)
        
        # Annoncer le site sur le réseau P2P
        await self.announce_site(site_hash, site_files)
        
        return web.json_response({
            'site_hash': site_hash,
            'files_count': len(site_files),
            'message': 'Site uploadé avec succès'
        })
    
    async def handle_discover(self, request):
        """Découvrir des sites sur le réseau P2P"""
        discovered_sites = await self.discover_peers_sites()
        return web.json_response({'sites': discovered_sites})
    
    async def handle_register(self, request):
        """Enregistrer un nouveau pair serveur web"""
        data = await request.json()
        peer_address = data.get('peer_address')
        
        if peer_address and peer_address not in self.peer_servers:
            self.peer_servers.append(peer_address)
            
        return web.json_response({'peers_count': len(self.peer_servers)})
    
    def create_site_hash(self, site_files: Dict[str, bytes]) -> str:
        """Créer un hash unique pour le site"""
        all_content = b''
        for filename in sorted(site_files.keys()):
            all_content += filename.encode() + site_files[filename]
        
        return hashlib.sha3_512(all_content).hexdigest()[:32]
    
    async def store_site(self, site_hash: str, site_files: Dict[str, bytes]):
        """Stocker un site localement"""
        site_dir = self.storage_path / site_hash
        site_dir.mkdir(exist_ok=True)
        
        total_size = 0
        for filename, content in site_files.items():
            file_path = site_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(content)
            total_size += len(content)
        
        self.hosted_sites[site_hash] = {
            'name': 'Site uploadé',
            'files': list(site_files.keys()),
            'size': total_size,
            'upload_time': datetime.now().isoformat()
        }
    
    async def get_local_file(self, site_hash: str, filepath: str) -> Optional[bytes]:
        """Récupérer un fichier localement"""
        file_path = self.storage_path / site_hash / filepath
        if file_path.exists():
            with open(file_path, 'rb') as f:
                return f.read()
        return None
    
    async def store_file(self, site_hash: str, filepath: str, content: bytes):
        """Stocker un fichier localement (cache)"""
        file_path = self.storage_path / site_hash / filepath
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(content)
    
    async def fetch_from_peers(self, site_hash: str, filepath: str) -> Optional[bytes]:
        """Chercher un fichier sur les pairs P2P"""
        for peer in self.peer_servers:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"http://{peer}/{site_hash}/{filepath}"
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            return await response.read()
            except:
                continue
        return None
    
    async def announce_site(self, site_hash: str, site_files: Dict[str, bytes]):
        """Annoncer un nouveau site sur le réseau P2P"""
        site_info = {
            'site_hash': site_hash,
            'files_count': len(site_files),
            'total_size': sum(len(c) for c in site_files.values()),
            'timestamp': datetime.now().isoformat()
        }
        
        # Annoncer à tous les pairs connus
        for peer in self.peer_servers:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(f"http://{peer}/announce", 
                                     json=site_info, timeout=5)
            except:
                continue  # Ignorer les pairs indisponibles
    
    async def discover_peers_sites(self) -> List[Dict]:
        """Découvrir les sites des pairs"""
        discovered_sites = []
        
        for peer in self.peer_servers:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{peer}/sites", timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            discovered_sites.extend(data.get('sites', []))
            except:
                continue
        
        return discovered_sites
    
    async def serve_file(self, content: bytes, filename: str) -> web.Response:
        """Servir un fichier avec le bon Content-Type"""
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        return web.Response(
            body=content,
            content_type=mime_type,
            headers={'Cache-Control': 'public, max-age=3600'}
        )
    
    async def start(self):
        """Démarrer le serveur web P2P"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        
        print(f"🌐 Serveur web P2P démarré sur le port {self.port}")
        print(f"📁 Stockage: {self.storage_path}")
    
    async def stop(self):
        """Arrêter le serveur web P2P"""
        await self.app.shutdown()
        await self.app.cleanup()