import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# =======================================
# PREGUNTA 1.-¿Cómo evolucionó la participación y el peso económico
#  de las casas de apuestas respecto a los sponsors tradicionales 
#  (bancos, financieras, etc.) entre 2021 y 2026?


def analisis_patrocinio_vs_tradicionales(df, guardar_path=None, mostrar=True):
    """Grafica el volumen de patrocinios tradicionales y de apuestas por año."""
    df_volumen = (
        df.groupby("año")[
            [
                "ingreso_sponsor_bet",
                "patrocinio_tradicional",
                "patrocinio_uniforme",
            ]
        ]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(
        df_volumen["año"],
        df_volumen["patrocinio_tradicional"],
        label="Sponsors Tradicionales (Bancos, Financieras, etc.)",
        color="#1F4E79",
        width=0.55,
    )
    ax.bar(
        df_volumen["año"],
        df_volumen["ingreso_sponsor_bet"],
        bottom=df_volumen["patrocinio_tradicional"],
        label="Casas de Apuestas (Bets)",
        color="#D14D49",
        width=0.55,
    )

    ax.set_title(
        "Observación 1: Explosión del Patrocinio de Bets vs. Tradicionales\n"
        "Evolución del Volumen Total (R$ Millones, 2019–2025)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_xlabel("Año", fontsize=11, fontweight="bold")
    ax.set_ylabel("Patrocinio Total (R$ Millones)", fontsize=11, fontweight="bold")
    ax.set_xticks(df_volumen["año"])
    ax.set_ylim(0, df_volumen["patrocinio_uniforme"].max() * 1.2)

    for _, row in df_volumen.iterrows():
        ax.text(
            row["año"],
            row["patrocinio_uniforme"] + 25,
            f"R$ {row['patrocinio_uniforme']:,.1f}M",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10,
            color="#111111",
        )
        if row["ingreso_sponsor_bet"] > 40:
            ax.text(
                row["año"],
                row["patrocinio_tradicional"] + row["ingreso_sponsor_bet"] / 2,
                f"R$ {row['ingreso_sponsor_bet']:,.1f}M",
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
                fontsize=9,
            )

    sns.despine()
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax


def analisis_participacion_bets_vs_tradicionales(
    df, guardar_path=None, mostrar=True
):
    """Grafica la participación de mercado de bets y sponsors tradicionales."""
    evolucion = (
        df.groupby("año")[
            [
                "ingreso_sponsor_bet",
                "patrocinio_tradicional",
                "patrocinio_uniforme",
            ]
        ]
        .sum()
        .reset_index()
    )
    evolucion["share_bets_%"] = (
        evolucion["ingreso_sponsor_bet"] / evolucion["patrocinio_uniforme"]
    ) * 100
    evolucion["share_tradicional_%"] = (
        evolucion["patrocinio_tradicional"] / evolucion["patrocinio_uniforme"]
    ) * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        evolucion["año"],
        evolucion["share_bets_%"],
        marker="o",
        linewidth=3,
        markersize=8,
        color="#D9534F",
        label="Casas de Apuestas (Bets)",
    )
    ax.plot(
        evolucion["año"],
        evolucion["share_tradicional_%"],
        marker="s",
        linewidth=3,
        markersize=8,
        color="#1F4E79",
        label="Sponsors Tradicionales",
    )
    ax.fill_between(
        evolucion["año"], evolucion["share_bets_%"], color="#D9534F", alpha=0.15
    )
    ax.fill_between(
        evolucion["año"],
        evolucion["share_tradicional_%"],
        color="#1F4E79",
        alpha=0.1,
    )
    ax.axvline(x=2024, color="#888888", linestyle="--", linewidth=1.5, alpha=0.7)
    ax.text(
        2024.05,
        50,
        "Punto de Inflexión (2024)",
        fontsize=9.5,
        fontstyle="italic",
        color="#333333",
        va="center",
    )

    ax.set_title(
        "Observación 2: Punto de Inflexión y Cambio de Mando\n"
        "Share de Mercado (%): Casas de Apuestas vs. Sponsors Tradicionales "
        "(2019–2025)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_xlabel("Año", fontsize=11, fontweight="bold")
    ax.set_ylabel("Participación de Mercado (%)", fontsize=11, fontweight="bold")
    ax.set_xticks(evolucion["año"])
    ax.set_ylim(0, 110)

    sns.despine()
    ax.legend(loc="center left", frameon=True, facecolor="white", framealpha=0.9)
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax


def analisis_desplazamiento(df, guardar_path=None, mostrar=True):
    """Grafica los roles de las casas de apuestas en las camisetas por año."""
    roles = (
        df.groupby(["año", "tipo_presencia_bet"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    categorias = ["Sin Bet", "Secundario / Transición", "Máster Principal"]
    for categoria in categorias:
        if categoria not in roles.columns:
            roles[categoria] = 0

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(
        roles["año"],
        roles["Sin Bet"],
        label="Sin Presencia de Bet",
        color="#7F7F7F",
        width=0.55,
    )
    ax.bar(
        roles["año"],
        roles["Secundario / Transición"],
        bottom=roles["Sin Bet"],
        label="Secundario / Transición",
        color="#F0AD4E",
        width=0.55,
    )
    ax.bar(
        roles["año"],
        roles["Máster Principal"],
        bottom=roles["Sin Bet"] + roles["Secundario / Transición"],
        label="Máster Principal (Pecho)",
        color="#D9534F",
        width=0.55,
    )

    ax.set_title(
        "Observación 3: Desplazamiento Directo en el Pecho de la Camiseta\n"
        "Número de Clubes por Tipo de Presencia (2019–2025)",
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=15,
    )
    ax.set_xlabel("Año", fontsize=11, fontweight="bold")
    ax.set_ylabel("Número de Clubes", fontsize=11, fontweight="bold")
    ax.set_xticks(roles["año"])
    ax.set_ylim(0, 10.5)

    sns.despine()
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
    fig.tight_layout()

    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax

# Cordero Martinez, Fiorella
# ========================================

# PREGUNTA 2.-