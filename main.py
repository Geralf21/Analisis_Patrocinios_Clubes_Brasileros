from pathlib import Path

import pandas as pd

from resultados.graficos import (
    analisis_desplazamiento,
    analisis_participacion_bets_vs_tradicionales,
    analisis_patrocinio_vs_tradicionales,
)


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_ORIGEN = BASE_DIR / "BaseDatos" / "balances_y_sponsors_2019_2025.csv"
DIRECTORIO_RESULTADOS = BASE_DIR / "resultados"

COLUMNAS = [
    "club",
    "año",
    "ingreso_operativo_bruto",
    "ingreso_recurrente",
    "ingreso_comercial_total",
    "patrocinio_uniforme",
    "sponsor_bet_principal",
    "tipo_presencia_bet",
    "ingreso_sponsor_bet",
    "contrato_bet_anualizado",
    "pasivo_derechos_imagen",
    "pasivo_circulante",
    "superavit_o_deficit",
]

DATOS_CORINTHIANS = [
    ["Corinthians", 2019, 426.40, 350.00, 73.30, 50.00, "Marjosports", "Secundario / Transición", 4.50, 4.50, 48.50, 967.30, -195.50],
    ["Corinthians", 2020, 438.20, 360.00, 71.10, 52.00, "Galera.bet", "Secundario / Transición", 8.00, 8.00, 121.40, 847.20, -123.30],
    ["Corinthians", 2021, 447.80, 390.00, 126.30, 84.00, "Galera.bet", "Secundario / Transición", 8.00, 8.00, 47.20, 962.30, 5.70],
    ["Corinthians", 2022, 687.00, 633.00, 93.60, 70.00, "Galera / Pixbet", "Secundario / Transición", 15.00, 15.00, 66.70, 824.30, 15.40],
    ["Corinthians", 2023, 872.40, 686.00, 128.60, 95.00, "Pixbet / Galera", "Secundario / Transición", 20.00, 20.00, 114.00, 1072.30, 1.20],
    ["Corinthians", 2024, 1114.90, 777.00, 264.50, 217.40, "VaiDeBet / Esportes da Sorte", "Máster Principal", 111.50, 111.50, 115.00, 1250.00, -9.50],
    ["Corinthians", 2025, 971.00, 787.00, 252.20, 124.80, "Esportes da Sorte / Viva da Sorte", "Máster Principal", 103.00, 103.00, 120.00, 979.80, 139.00],
]

DATOS_INTERNACIONAL = [
    ["Internacional", 2019, 441.34, 362.00, 55.20, 39.72, "Nenhum", "Sin Bet", 0.00, 0.00, 18.50, 474.05, -3.02],
    ["Internacional", 2020, 281.00, 225.00, 42.10, 29.60, "Betsul", "Secundario / Transición", 2.00, 2.00, 21.30, 463.32, -91.89],
    ["Internacional", 2021, 380.00, 310.00, 48.50, 32.30, "Betsul", "Secundario / Transición", 3.00, 3.00, 19.80, 475.53, 0.79],
    ["Internacional", 2022, 466.00, 355.00, 58.20, 38.47, "EstrelaBet", "Secundario / Transición", 5.00, 5.00, 22.40, 457.45, 1.03],
    ["Internacional", 2023, 553.00, 415.00, 88.50, 57.39, "EstrelaBet", "Secundario / Transición", 12.00, 12.00, 23.80, 478.47, 170.38],
    ["Internacional", 2024, 510.00, 398.00, 95.00, 62.65, "EstrelaBet", "Secundario / Transición", 15.00, 15.00, 23.84, 610.71, -34.50],
    ["Internacional", 2025, 682.00, 469.89, 245.00, 83.04, "EstrelaBet / Betano", "Máster Principal", 35.00, 35.00, 26.17, 606.92, 8.97],
]


def cargar_datos():
    df = pd.read_csv(ARCHIVO_ORIGEN, encoding="utf-8")
    df.columns = df.columns.str.strip()

    df_base = df[~df["club"].isin(["Corinthians", "Internacional"])].copy()
    df_explicitos = pd.DataFrame(
        DATOS_CORINTHIANS + DATOS_INTERNACIONAL, columns=COLUMNAS
    )
    df_completo = pd.concat([df_base, df_explicitos], ignore_index=True)

    df_completo["año"] = pd.to_numeric(
        df_completo["año"], errors="coerce"
    ).astype("Int64")
    columnas_numericas = [
        "ingreso_operativo_bruto",
        "ingreso_recurrente",
        "ingreso_comercial_total",
        "patrocinio_uniforme",
        "ingreso_sponsor_bet",
        "contrato_bet_anualizado",
        "pasivo_derechos_imagen",
        "pasivo_circulante",
        "superavit_o_deficit",
    ]
    for columna in columnas_numericas:
        df_completo[columna] = pd.to_numeric(
            df_completo[columna], errors="coerce"
        )

    df_completo["patrocinio_tradicional"] = (
        df_completo["patrocinio_uniforme"] - df_completo["ingreso_sponsor_bet"]
    )
    return df_completo


def main():
    print("Iniciando análisis de Sponsors (Bets vs Tradicionales)...")
    df = cargar_datos()
    DIRECTORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        DIRECTORIO_RESULTADOS / "balance_sponsor_completo.csv",
        index=False,
        encoding="utf-8",
    )
    print(f"Base de datos integrada: {len(df)} filas.")

    graficos = [
        (
            "Gráfico 1: Volumen de Patrocinio",
            analisis_patrocinio_vs_tradicionales,
            "grafico_volumen_patrocinio.png",
        ),
        (
            "Gráfico 2: Participación de Mercado (Share %)",
            analisis_participacion_bets_vs_tradicionales,
            "grafico_share_mercado.png",
        ),
        (
            "Gráfico 3: Desplazamiento y Roles en la camiseta",
            analisis_desplazamiento,
            "grafico_roles_desplazamiento.png",
        ),
    ]
    for titulo, funcion, nombre_archivo in graficos:
        print(f"Generando {titulo}...")
        funcion(
            df,
            guardar_path=DIRECTORIO_RESULTADOS / nombre_archivo,
            mostrar=True,
        )

    print(f"Análisis finalizado. Resultados guardados en: {DIRECTORIO_RESULTADOS}")


if __name__ == "__main__":
    main()
