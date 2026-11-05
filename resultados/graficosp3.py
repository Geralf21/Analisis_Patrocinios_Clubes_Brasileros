import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# =======================================
# PREGUNTA 3.-¿Existe una relación directa entre el monto recibido por
#  patrocinio de casas de apuestas y el desempeño deportivo/financiero?


COLUMNAS_REQUERIDAS_P3 = {
    "club",
    "año",
    "patrocinador_master",
    "ingresos_sponsors_millones_BRL",
    "posicion_liga",
    "puntos_obtenidos",
    "gasto_fichajes_millones_EUR",
    "ingresos_ventas_millones_EUR",
}


def preparar_datos_p3(df):
    """Prepara las columnas y categorías utilizadas por los análisis de P3."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    faltantes = COLUMNAS_REQUERIDAS_P3.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas para el análisis P3: "
            + ", ".join(sorted(faltantes))
        )

    columnas_numericas = [
        "año",
        "ingresos_sponsors_millones_BRL",
        "posicion_liga",
        "puntos_obtenidos",
        "gasto_fichajes_millones_EUR",
        "ingresos_ventas_millones_EUR",
    ]
    for columna in columnas_numericas:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

    df["es_bet"] = df["patrocinador_master"].str.contains(
        r"bet|pix|blaze|esportes",
        case=False,
        na=False,
        regex=True,
    )
    df["ingresos_netos_transferencias_millones_EUR"] = (
        df["ingresos_ventas_millones_EUR"]
        - df["gasto_fichajes_millones_EUR"]
    )
    return df


def crear_resumen_sponsors_p3(df):
    """Agrega indicadores financieros y deportivos por tipo de patrocinador."""
    columnas_requeridas = {
        "es_bet",
        "ingresos_sponsors_millones_BRL",
        "ingresos_netos_transferencias_millones_EUR",
        "gasto_fichajes_millones_EUR",
        "puntos_obtenidos",
        "posicion_liga",
    }
    faltantes = columnas_requeridas.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas para resumir los datos de P3: "
            + ", ".join(sorted(faltantes))
        )

    resumen = (
        df.groupby("es_bet")
        .agg(
            total_sponsors_BRL=("ingresos_sponsors_millones_BRL", "sum"),
            promedio_sponsors_BRL=("ingresos_sponsors_millones_BRL", "mean"),
            total_neto_transferencias_EUR=(
                "ingresos_netos_transferencias_millones_EUR",
                "sum",
            ),
            promedio_neto_transferencias_EUR=(
                "ingresos_netos_transferencias_millones_EUR",
                "mean",
            ),
            total_gasto_fichajes_EUR=("gasto_fichajes_millones_EUR", "sum"),
            promedio_puntos=("puntos_obtenidos", "mean"),
            promedio_posicion=("posicion_liga", "mean"),
        )
        .reset_index()
    )
    resumen["total_ingreso_sponsors_BRL"] = resumen["total_sponsors_BRL"]
    resumen["categoria"] = resumen["es_bet"].map(
        {True: "Casas de Apuestas", False: "Sponsors Tradicionales"}
    )
    return resumen


def mostrar_resumen_p3(df, resumen):
    """Muestra indicadores descriptivos y el resumen comparativo de P3."""
    periodo1 = df.loc[(df["es_bet"]) & (df["año"] <= 2023)]
    periodo2 = df.loc[(df["es_bet"]) & (df["año"] >= 2024)]
    estadisticas_periodos = pd.DataFrame(
        {
            "n": [len(periodo1), len(periodo2)],
            "mediana_sponsor_BRL": [
                periodo1["ingresos_sponsors_millones_BRL"].median(),
                periodo2["ingresos_sponsors_millones_BRL"].median(),
            ],
            "min_sponsor_BRL": [
                periodo1["ingresos_sponsors_millones_BRL"].min(),
                periodo2["ingresos_sponsors_millones_BRL"].min(),
            ],
            "max_sponsor_BRL": [
                periodo1["ingresos_sponsors_millones_BRL"].max(),
                periodo2["ingresos_sponsors_millones_BRL"].max(),
            ],
            "mediana_fichajes_EUR": [
                periodo1["gasto_fichajes_millones_EUR"].median(),
                periodo2["gasto_fichajes_millones_EUR"].median(),
            ],
        },
        index=["2021-2023", "2024-2026"],
    )
    mayor_gasto = df.loc[df["gasto_fichajes_millones_EUR"].idxmax()]

    print("\n--- P3: Resumen por período (patrocinadores de apuestas) ---")
    print(estadisticas_periodos.to_string())
    print(
        "\nMayor gasto en fichajes: "
        f"{mayor_gasto['club']} ({int(mayor_gasto['año'])}), "
        f"{mayor_gasto['gasto_fichajes_millones_EUR']:.1f} M EUR"
    )
    print("\n--- P3: Indicadores por tipo de patrocinador ---")
    print(
        resumen[
            [
                "categoria",
                "total_sponsors_BRL",
                "promedio_sponsors_BRL",
                "total_neto_transferencias_EUR",
                "promedio_neto_transferencias_EUR",
                "total_gasto_fichajes_EUR",
                "promedio_puntos",
                "promedio_posicion",
            ]
        ].to_string(index=False)
    )
    return estadisticas_periodos


def analisis_rendimiento_posicion_promedio(df, guardar_path=None, mostrar=True):
    """Grafica la posición promedio en liga (Serie A) entre sponsors Tradicionales vs Bets."""
    df_valid = df.loc[df["posicion_liga"].notnull()].copy()
    promedios = df_valid.groupby("es_bet")["posicion_liga"].mean().reset_index()
    promedios["categoria"] = promedios["es_bet"].map(
        {True: "Casas de Apuestas", False: "Sponsors Tradicionales"}
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=promedios,
        x="categoria",
        y="posicion_liga",
        hue="categoria",
        hue_order=["Casas de Apuestas", "Sponsors Tradicionales"],
        palette={
            "Casas de Apuestas": "#1F4E79",
            "Sponsors Tradicionales": "#D14D49",
        },
        dodge=False,
        legend=False,
        width=0.4,
        ax=ax,
    )

    ax.invert_yaxis()
    ax.set_yticks(range(1, 12))

    ax.set_title(
        "Observación 3.1: Rendimiento Deportivo en Tabla\n"
        "Posición Promedio en Brasileirão Serie A (Menor es mejor)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_xlabel("")
    ax.set_ylabel("Posición Promedio en Tabla", fontsize=11, fontweight="bold")

    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}° puesto",
            (bar.get_x() + bar.get_width() / 2.0, height),
            ha="center",
            va="top",
            fontsize=11,
            fontweight="bold",
            xytext=(0, -12),
            textcoords="offset points",
        )

    sns.despine()
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax


def analisis_transferencias_paridad_vs_gasto(
    df_resumen, guardar_path=None, mostrar=True
):
    """Grafica la comparativa de Ingresos Netos vs Gasto Bruto en Fichajes (€ M)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

    # Subgráfico 1: Ingresos Netos
    sns.barplot(
        data=df_resumen,
        x="categoria",
        y="total_neto_transferencias_EUR",
        hue="categoria",
        hue_order=["Casas de Apuestas", "Sponsors Tradicionales"],
        palette={
            "Casas de Apuestas": "#1F4E79",
            "Sponsors Tradicionales": "#D14D49",
        },
        dodge=False,
        legend=False,
        width=0.4,
        ax=ax1,
    )
    ax1.set_title(
        "1. Ingresos Netos de Transferencias (€ M)\n(Ventas - Fichajes)",
        fontsize=12,
        fontweight="bold",
    )
    ax1.set_ylabel("Millones de Euros (€ M)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in ax1.patches:
        ax1.annotate(
            f"€{bar.get_height():.1f}M",
            (bar.get_x() + bar.get_width() / 2.0, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

    # Subgráfico 2: Gasto Bruto
    sns.barplot(
        data=df_resumen,
        x="categoria",
        y="total_gasto_fichajes_EUR",
        hue="categoria",
        hue_order=["Casas de Apuestas", "Sponsors Tradicionales"],
        palette={
            "Casas de Apuestas": "#1F4E79",
            "Sponsors Tradicionales": "#D14D49",
        },
        dodge=False,
        legend=False,
        width=0.4,
        ax=ax2,
    )
    ax2.set_title(
        "2. Gasto Bruto en Fichajes (€ M)\n(Inversión en Compras)",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_ylabel("")
    ax2.set_xlabel("")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in ax2.patches:
        ax2.annotate(
            f"€{bar.get_height():.1f}M",
            (bar.get_x() + bar.get_width() / 2.0, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

    sns.despine()
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, (ax1, ax2)


def analisis_total_ingresos_sponsors(
    df_resumen, guardar_path=None, mostrar=True
):
    """Grafica el total acumulado de ingresos por patrocinio en BRL."""
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(
        data=df_resumen,
        x="categoria",
        y="total_ingreso_sponsors_BRL",
        palette=["#1F4E79", "#D14D49"],
        width=0.4,
        ax=ax,
    )

    ax.set_title(
        "Observación 3.3: Inyección Total de Capital\n"
        "Total Acumulado de Ingresos por Sponsors (Millones BRL)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_ylabel("Millones de Reales (BRL M)", fontsize=11, fontweight="bold")
    ax.set_xlabel("")

    for bar in ax.patches:
        ax.annotate(
            f"R$ {bar.get_height():.1f}M",
            (bar.get_x() + bar.get_width() / 2.0, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

    sns.despine()
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax


def analisis_scatter_etapas_pearson(df, guardar_path=None, mostrar=True):
    """Grafica la dispersión por etapas (2021-2023 vs 2024-2026) con Pearson."""
    df_periodo1 = df.loc[(df["es_bet"] == True) & (df["año"] <= 2023)]
    df_periodo2 = df.loc[(df["es_bet"] == True) & (df["año"] >= 2024)]

    r_p1 = df_periodo1["ingresos_sponsors_millones_BRL"].corr(
        df_periodo1["gasto_fichajes_millones_EUR"]
    )
    r_p2 = df_periodo2["ingresos_sponsors_millones_BRL"].corr(
        df_periodo2["gasto_fichajes_millones_EUR"]
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Subgráfico 1
    sns.scatterplot(
        data=df_periodo1,
        x="ingresos_sponsors_millones_BRL",
        y="gasto_fichajes_millones_EUR",
        hue="club",
        style="año",
        s=140,
        ax=ax1,
    )
    ax1.set_title(
        "1. Surgimiento de Bets (2021-2023)", fontsize=12, fontweight="bold"
    )
    ax1.set_ylabel("Inversión en Fichajes (M EUR)", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax1.text(
        0.45,
        0.85,
        f"Coef. Pearson (r) = {r_p1:.2f}",
        transform=ax1.transAxes,
        fontsize=11,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="gray",
            alpha=0.9,
        ),
    )

    # Subgráfico 2
    sns.scatterplot(
        data=df_periodo2,
        x="ingresos_sponsors_millones_BRL",
        y="gasto_fichajes_millones_EUR",
        hue="club",
        style="año",
        s=140,
        ax=ax2,
    )
    ax2.set_title(
        "2. Consolidación del Mercado (2024-2026)",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xlabel("Ingresos por Sponsor Bet (Millones BRL)", fontsize=11)
    ax2.set_ylabel("Inversión en Fichajes (M EUR)", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.5)

    ax2.text(
        0.45,
        0.85,
        f"Coef. Pearson (r) = {r_p2:.2f}",
        transform=ax2.transAxes,
        fontsize=11,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="gray",
            alpha=0.9,
        ),
    )

    sns.despine()
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, (ax1, ax2)

def analisis_scatter_bets_vs_ingresos_netos(
    df, guardar_path=None, mostrar=True
):
    """Grafica la dispersión entre Ingresos por Sponsor Bet (BRL M)

    e Ingresos Netos por Transferencias (€ M) para los clubes con Bet.
    """
    # 1. Asegurar el filtro de clubes con Casa de Apuestas
    df_bets = df.loc[df["es_bet"] == True].copy()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot
    sns.scatterplot(
        data=df_bets,
        x="ingresos_sponsors_millones_BRL",
        y="ingresos_netos_transferencias_millones_EUR",
        hue="club",
        style="año",
        s=140,
        ax=ax,
    )

    # Línea de referencia horizontal en y=0 (Superávit vs Déficit)
    ax.axhline(0, color="#7F7F7F", linestyle="--", linewidth=1.5, alpha=0.8)

    ax.set_title(
        "Observación 3.5: Financiamiento de planteles vs Balance Neto\n"
        "Ingresos por Sponsor Bet vs. Ingresos Netos por Transferencias (€ M)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_xlabel(
        "Ingresos por Sponsor Bet (Millones BRL)", fontsize=11, fontweight="bold"
    )
    ax.set_ylabel(
        "Ingresos Netos Transferencias (€ M) [Ventas - Fichajes]",
        fontsize=11,
        fontweight="bold",
    )
    ax.grid(True, linestyle="--", alpha=0.5)

    # Anotaciones explicativas de zonas de superávit / déficit
    ax.text(
        0.02,
        0.93,
        "▲ Superávit (Mayor venta que compra)",
        transform=ax.transAxes,
        fontsize=9.5,
        fontweight="bold",
        color="#1F4E79",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="#1F4E79",
            alpha=0.8,
        ),
    )
    ax.text(
        0.02,
        0.05,
        "▼ Déficit / Inversión Neta en Compras",
        transform=ax.transAxes,
        fontsize=9.5,
        fontweight="bold",
        color="#D14D49",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="#D14D49",
            alpha=0.8,
        ),
    )

    sns.despine()
    ax.legend(title="Club / Año", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax
