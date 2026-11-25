"""
styles.py
Charte graphique : Rose poudré + Lavande + Blanc cassé + Bordeaux doux.
Élégant, raffiné et scientifique pour soutenance PFE (Mention Très Bien).
"""

# ─── Palette de couleurs ──────────────────────────────────────────────────────
COLORS = {
    "primary":      "#C0637A",   # Rose bordeaux (accent principal)
    "secondary":    "#9B72AA",   # Lavande foncée
    "accent":       "#E8A0B4",   # Rose poudré
    "rose_vif":     "#D87093",   # Rose vif élégant
    "light_pink":   "#FDE8EF",   # Rose très clair (fond de carte)
    "light_purple": "#EDE0F5",   # Lavande très claire
    "white":        "#FFFAF9",   # Blanc cassé
    "text_dark":    "#2D1B33",   # Violet très foncé (texte principal)
    "text_mid":     "#6B4D7A",   # Violet moyen
    "success":      "#6BAB90",   # Vert sauge (succès, gain)
    "warning":      "#E8A45A",   # Ambre (attention)
    "danger":       "#D96B6B",   # Rouge doux (perte)
    "grey":         "#B0A0B8",   # Gris lavandé
    "bg_gradient1": "#FDE8EF",
    "bg_gradient2": "#EDE0F5",
}

# Palette Plotly pour les graphiques
PLOTLY_PALETTE = [
    "#C0637A",  # rose bordeaux
    "#9B72AA",  # lavande
    "#E8A0B4",  # rose poudré
    "#6BAB90",  # vert sauge
    "#E8A45A",  # ambre
    "#7BAFD4",  # bleu ciel
    "#D96B6B",  # rouge doux
    "#B0A0B8",  # gris lavandé
]

# Couleurs spécifiques VA / NNVA / NVA
CLASS_COLORS = {
    "VA":   "#6BAB90",  # Vert sauge = valeur ajoutée
    "NNVA": "#E8A45A",  # Ambre = nécessaire sans VA
    "NVA":  "#D96B6B",  # Rouge doux = perte
}

# ─── CSS global injecté dans Streamlit ───────────────────────────────────────
CSS = """
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #2D1B33;
}

/* ── Fond principal ── */
.stApp {
    background: linear-gradient(135deg, #FFF6F8 0%, #F6EEF8 50%, #FFF8FA 100%);
    background-attachment: fixed;
}

/* ── Sidebar — Bleu Neapolis Pharma ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D3B5E 0%, #1A5F8E 45%, #0D3B5E 100%);
    border-right: none;
    box-shadow: 4px 0 25px rgba(26, 95, 142, 0.35);
}
[data-testid="stSidebar"] * {
    color: #E8F4FD !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label {
    color: #7EC8E3 !important;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Boutons Roses Très Visibles ── */
div.stButton > button {
    background: linear-gradient(135deg, #C0637A 0%, #D87093 50%, #C0637A 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: 0 4px 18px rgba(192, 99, 122, 0.45) !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 24px rgba(216, 112, 147, 0.65) !important;
    background: linear-gradient(135deg, #D87093 0%, #C0637A 100%) !important;
}
div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Zone Uploader Drag & Drop Rose ── */
[data-testid="stFileUploader"] {
    background: rgba(253, 232, 239, 0.12) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(253, 232, 239, 0.18) !important;
    border: 2px dashed #D87093 !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #E8A0B4 !important;
    background: rgba(253, 232, 239, 0.3) !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #C0637A 0%, #D87093 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 12px rgba(192, 99, 122, 0.4) !important;
}

/* ── Titre principal ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #C0637A, #9B72AA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}
.subtitle {
    color: #9B72AA;
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 1.2rem;
    letter-spacing: 0.02em;
}

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 1.4rem 1.1rem;
    text-align: center;
    box-shadow: 0 4px 18px rgba(192, 99, 122, 0.09);
    border: 1px solid rgba(232, 160, 180, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(192, 99, 122, 0.18);
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #C0637A;
    line-height: 1.1;
}
.kpi-value-green {
    font-size: 2.2rem;
    font-weight: 800;
    color: #6BAB90;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.76rem;
    color: #9B72AA;
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
    color: #2D1B33;
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid;
    border-image: linear-gradient(90deg, #C0637A, #9B72AA, transparent) 1;
}

/* ── Info box ── */
.info-box {
    background: linear-gradient(135deg, #FDE8EF, #EDE0F5);
    border-left: 4px solid #C0637A;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.1rem;
    margin: 1rem 0;
    font-size: 0.88rem;
    color: #4A2D5A;
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
    color: #9B72AA;
    font-weight: 600;
    font-size: 0.85rem;
    border: 1px solid rgba(232, 160, 180, 0.4);
    border-bottom: none;
    padding: 0.6rem 1.2rem;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #C0637A, #9B72AA) !important;
    color: white !important;
    border-color: transparent !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 14px rgba(192, 99, 122, 0.08);
}
thead tr th {
    background: linear-gradient(135deg, #C0637A, #9B72AA) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #FDE8EF; }
::-webkit-scrollbar-thumb { background: #C0637A; border-radius: 10px; }
</style>
"""
