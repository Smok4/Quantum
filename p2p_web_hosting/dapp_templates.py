"""
Templates de sites web/dApps pour le réseau P2P
"""

DAPP_TEMPLATES = {
    "basic": """
<!DOCTYPE html>
<html>
<head>
    <title>Quantum dApp</title>
    <script src="/quantum-web3.js"></script>
</head>
<body>
    <h1>🌐 Quantum dApp</h1>
    <div id="blockchain-info">Chargement...</div>
    
    <script>
        // Intégration Web3
        async function loadBlockchainInfo() {
            try {
                const response = await fetch('/api/blockchain');
                const data = await response.json();
                
                document.getElementById('blockchain-info').innerHTML = `
                    <p>Blockchain: ${data.network}</p>
                    <p>Bloc actuel: ${data.block_height}</p>
                    <p>Difficulté: ${data.difficulty}</p>
                `;
            } catch (error) {
                console.error('Erreur:', error);
            }
        }
        
        loadBlockchainInfo();
    </script>
</body>
</html>
""",
    
    "crypto_wallet": """
<!DOCTYPE html>
<html>
<head>
    <title>Portefeuille Quantum</title>
    <script src="/quantum-web3.js"></script>
    <style>
        .wallet { max-width: 400px; margin: 0 auto; padding: 20px; }
        .balance { font-size: 24px; text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="wallet">
        <h1>💰 Portefeuille Quantum</h1>
        <div class="balance" id="balance">-- QC</div>
        <button onclick="sendTransaction()">Envoyer</button>
    </div>
    
    <script>
        class QuantumWallet {
            constructor() {
                this.address = null;
                this.balance = 0;
            }
            
            async connect() {
                // Connexion à la blockchain Quantum
                const response = await fetch('/api/wallet/connect');
                const data = await response.json();
                this.address = data.address;
                this.balance = data.balance;
            }
            
            async updateBalance() {
                document.getElementById('balance').textContent = 
                    this.balance + ' QC';
            }
        }
        
        const wallet = new QuantumWallet();
        wallet.connect().then(() => wallet.updateBalance());
        
        async function sendTransaction() {
            const to = prompt('Adresse destination:');
            const amount = prompt('Montant:');
            
            if (to && amount) {
                await fetch('/api/wallet/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to, amount})
                });
                
                alert('Transaction envoyée!');
            }
        }
    </script>
</body>
</html>
""",
    
    "block_explorer": """
<!DOCTYPE html>
<html>
<head>
    <title>Explorateur Quantum</title>
    <script src="/quantum-web3.js"></script>
    <style>
        .block { border: 1px solid #ccc; margin: 10px; padding: 10px; }
        .transaction { background: #f9f9f9; margin: 5px; padding: 5px; }
    </style>
</head>
<body>
    <h1>🔍 Explorateur de Blocs Quantum</h1>
    <input type="number" id="blockNumber" placeholder="Numéro de bloc">
    <button onclick="loadBlock()">Charger</button>
    
    <div id="blockInfo"></div>
    
    <script>
        async function loadBlock() {
            const blockNumber = document.getElementById('blockNumber').value;
            
            const response = await fetch(`/api/blocks/${blockNumber}`);
            const block = await response.json();
            
            document.getElementById('blockInfo').innerHTML = `
                <div class="block">
                    <h3>Bloc #${block.number}</h3>
                    <p>Hash: ${block.hash}</p>
                    <p>Transactions: ${block.transactions.length}</p>
                    
                    ${block.transactions.map(tx => `
                        <div class="transaction">
                            De: ${tx.from} → À: ${tx.to} (${tx.amount} QC)
                        </div>
                    `).join('')}
                </div>
            `;
        }
    </script>
</body>
</html>
"""
}

class DAppTemplateManager:
    """Gestionnaire de templates de dApps"""
    
    def __init__(self):
        self.templates = DAPP_TEMPLATES
    
    def create_dapp_from_template(self, template_name: str, custom_data: dict = None) -> str:
        """Créer une dApp à partir d'un template"""
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} non trouvé")
        
        template = self.templates[template_name]
        
        if custom_data:
            # Remplacer les variables du template
            for key, value in custom_data.items():
                template = template.replace(f'{{{{ {key} }}}}', str(value))
        
        return template
    
    def get_available_templates(self) -> list:
        """Obtenir la liste des templates disponibles"""
        return list(self.templates.keys())