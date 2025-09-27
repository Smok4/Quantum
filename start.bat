<<<<<<< HEAD
@echo off
chcp 65001
title Quantum Blockchain Windows

echo 🌐 Quantum Blockchain - Démarrage...
echo.

# Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo 📥 Téléchargez Python depuis: https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté

# Vérifier et installer les dépendances
if not exist "requirements.txt" (
    echo ❌ Fichier requirements.txt manquant
    pause
    exit /b 1
)

echo 📦 Installation des dépendances...
pip install -r requirements.txt

echo 🚀 Lancement de Quantum Blockchain...
python main.py --web-port 8080 --p2p-port 8333

=======
@echo off
chcp 65001
cd /d "C:\Users\adrie\Desktop\Projet code\BLOCKCHAIN\Quantum_Blockchain\src"
python main.py
>>>>>>> aabbdd6 (Quantum)
pause