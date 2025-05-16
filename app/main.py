import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos_dia_anterior
from utils.graficos import concentracion_horaria_heatmap, concentracion_horaria
from utils.mapa import mapa
from utils.levels_contaminacion import menu_contaminante

# Configuración de la página
st.set_page_config(
    page_title="Calidad del Aire Puebla",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =======================
# 🧠 Encabezado
# =======================
st.title("💨 Calidad del Aire en Puebla - Día Anterior")
st.caption("Último análisis con datos por estación, contaminante y hora. Incluye visualización y evaluación diaria.")

# ========================
# 📥 Carga y limpieza de datos
# ========================
df = cargar_datos_dia_anterior()
df = df.drop(columns=['O3_8hrs'])

# ========================
# 📌 Estadísticas por estación
# ========================
media_por_estacion = df.groupby('Estacion').mean()
media_por_estacion = media_por_estacion.drop(columns=['DateTime', 'Anio', 'Mes', 'Dia', 'Hora'])

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
        cols = st.columns(3)
        for i, contaminante in enumerate(media_por_estacion.columns):
            valor = media_por_estacion.loc[estacion, contaminante]

            if pd.isna(valor):
                cols[i % 3].info(f"**{contaminante}**: No se obtuvo información.")
                continue

            calidad, nivel, color = menu_contaminante(contaminante, valor)
            texto = f"**{contaminante}**: {calidad} (Nivel {nivel})\n\n`{valor:.3f} ppm`"

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
# 🔍 Contaminante más crítico automáticamente
# ========================
contaminantes = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
contaminante_default = max(contaminantes, key=lambda c: df[c].mean())
selection = st.selectbox("🧪 Selecciona el contaminante a analizar:", contaminantes, index=contaminantes.index(contaminante_default))

# ========================
# 📊 Métricas generales
# ========================
st.markdown("### 📊 Métricas generales del día")
media_general = df[selection].mean()
maximo = df[selection].max()
minimo = df[selection].min()

col_a, col_b, col_c = st.columns(3)
col_a.metric("Promedio general", f"{media_general:.3f} ppm")
col_b.metric("Máximo diario", f"{maximo:.3f} ppm")
col_c.metric("Mínimo diario", f"{minimo:.3f} ppm")

# ========================
# 📊 Comparación + Mapa en columnas
# ========================
st.markdown("### 🌡️ Comparación Horaria y Mapa Interactivo")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 🔍 Punto más crítico del día")

    try:
        df_valido = df.dropna(subset=[selection])
        idx_max = df_valido[selection].idxmax()
        fila_max = df_valido.loc[idx_max]

        estacion_critica = fila_max['Estacion']
        hora_critica = int(fila_max['Hora'])
        valor_max = fila_max[selection]
        calidad, _, _ = menu_contaminante(selection, valor_max)

        color_emojis = {
            "Buena": "🟢",
            "Aceptable": "🟡",
            "Mala": "🔴",
            "Muy Mala": "🟥",
            "Extremadamente Mala": "🟣"
        }

        st.info(
            f"{color_emojis.get(calidad, '')} Concentración más alta de **{selection}**: "
            f"**{valor_max:.3f} ppm** en **{estacion_critica}** a las **{hora_critica}:00 hrs** "
            f"— _Calidad: **{calidad}**_"
        )
    except:
        st.warning("No se pudo calcular el punto más crítico por falta de datos.")

    tipo_grafico = st.radio(
        "📊 Tipo de gráfico a mostrar:",
        ['Gráfico de líneas', 'Mapa de calor'],
        horizontal=True
    )

    if tipo_grafico == 'Gráfico de líneas':
        st.markdown(f"#### 📈 Evolución horaria de `{selection}`")
        concentracion_horaria(df, selection)
    else:
        st.markdown(f"#### 🔥 Mapa de calor de `{selection}`")
        concentracion_horaria_heatmap(df, selection)

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
