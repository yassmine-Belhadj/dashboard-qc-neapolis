"""
app.py — Système de pilotage de la performance et amélioration continue
Laboratoire de Contrôle Qualité Pharmaceutique — Néapolis Pharma (Laboratoires Médis)
Hana Brinis — Projet de Fin d'Études 2026 — Master Bio-santé (FST)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openpyxl
import os
import sys

# ── Import des modules internes ─────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_qc"))
from styles import CSS, COLORS, CLASS_COLORS, PLOTLY_PALETTE
from charts import (
    donut_repartition, bar_pertes_par_cause, gauge_taux_nva,
    waterfall_gain, pareto_chart, radar_chart_essais, bar_par_essai,
    scatter_nva_events, bar_avant_apres_global, heatmap_nva_produit_essai,
    boxplot_distribution_taches, line_evolution_temporelle_lots,
    bar_cumul_gains_temporels,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION PAGE (Fleur 🌸)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Système de pilotage QC — Hana Brinis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)

# Styles CSS personnalisés pour les boutons roses, les bannières et les badges
st.markdown("""
<style>
/* Navigation dans la sidebar */
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.4rem 0 !important;
}

/* ── Boutons Roses Très Visibles ── */
div.stButton > button {
    background: linear-gradient(135deg, #C0637A 0%, #D87093 50%, #C0637A 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 0.90rem !important;
    letter-spacing: 0.03em !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    padding: 0.70rem 1.2rem !important;
    box-shadow: 0 4px 18px rgba(192, 99, 122, 0.45) !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 24px rgba(216, 112, 147, 0.65) !important;
    background: linear-gradient(135deg, #D87093 0%, #C0637A 100%) !important;
}

/* ── File Uploader Rose ── */
[data-testid="stFileUploader"] {
    background: rgba(253, 232, 239, 0.15) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(253, 232, 239, 0.25) !important;
    border: 2px dashed #D87093 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #C0637A 0%, #D87093 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 12px rgba(192, 99, 122, 0.4) !important;
}

/* Badges */
.badge-realise  { background:#E8F5F0; color:#2D6A50; border:1px solid #6BAB90; padding:0.2rem 0.7rem; border-radius:50px; font-size:0.75rem; font-weight:700; }
.badge-encours  { background:#EDE0F5; color:#5A3D7A; border:1px solid #9B72AA; padding:0.2rem 0.7rem; border-radius:50px; font-size:0.75rem; font-weight:700; }
.badge-etude    { background:#FEF3E8; color:#8B5E1A; border:1px solid #E8A45A; padding:0.2rem 0.7rem; border-radius:50px; font-size:0.75rem; font-weight:700; }
.badge-haute    { background:#FDE8E8; color:#8B2020; border:1px solid #D96B6B; padding:0.2rem 0.7rem; border-radius:50px; font-size:0.75rem; font-weight:700; }
.badge-moyenne  { background:#FEF3E8; color:#8B5E1A; border:1px solid #E8A45A; padding:0.2rem 0.7rem; border-radius:50px; font-size:0.75rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GESTION DU CLASSEUR EXCEL
# ─────────────────────────────────────────────────────────────────────────────
EXCEL_DEFAULT_NAME = "Dashboard_QC_Final_Dates_Mars_Aout_Saisie_Simplifiee.xlsx"
EXCEL_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(EXCEL_DIR, EXCEL_DEFAULT_NAME)

def get_excel_path():
    xlsx_files = [f for f in os.listdir(EXCEL_DIR) if f.endswith(".xlsx") and not f.startswith("~$")]
    if xlsx_files:
        return os.path.join(EXCEL_DIR, xlsx_files[0])
    return EXCEL_PATH


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES (100% Dynamique)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=0)
def load_timesheets(path):
    df = pd.read_excel(path, sheet_name="Saisie TimeSheets", header=4)
    df = df[df.iloc[:, 0].notna() & df.iloc[:, 0].astype(str).str.startswith("QC-")]
    cols = [
        "ID activité", "Date", "Produit", "Lot", "Essai", "Sous-tâche",
        "Classe VA/NNVA", "Début", "Fin", "Durée brute (min)", "NVA inclus (min)",
        "Machine autonome", "Temps net (min)", "Périmètre R/I/A", "Code HPLC",
        "ID exécution", "Traçabilité", "Période", "Conforme", "Flag", "Filtre actif (auto)"
    ]
    df.columns = cols[:df.shape[1]]
    for col in ["Durée brute (min)", "Temps net (min)", "NVA inclus (min)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st.cache_data(ttl=0)
def load_evenements_nva(path):
    df = pd.read_excel(path, sheet_name="Evenements NVA", header=3)
    df = df[df.iloc[:, 0].notna() & df.iloc[:, 0].astype(str).str.match(r"(NVA|EX)-\d+")]
    cols = ["ID", "Date", "Produit", "Lot", "Essai", "Catégorie NVA",
            "Période", "Durée (min)", "Inclure ?", "Phase du mémoire",
            "Code HPLC", "Col12", "Filtre actif"]
    df.columns = cols[:df.shape[1]]
    df["Durée (min)"] = pd.to_numeric(df["Durée (min)"], errors="coerce")
    df = df[df["Inclure ?"].astype(str).str.strip() == "Oui"]
    return df


@st.cache_data(ttl=0)
def load_referentiel(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Referentiel"]
    rows = []
    for r in range(6, ws.max_row + 1):
        prod = ws.cell(r, 1).value
        essai = ws.cell(r, 2).value
        stache = ws.cell(r, 3).value
        std = ws.cell(r, 4).value
        if prod and essai and stache:
            rows.append({
                "Produit": str(prod).strip(),
                "Essai": str(essai).strip(),
                "Sous-tâche": str(stache).strip(),
                "Standard (min)": float(std) if std is not None else 0.0
            })
    df = pd.DataFrame(rows)
    va_keywords = [
        "Préparation de la phase mobile",
        "Préparation des solutions",
        "Temps d'analyse / injection",
        "Traitement des résultats"
    ]
    df["Classe"] = df["Sous-tâche"].apply(
        lambda x: "VA" if any(k in str(x) for k in va_keywords) else "NNVA"
    )
    return df


@st.cache_data(ttl=0)
def load_actions(path):
    df = pd.read_excel(path, sheet_name="Suivi Actions", header=4)
    cols = ["ID", "Cause / axe d'amélioration", "Action d'amélioration",
            "État d'avancement", "Priorité", "Responsable", "Échéance",
            "Observations / indicateur de suivi"]
    df = df.iloc[:, :len(cols)]
    df.columns = cols
    df = df[df["ID"].notna() & df["ID"].astype(str).str.startswith("P-")]
    return df


@st.cache_data(ttl=0)
def load_analyse_pertes(path):
    df = pd.read_excel(path, sheet_name="Analyse Pertes", header=4)
    df = df.iloc[:, :8]
    df.columns = ["Source de perte NVA", "AVANT (min)", "APRÈS (min)", "Gain (min)",
                  "Réduction (%)", "Occ. AVANT", "Occ. APRÈS", "Cumul AVANT (%)"]
    df = df[df["Source de perte NVA"].notna()]
    df = df[~df["Source de perte NVA"].astype(str).str.startswith(("TOTAL", "Source"))]
    for col in ["AVANT (min)", "APRÈS (min)", "Gain (min)", "Réduction (%)", "Occ. AVANT", "Occ. APRÈS"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["AVANT (min)"])


@st.cache_data(ttl=0)
def load_comparaison(path):
    df = pd.read_excel(path, sheet_name="Comparaison Globale", header=4)
    df = df.iloc[:, :4]
    df.columns = ["Indicateur", "AVANT", "APRÈS", "Variation"]
    df = df[df["Indicateur"].notna()]
    df = df[~df["Indicateur"].astype(str).str.strip().isin(["", "Indicateur"])]
    df = df[~df["Indicateur"].astype(str).str.startswith(
        ("PÉRIMÈTRE", "VA et", "Les val", "CONTRÔLE", "Événements", "Durée", "État")
    )]
    for col in ["AVANT", "APRÈS", "Variation"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["AVANT"])


@st.cache_data(ttl=0)
def calculate_dynamic_kpi(df_nva, df_ts):
    """Calcul 100% dynamique et automatique des KPI."""
    nva_avant = float(df_nva[df_nva["Période"] == "AVANT"]["Durée (min)"].sum())
    nva_apres = float(df_nva[df_nva["Période"] == "APRÈS"]["Durée (min)"].sum())
    gain_nva  = nva_avant - nva_apres

    va_avant   = float(df_ts[df_ts["Classe VA/NNVA"] == "VA"]["Temps net (min)"].sum())
    nnva_avant = float(df_ts[df_ts["Classe VA/NNVA"] == "NNVA"]["Temps net (min)"].sum())

    temps_global_avant = va_avant + nnva_avant + nva_avant
    temps_global_apres = va_avant + nnva_avant + nva_apres

    taux_nva_avant = nva_avant / temps_global_avant if temps_global_avant > 0 else 0.0
    taux_nva_apres = nva_apres / temps_global_apres if temps_global_apres > 0 else 0.0

    return {
        "nva_avant": nva_avant,
        "nva_apres": nva_apres,
        "gain_nva": gain_nva,
        "va_avant": va_avant,
        "nnva_avant": nnva_avant,
        "temps_global_avant": temps_global_avant,
        "temps_global_apres": temps_global_apres,
        "taux_nva_avant": taux_nva_avant,
        "taux_nva_apres": taux_nva_apres,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES OBJETS
# ─────────────────────────────────────────────────────────────────────────────
excel_path = get_excel_path()

try:
    df_ts      = load_timesheets(excel_path)
    df_nva     = load_evenements_nva(excel_path)
    df_pertes  = load_analyse_pertes(excel_path)
    df_comp    = load_comparaison(excel_path)
    df_actions = load_actions(excel_path)
    df_ref     = load_referentiel(excel_path)
    kpi        = calculate_dynamic_kpi(df_nva, df_ts)
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.2rem 0 0.8rem;'>
        <div style='font-size:2.2rem; line-height:1; margin-bottom:0.4rem;'>🌸</div>
        <div style='font-size:1.4rem; color:#E8A0B4; font-weight:800; 
                    letter-spacing:0.08em; font-family: serif;'>QC</div>
        <div style='width:36px; height:2px; background:linear-gradient(90deg,#C0637A,#9B72AA); 
                    margin:0.4rem auto;'></div>
        <div style='font-size:0.80rem; color:#FDE8EF; font-weight:700; 
                    letter-spacing:0.04em; margin-top:0.3rem;'>
            PILOTAGE DE LA PERFORMANCE
        </div>
        <div style='font-size:0.70rem; color:#9B72AA; margin-top:0.2rem;'>
            Projet de Fin d'Études — 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style='border-top:1px solid rgba(232,160,180,0.2); margin:0.4rem 0 0.6rem;'></div>""",
                unsafe_allow_html=True)

    # 9 pages ciblées et 100% pertinentes
    page = st.radio(
        "Navigation",
        options=[
            "Vue d'ensemble & Indicateurs",
            "Évolution Temporelle des Gains",
            "Journal des Activités",
            "Événements NVA",
            "Analyse des Pertes",
            "Comparaison AVANT / APRÈS",
            "Plan d'Actions",
            "Référentiel des Tâches",
            "Démarche Lean & DMAIC",
        ],
        label_visibility="collapsed",
    )

    st.markdown("""<div style='border-top:1px solid rgba(232,160,180,0.2); margin:0.8rem 0 0.6rem;'></div>""",
                unsafe_allow_html=True)

    st.markdown("""<div style='color:#E8A0B4; font-size:0.72rem; font-weight:700; 
                    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.4rem;'>
                    Mise à jour des données</div>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Importer un nouveau classeur Excel",
        type=["xlsx"],
        help="Glissez-déposez le nouveau fichier Excel. Tous les KPI, graphiques et tableaux se recalculent automatiquement.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        save_path = os.path.join(EXCEL_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.cache_data.clear()
        st.success("Données actualisées avec succès !")
        st.rerun()

    if st.button("Recharger les données actuelles", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    xlsx_files = [f for f in os.listdir(EXCEL_DIR) if f.endswith(".xlsx") and not f.startswith("~$")]
    if xlsx_files:
        st.markdown(f"""
        <div style='font-size:0.70rem; color:#6B4D7A; margin-top:0.4rem; 
                    background:rgba(0,0,0,0.15); border-radius:8px; padding:0.45rem 0.6rem;'>
            Source active :<br>
            <span style='color:#E8A0B4; font-weight:600;'>{xlsx_files[0][:32]}...</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""<div style='border-top:1px solid rgba(232,160,180,0.2); margin:0.8rem 0 0.6rem;'></div>""",
                unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; color:#6B4D7A; font-size:0.70rem; padding:0 0.3rem;'>
        Période d'évaluation<br>
        <span style='color:#E8A0B4; font-weight:700;'>Mars — Août 2026</span><br><br>
        <span style='color:#9B72AA;'>Néapolis Pharma (Médis)</span><br><br>
        <span style='color:#4A2D5A; font-weight:700;'>Hana Brinis</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# COMPOSANTS DE PRÉSENTATION
# ─────────────────────────────────────────────────────────────────────────────
def section_title(text):
    st.markdown(f"""
    <div style='margin:2rem 0 1rem; padding-bottom:0.45rem;
                border-bottom:2px solid; 
                border-image:linear-gradient(90deg,#C0637A,#9B72AA,transparent) 1;
                font-size:1.15rem; font-weight:700; color:#2D1B33; 
                font-family: serif; letter-spacing:0.02em;'>
        {text}
    </div>
    """, unsafe_allow_html=True)


def page_header(title, subtitle=""):
    st.markdown(f"""
    <div style='padding:0.3rem 0 0.6rem;'>
        <div style='font-family: Playfair Display, serif; font-size:2rem; font-weight:700;
                    background:linear-gradient(135deg,#C0637A,#9B72AA);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; line-height:1.2; margin-bottom:0.3rem;'>
            {title}
        </div>
        <div style='color:#9B72AA; font-size:0.92rem; font-weight:500; letter-spacing:0.02em;'>
            {subtitle}
        </div>
    </div>
    <hr style='border:none; height:1px; background:linear-gradient(90deg,transparent,#E8A0B4,transparent); margin:0.4rem 0 1.3rem;'>
    """, unsafe_allow_html=True)


def info_box(text):
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#FDE8EF,#EDE0F5); border-left:4px solid #C0637A;
                border-radius:0 12px 12px 0; padding:0.9rem 1.1rem; margin:1rem 0;
                font-size:0.88rem; color:#4A2D5A; line-height:1.6;'>
        {text}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 : VUE D'ENSEMBLE & INDICATEURS
# ─────────────────────────────────────────────────────────────────────────────
if page == "Vue d'ensemble & Indicateurs":

    page_header(
        "🌸 Système de pilotage de la performance et amélioration continue",
        "Laboratoire de Contrôle Qualité Pharmaceutique — Néapolis Pharma (Laboratoires Médis) · Mars – Août 2026"
    )

    reduction_pct = round((kpi['nva_avant'] - kpi['nva_apres']) / kpi['nva_avant'] * 100, 1) if kpi['nva_avant'] > 0 else 0
    gain_heures = round(kpi['gain_nva'] / 60, 1)

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(192,99,122,0.12) 0%, rgba(155,114,170,0.14) 100%);
                border: 1px solid rgba(192,99,122,0.30); border-radius: 16px; padding: 1.1rem 1.5rem;
                margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;'>
        <div>
            <div style='font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: #9B72AA; font-weight: 800;'>
                BILAN STRATÉGIQUE DE L'AMÉLIORATION CONTINUE
            </div>
            <div style='font-size: 1.25rem; font-weight: 800; color: #2D1B33; font-family: serif; margin-top: 0.2rem;'>
                Gain net : <span style='color: #6BAB90;'>+{int(kpi['gain_nva'])} minutes</span> ({gain_heures} h restituées) &nbsp;·&nbsp; Pertes NVA : <span style='color: #C0637A;'>-{reduction_pct} %</span>
            </div>
        </div>
        <div style='text-align: right;'>
            <span style='background: #E8F5F0; color: #2D6A50; font-weight: 800; font-size: 0.85rem; padding: 0.4rem 0.9rem; border-radius: 50px; border: 1px solid #6BAB90;'>
                Taux de perte divisé par 2 (11,35 % → 4,96 %)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_title("Indicateurs Clés de Performance (Calcul Dynamique)")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div style='background: white; border-radius: 18px; padding: 1.4rem 1.1rem; text-align: center;
                    box-shadow: 0 4px 20px rgba(217, 107, 107, 0.12); border: 1px solid rgba(217, 107, 107, 0.25);
                    border-top: 4px solid #D96B6B; height: 100%;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;'>
                Pertes NVA — AVANT
            </div>
            <div style='font-size: 2.3rem; font-weight: 900; color: #D96B6B; line-height: 1.1; margin: 0.4rem 0;'>
                {int(kpi['nva_avant'])} <span style='font-size: 1.1rem; font-weight: 700;'>min</span>
            </div>
            <div style='display: inline-block; background: #FDE8E8; color: #8B2020; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px;'>
                Phase Mesurer · 11,35 %
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style='background: white; border-radius: 18px; padding: 1.4rem 1.1rem; text-align: center;
                    box-shadow: 0 4px 20px rgba(107, 171, 144, 0.12); border: 1px solid rgba(107, 171, 144, 0.25);
                    border-top: 4px solid #6BAB90; height: 100%;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;'>
                Pertes NVA — APRÈS
            </div>
            <div style='font-size: 2.3rem; font-weight: 900; color: #6BAB90; line-height: 1.1; margin: 0.4rem 0;'>
                {int(kpi['nva_apres'])} <span style='font-size: 1.1rem; font-weight: 700;'>min</span>
            </div>
            <div style='display: inline-block; background: #E8F5F0; color: #2D6A50; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px;'>
                Phase Contrôler · 4,96 %
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style='background: white; border-radius: 18px; padding: 1.4rem 1.1rem; text-align: center;
                    box-shadow: 0 4px 20px rgba(192, 99, 122, 0.14); border: 1px solid rgba(192, 99, 122, 0.25);
                    border-top: 4px solid #C0637A; height: 100%;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;'>
                Temps Net Récupéré
            </div>
            <div style='font-size: 2.3rem; font-weight: 900; color: #C0637A; line-height: 1.1; margin: 0.4rem 0;'>
                +{int(kpi['gain_nva'])} <span style='font-size: 1.1rem; font-weight: 700;'>min</span>
            </div>
            <div style='display: inline-block; background: #FDE8EF; color: #8B2020; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px;'>
                ≈ {gain_heures} heures utiles
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div style='background: white; border-radius: 18px; padding: 1.4rem 1.1rem; text-align: center;
                    box-shadow: 0 4px 20px rgba(107, 171, 144, 0.14); border: 1px solid rgba(107, 171, 144, 0.25);
                    border-top: 4px solid #6BAB90; height: 100%;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;'>
                Taux de Réduction NVA
            </div>
            <div style='font-size: 2.3rem; font-weight: 900; color: #6BAB90; line-height: 1.1; margin: 0.4rem 0;'>
                -{reduction_pct} <span style='font-size: 1.1rem; font-weight: 700;'>%</span>
            </div>
            <div style='display: inline-block; background: #E8F5F0; color: #2D6A50; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px;'>
                Pertes réduites de plus de moitié
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    ratio_avant = round(kpi['va_avant'] / kpi['nva_avant'], 1) if kpi['nva_avant'] > 0 else 0
    ratio_apres = round(kpi['va_avant'] / kpi['nva_apres'], 1) if kpi['nva_apres'] > 0 else 0

    with c1:
        st.markdown(f"""
        <div style='background: white; border-radius: 16px; padding: 1.2rem 1rem; text-align: center;
                    border: 1px solid rgba(107, 171, 144, 0.25); border-left: 4px solid #6BAB90;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 700; text-transform: uppercase;'>
                Temps à Valeur Ajoutée (VA)
            </div>
            <div style='font-size: 1.9rem; font-weight: 800; color: #6BAB90; margin: 0.3rem 0;'>
                {int(kpi['va_avant'])} min
            </div>
            <div style='font-size: 0.80rem; color: #4A2D5A;'>
                <b>61,1 %</b> du temps opérateur total (Cœur de métier)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style='background: white; border-radius: 16px; padding: 1.2rem 1rem; text-align: center;
                    border: 1px solid rgba(232, 164, 90, 0.25); border-left: 4px solid #E8A45A;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 700; text-transform: uppercase;'>
                Temps Nécessaire Sans VA (NNVA)
            </div>
            <div style='font-size: 1.9rem; font-weight: 800; color: #E8A45A; margin: 0.3rem 0;'>
                {int(kpi['nnva_avant'])} min
            </div>
            <div style='font-size: 0.80rem; color: #4A2D5A;'>
                <b>27,5 %</b> du temps total (Traçabilité & BPF)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style='background: white; border-radius: 16px; padding: 1.2rem 1rem; text-align: center;
                    border: 1px solid rgba(192, 99, 122, 0.25); border-left: 4px solid #C0637A;'>
            <div style='font-size: 0.74rem; color: #9B72AA; font-weight: 700; text-transform: uppercase;'>
                Ratio d'Efficience (VA / NVA)
            </div>
            <div style='font-size: 1.9rem; font-weight: 800; color: #C0637A; margin: 0.3rem 0;'>
                {ratio_avant} → {ratio_apres}
            </div>
            <div style='font-size: 0.80rem; color: #4A2D5A;'>
                La valeur ajoutée est désormais <b>{ratio_apres}×</b> supérieure aux pertes
            </div>
        </div>
        """, unsafe_allow_html=True)

    section_title("Répartition du Temps Opérateur — Comparaison AVANT / APRÈS")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        fig1 = donut_repartition(kpi["va_avant"], kpi["nnva_avant"], kpi["nva_avant"], "Phase Mesurer (AVANT)")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = donut_repartition(kpi["va_avant"], kpi["nnva_avant"], kpi["nva_apres"], "Phase Contrôler (APRÈS)")
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 = bar_avant_apres_global(kpi)
        st.plotly_chart(fig3, use_container_width=True)

    section_title("Évolution du Taux de Non-Valeur Ajoutée")
    col1, col2 = st.columns(2)
    with col1:
        fig_g1 = gauge_taux_nva(kpi["taux_nva_avant"], "Taux NVA — Phase Mesurer (AVANT)")
        st.plotly_chart(fig_g1, use_container_width=True)
    with col2:
        fig_g2 = gauge_taux_nva(kpi["taux_nva_apres"], "Taux NVA — Phase Contrôler (APRÈS)")
        st.plotly_chart(fig_g2, use_container_width=True)

    info_box(
        "<b>Synthèse méthodologique (PFE Hana Brinis) :</b> Le taux NVA reflète la proportion du temps opérateur consacrée à des "
        "tâches sans valeur ajoutée pour le produit (attentes d'eau ou de chaînes HPLC, reprises, recherches de solvants). "
        "Les six actions d'amélioration ont permis de réduire ce taux de <b>11,35 % à 4,96 %</b>, "
        "libérant <b>368 minutes</b> d'activité analytique utile (gain net de 59,3 % sur les pertes)."
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 : ÉVOLUTION TEMPORELLE DES GAINS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Évolution Temporelle des Gains":

    page_header(
        "Évolution Temporelle des Pertes & Trajectoire des Gains",
        "Suivi chronologique des temps perdus à travers les séries de lots analytiques (Mars → Août 2026)"
    )

    section_title("Trajectoire de réduction du temps perdu par lot")

    col1, col2 = st.columns(2)
    with col1:
        fig_evo = line_evolution_temporelle_lots(df_nva)
        st.plotly_chart(fig_evo, use_container_width=True)
    with col2:
        fig_cumul = bar_cumul_gains_temporels(df_nva)
        st.plotly_chart(fig_cumul, use_container_width=True)

    info_box(
        "<b>Analyse de la trajectoire :</b> La courbe chronologique par lot démontre une diminution continue "
        "des temps perdus (de 191 min à 103 min pour le Lot 1, et jusqu'à 18 min pour le Lot 3). "
        "L'effet cumulé atteint <b>368 minutes récupérées</b> sur l'ensemble de la campagne, attestant de l'efficacité "
        "et de la pérennisation des actions correctives mises en œuvre en Phase Contrôler."
    )

    section_title("Bilan comparatif par lot analytique et par produit")

    df_lot_prod = df_nva.groupby(["Produit", "Lot", "Période"])["Durée (min)"].sum().unstack(fill_value=0).reset_index()
    df_lot_prod["Gain (min)"] = df_lot_prod["AVANT"] - df_lot_prod["APRÈS"]
    df_lot_prod["Réduction (%)"] = (df_lot_prod["Gain (min)"] / df_lot_prod["AVANT"] * 100).round(1).astype(str) + " %"

    st.dataframe(
        df_lot_prod.style.format({"AVANT": "{:.0f} min", "APRÈS": "{:.0f} min", "Gain (min)": "+{:.0f} min"}),
        use_container_width=True, hide_index=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 : JOURNAL DES ACTIVITÉS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Journal des Activités":

    page_header(
        "Journal des Activités — Time Sheets",
        "248 activités enregistrées · Phase Mesurer (AVANT) · Classification VA / NNVA"
    )

    with st.expander("Filtres de sélection", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            produits = ["Tous"] + sorted(df_ts["Produit"].dropna().unique().tolist())
            produit_sel = st.selectbox("Produit", produits, key="ts_prod")

        df_sub = df_ts if produit_sel == "Tous" else df_ts[df_ts["Produit"] == produit_sel]

        with col2:
            lots = ["Tous"] + sorted(df_sub["Lot"].dropna().unique().tolist())
            lot_sel = st.selectbox("Lot", lots, key="ts_lot")

        if lot_sel != "Tous":
            df_sub = df_sub[df_sub["Lot"] == lot_sel]

        with col3:
            essais = ["Tous"] + sorted(df_sub["Essai"].dropna().unique().tolist())
            essai_sel = st.selectbox("Essai", essais, key="ts_essai")

        with col4:
            classes = ["Toutes"] + sorted(df_ts["Classe VA/NNVA"].dropna().unique().tolist())
            classe_sel = st.selectbox("Classe VA/NNVA", classes, key="ts_classe")

    df_f = df_ts.copy()
    if produit_sel != "Tous":    df_f = df_f[df_f["Produit"] == produit_sel]
    if lot_sel != "Tous":        df_f = df_f[df_f["Lot"] == lot_sel]
    if essai_sel != "Tous":      df_f = df_f[df_f["Essai"] == essai_sel]
    if classe_sel != "Toutes":   df_f = df_f[df_f["Classe VA/NNVA"] == classe_sel]

    section_title("Synthèse de la sélection")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Activités recensées", len(df_f))
    with c2: st.metric("Durée cumulée", f"{int(df_f['Durée brute (min)'].sum())} min")
    with c3: st.metric("Activités VA", len(df_f[df_f["Classe VA/NNVA"] == "VA"]))
    with c4: st.metric("Activités NNVA", len(df_f[df_f["Classe VA/NNVA"] == "NNVA"]))

    section_title("Analyse de la répartition et de la dispersion")
    col1, col2 = st.columns(2)
    with col1:
        df_grp = df_f.groupby("Classe VA/NNVA")["Durée brute (min)"].sum().reset_index()
        fig = px.pie(df_grp, names="Classe VA/NNVA", values="Durée brute (min)",
                     color="Classe VA/NNVA",
                     color_discrete_map={"VA": CLASS_COLORS["VA"], "NNVA": CLASS_COLORS["NNVA"]},
                     hole=0.55, title="Part de durée : VA vs NNVA")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300,
                          font=dict(family="Nunito"), margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df_grp2 = df_f.groupby(["Produit", "Essai"])["Durée brute (min)"].sum().reset_index()
        fig2 = px.bar(df_grp2, x="Essai", y="Durée brute (min)", color="Produit",
                      barmode="group",
                      color_discrete_sequence=[COLORS["primary"], COLORS["secondary"]],
                      title="Volume horaire par type d'essai",
                      text_auto=True)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(255,255,255,0.5)",
                           height=300, font=dict(family="Nunito"),
                           margin=dict(t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    section_title("Distribution des durées unitaires par tâche")
    fig_box = boxplot_distribution_taches(df_f)
    st.plotly_chart(fig_box, use_container_width=True)

    section_title("Tableau détaillé des activités")
    cols_display = ["ID activité", "Produit", "Lot", "Essai", "Sous-tâche",
                    "Classe VA/NNVA", "Durée brute (min)", "Temps net (min)", "Périmètre R/I/A"]

    def color_classe(val):
        if val == "VA":
            return f"background-color: {CLASS_COLORS['VA']}22; color:#2D6A50; font-weight:600;"
        elif val == "NNVA":
            return f"background-color: {CLASS_COLORS['NNVA']}22; color:#8B5E1A; font-weight:600;"
        return ""

    styled = df_f[cols_display].style.applymap(color_classe, subset=["Classe VA/NNVA"]) \
                               .format({"Durée brute (min)": "{:.0f}", "Temps net (min)": "{:.0f}"})
    st.dataframe(styled, use_container_width=True, height=400)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 : ÉVÉNEMENTS NVA
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Événements NVA":

    page_header(
        "Événements de Non-Valeur Ajoutée",
        "44 événements répertoriés · 22 en Phase Mesurer (AVANT) · 22 en Phase Contrôler (APRÈS)"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        periode_sel = st.selectbox("Période", ["Toutes", "AVANT", "APRÈS"], key="nva_per")
    with col2:
        cats = ["Toutes"] + sorted(df_nva["Catégorie NVA"].dropna().unique().tolist())
        cat_sel = st.selectbox("Catégorie NVA", cats, key="nva_cat")
    with col3:
        produits_nva = ["Tous"] + sorted(df_nva["Produit"].dropna().unique().tolist())
        prod_nva = st.selectbox("Produit", produits_nva, key="nva_prod")

    df_nva_f = df_nva.copy()
    if periode_sel != "Toutes": df_nva_f = df_nva_f[df_nva_f["Période"] == periode_sel]
    if cat_sel != "Toutes":     df_nva_f = df_nva_f[df_nva_f["Catégorie NVA"] == cat_sel]
    if prod_nva != "Tous":      df_nva_f = df_nva_f[df_nva_f["Produit"] == prod_nva]

    section_title("Synthèse de la sélection")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Événements", len(df_nva_f))
    with c2: st.metric("Durée totale", f"{int(df_nva_f['Durée (min)'].sum())} min")
    with c3: st.metric("Catégories distinctes", df_nva_f["Catégorie NVA"].nunique())

    section_title("Visualisations analytiques")
    col1, col2 = st.columns(2)
    with col1:
        fig_sc = scatter_nva_events(df_nva_f)
        st.plotly_chart(fig_sc, use_container_width=True)
    with col2:
        fig_hm = heatmap_nva_produit_essai(df_nva if periode_sel == "Toutes" else df_nva_f)
        st.plotly_chart(fig_hm, use_container_width=True)

    section_title("Comparaison AVANT / APRÈS par catégorie de perte")
    df_comp_nva = df_nva.groupby(["Catégorie NVA", "Période"])["Durée (min)"].sum().reset_index()
    fig_comp = px.bar(df_comp_nva, x="Catégorie NVA", y="Durée (min)", color="Période",
                      barmode="group",
                      color_discrete_map={"AVANT": COLORS["danger"], "APRÈS": COLORS["success"]},
                      text_auto=True)
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.5)",
        height=380, font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.08),
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        margin=dict(l=20, r=20, t=30, b=80),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    section_title("Détail des événements NVA")
    cols_nva = ["ID", "Produit", "Lot", "Essai", "Catégorie NVA", "Période", "Durée (min)", "Phase du mémoire"]

    def color_periode_cell(val):
        if val == "AVANT":
            return "background-color:#FDE8EF; color:#8B2020; font-weight:600;"
        elif val == "APRÈS":
            return "background-color:#E8F5F0; color:#2D6A50; font-weight:600;"
        return ""

    styled_nva = df_nva_f[cols_nva].style.applymap(color_periode_cell, subset=["Période"])
    st.dataframe(styled_nva, use_container_width=True, height=400)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 : ANALYSE DES PERTES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Analyse des Pertes":

    page_header(
        "Analyse des Pertes — Comparaison AVANT / APRÈS",
        "Diagramme de Pareto (80/20) · Décomposition en cascade (Waterfall) · Profil radar"
    )

    total_avant = int(df_pertes["AVANT (min)"].sum())
    total_apres = int(df_pertes["APRÈS (min)"].sum())
    total_gain  = int(df_pertes["Gain (min)"].sum())
    idx_max     = df_pertes["Gain (min)"].idxmax()
    cat_max     = df_pertes.loc[idx_max, "Source de perte NVA"]
    gain_max    = int(df_pertes.loc[idx_max, "Gain (min)"])

    section_title("Synthèse globale")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("NVA AVANT", f"{total_avant} min")
    with c2: st.metric("NVA APRÈS", f"{total_apres} min", delta=f"-{total_gain} min")
    with c3: st.metric("Gain Net Total", f"+{total_gain} min",
                       delta=f"{round(total_gain/total_avant*100,1)} % réduit")
    with c4: st.metric("Gain principal", f"+{gain_max} min", delta=cat_max[:28])

    section_title("Analyses descriptives et graphiques décisionnels")
    tab1, tab2, tab3, tab4 = st.tabs([
        "Courbe de Pareto (Loi 80/20)",
        "Comparaison AVANT / APRÈS par cause",
        "Décomposition du gain (Waterfall)",
        "Tableau complet"
    ])

    with tab1:
        fig_pareto = pareto_chart(df_pertes)
        st.plotly_chart(fig_pareto, use_container_width=True)
        info_box(
            "<b>Interprétation Lean (Loi de Pareto 80/20) :</b> Les deux premières causes de pertes "
            "(Indisponibilité de l'eau et Événements chromatographiques) concentraient à elles seules "
            "près de <b>60 % des pertes initiales</b>. Le ciblage prioritaire de ces axes par les actions "
            "P-01 et P-02 a permis d'optimiser l'efficacité des investissements."
        )

    with tab2:
        fig_bar = bar_pertes_par_cause(df_pertes)
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        fig_wf = waterfall_gain(df_pertes)
        st.plotly_chart(fig_wf, use_container_width=True)

    with tab4:
        df_disp = df_pertes.copy()
        df_disp["Réduction (%)"] = df_disp["Réduction (%)"].apply(
            lambda x: f"{round(x*100, 1)} %" if pd.notna(x) and x <= 1 else f"{round(x, 1)} %"
        )
        def color_gain_cell(val):
            try:
                v = float(str(val).replace(" %", "").replace("+", ""))
                if v > 0: return "color:#2D6A50; font-weight:700;"
                if v == 0: return "color:#8B5E1A;"
            except: pass
            return ""

        styled_p = df_disp.style.applymap(color_gain_cell, subset=["Gain (min)"])
        st.dataframe(styled_p, use_container_width=True, height=320)

    section_title("Profil comparatif par type d'essai")
    df_essai = df_nva.groupby(["Essai", "Période"])["Durée (min)"].sum().reset_index()
    df_ep = df_essai.pivot(index="Essai", columns="Période", values="Durée (min)").fillna(0).reset_index()
    df_ep.columns.name = None
    if "AVANT" not in df_ep.columns: df_ep["AVANT"] = 0
    if "APRÈS" not in df_ep.columns: df_ep["APRÈS"] = 0

    col1, col2 = st.columns(2)
    with col1:
        fig_radar = radar_chart_essais(df_ep)
        st.plotly_chart(fig_radar, use_container_width=True)
    with col2:
        fig_essai = bar_par_essai(df_ep)
        st.plotly_chart(fig_essai, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 : COMPARAISON GLOBALE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Comparaison AVANT / APRÈS":

    page_header(
        "Comparaison Globale des Indicateurs",
        "Évaluation à périmètre analytique constant — Intégrité rigoureuse des bases VA et NNVA"
    )

    fig_stack = bar_avant_apres_global(kpi)
    st.plotly_chart(fig_stack, use_container_width=True)

    section_title("Tableau de bord de synthèse")
    col1, col2 = st.columns([1.2, 1])

    with col1:
        rows = []
        for _, row in df_comp.iterrows():
            indic = str(row["Indicateur"])
            avant_v = row["AVANT"]
            apres_v = row["APRÈS"]
            var_v   = row["Variation"]
            if "%" in indic or abs(avant_v) < 1:
                avant_str = f"{avant_v*100:.2f} %"
                apres_str = f"{apres_v*100:.2f} %"
                var_str   = f"{var_v*100:.2f} pts"
            else:
                avant_str = f"{int(avant_v)} min"
                apres_str = f"{int(apres_v)} min"
                var_str   = f"{int(var_v)} min"
            arrow = "▼" if var_v < 0 else ("=" if var_v == 0 else "▲")
            rows.append({
                "Indicateur": indic,
                "AVANT": avant_str,
                "APRÈS": apres_str,
                "Variation": f"{arrow}  {var_str}"
            })
        df_table = pd.DataFrame(rows)

        def color_var(val):
            if "▼" in str(val): return "color:#2D6A50; font-weight:700;"
            if "=" in str(val):  return "color:#8B5E1A;"
            return "color:#8B2020;"

        st.dataframe(
            df_table.style.applymap(color_var, subset=["Variation"]),
            use_container_width=True, hide_index=True, height=240
        )

    with col2:
        fig_g1 = gauge_taux_nva(kpi["taux_nva_avant"], "Taux NVA — AVANT")
        st.plotly_chart(fig_g1, use_container_width=True)
        fig_g2 = gauge_taux_nva(kpi["taux_nva_apres"], "Taux NVA — APRÈS")
        st.plotly_chart(fig_g2, use_container_width=True)

    info_box(
        "<b>Périmètre analytique :</b> Les activités à Valeur Ajoutée (3 345 min) et Nécessaires (1 507 min) "
        "demeurent strictement constantes afin d'assurer la comparabilité scientifique des deux phases. "
        "L'unique levier mesuré est la résorption des dysfonctionnements opérationnels (NVA)."
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 : PLAN D'ACTIONS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Plan d'Actions":

    page_header(
        "Plan d'Actions — Phase Contrôler",
        "Suivi des six actions d'amélioration continue et pérennisation des gains"
    )

    section_title("Avancement global")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Actions au total", len(df_actions))
    with c2:
        r = len(df_actions[df_actions["État d'avancement"].str.contains("Réalisée|Conception", na=False)])
        st.metric("Réalisées / Conception", r)
    with c3:
        ec = len(df_actions[df_actions["État d'avancement"].str.contains("En cours", na=False)])
        st.metric("En cours", ec)
    with c4:
        h = len(df_actions[df_actions["Priorité"].str.contains("Haute", na=False)])
        st.metric("Priorité haute", h)

    col1, col2 = st.columns([1, 1])
    with col1:
        df_etat = df_actions["État d'avancement"].value_counts().reset_index()
        df_etat.columns = ["État", "Nombre"]
        fig_etat = px.pie(df_etat, names="État", values="Nombre",
                          color_discrete_sequence=[COLORS["success"], COLORS["secondary"],
                                                   COLORS["warning"], COLORS["accent"]],
                          hole=0.5, title="État d'avancement des actions")
        fig_etat.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280,
                               font=dict(family="Nunito"), margin=dict(t=50, b=20))
        st.plotly_chart(fig_etat, use_container_width=True)
    with col2:
        df_prio = df_actions["Priorité"].dropna().value_counts().reset_index()
        df_prio.columns = ["Priorité", "Nombre"]
        fig_prio = px.bar(df_prio, x="Priorité", y="Nombre",
                          color="Priorité",
                          color_discrete_map={"Haute": COLORS["danger"],
                                              "Moyenne": COLORS["warning"],
                                              "Basse": COLORS["success"]},
                          title="Répartition par niveau de priorité",
                          text_auto=True)
        fig_prio.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(255,255,255,0.5)",
                               height=280, font=dict(family="Nunito"),
                               showlegend=False, margin=dict(t=50, b=20))
        st.plotly_chart(fig_prio, use_container_width=True)

    section_title("Détail des six actions d'amélioration")

    etat_badge = {
        "Réalisée":            ("badge-realise",  "Réalisée"),
        "En cours":            ("badge-encours",  "En cours"),
        "À l'étude":           ("badge-etude",    "À l'étude"),
        "Conception réalisée": ("badge-encours",  "Conception réalisée"),
    }
    priorite_badge = {
        "Haute":   ("badge-haute",   "Priorité haute"),
        "Moyenne": ("badge-moyenne", "Priorité moyenne"),
    }

    for _, row in df_actions.iterrows():
        etat_raw = str(row.get("État d'avancement", "")).strip()
        prio_raw = str(row.get("Priorité", "")).strip()
        b_etat_cls, b_etat_txt = etat_badge.get(etat_raw, ("badge-encours", etat_raw))
        b_prio_cls, b_prio_txt = priorite_badge.get(prio_raw, ("badge-moyenne", prio_raw))

        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:1.2rem 1.4rem; margin-bottom:1rem;
                    box-shadow:0 2px 14px rgba(192,99,122,0.09); 
                    border-left:4px solid #C0637A;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;'>
                <div style='font-size:1.05rem; font-weight:800; color:#C0637A; 
                            font-family:serif; letter-spacing:0.03em;'>
                    Action {row["ID"]}
                </div>
                <div>
                    <span class='{b_etat_cls}'>{b_etat_txt}</span>
                    &nbsp;&nbsp;
                    <span class='{b_prio_cls}'>{b_prio_txt}</span>
                </div>
            </div>
            <div style='font-weight:700; color:#2D1B33; margin-bottom:0.4rem; font-size:0.95rem;'>
                {row["Action d'amélioration"]}
            </div>
            <div style='color:#6B4D7A; font-size:0.85rem; margin-bottom:0.3rem;'>
                <span style='font-weight:600;'>Cause identifiée :</span> 
                {row["Cause / axe d'amélioration"]}
            </div>
            <div style='color:#9B72AA; font-size:0.82rem; font-style:italic;'>
                Indicateur de suivi : {row["Observations / indicateur de suivi"]}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 8 : RÉFÉRENTIEL DES TÂCHES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Référentiel des Tâches":

    page_header(
        "Référentiel des Tâches & Classification",
        "Standards de durée par opération · Classification VA / NNVA selon le référentiel initial"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        produits_ref = ["Tous"] + sorted(df_ref["Produit"].dropna().unique().tolist())
        prod_ref = st.selectbox("Produit", produits_ref, key="ref_prod")

    df_ref_sub = df_ref if prod_ref == "Tous" else df_ref[df_ref["Produit"] == prod_ref]

    with col2:
        essais_ref = ["Tous"] + sorted(df_ref_sub["Essai"].dropna().unique().tolist())
        essai_ref = st.selectbox("Essai", essais_ref, key="ref_essai")

    if essai_ref != "Tous":
        df_ref_sub = df_ref_sub[df_ref_sub["Essai"] == essai_ref]

    with col3:
        classes_ref = ["Toutes"] + sorted(df_ref_sub["Classe"].dropna().unique().tolist())
        classe_ref = st.selectbox("Classe", classes_ref, key="ref_classe")

    df_ref_f = df_ref_sub.copy()
    if classe_ref != "Toutes":
        df_ref_f = df_ref_f[df_ref_f["Classe"] == classe_ref]

    section_title("Synthèse de la sélection")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Tâches référencées", len(df_ref_f))
    with c2: st.metric("Durée standard cumulée", f"{int(df_ref_f['Standard (min)'].sum())} min")
    with c3:
        va_n = len(df_ref_f[df_ref_f["Classe"] == "VA"])
        st.metric("Tâches à Valeur Ajoutée", f"{va_n} / {len(df_ref_f)}")

    section_title("Analyse comparative des durées standards")
    col1, col2 = st.columns(2)
    with col1:
        df_cls = df_ref_f.groupby("Classe")["Standard (min)"].sum().reset_index()
        fig_cls = px.bar(df_cls, x="Classe", y="Standard (min)",
                         color="Classe",
                         color_discrete_map={"VA": CLASS_COLORS["VA"], "NNVA": CLASS_COLORS["NNVA"]},
                         title="Durée standard cumulée par classe",
                         text_auto=True)
        fig_cls.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(255,255,255,0.5)",
                              height=300, font=dict(family="Nunito"),
                              showlegend=False, margin=dict(t=50))
        st.plotly_chart(fig_cls, use_container_width=True)
    with col2:
        df_essai_ref = df_ref_f.groupby(["Essai", "Classe"])["Standard (min)"].sum().reset_index()
        fig_er = px.bar(df_essai_ref, x="Essai", y="Standard (min)", color="Classe",
                        color_discrete_map={"VA": CLASS_COLORS["VA"], "NNVA": CLASS_COLORS["NNVA"]},
                        barmode="stack", title="Répartition VA / NNVA par essai",
                        text_auto=True)
        fig_er.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(255,255,255,0.5)",
                             height=300, font=dict(family="Nunito"), margin=dict(t=50))
        st.plotly_chart(fig_er, use_container_width=True)

    section_title("Catalogue des tâches et standards de temps")
    styled_ref = df_ref_f[["Produit", "Essai", "Sous-tâche", "Standard (min)", "Classe"]].style.applymap(
        lambda v: (
            f"background-color:{CLASS_COLORS.get(v,'')}22;"
            f"color:{'#2D6A50' if v=='VA' else '#8B5E1A'}; font-weight:600;"
        ) if v in CLASS_COLORS else "",
        subset=["Classe"]
    ).format({"Standard (min)": "{:.0f}"})
    st.dataframe(styled_ref, use_container_width=True, height=440)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9 : DÉMARCHE LEAN & DMAIC (Directement alignée avec le mémoire de Hana Brinis !)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Démarche Lean & DMAIC":

    page_header(
        "Cadre Méthodologique — Démarche DMAIC & Lean Lab",
        "Mémoire PFE Hana Brinis · Laboratoires Néapolis Pharma (Médis) · Université de Tunis El Manar"
    )

    section_title("Les 5 Étapes de la Démarche DMAIC appliquées au laboratoire QC")

    dmaic_steps = [
        {"lettre": "D", "etape": "Définir", "desc": "Cadrage du projet, cartographie SIPOC/processus, analyse QQOQCCP et charte de projet pour cibler les pertes de productivité."},
        {"lettre": "M", "etape": "Mesurer", "desc": "Mise en place des Time Sheets (248 activités), construction du référentiel temporel standard et relevé initial des 22 événements NVA (621 min)."},
        {"lettre": "A", "etape": "Analyser", "desc": "Classification ABC des pertes, Diagramme de Pareto (80/20), diagrammes d'Ishikawa (5M) pour l'eau, les pannes HPLC et réactifs."},
        {"lettre": "I", "etape": "Innover / Améliorer", "desc": "Définition du plan d'action (P-01 à P-06) : remplacement du système d'eau, chaînes HPLC additionnelles, 5S, prototype de tableau de bord."},
        {"lettre": "C", "etape": "Contrôler", "desc": "Mesure des gains (NVA réduite à 253 min, gain net de 368 min), déploiement de ce tableau de bord interactif pour pérenniser la performance."},
    ]

    cols_d = st.columns(5)
    for i, step in enumerate(dmaic_steps):
        with cols_d[i]:
            st.markdown(f"""
            <div style='background:white; border-radius:14px; padding:1.1rem 0.8rem; text-align:center;
                        box-shadow:0 3px 14px rgba(192,99,122,0.08); border-top:3px solid #C0637A; height:100%;'>
                <div style='font-size:1.8rem; font-weight:900; color:#C0637A;'>{step['lettre']}</div>
                <div style='font-size:0.85rem; font-weight:800; color:#2D1B33; margin:0.3rem 0;'>{step['etape']}</div>
                <div style='font-size:0.75rem; color:#6B4D7A; line-height:1.4;'>{step['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    section_title("Classification des 8 Formes de Gaspillage (Muda) en Laboratoire QC")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style='background:white; border-radius:14px; padding:1.2rem; box-shadow:0 2px 12px rgba(192,99,122,0.08);'>
            <div style='font-weight:700; color:#C0637A; margin-bottom:0.5rem;'>1. Attentes (Temps NVA majeur)</div>
            <div style='font-size:0.82rem; color:#4A2D5A;'>Indisponibilité de l'eau purifiée (265 min), attente de libération des chaînes HPLC (95 min), ressources de préparation (50 min).</div>
            <div style='font-weight:700; color:#C0637A; margin:0.8rem 0 0.5rem;'>2. Mouvements et Déplacements Inutiles</div>
            <div style='font-size:0.82rem; color:#4A2D5A;'>Déplacements pour rechercher des solvants, réactifs ou colonnes non centralisés (34 min). Résolu par la méthode 5S (Action P-05).</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style='background:white; border-radius:14px; padding:1.2rem; box-shadow:0 2px 12px rgba(192,99,122,0.08);'>
            <div style='font-weight:700; color:#C0637A; margin-bottom:0.5rem;'>3. Défauts / Retouches & Reprises</div>
            <div style='font-size:0.82rem; color:#4A2D5A;'>Vérifications répétitives et réinjections suite à des anomalies chromatographiques (99 min). Résolu par maintenance préventive (Action P-04).</div>
            <div style='font-weight:700; color:#C0637A; margin:0.8rem 0 0.5rem;'>4. Sur-traitement & Activités NNVA</div>
            <div style='font-size:0.82rem; color:#4A2D5A;'>Enregistrements multiples sur cahiers papier et registres manuels (1 507 min). Standardisés dans le Référentiel des Tâches.</div>
        </div>
        """, unsafe_allow_html=True)

    info_box(
        "<b>Rôle du Tableau de Bord (Action P-06 du mémoire) :</b> Développé par Hana Brinis dans le cadre de son PFE, "
        "cet outil numérique interactif incarne l'aboutissement de la Phase Contrôler. Il transforme les relevés "
        "statiques des Time Sheets en un système décisionnel dynamique pour le management de la qualité."
    )
