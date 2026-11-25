"""
charts.py
Fonctions de visualisation Plotly pour le Système de Pilotage QC.
Charte graphique : Rose poudré + Lavande + Blanc cassé + Vert sauge.
"""

import plotly.graph_objects as go
import plotly.express as px
from styles import COLORS, PLOTLY_PALETTE, CLASS_COLORS


# ── 1. Donut : Répartition VA / NNVA / NVA ──────────────────────────────────
def donut_repartition(va, nnva, nva, periode="AVANT"):
    """Donut chart de répartition du temps opérateur."""
    colors = [CLASS_COLORS["VA"], CLASS_COLORS["NNVA"], CLASS_COLORS["NVA"]]
    total = va + nnva + nva

    fig = go.Figure(go.Pie(
        labels=["Valeur Ajoutée (VA)", "Nécessaire Sans VA (NNVA)", "Non-Valeur Ajoutée (NVA)"],
        values=[va, nnva, nva],
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="white", width=2.5)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Nunito"),
        hovertemplate="<b>%{label}</b><br>%{value} min<br>%{percent}<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{int(total)}</b><br><span style='font-size:10px; color:#9B72AA;'>min total</span>",
        x=0.5, y=0.5,
        font=dict(size=14, color=COLORS["text_dark"], family="Nunito"),
        showarrow=False,
    )

    fig.update_layout(
        title=dict(
            text=f"Répartition — {periode}",
            font=dict(family="Playfair Display, serif", size=15, color=COLORS["text_dark"]),
            x=0.05
        ),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=10)),
        font=dict(family="Nunito"),
        margin=dict(l=10, r=10, t=50, b=40),
    )
    return fig


# ── 2. Barres groupées : NVA AVANT vs APRÈS par cause ───────────────────────
def bar_pertes_par_cause(df_pertes):
    """Barres horizontales comparant AVANT vs APRÈS par source de perte."""
    df = df_pertes.copy()
    df["Source courte"] = df["Source de perte NVA"].str[:35]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Source courte"],
        x=df["AVANT (min)"],
        name="Phase Mesurer (AVANT)",
        orientation="h",
        marker=dict(color=COLORS["danger"], opacity=0.85),
        text=df["AVANT (min)"].apply(lambda x: f"{int(x)} min"),
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        y=df["Source courte"],
        x=df["APRÈS (min)"],
        name="Phase Contrôler (APRÈS)",
        orientation="h",
        marker=dict(color=COLORS["success"], opacity=0.85),
        text=df["APRÈS (min)"].apply(lambda x: f"{int(x)} min"),
        textposition="outside",
    ))

    fig.update_layout(
        barmode="group",
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        margin=dict(l=10, r=70, t=30, b=20),
        xaxis=dict(title="Durée de non-valeur ajoutée (min)", gridcolor="rgba(176,160,184,0.2)"),
        yaxis=dict(tickfont=dict(size=11)),
    )
    return fig


# ── 3. Gauge : Taux NVA ──────────────────────────────────────────────────────
def gauge_taux_nva(taux, label="Taux NVA"):
    """Jauge industrielle affichant le pourcentage NVA."""
    pct = round(taux * 100, 2)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number=dict(suffix=" %", font=dict(size=26, color=COLORS["primary"], family="Nunito")),
        gauge=dict(
            axis=dict(range=[0, 20], ticksuffix=" %", tickfont=dict(size=10)),
            bar=dict(color=COLORS["primary"], thickness=0.55),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0, 5],  color="#E8F5F0"),
                dict(range=[5, 10], color="#FDE8EF"),
                dict(range=[10, 20], color="#FDD5D5"),
            ],
            threshold=dict(
                line=dict(color=COLORS["danger"], width=2.5),
                thickness=0.75, value=11.35
            ),
        ),
        title=dict(text=label, font=dict(size=12, color=COLORS["text_mid"], family="Nunito")),
    ))
    fig.update_layout(
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=30, b=10),
        font=dict(family="Nunito"),
    )
    return fig


