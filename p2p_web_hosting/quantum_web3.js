// Bibliothèque JavaScript pour l'intégration Web3 Quantum
class QuantumWeb3 {
    constructor(providerUrl = '/api/quantum') {
        this.providerUrl = providerUrl;
        this.connected = false;
        this.account = null;
    }

    async connect() {
        try {
            const response = await fetch(`${this.providerUrl}/connect`);
            const data = await response.json();
            
            this.connected = true;
            this.account = data.account;
            
            return this.account;
        } catch (error) {
            console.error('Erreur connexion Quantum Web3:', error);
            throw error;
        }
    }

    async getBalance(address = this.account) {
        const response = await fetch(`${this.providerUrl}/balance/${address}`);
        return await response.json();
    }

    async sendTransaction(to, amount, data = null) {
        const transaction = {
            from: this.account,
            to,
            amount,
            data
        };

        const response = await fetch(`${this.providerUrl}/send`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(transaction)
        });

        return await response.json();
    }

    async callContract(contractAddress, method, args = []) {
        const request = {
            contractAddress,
            method,
            args
        };

        const response = await fetch(`${this.providerUrl}/contract/call`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request)
        });

        return await response.json();
    }

    async getBlockNumber() {
        const response = await fetch(`${this.providerUrl}/blocknumber`);
        return await response.json();
    }
}

// Exporter pour utilisation globale
window.QuantumWeb3 = QuantumWeb3;

// Initialisation automatique
document.addEventListener('DOMContentLoaded', async function() {
    if (typeof window.quantumWeb3 === 'undefined') {
        window.quantumWeb3 = new QuantumWeb3();
        
        try {
            await window.quantumWeb3.connect();
            console.log('🌐 Quantum Web3 connecté');
        } catch (error) {
            console.log('⚠️ Mode déconnecté - Blockchain non disponible');
        }
    }
});