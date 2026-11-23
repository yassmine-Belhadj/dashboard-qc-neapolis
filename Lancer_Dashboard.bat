@echo off
title Systeme de Pilotage de la Performance QC - Hana Brinis
chcp 65001 >nul
cls
echo ======================================================================
echo    🌸 SYSTEME DE PILOTAGE DE LA PERFORMANCE QC - HANA BRINIS 🌸
echo    Laboratoires Neapolis Pharma (Projet de Fin d'Etudes)
echo ======================================================================
echo.
cd /d "%~dp0"

echo [1/3] Verification des modules Python...
python -m pip install -r requirements.txt --quiet --no-warn-script-location

echo.
echo [2/3] Ouverture automatique de la page Web...
start http://localhost:8502

echo.
echo [3/3] Lancement de l'application Streamlit sur le port 8502...
echo (Ne fermez pas cette fenetre noire pendant l'utilisation)
echo.
python -m streamlit run app.py --server.port 8502 --server.headless true

pause
