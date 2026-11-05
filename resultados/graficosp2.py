import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COLUMNAS_REQUERIDAS = {"año", "club", "monto_brl", "es_bet", "hinchas_m"}


def _validar_columnas(df):
    faltantes = COLUMNAS_REQUERIDAS.difference(df.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas para el análisis P2: "
            + ", ".join(sorted(faltantes))
        )


def _variacion_porcentual(valor_inicial, valor_final, descripcion):
    if valor_inicial == 0:
        raise ValueError(
            f"No se puede calcular la variación porcentual de {descripcion}: "
            "el valor inicial es cero."
        )
    return (valor_final - valor_inicial) / valor_inicial * 100


def calcular_metricas_patrocinio(df):
    """Calcula los indicadores de patrocinio usados en la pregunta 2."""
    _validar_columnas(df)
    metricas = {}

    for anio in (2023, 2024):
        datos_anio = df[df["año"] == anio]
        if datos_anio.empty:
            raise ValueError(f"No hay datos de patrocinios para {anio}.")

        totales = datos_anio.groupby("es_bet")["monto_brl"].sum()
        metricas[f"total_bets_{str(anio)[-2:]}"] = float(totales.get(1, 0))
        metricas[f"total_tradicionales_{str(anio)[-2:]}"] = float(
            totales.get(0, 0)
        )

        montos = datos_anio["monto_brl"].dropna()
        if montos.empty:
            raise ValueError(f"No hay montos de patrocinio válidos para {anio}.")
        metricas[f"brecha_{str(anio)[-2:]}"] = float(
            montos.max() - montos.min()
        )

        apuestas = datos_anio.loc[datos_anio["es_bet"] == 1, "monto_brl"].dropna()
        if apuestas.empty:
            raise ValueError(f"No hay patrocinios de apuestas para {anio}.")
        metricas[f"promedio_bets_{str(anio)[-2:]}"] = float(apuestas.mean())

    metricas["variacion_bets_pct"] = _variacion_porcentual(
        metricas["total_bets_23"], metricas["total_bets_24"], "bets"
    )
    metricas["variacion_tradicionales_pct"] = _variacion_porcentual(
        metricas["total_tradicionales_23"],
        metricas["total_tradicionales_24"],
        "patrocinios tradicionales",
    )
    metricas["variacion_brecha_pct"] = _variacion_porcentual(
        metricas["brecha_23"], metricas["brecha_24"], "brecha de ingresos"
    )
    metricas["variacion_promedio_bets_pct"] = _variacion_porcentual(
        metricas["promedio_bets_23"],
        metricas["promedio_bets_24"],
        "promedio de patrocinios de apuestas",
    )

    apuestas_2024 = df.loc[
        (df["año"] == 2024) & (df["es_bet"] == 1),
        ["monto_brl", "hinchas_m"],
    ].dropna()
    if len(apuestas_2024) < 2:
        raise ValueError(
            "Se necesitan al menos dos patrocinios de apuestas válidos en 2024 "
            "para calcular la correlación."
        )
    metricas["correlacion_2024"] = float(
        apuestas_2024["monto_brl"].corr(apuestas_2024["hinchas_m"])
    )
    return metricas


def mostrar_metricas_patrocinio(df):
    metricas = calcular_metricas_patrocinio(df)
    print(
        "Total destinado a sponsors de apuestas: "
        f"2023: {metricas['total_bets_23']:.1f} M | "
        f"2024: {metricas['total_bets_24']:.1f} M | "
        f"Crecimiento: {metricas['variacion_bets_pct']:+.2f}%"
    )
    print(
        "Total destinado a sponsors tradicionales: "
        f"2023: {metricas['total_tradicionales_23']:.1f} M | "
        f"2024: {metricas['total_tradicionales_24']:.1f} M | "
        f"Crecimiento: {metricas['variacion_tradicionales_pct']:+.2f}%"
    )
    print(
        f"Brecha 2023: {metricas['brecha_23']:.1f} M | "
        f"Brecha 2024: {metricas['brecha_24']:.1f} M | "
        f"Aumento: {metricas['variacion_brecha_pct']:.2f}%"
    )
    print(
        "Promedio de ingresos por sponsors de apuestas: "
        f"2023: {metricas['promedio_bets_23']:.2f} M | "
        f"2024: {metricas['promedio_bets_24']:.2f} M | "
        f"Aumento: {metricas['variacion_promedio_bets_pct']:.2f}%"
    )
    print(f"Coeficiente de Pearson (r, 2024): {metricas['correlacion_2024']:.4f}")
    return metricas


