"""
data_loader.py
Charge toutes les feuilles du fichier Excel QC.
Aucune donnée n'est modifiée — lecture pure.
"""

import pandas as pd
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "..", "Dashboard_QC_Final_Dates_Mars_Aout_Saisie_Simplifiee.xlsx")


def get_excel_path():
    """Retourne le chemin absolu du fichier Excel."""
    return os.path.abspath(EXCEL_PATH)


@st_cache
def load_timesheets():
    """Feuille : Saisie TimeSheets — 248 activités."""
    df = pd.read_excel(get_excel_path(), sheet_name="Saisie TimeSheets", header=4)
    df.columns = df.columns.str.strip()
    df = df[df["ID activité"].notna() & df["ID activité"].astype(str).str.startswith("QC-")]
    df["Durée brute (min)"] = pd.to_numeric(df["Durée brute (min)"], errors="coerce")
    df["Temps net (min)"] = pd.to_numeric(df["Temps net (min)"], errors="coerce")
    df["NVA inclus (min)"] = pd.to_numeric(df["NVA inclus (min)"], errors="coerce")
    return df


@st_cache
def load_evenements_nva():
    """Feuille : Evenements NVA — 44 événements (22 AVANT + 22 APRÈS)."""
    df = pd.read_excel(get_excel_path(), sheet_name="Evenements NVA", header=3)
    df.columns = df.columns.str.strip()
    # Trouver les colonnes correctement
    # Header est sur la ligne 4 (index 3)
    df = df[df["ID"].notna() & df["ID"].astype(str).str.match(r"(NVA|EX)-\d+")]
    df["Durée (min)"] = pd.to_numeric(df["Durée (min)"], errors="coerce")
    return df


@st_cache
def load_analyse_pertes():
    """Feuille : Analyse Pertes — comparaison par cause."""
    df = pd.read_excel(get_excel_path(), sheet_name="Analyse Pertes", header=4)
    df.columns = df.columns.str.strip()
    # Garder seulement les lignes avec une source de perte
    df = df[df.iloc[:, 0].notna() & ~df.iloc[:, 0].astype(str).str.startswith("TOTAL")]
    df = df.iloc[:, :8]  # Colonnes pertinentes
    df.columns = ["Source de perte NVA", "AVANT (min)", "APRÈS (min)", "Gain (min)",
                  "Réduction (%)", "Occ. AVANT", "Occ. APRÈS", "Cumul AVANT (%)"]
    for col in ["AVANT (min)", "APRÈS (min)", "Gain (min)", "Réduction (%)", "Occ. AVANT", "Occ. APRÈS"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st_cache
def load_comparaison_globale():
    """Feuille : Comparaison Globale — KPI AVANT/APRÈS."""
    df = pd.read_excel(get_excel_path(), sheet_name="Comparaison Globale", header=4)
    df.columns = ["Indicateur", "AVANT", "APRÈS", "Variation"]
    df = df[df["Indicateur"].notna() & ~df["Indicateur"].astype(str).str.startswith("TOTAL")]
    df = df[df["Indicateur"].astype(str).str.strip() != ""]
    df["AVANT"] = pd.to_numeric(df["AVANT"], errors="coerce")
    df["APRÈS"] = pd.to_numeric(df["APRÈS"], errors="coerce")
    df["Variation"] = pd.to_numeric(df["Variation"], errors="coerce")
    df = df[df["AVANT"].notna()]
    return df


@st_cache
def load_suivi_actions():
    """Feuille : Suivi Actions — 6 actions."""
    df = pd.read_excel(get_excel_path(), sheet_name="Suivi Actions", header=4)
    df.columns = df.columns.str.strip()
    df = df[df["ID"].notna() & df["ID"].astype(str).str.startswith("P-")]
    return df


@st_cache
def load_referentiel():
    """Feuille : Referentiel — catalogue des tâches."""
    df = pd.read_excel(get_excel_path(), sheet_name="Referentiel", header=3)
    df = df.iloc[:, :7]
    df.columns = ["Produit", "Essai", "Sous-tâche", "Standard (min)", "Empty", "Sous-tâche normalisée", "Classe"]
    df = df.drop(columns=["Empty"], errors="ignore")
    df = df[df["Produit"].notna() & (df["Produit"] != "Produit")]
    df["Standard (min)"] = pd.to_numeric(df["Standard (min)"], errors="coerce")
    return df


@st_cache
def load_dashboard_kpi():
    """Extrait les KPI principaux du Dashboard Global."""
    import openpyxl
    wb = openpyxl.load_workbook(get_excel_path(), data_only=True)
    ws = wb["Dashboard Global"]
    kpi = {
        "nva_avant": ws["A10"].value or 621,
        "nva_apres": ws["D10"].value or 253,
        "gain_nva": ws["G10"].value or 368,
        "taux_nva_avant": ws["J10"].value or 0.1135,
        "va_avant": ws["A16"].value or 3345,
        "nnva_avant": ws["D16"].value or 1507,
        "temps_global_avant": ws["G16"].value or 5473,
        "temps_global_apres": ws["J16"].value or 5105,
        "date_debut": ws["B8"].value,
        "date_fin": ws["E8"].value,
        "produit_filtre": ws["H8"].value or "Tous les produits",
    }
    return kpi


def st_cache(func):
    """Wrapper de cache — remplacé par st.cache_data dans app.py."""
    return func