# ── 4. Waterfall : Décomposition du gain ────────────────────────────────────
def waterfall_gain(df_pertes):
    """Waterfall chart montrant la contribution de chaque cause au gain net."""
    df = df_pertes.copy()
    df["Source courte"] = df["Source de perte NVA"].str[:28]
    df = df.sort_values("Gain (min)", ascending=False)

    total_gain = int(df["Gain (min)"].sum())

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"] * len(df) + ["total"],
        x=list(df["Source courte"]) + ["GAIN NET TOTAL"],
        y=list(df["Gain (min)"]) + [total_gain],
        text=[f"+{int(g)}" if g > 0 else f"{int(g)}" for g in df["Gain (min)"]] + [f"+{total_gain} min"],
        textposition="outside",
        connector=dict(line=dict(color=COLORS["grey"], width=1)),
        increasing=dict(marker=dict(color=COLORS["success"])),
        decreasing=dict(marker=dict(color=COLORS["danger"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
        textfont=dict(family="Nunito", size=10.5),
    ))
    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        margin=dict(l=20, r=20, t=30, b=90),
        yaxis=dict(title="Gain en temps (min)", gridcolor="rgba(176,160,184,0.2)"),
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        showlegend=False,
    )
    return fig


# ── 5. Courbe de Pareto (Loi 80/20) ──────────────────────────────────────────
def pareto_chart(df_pertes):
    """Diagramme de Pareto professionnel : Barres décroissantes + Courbe cumulative."""
    df = df_pertes.copy().sort_values("AVANT (min)", ascending=False).reset_index(drop=True)
    df["Source courte"] = df["Source de perte NVA"].str[:28]
    total = df["AVANT (min)"].sum()
    df["Cumul %"] = (df["AVANT (min)"].cumsum() / total) * 100

    fig = go.Figure()

    # Barres de durée
    fig.add_trace(go.Bar(
        x=df["Source courte"],
        y=df["AVANT (min)"],
        name="Durée NVA (min)",
        marker=dict(color=COLORS["primary"], opacity=0.85),
        text=df["AVANT (min)"].apply(lambda x: f"{int(x)} min"),
        textposition="outside",
        yaxis="y1"
    ))

    # Courbe cumulative
    fig.add_trace(go.Scatter(
        x=df["Source courte"],
        y=df["Cumul %"],
        name="Cumul relatif (%)",
        mode="lines+markers",
        line=dict(color=COLORS["secondary"], width=2.5),
        marker=dict(size=7, color=COLORS["secondary"]),
        yaxis="y2"
    ))

    # Ligne de seuil 80%
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(df)-0.5,
        y0=80, y1=80,
        yref="y2",
        line=dict(color="#D96B6B", width=1.5, dash="dash"),
    )
    fig.add_annotation(
        x=len(df)-1, y=82,
        yref="y2",
        text="Seuil 80% (Pareto)",
        showarrow=False,
        font=dict(size=10, color="#D96B6B", family="Nunito")
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        margin=dict(l=20, r=40, t=30, b=90),
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        yaxis=dict(
            title="Durée NVA (min)",
            gridcolor="rgba(176,160,184,0.2)"
        ),
        yaxis2=dict(
            title="Pourcentage cumulé (%)",
            overlaying="y",
            side="right",
            range=[0, 105],
            ticksuffix=" %",
            showgrid=False
        )
    )
    return fig


# ── 6. Radar Chart : Profil comparatif par essai ─────────────────────────────
def radar_chart_essais(df_ep):
    """Profil en radar comparant les pertes par type d'essai AVANT vs APRÈS."""
    categories = df_ep["Essai"].tolist()
    if not categories:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df_ep["AVANT"].tolist() + [df_ep["AVANT"].iloc[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(217, 107, 107, 0.25)',
        line=dict(color=COLORS["danger"], width=2),
        name="Phase Mesurer (AVANT)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=df_ep["APRÈS"].tolist() + [df_ep["APRÈS"].iloc[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(107, 171, 144, 0.25)',
        line=dict(color=COLORS["success"], width=2),
        name="Phase Contrôler (APRÈS)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(df_ep["AVANT"].max(), 10) * 1.15],
                            gridcolor="rgba(176,160,184,0.25)"),
            bgcolor="rgba(255,255,255,0.4)"
        ),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=10.5)),
        margin=dict(l=30, r=30, t=20, b=40)
    )
    return fig


