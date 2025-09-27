import click
from core.blockchain import QuantumBlockchain

@click.group()
def cli():
    """Interface CLI pour Quantum Blockchain"""
    pass

@cli.command()
def start():
    """Démarrer le nœud"""
    blockchain = QuantumBlockchain()
    click.echo("🚀 Nœud Quantum Blockchain démarré")

@cli.command()
@click.option('--to', required=True, help='Adresse du destinataire')
@click.option('--amount', required=True, type=float, help='Montant à envoyer')
def send(to, amount):
    """Envoyer une transaction"""
    click.echo(f"📤 Envoi de {amount} QC à {to}")

@cli.command()
def info():
    """Afficher les informations du nœud"""
    click.echo("📊 Informations du nœud:")
    click.echo("- Blockchain: Quantum Mainnet")
    click.echo("- Status: Actif")

if __name__ == '__main__':
    cli()