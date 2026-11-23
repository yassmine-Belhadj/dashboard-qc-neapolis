# Système de pilotage de la performance et amélioration continue
### Laboratoire de Contrôle Qualité Pharmaceutique — Hana Brinis
**Projet de Fin d'Études (PFE) — 2026**

Tableau de bord interactif d'évaluation de la performance analytique et de suivi des gains temporels issus de la démarche d'amélioration continue (**Phase Mesurer → Phase Contrôler**).

---

## 1. Contexte & Périmètre

- **Période d'évaluation :** Mars 2026 — Août 2026
- **Produits analysés :** Lénalidomide & Respyva
- **Périmètre analytique :** Dosage, Dissolution, PDG, DUSA, NGI
- **Équipements :** Chaînes HPLC, systèmes de préparation, dissolution et tests aérosols

### Résultats Clés :
- **Temps de Non-Valeur Ajoutée (NVA) :** Réduit de **621 min à 253 min** (**-59,3 %**)
- **Gain temporel net :** **+368 minutes** (≈ 6,1 heures d'activité à forte valeur ajoutée restituées)
- **Taux de perte global :** Réduit de **11,35 % à 4,96 %** du temps opérateur global
- **Facteur déterminant :** Remplacement du système d'eau purifiée (Action P-01) éliminant **265 min** de perte (**72 % du gain total**).

---

## 2. Lancement en Local (sur votre ordinateur)

Dans un terminal PowerShell ou Invite de commandes, dans ce dossier :

```powershell
pip install -r requirements.txt
streamlit run app.py
```

L'application s'ouvrira automatiquement à l'adresse : **http://localhost:8502** (ou 8501).

---

## 3. Déploiement en Ligne Gratuit (pour le jour de la soutenance)

Pour permettre aux membres du jury d'accéder au système via un lien web direct :

1. Créez un compte gratuit sur [GitHub](https://github.com).
2. Créez un nouveau dépôt public (ex : `qc-performance-dashboard`).
3. Déposez l'ensemble des fichiers de ce dossier sur le dépôt :
   - `app.py`
   - `requirements.txt`
   - `Dashboard_QC_Final_Dates_Mars_Aout_Saisie_Simplifiee.xlsx`
   - Le dossier `dashboard_qc/`
   - Le dossier `.streamlit/`
4. Connectez-vous sur [Streamlit Community Cloud](https://share.streamlit.io) avec votre compte GitHub.
5. Cliquez sur **New app**, sélectionnez votre dépôt et validez (`Main file path: app.py`).
6. Votre tableau de bord sera instantanément accessible via une URL sécurisée (ex : `https://qc-pilotage-performance.streamlit.app`).

---

## 4. Mise à Jour Automatisée des Données

Le système est conçu pour intégrer dynamiquement de nouveaux relevés sans modification du code :

- **Via l'interface :** Glissez-déposez simplement un nouveau fichier `.xlsx` dans la zone **"Importer un nouveau fichier Excel"** située dans le menu latéral. L'application met immédiatement à jour l'ensemble des indicateurs, graphiques et tableaux.
- **En local :** Déposez le nouveau classeur Excel dans le répertoire racine et cliquez sur **"Recharger les données actuelles"**.

---

## 5. Structure de l'Application

```
HanaBrinis/
├── app.py                                         # Application principale Streamlit
├── requirements.txt                               # Dépendances Python
├── README.md                                      # Documentation technique & présentation
├── Dashboard_QC_Final_Dates_Mars_Aout_...xlsx     # Source de données Excel active
├── .streamlit/
│   └── config.toml                                # Configuration de la charte graphique
└── dashboard_qc/
    ├── styles.py                                  # Palette de couleurs et styles CSS
    ├── charts.py                                  # Moteur de génération des visualisations Plotly
    └── data_loader.py                             # Modules d'extraction et contrôle d'intégrité
```
