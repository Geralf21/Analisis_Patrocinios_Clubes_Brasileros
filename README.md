# Análisis de patrocinios de clubes del Brasileirão

Proyecto de análisis del impacto económico y la evolución de los patrocinios de casas de apuestas en clubes del fútbol brasileño. Reúne datos financieros, deportivos y de patrocinio para generar tablas e informes gráficos de las preguntas 1 a 5 del trabajo práctico.

## Contenido

- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Datos utilizados](#datos-utilizados)
- [Análisis incluidos](#análisis-incluidos)
- [Resultados](#resultados)
- [Criterios y limitaciones](#criterios-y-limitaciones)

## Requisitos

- Python 3.11 o superior.
- Dependencias listadas en [`requerimientos.txt`](./requerimientos.txt).

## Instalación y ejecución

Desde una terminal, ubicarse en la carpeta raíz del repositorio y crear un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requerimientos.txt
python main.py
```

En Linux o macOS, usar los comandos equivalentes:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requerimientos.txt
python main.py
```

El programa lee los CSV desde `BaseDatos/`, genera las tablas de apoyo y guarda los gráficos y la base financiera integrada en `resultados/`. Las ventanas de los gráficos pueden mostrarse durante la ejecución; para ejecutarlo sin interfaz gráfica, se puede configurar un backend no interactivo de Matplotlib.

## Estructura del proyecto

```text
.
├── BaseDatos/
│   ├── balances_y_sponsors_2019_2025.csv
│   ├── brasileirao_futbolistico.csv
│   ├── patrocinios_brsileirao.csv
│   └── informes financieros 2019-2025/
├── notebooks/
│   ├── TP_Pregunta_1.ipynb
│   ├── TP_Pregunta_2.ipynb
│   ├── TP pregunta_3.ipynb
│   ├── TP_pregunta_4.ipynb
│   └── TP_pregunta_5*.ipynb
├── resultados/
│   ├── graficos.py
│   ├── graficosp2.py
│   ├── graficosp3.py
│   └── graficosp4.py
├── main.py
└── requerimientos.txt
```

- `main.py` coordina la carga de datos, los análisis y la generación de resultados.
- `resultados/graficos.py` contiene los gráficos generales y los de la pregunta 5.
- `resultados/graficosp2.py`, `graficosp3.py` y `graficosp4.py` contienen los cálculos y gráficos específicos de las preguntas 2, 3 y 4.
- `notebooks/` conserva el desarrollo exploratorio de cada pregunta.
- `BaseDatos/informes financieros 2019-2025/` reúne los informes financieros consultados.

## Datos utilizados

| Archivo | Contenido |
|---|---|
| `BaseDatos/balances_y_sponsors_2019_2025.csv` | Ingresos, patrocinios, pasivos y resultados financieros por club y temporada. |
| `BaseDatos/patrocinios_brsileirao.csv` | Patrocinador máster, monto, rubro, clasificación de apuestas e hinchas para 2023 y 2024. |
| `BaseDatos/brasileirao_futbolistico.csv` | Patrocinios, posiciones, puntos, transferencias y competición internacional para 2021–2026. |
| `BaseDatos/informes financieros 2019-2025/` | Documentación financiera utilizada como fuente de datos. |

Los análisis automatizados leen los CSV locales. La carga del balance financiero de `main.py` cuenta además con una URL de respaldo si no encuentra el archivo local.

## Análisis incluidos

Al ejecutar `python main.py` se realizan los siguientes análisis:

1. **Evolución y participación de los patrocinios:** compara los ingresos de casas de apuestas con patrocinios tradicionales y muestra el cambio de roles en las camisetas.
2. **Patrocinios en 2023 y 2024:** compara los montos por club y tipo de patrocinador; calcula variaciones de totales, brecha entre montos, promedio de patrocinios de apuestas y correlación con la cantidad de hinchas.
3. **Desempeño deportivo y financiero:** compara ingresos de patrocinio de apuestas con gasto en fichajes y saldo neto de transferencias; resume puntos y posiciones por tipo de patrocinador.
4. **Competiciones internacionales:** estima premios CONMEBOL, compara ingresos medios por competición y grafica la relación entre patrocinios y premios antes de 2023 y desde 2023.
5. **Dependencia financiera de las apuestas:** calcula la proporción de ingresos de apuestas sobre ingresos comerciales, compara el resultado real con un escenario sin esos ingresos y analiza 2019 frente a 2025.

## Resultados

Los gráficos se generan en `resultados/`:

- Pregunta 1: `grafico_volumen_patrocinio.png`, `grafico_share_mercado.png`, `grafico_roles_desplazamiento.png`.
- Pregunta 2: `patrocinios_2023_2024.png`, `bets_vs_hinchada_2024.png`.
- Pregunta 3: `p3_apuestas_vs_fichajes_por_periodo.png`, `p3_apuestas_vs_transferencias_netas.png`, `p3_transferencias_netas_y_gasto.png`, `p3_posicion_promedio.png`.
- Pregunta 4: `p4_ingresos_promedio_por_competicion.png`, `p4_sponsors_vs_premios_por_periodo.png`.
- Pregunta 5: `dependencia_bets_2025.png`, `resultado_sin_bets_2025.png`, `caida_superavit_lollipop_2025.png`, `tipo_presencia_por_anio.png`, `superavit_2019.png`, `dependencia_2019_vs_2025.png`.

También se crea o actualiza `resultados/balance_sponsor_completo.csv`, con los registros financieros integrados utilizados por los primeros gráficos.

## Criterios y limitaciones

- Los resultados dependen de la cobertura y calidad de los CSV incluidos en `BaseDatos/`.
- En el análisis de la pregunta 3, la identificación de patrocinadores de apuestas se basa en palabras clave del nombre del patrocinador.
- Los premios CONMEBOL de la pregunta 4 son estimaciones definidas mediante reglas por club, año y competición; la conversión utilizada es de 5 BRL por USD. La comparación es descriptiva y no constituye una prueba estadística de significancia.
- El escenario “sin bets” de la pregunta 5 resta los ingresos de apuestas del resultado del ejercicio. Es una simulación contable simplificada, no una predicción de cómo reaccionaría un club ante una restricción real.
- `TP_pregunta_5_v2.ipynb` explora además escenarios de recorte del 25 % y 50 %; esos escenarios no forman parte del flujo actual de `main.py`.
