@echo off
chcp 65001
title Quantum Blockchain - Version Complete

echo 🌐 QUANTUM BLOCKCHAIN - LANCEMENT COMPLET
echo ========================================
echo.

cd /d "C:\Users\adrie\Desktop\Projet code\BLOCKCHAIN\Quantum_Blockchain\src"

echo 📦 Vérification des dépendances...
python -c "import aiohttp, websockets, cryptography, psutil" 2>nul
if errorlevel 1 (
    echo ❌ Dépendances manquantes. Installation...
    pip install aiohttp websockets cryptography psutil
)

echo.
echo 🚀 Lancement du nœud complet...
echo 💡 URLs d'accès:
echo    - Interface web: http://localhost:8080
echo    - API REST: http://localhost:8334/api
echo    - Minage CPU: Activé
echo.
echo ⏳ Initialisation en cours...

python main.py --threads 2

pause