def analisis_patrocinios_por_anio(df, guardar_path=None, mostrar=True):
    """Compara los montos de patrocinio de cada club en 2023 y 2024."""
    _validar_columnas(df)
    datos_por_anio = {}
    for anio in (2023, 2024):
        datos = df[df["año"] == anio].sort_values(
            by=["es_bet", "monto_brl"], ascending=[False, False]
        )
        if datos.empty:
            raise ValueError(f"No hay datos de patrocinios para {anio}.")
        datos_por_anio[anio] = datos

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
    for ax, anio in zip((ax1, ax2), (2023, 2024)):
        datos = datos_por_anio[anio]
        colores = np.where(datos["es_bet"] == 1, "#2ecc71", "#3498db")
        ax.bar(
            datos["club"],
            datos["monto_brl"],
            color=colores,
            edgecolor="black",
            width=0.55,
        )
        ax.set_title(str(anio), fontweight="bold", fontsize=13)
        ax.grid(axis="y", linestyle=":", alpha=0.5)
        plt.setp(
            ax.get_xticklabels(),
            rotation=45,
            ha="right",
            rotation_mode="anchor",
        )

    ax1.set_ylabel("Monto anual (millones R$)", fontsize=11)
    fig.suptitle("Ingresos por patrocinio de clubes: 2023 vs. 2024")
    fig.tight_layout()
    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, (ax1, ax2)


def analisis_bets_vs_hinchada_2024(df, guardar_path=None, mostrar=True):
    """Grafica la relación entre hinchada y monto de patrocinio bet en 2024."""
    _validar_columnas(df)
    datos = df.loc[
        (df["año"] == 2024) & (df["es_bet"] == 1),
        ["club", "monto_brl", "hinchas_m"],
    ].dropna()
    if len(datos) < 2 or datos["hinchas_m"].nunique() < 2:
        raise ValueError(
            "Se necesitan al menos dos clubes con valores distintos de hinchas "
            "y datos completos de patrocinio en 2024."
        )

    metricas = calcular_metricas_patrocinio(df)
    pendiente, ordenada = np.polyfit(datos["hinchas_m"], datos["monto_brl"], 1)
    x_linea = np.linspace(datos["hinchas_m"].min(), datos["hinchas_m"].max(), 100)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(
        datos["hinchas_m"],
        datos["monto_brl"],
        color="#2ecc71",
        edgecolor="black",
        s=45,
        zorder=3,
    )
    ax.plot(
        x_linea,
        pendiente * x_linea + ordenada,
        color="#3498db",
        linestyle="--",
        label=f"Tendencia (r = {metricas['correlacion_2024']:.4f})",
    )

    offsets = {
        "Athletico-PR": (-25, -12),
        "Fortaleza": (-40, 4),
        "Bahia": (-6, 6),
        "Atlético-MG": (6, -5),
        "Cruzeiro": (6, -2),
        "Botafogo": (6, 4),
        "Flamengo": (-45, 6),
    }
    for _, fila in datos.iterrows():
        dx, dy = offsets.get(fila["club"], (6, 4))
        ax.annotate(
            fila["club"],
            (fila["hinchas_m"], fila["monto_brl"]),
            textcoords="offset points",
            xytext=(dx, dy),
            fontsize=8,
        )

    ax.set_xlabel("Hinchas (millones)", fontweight="bold")
    ax.set_ylabel("Monto anual (millones R$)", fontweight="bold")
    ax.set_title("Ingresos por sponsors de apuestas vs. hinchada (2024)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    if guardar_path:
        fig.savefig(guardar_path, dpi=200, bbox_inches="tight")
    if mostrar:
        plt.show()
    return fig, ax
