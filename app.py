import streamlit as st
import pandas as pd

#pagina vibecodeada que nos ayudara a organizarnos 
st.set_page_config(page_title="Tablero TP Brasileirão", page_icon="⚽", layout="wide")

st.title("⚽ Tablero de Gestión: TP Brasileirão & Casas de Apuestas")
st.caption("FCE UBA - Elección de Minipreguntas y Seguimiento de Trabajo Grupal")

# Preguntas base
PREGUNTAS_BASE = [
    {
        "id": 1,
        "pregunta": "1. Evolución temporal de sponsors (Casas de Apuestas vs. Tradicionales)",
        "entregable": "Gráfico de líneas/evolución temporal del volumen de dinero por año."
    },
    {
        "id": 2,
        "pregunta": "2. Concentración y brecha entre clubes (2021 vs. 2026)",
        "entregable": "Gráfico de barras comparativo por club y salto porcentual."
    },
    {
        "id": 3,
        "pregunta": "3. Relación sponsor vs. Rendimiento deportivo (Posición en Liga)",
        "entregable": "Gráfico de dispersión (Scatter plot) de Ingresos vs. Posición."
    },
    {
        "id": 4,
        "pregunta": "4. Impacto en clasificación a Copas Internacionales",
        "entregable": "Groupby por competición y gráfico de cajas (Boxplot)."
    },
    {
        "id": 5,
        "pregunta": "5. Riesgo/Simulación por regulación estatal (Ban de Lula)",
        "entregable": "Columna derivada y cálculo de pérdida potencial por club."
    }
]

# Estado inicial en memoria
if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {
            "id": item["id"],
            "pregunta": item["pregunta"],
            "entregable": item["entregable"],
            "integrante": "Sin asignar",
            "estado": "Pendiente",
            "descripcion": ""
        }
        for item in PREGUNTAS_BASE
    ]

tab_general, tab_elegir = st.tabs(["📌 Tablero General", "✍️ Elegir / Actualizar Mi Pregunta"])

# --- TAB 1: VISUALIZACIÓN ---
with tab_general:
    st.subheader("Estado de asignación de minipreguntas")
    
    # Progreso
    asignadas = len([t for t in st.session_state.tareas if t["integrante"] != "Sin asignar"])
    st.progress(asignadas / 5)
    st.write(f"**Preguntas Elegidas:** {asignadas} / 5")
    
    st.markdown("---")
    
    for t in st.session_state.tareas:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {t['pregunta']}")
            st.write(f"**Entregable:** {t['entregable']}")
            if t['descripcion']:
                st.info(f"**Hallazgos en Python:** {t['descripcion']}")
        with col2:
            st.write(f"**Integrante:** `{t['integrante']}`")
            st.write(f"**Estado:** `{t['estado']}`")
        st.markdown("---")

# --- TAB 2: SELECCIÓN Y EDICIÓN ---
with tab_elegir:
    st.subheader("Elegí tu minipregunta o actualizá tu avance")
    
    opciones = [f"{t['id']}. {t['pregunta']}" for t in st.session_state.tareas]
    seleccion = st.selectbox("Seleccioná la pregunta sobre la que vas a trabajar:", opciones)
    
    idx_sel = int(seleccion.split(".")[0]) - 1
    tarea_actual = st.session_state.tareas[idx_sel]
    
    with st.form("form_asignacion"):
        nombre = st.text_input("Tu Nombre y Apellido:", value="" if tarea_actual["integrante"] == "Sin asignar" else tarea_actual["integrante"])
        estado = st.selectbox("Estado del trabajo:", ["Pendiente", "En Proceso", "Completado"], index=["Pendiente", "En Proceso", "Completado"].index(tarea_actual["estado"]))
        descripcion = st.text_area("Descripción de tus avances / hallazgos en Pandas:", value=tarea_actual["descripcion"], placeholder="Ejemplo: Armé el groupby por competición internacional y generé el boxplot. El promedio de ingresos para Libertadores fue de 80M BRL...")
        
        btn_guardar = st.form_submit_button("Guardar Mi Selección / Avance")
        
        if btn_guardar:
            if not nombre.strip():
                st.error("Por favor ingresá tu nombre antes de guardar.")
            else:
                st.session_state.tareas[idx_sel]["integrante"] = nombre
                st.session_state.tareas[idx_sel]["estado"] = estado
                st.session_state.tareas[idx_sel]["descripcion"] = descripcion
                st.success(f"¡Guardado con éxito! Elegiste la pregunta {idx_sel + 1}.")
                st.rerun()
