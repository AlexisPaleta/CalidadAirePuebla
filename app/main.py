import streamlit as st
from utils.data_loader import cargar_datos_dia_anterior
from utils.graficos import concentracion_horaria_heatmap, concentracion_horaria
from utils.mapa import mapa
from utils.levels_contaminacion import menu_contaminante  # Para clasificar cada contaminante

import pandas as pd

# Configuración general de la página
st.set_page_config(
    page_title="Calidad del Aire Puebla",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =======================
# 🧠 Título & Introducción
# =======================
st.title("📊 Análisis de Calidad del Aire en Puebla (Día Anterior)")
st.markdown(
    """
    Visualiza la calidad del aire registrada en la ciudad de Puebla durante el día anterior.
    Revisa concentraciones horarias por estación, un mapa interactivo de contaminación y
    un resumen general del estado del aire.
    """
)

# ========================
# 📥 Carga y limpieza de datos
# ========================
df = cargar_datos_dia_anterior()
df = df.drop(columns=['O3_8hrs'])

# ========================
# 📌 Estadísticas por estación (promedios)
# ========================
media_por_estacion = df.groupby('Estacion').mean()
media_por_estacion = media_por_estacion.drop(columns=['DateTime', 'Anio', 'Mes', 'Dia', 'Hora'])

# Mostrar resumen en expansor
st.markdown("### 🧾 Promedio diario por estación")
with st.expander("🔍 Ver tabla de promedios por estación"):
    st.dataframe(media_por_estacion, use_container_width=True)

# ========================
# 🌤️ Evaluación por estación y contaminante
# ========================
st.markdown("### 🌤️ Evaluación por estación y contaminante")

switcher = {
    'santa': 'Agua Santa',
    'bine': 'Benemérito Instituto Normal del Estado (BINE)',
    'ninfas': 'Las Ninfas',
    'utp': 'Universidad Tecnológica de Puebla (UTP)',
    'vel': 'Velódromo'
}

try:
    for estacion in media_por_estacion.index:
        st.markdown(f"#### 🏭 Estación: `{switcher.get(estacion)}`")
        cols = st.columns(3)  # Mostrar tarjetas en filas de 3

        for i, contaminante in enumerate(media_por_estacion.columns):
            valor = media_por_estacion.loc[estacion, contaminante]

            if pd.isna(valor):
                texto = f"**{contaminante}**: No se obtuvo información."
                cols[i % 3].info(texto)
                continue

            calidad, nivel, color = menu_contaminante(contaminante, valor)

            texto = f"**{contaminante}**: {calidad} (Nivel {nivel})\n\n`{valor:.3f} ppm`"

            # Tarjetas con color según calidad
            if calidad == "Buena":
                cols[i % 3].success(texto)
            elif calidad == "Aceptable":
                cols[i % 3].warning(texto)
            else:
                cols[i % 3].error(texto)

        st.divider()
except Exception as e:
    st.error("⚠️ No se pudo generar el resumen por estación.")
    st.text(str(e))

# ========================
# 📊 Comparación + Mapa en columnas
# ========================
st.markdown("### 🌡️ Comparación Horaria y Mapa Interactivo")

options = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
selection = st.selectbox("🧪 Selecciona el contaminante a analizar:", options)

col1, col2 = st.columns([1, 1])  # Mismo tamaño

# === Columna izquierda: gráfica + resumen
with col1:
    st.markdown("#### 🔍 Punto más crítico del día")

    try:
        df_valido = df.dropna(subset=[selection])
        idx_max = df_valido[selection].idxmax()
        fila_max = df_valido.loc[idx_max]

        estacion_critica = fila_max['Estacion']
        hora_critica = int(fila_max['Hora'])
        valor_max = fila_max[selection]

        st.info(
            f"La concentración más alta de **{selection}** se registró en "
            f"**{estacion_critica}** a las **{hora_critica}:00 hrs** con un valor de "
            f"**{valor_max:.3f} ppm**."
        )
    except:
        st.warning("No se pudo calcular el punto más crítico por falta de datos.")

    grafico = st.radio(
        "📊 Tipo de gráfico a mostrar:",
        ['Gráfico de líneas', 'Mapa de calor'],
        horizontal=True
    )

    if grafico == 'Gráfico de líneas':
        st.markdown(f"#### 📈 Evolución horaria de `{selection}`")
        concentracion_horaria(df, selection)
    else:
        st.markdown(f"#### 🔥 Mapa de calor de `{selection}`")
        concentracion_horaria_heatmap(df, selection)

# === Columna derecha: mapa
with col2:
    st.markdown(f"#### 🗺️ Distribución por estación para `{selection}`")
    mapa(media_por_estacion, selection)

# ========================
# 📎 Información técnica y descarga
# ========================
with st.expander("📎 Ver registros sin procesar"):
    st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar datos diarios en CSV",
    data=csv,
    file_name="datos_dia_anterior.csv",
    mime="text/csv"
)
