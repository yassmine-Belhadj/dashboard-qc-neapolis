"""
styles.py
Charte graphique : Vert Clair & Bleu Neapolis Pharma + Blanc épuré.
Professionnel, pharmaceutique, corporate et élégant pour soutenance PFE (Mention Très Bien).
"""

# ─── Palette de couleurs Neapolis Pharma ──────────────────────────────────────
COLORS = {
    "primary":      "#3A7D34",   # Vert Neapolis Pharma
    "secondary":    "#1A5F8E",   # Bleu Neapolis Pharma
    "accent":       "#5A9E3A",   # Vert vif corporate
    "vert_clair":   "#6BB34C",   # Vert clair dynamique
    "light_green":  "#EBF5EE",   # Fond vert clair doux
    "light_blue":   "#E8F4FD",   # Fond bleu clair doux
    "white":        "#FFFFFF",   # Blanc pur
    "text_dark":    "#132E20",   # Vert forêt très foncé (texte principal)
    "text_mid":     "#2E5339",   # Vert forêt moyen
    "success":      "#438938",   # Vert succès / gain
    "warning":      "#E8A45A",   # Ambre (attention)
    "danger":       "#D9534F",   # Rouge doux (pertes NVA)
    "grey":         "#8FA89B",   # Gris vert sauge
    "bg_gradient1": "#F2FAF4",
    "bg_gradient2": "#E8F4EC",
}

# Palette Plotly pour les graphiques
PLOTLY_PALETTE = [
    "#3A7D34",  # vert Neapolis
    "#1A5F8E",  # bleu Neapolis
    "#5A9E3A",  # vert clair
    "#438938",  # vert forêt
    "#E8A45A",  # ambre
    "#7EC8E3",  # bleu ciel
    "#D9534F",  # rouge perte
    "#8FA89B",  # gris vert
]

# Couleurs spécifiques VA / NNVA / NVA (Standard Lean Pharma)
CLASS_COLORS = {
    "VA":   "#4A9B68",  # Vert sauge Neapolis = valeur ajoutée
    "NNVA": "#E69A38",  # Ambre = nécessaire sans VA
    "NVA":  "#D9534F",  # Rouge doux = perte
}

# ─── CSS global injecté dans Streamlit ───────────────────────────────────────
CSS = """
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #132E20;
}

/* ── Fond principal : Vert clair pharmaceutique très doux ── */
.stApp {
    background: linear-gradient(135deg, #F3F9F4 0%, #EBF5EE 50%, #F5FAF6 100%);
    background-attachment: fixed;
}

/* ── Sidebar — Bleu Neapolis Pharma Corporate ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2F4C 0%, #134B70 50%, #0A2F4C 100%);
    border-right: none;
    box-shadow: 4px 0 25px rgba(10, 47, 76, 0.4);
}
[data-testid="stSidebar"] * {
    color: #E8F4FD !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label {
    color: #7EC8E3 !important;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Boutons Corporate Vert & Bleu Neapolis ── */
div.stButton > button {
    background: linear-gradient(135deg, #3A7D34 0%, #1A5F8E 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: 0 4px 18px rgba(58, 125, 52, 0.4) !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 24px rgba(26, 95, 142, 0.6) !important;
    background: linear-gradient(135deg, #438938 0%, #2072A8 100%) !important;
}
div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Zone Uploader Drag & Drop Vert Clair ── */
[data-testid="stFileUploader"] {
    background: rgba(235, 245, 238, 0.15) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(235, 245, 238, 0.22) !important;
    border: 2px dashed #7EC8E3 !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #5A9E3A !important;
    background: rgba(235, 245, 238, 0.35) !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #3A7D34 0%, #1A5F8E 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 12px rgba(58, 125, 52, 0.35) !important;
}

/* ── Titre principal Corporate ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #0A2F4C, #3A7D34);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}
.subtitle {
    color: #1A5F8E;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 1.2rem;
    letter-spacing: 0.02em;
}

/* ── Cartes KPI Vert Clair & Blanc ── */
.kpi-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.4rem 1.1rem;
    text-align: center;
    box-shadow: 0 4px 18px rgba(26, 95, 142, 0.08);
    border: 1px solid rgba(90, 158, 58, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(58, 125, 52, 0.16);
    border-color: rgba(90, 158, 58, 0.45);
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #D9534F;
    line-height: 1.1;
}
.kpi-value-green {
    font-size: 2.2rem;
    font-weight: 800;
    color: #3A7D34;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.76rem;
    color: #1A5F8E;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.4rem;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #0A2F4C;
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid;
    border-image: linear-gradient(90deg, #3A7D34, #1A5F8E, transparent) 1;
}

/* ── Info box vert clair ── */
.info-box {
    background: linear-gradient(135deg, #EBF5EE, #E8F4FD);
    border-left: 4px solid #3A7D34;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.1rem;
    margin: 1rem 0;
    font-size: 0.88rem;
    color: #132E20;
    line-height: 1.6;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 12px 12px 0 0;
    color: #1A5F8E;
    font-weight: 600;
    font-size: 0.85rem;
    border: 1px solid rgba(90, 158, 58, 0.3);
    border-bottom: none;
    padding: 0.6rem 1.2rem;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3A7D34, #1A5F8E) !important;
    color: white !important;
    border-color: transparent !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 14px rgba(26, 95, 142, 0.08);
}
thead tr th {
    background: linear-gradient(135deg, #134B70, #3A7D34) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #EBF5EE; }
::-webkit-scrollbar-thumb { background: #3A7D34; border-radius: 10px; }
</style>
"""
