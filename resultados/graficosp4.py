import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


COMPETICIONES_P4 = ["Libertadores", "Sudamericana", "Ninguna"]
COLUMNAS_REQUERIDAS_P4 = {
    "club",
    "año",
    "competicion_internacional",
    "ingresos_sponsors_millones_BRL",
}


def preparar_datos_p4(df):
    """Calcula los premios CONMEBOL estimados y el ingreso total internacional."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    faltantes = COLUMNAS_REQUERIDAS_P4.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas para el análisis P4: "
            + ", ".join(sorted(faltantes))
        )

    df["año"] = pd.to_numeric(df["año"], errors="coerce")
    df["ingresos_sponsors_millones_BRL"] = pd.to_numeric(
        df["ingresos_sponsors_millones_BRL"], errors="coerce"
    )
    if df["año"].isna().any():
        raise ValueError("Hay años vacíos o inválidos en la base futbolística.")
    if df["ingresos_sponsors_millones_BRL"].isna().any():
        raise ValueError("Hay ingresos por sponsors vacíos o inválidos en P4.")
    if df["competicion_internacional"].isna().any():
        raise ValueError("Hay competiciones internacionales sin clasificar en P4.")

    premios = df.apply(calcular_premios_conmebol, axis=1)
    if premios.isna().any():
        raise ValueError("No se pudieron calcular premios CONMEBOL para todas las filas.")

    df["premios_conmebol_millones_USD"] = premios
    df["premios_conmebol_millones_BRL"] = premios * 5.0
    df["ingreso_total_internacional_BRL"] = (
        df["ingresos_sponsors_millones_BRL"]
        + df["premios_conmebol_millones_BRL"]
    )
    return df


def calcular_premios_conmebol(row):
    """Estima premios CONMEBOL en millones de USD según competición, club y año."""
    competicion = row["competicion_internacional"]
    club = row["club"]
    año = int(row["año"])

    if competicion == "Ninguna":
        return 0.0
    if competicion == "Sudamericana":
        if (
            (club == "Red Bull Bragantino" and año == 2021)
            or (club == "Sao Paulo" and año == 2022)
            or (club == "Fortaleza" and año == 2023)
        ):
            return 5.5
        if club in [
            "Athletico-PR",
            "Corinthians",
            "Atlético Goianiense",
            "Ceará",
            "America-MG",
        ]:
            return 2.8
        return 1.2
    if competicion == "Libertadores":
        if (
            (club == "Palmeiras" and año == 2021)
            or (club == "Flamengo" and año == 2022)
            or (club == "Fluminense" and año == 2023)
        ):
            return 22.5
        if (
            (club == "Flamengo" and año == 2021)
            or (club == "Athletico-PR" and año == 2022)
            or (club in ["Palmeiras", "Internacional"] and año == 2023)
        ):
            return 12.0
        if club in ["Atlético Mineiro", "Sao Paulo", "Corinthians", "Fluminense"]:
            return 6.5
        return 3.3
    raise ValueError(f"Competición internacional no reconocida: {competicion!r}")


def crear_resumen_competiciones_p4(df):
    """Resume ingresos medios por competición internacional."""
    columnas = {
        "competicion_internacional",
        "ingresos_sponsors_millones_BRL",
        "premios_conmebol_millones_BRL",
        "ingreso_total_internacional_BRL",
    }
    faltantes = columnas.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas para resumir los datos de P4: "
            + ", ".join(sorted(faltantes))
        )
    if not set(df["competicion_internacional"]).issubset(COMPETICIONES_P4):
        raise ValueError("La base contiene categorías de competición no reconocidas.")

    resumen = (
        df.groupby("competicion_internacional")
        .agg(
            sponsoreo_mean=("ingresos_sponsors_millones_BRL", "mean"),
            premios_mean=("premios_conmebol_millones_BRL", "mean"),
            total_mean=("ingreso_total_internacional_BRL", "mean"),
        )
        .reindex(COMPETICIONES_P4)
        .reset_index()
    )
    if resumen[["sponsoreo_mean", "premios_mean", "total_mean"]].isna().any().any():
        raise ValueError(
            "Se necesita al menos una observación para cada categoría de competición."
        )
    return resumen


def mostrar_resumen_competiciones_p4(resumen):
    """Imprime promedios descriptivos de sponsorship y premios por competición."""
    print("\n--- P4: Ingresos promedio por competición (millones de BRL) ---")
    print(
        resumen[
            [
                "competicion_internacional",
                "sponsoreo_mean",
                "premios_mean",
                "total_mean",
            ]
        ].to_string(index=False, float_format=lambda valor: f"{valor:.2f}")
    )
    print(
        "Nota: los promedios son descriptivos; no representan una prueba "
        "estadística de significancia."
    )


def grafico_ingresos_promedio_competicion_p4(
    resumen, guardar_path=None, mostrar=True
):
    """Grafica ingresos medios por sponsors y premios CONMEBOL por competición."""
    columnas = {
        "competicion_internacional",
        "sponsoreo_mean",
        "premios_mean",
        "total_mean",
    }
    faltantes = columnas.difference(resumen.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas para graficar P4: " + ", ".join(sorted(faltantes))
        )

    resumen = resumen.set_index("competicion_internacional").reindex(
        COMPETICIONES_P4
    )
    if resumen[["sponsoreo_mean", "premios_mean", "total_mean"]].isna().any().any():
        raise ValueError("El resumen de P4 tiene valores faltantes.")

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))
    posiciones = range(len(resumen))
    ax.bar(
        posiciones,
        resumen["sponsoreo_mean"],
        label="Sponsoreo comercial",
        color="#3182bd",
        width=0.45,
    )
    ax.bar(
        posiciones,
        resumen["premios_mean"],
        bottom=resumen["sponsoreo_mean"],
        label="Premios CONMEBOL",
        color="#31a354",
        width=0.45,
    )

    for posicion, (_, fila) in enumerate(resumen.iterrows()):
        sponsoreo = fila["sponsoreo_mean"]
        premios = fila["premios_mean"]
        ax.text(
            posicion,
            sponsoreo / 2,
            f"{sponsoreo:.1f}M",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=10,
        )
        if premios > 0:
            ax.text(
                posicion,
                sponsoreo + premios / 2,
                f"{premios:.1f}M",
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
                fontsize=10,
            )
        ax.text(
            posicion,
            fila["total_mean"] + 2.5,
            f"Total: {fila['total_mean']:.1f}M BRL",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10,
        )

    ax.set_xticks(list(posiciones), resumen.index)
    ax.set_title(
        "Ingreso promedio por competición (sponsoreo + premios)",
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    ax.set_ylabel("Promedio (millones de BRL)", fontsize=11)
    ax.set_xlabel("Competición internacional", fontsize=11)
    ax.legend(loc="upper right", frameon=True)
    ax.set_ylim(0, max(110, resumen["total_mean"].max() + 15))
    fig.tight_layout()
    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax


def grafico_sponsors_vs_premios_por_periodo_p4(
    df, guardar_path=None, mostrar=True
):
    """Compara ingresos por sponsors y premios antes y desde 2023."""
    columnas = {
        "año",
        "club",
        "ingresos_sponsors_millones_BRL",
        "premios_conmebol_millones_BRL",
    }
    faltantes = columnas.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas para graficar P4: " + ", ".join(sorted(faltantes))
        )

    periodos = [
        ("Pre-2023", df.loc[df["año"] < 2023]),
        ("2023 en adelante", df.loc[df["año"] >= 2023]),
    ]
    for nombre, datos in periodos:
        if datos.empty:
            raise ValueError(f"No hay observaciones para el período {nombre}.")

    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    for ax, (nombre, datos) in zip((ax1, ax2), periodos):
        sns.scatterplot(
            data=datos,
            x="ingresos_sponsors_millones_BRL",
            y="premios_conmebol_millones_BRL",
            hue="club",
            style="año",
            s=140,
            ax=ax,
        )
        ax.set_title(f"{nombre}: sponsors vs. premios CONMEBOL", fontweight="bold")
        ax.set_xlabel("Ingresos por sponsors (millones BRL)")
        ax.set_ylabel("Premios CONMEBOL (millones BRL)")
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)

    fig.tight_layout()
    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, (ax1, ax2)