# ── 7. Barres comparatives par essai ─────────────────────────────────────────
def bar_par_essai(df_ep):
    """Barres groupées AVANT/APRÈS par essai avec affichage de valeurs."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_ep["Essai"],
        y=df_ep["AVANT"],
        name="Phase Mesurer (AVANT)",
        marker_color=COLORS["danger"],
        opacity=0.85,
        text=df_ep["AVANT"].apply(lambda x: f"{int(x)} min"),
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=df_ep["Essai"],
        y=df_ep["APRÈS"],
        name="Phase Contrôler (APRÈS)",
        marker_color=COLORS["success"],
        opacity=0.85,
        text=df_ep["APRÈS"].apply(lambda x: f"{int(x)} min"),
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        margin=dict(l=20, r=20, t=30, b=40),
        xaxis=dict(title="Type d'essai"),
        yaxis=dict(title="Durée NVA (min)", gridcolor="rgba(176,160,184,0.2)"),
    )
    return fig


# ── 8. Scatter : NVA par événement ──────────────────────────────────────────
def scatter_nva_events(df_nva):
    """Distribution des événements NVA par catégorie et durée."""
    fig = px.scatter(
        df_nva,
        x="Catégorie NVA",
        y="Durée (min)",
        color="Période",
        size="Durée (min)",
        size_max=35,
        color_discrete_map={"AVANT": COLORS["danger"], "APRÈS": COLORS["success"]},
        hover_data=["ID", "Produit", "Lot", "Essai"],
        labels={"Catégorie NVA": "Catégorie", "Durée (min)": "Durée (min)"},
    )
    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        margin=dict(l=20, r=20, t=20, b=80),
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        yaxis=dict(gridcolor="rgba(176,160,184,0.2)")
    )
    return fig


# ── 9. Stacked Bar : VA / NNVA / NVA comparaison globale ────────────────────
def bar_avant_apres_global(kpi):
    """Stacked bar AVANT vs APRÈS mettant en évidence la contraction de la NVA."""
    categories = ["Phase Mesurer (AVANT)", "Phase Contrôler (APRÈS)"]
    va_vals    = [kpi["va_avant"], kpi["va_avant"]]
    nnva_vals  = [kpi["nnva_avant"], kpi["nnva_avant"]]
    nva_vals   = [kpi["nva_avant"], kpi["nva_apres"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Valeur Ajoutée (VA)",
        x=categories, y=va_vals,
        marker_color=CLASS_COLORS["VA"],
        text=[f"{int(v)} min" for v in va_vals], textposition="inside",
        textfont=dict(size=12, color="white", family="Nunito", weight="bold"),
        insidetextanchor="middle",
    ))
    fig.add_trace(go.Bar(
        name="Nécessaire Sans VA (NNVA)",
        x=categories, y=nnva_vals,
        marker_color=CLASS_COLORS["NNVA"],
        text=[f"{int(v)} min" for v in nnva_vals], textposition="inside",
        textfont=dict(size=12, color="white", family="Nunito", weight="bold"),
        insidetextanchor="middle",
    ))
    fig.add_trace(go.Bar(
        name="Non-Valeur Ajoutée (NVA)",
        x=categories, y=nva_vals,
        marker_color=CLASS_COLORS["NVA"],
        text=[f"{int(v)} min" for v in nva_vals], textposition="inside",
        textfont=dict(size=12, color="white", family="Nunito", weight="bold"),
        insidetextanchor="middle",
    ))

    fig.update_layout(
        barmode="stack",
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(
            orientation="h",
            y=1.18, x=0.5, xanchor="center",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="rgba(0,0,0,0.08)",
            borderwidth=1,
            font=dict(size=12),
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        yaxis=dict(title="Temps opérateur global (min)", gridcolor="rgba(176,160,184,0.2)"),
    )
    return fig


# ── 10. Heatmap : NVA par produit × essai ───────────────────────────────────
def heatmap_nva_produit_essai(df_nva):
    """Heatmap de la durée NVA par Produit et Essai."""
    df_avant = df_nva[df_nva["Période"] == "AVANT"].groupby(["Produit", "Essai"])["Durée (min)"].sum().reset_index()
    pivot = df_avant.pivot(index="Produit", columns="Essai", values="Durée (min)").fillna(0)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#FDE8EF"], [0.5, "#C0637A"], [1, "#2D1B33"]],
        text=pivot.values,
        texttemplate="%{text:.0f} min",
        textfont=dict(size=11, color="white", family="Nunito"),
        hovertemplate="Produit: %{y}<br>Essai: %{x}<br>NVA: %{z:.0f} min<extra></extra>",
        showscale=True,
        colorbar=dict(title="min"),
    ))
    fig.update_layout(
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        margin=dict(l=10, r=10, t=20, b=30),
        xaxis=dict(title="Type d'essai"),
        yaxis=dict(title=""),
    )
    return fig


# ── 11. Box plot : Distribution des durées des sous-tâches ───────────────────
def boxplot_distribution_taches(df_ts):
    """Courbe de distribution (Box Plot) des durées unitaires des sous-tâches."""
    fig = px.box(
        df_ts,
        x="Classe VA/NNVA",
        y="Durée brute (min)",
        color="Classe VA/NNVA",
        color_discrete_map={"VA": CLASS_COLORS["VA"], "NNVA": CLASS_COLORS["NNVA"]},
        points="all",
        hover_data=["Sous-tâche", "Produit", "Essai"]
    )
    fig.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=30),
        xaxis=dict(title="Classification de l'activité"),
        yaxis=dict(title="Durée brute unitaire (min)", gridcolor="rgba(176,160,184,0.2)"),
    )
    return fig


# ── 12. Courbe d'évolution temporelle par lot ───────────────────────────────
def line_evolution_temporelle_lots(df_nva):
    """Courbe de tendance chronologique de la perte de temps à travers les lots analytiques."""
    df_lot = df_nva.groupby(["Lot", "Période"])["Durée (min)"].sum().unstack(fill_value=0).reset_index()
    # Trier proprement les lots
    df_lot["Lot_num"] = df_lot["Lot"].str.extract(r'(\d+)').astype(int)
    df_lot = df_lot.sort_values("Lot_num").reset_index(drop=True)

    fig = go.Figure()
    # Courbe AVANT
    fig.add_trace(go.Scatter(
        x=df_lot["Lot"],
        y=df_lot["AVANT"],
        mode="lines+markers",
        name="Phase Mesurer (AVANT)",
        line=dict(color=COLORS["danger"], width=3),
        marker=dict(size=9, color=COLORS["danger"]),
        text=[f"{int(v)} min" for v in df_lot["AVANT"]],
        textposition="top center"
    ))
    # Courbe APRÈS
    fig.add_trace(go.Scatter(
        x=df_lot["Lot"],
        y=df_lot["APRÈS"],
        mode="lines+markers",
        name="Phase Contrôler (APRÈS)",
        line=dict(color=COLORS["success"], width=3),
        marker=dict(size=9, color=COLORS["success"]),
        text=[f"{int(v)} min" for v in df_lot["APRÈS"]],
        textposition="bottom center"
    ))

    fig.update_layout(
        title=dict(
            text="Trajectoire de réduction du temps perdu par lot analytique",
            font=dict(family="Playfair Display, serif", size=14, color=COLORS["text_dark"]),
            x=0.03
        ),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis=dict(title="Lot analytique successif"),
        yaxis=dict(title="Durée NVA totale (min)", gridcolor="rgba(176,160,184,0.2)"),
    )
    return fig


# ── 13. Graphique des gains temporels cumulés ───────────────────────────────
def bar_cumul_gains_temporels(df_nva):
    """Courbe des gains temporels cumulés au fil des lots."""
    df_lot = df_nva.groupby(["Lot", "Période"])["Durée (min)"].sum().unstack(fill_value=0).reset_index()
    df_lot["Lot_num"] = df_lot["Lot"].str.extract(r'(\d+)').astype(int)
    df_lot = df_lot.sort_values("Lot_num").reset_index(drop=True)
    df_lot["Gain"] = df_lot["AVANT"] - df_lot["APRÈS"]
    df_lot["Gain_Cumul"] = df_lot["Gain"].cumsum()

    fig = go.Figure()

    # Barres de gain par lot
    fig.add_trace(go.Bar(
        x=df_lot["Lot"],
        y=df_lot["Gain"],
        name="Gain par lot (min)",
        marker=dict(color=COLORS["accent"], opacity=0.85),
        text=[f"+{int(g)} min" for g in df_lot["Gain"]],
        textposition="outside",
        yaxis="y1"
    ))

    # Courbe cumulative
    fig.add_trace(go.Scatter(
        x=df_lot["Lot"],
        y=df_lot["Gain_Cumul"],
        name="Gain cumulé (min)",
        mode="lines+markers",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=8, color=COLORS["primary"]),
        text=[f"+{int(c)} min cumulées" for c in df_lot["Gain_Cumul"]],
        textposition="top left",
        yaxis="y2"
    ))

    fig.update_layout(
        title=dict(
            text="Accumulation progressive du temps récupéré",
            font=dict(family="Playfair Display, serif", size=14, color=COLORS["text_dark"]),
            x=0.03
        ),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Nunito", color=COLORS["text_mid"]),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        margin=dict(l=20, r=40, t=50, b=40),
        xaxis=dict(title="Lot analytique successif"),
        yaxis=dict(title="Gain par lot (min)", gridcolor="rgba(176,160,184,0.2)"),
        yaxis2=dict(
            title="Gain cumulé (min)",
            overlaying="y",
            side="right",
            range=[0, df_lot["Gain_Cumul"].max() * 1.2],
            ticksuffix=" min",
            showgrid=False
        )
    )
    return fig
