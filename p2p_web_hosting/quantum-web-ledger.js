// Bibliothèque Web3 avec support Ledger pour Quantum Blockchain
class QuantumWeb3Ledger {
    constructor(providerUrl = '/api/quantum') {
        this.providerUrl = providerUrl;
        this.connected = false;
        this.account = null;
        this.isLedger = false;
        this.ledgerDevice = null;
    }

    // ==================== CONNEXION STANDARD ====================
    async connect() {
        try {
            const response = await fetch(`${this.providerUrl}/connect`);
            const data = await response.json();
            
            this.connected = true;
            this.account = data.account;
            this.isLedger = false;
            
            return this.account;
        } catch (error) {
            console.error('Erreur connexion Quantum Web3:', error);
            throw error;
        }
    }

    // ==================== INTÉGRATION LEDGER ====================
    async connectLedger() {
        try {
            // Vérifier si WebUSB est disponible
            if (!navigator.usb) {
                throw new Error('WebUSB non supporté. Utilisez Chrome ou Edge.');
            }

            // Demander l'accès à la Ledger
            const device = await this.requestLedgerDevice();
            this.ledgerDevice = device;
            
            // Se connecter à l'app Ethereum
            await this.openLedgerApp();
            
            // Récupérer l'adresse
            this.account = await this.getLedgerAddress();
            this.connected = true;
            this.isLedger = true;
            
            console.log('✅ Ledger connecté:', this.account);
            return this.account;
            
        } catch (error) {
            console.error('Erreur connexion Ledger:', error);
            throw error;
        }
    }

    async requestLedgerDevice() {
        const filters = [
            { vendorId: 0x2c97 }, // Ledger vendor ID
            { vendorId: 0x2581 }  // Alternative
        ];
        
        const device = await navigator.usb.requestDevice({ filters });
        await device.open();
        await device.selectConfiguration(1);
        await device.claimInterface(0);
        
        return device;
    }

    async openLedgerApp() {
        // Envoyer la commande pour ouvrir l'app Ethereum
        const OPEN_ETH_APP = [0xe0, 0xd8, 0x00, 0x00, 0x00];
        await this.ledgerDevice.transferOut(1, new Uint8Array(OPEN_ETH_APP));
        
        // Attendre que l'app soit ouverte
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    async getLedgerAddress() {
        // Commande pour récupérer l'adresse Ethereum
        const GET_ADDRESS = [0xe0, 0x02, 0x00, 0x00, 0x00];
        const response = await this.ledgerDevice.transferIn(1, 64);
        
        // Convertir la réponse en adresse
        const data = new Uint8Array(response.data.buffer);
        const address = this.bytesToHex(data).substring(0, 40);
        
        return '0x' + address;
    }

    async signTransactionWithLedger(transactionData) {
        if (!this.isLedger || !this.ledgerDevice) {
            throw new Error('Ledger non connecté');
        }

        // Préparer la transaction pour la Ledger
        const rawTx = this.prepareTransactionForLedger(transactionData);
        
        // Envoyer la transaction à signer
        const SIGN_TX = [0xe0, 0x04, 0x00, 0x00, ...rawTx];
        const response = await this.ledgerDevice.transferIn(1, 64);
        
        // Récupérer la signature
        const signatureData = new Uint8Array(response.data.buffer);
        return this.bytesToHex(signatureData);
    }

    // ==================== FONCTIONS WALLET ====================
    async getBalance(address = this.account) {
        if (this.isLedger) {
            // Solde depuis la Ledger
            return await this.getLedgerBalance();
        }

        const response = await fetch(`${this.providerUrl}/balance/${address}`);
        return await response.json();
    }

    async sendTransaction(to, amount, data = null) {
        const transaction = {
            from: this.account,
            to,
            amount,
            data,
            timestamp: Date.now()
        };

        if (this.isLedger) {
            // Signer avec Ledger
            transaction.signature = await this.signTransactionWithLedger(transaction);
        }

        const response = await fetch(`${this.providerUrl}/send`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(transaction)
        });

        return await response.json();
    }

    async sendWithLedger(to, amount) {
        if (!this.isLedger) {
            await this.connectLedger();
        }
        return await this.sendTransaction(to, amount);
    }

    // ==================== FONCTIONS CONTRATS ====================
    async callContract(contractAddress, method, args = []) {
        const request = {
            contractAddress,
            method,
            args,
            caller: this.account
        };

        const response = await fetch(`${this.providerUrl}/contract/call`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request)
        });

        return await response.json();
    }

    async deployContract(code, initialFunds = 0) {
        const request = {
            code,
            initialFunds,
            deployer: this.account
        };

        const response = await fetch(`${this.providerUrl}/contract/deploy`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request)
        });

        return await response.json();
    }

    // ==================== UTILITAIRES ====================
    bytesToHex(bytes) {
        return Array.from(bytes, byte => 
            byte.toString(16).padStart(2, '0')
        ).join('');
    }

    prepareTransactionForLedger(txData) {
        // Convertir la transaction en format Ledger
        const serialized = JSON.stringify(txData);
        return new TextEncoder().encode(serialized);
    }

    async getLedgerBalance() {
        // Récupérer le solde depuis la Ledger
        const GET_BALANCE = [0xe0, 0x05, 0x00, 0x00, 0x00];
        const response = await this.ledgerDevice.transferIn(1, 32);
        
        const balanceData = new Uint8Array(response.data.buffer);
        const balance = parseInt(this.bytesToHex(balanceData), 16) / 1e18;
        
        return { balance };
    }
}

// Extension pour le support Hardware Wallet
class HardwareWalletSupport {
    static async getSupportedWallets() {
        return {
            'ledger': {
                name: 'Ledger Nano S/X',
                supported: !!navigator.usb,
                vendorIds: [0x2c97, 0x2581]
            },
            'trezor': {
                name: 'Trezor Model T',
                supported: false, // À implémenter
                vendorIds: [0x1209, 0x53c1]
            }
        };
    }

    static async detectConnectedWallets() {
        const connected = [];
        
        if (navigator.usb) {
            try {
                const devices = await navigator.usb.getDevices();
                for (const device of devices) {
                    if (device.vendorId === 0x2c97 || device.vendorId === 0x2581) {
                        connected.push({ type: 'ledger', device });
                    }
                }
            } catch (error) {
                console.error('Erreur détection wallets:', error);
            }
        }
        
        return connected;
    }
}

// Export pour utilisation globale
window.QuantumWeb3 = QuantumWeb3Ledger;
window.HardwareWalletSupport = HardwareWalletSupport;

// Initialisation automatique
document.addEventListener('DOMContentLoaded', async function() {
    if (typeof window.quantumWeb3 === 'undefined') {
        window.quantumWeb3 = new QuantumWeb3Ledger();
        
        // Détecter les wallets connectés
        const connectedWallets = await HardwareWalletSupport.detectConnectedWallets();
        if (connectedWallets.length > 0) {
            console.log('🔗 Wallets détectés:', connectedWallets);
        }
    }
});