import streamlit as st
import pandas as pd
import datetime

# Graficas importadas
from utils.graficos import evolucion_promedio, concentracion_horaria, concentracion_horaria_heatmap

# Configuración de página
st.set_page_config(page_title="Histórico de Calidad del Aire", page_icon="📅", layout="wide")

st.title("📅 Análisis Histórico de Calidad del Aire")
st.markdown("""
Explora los niveles históricos de contaminantes en la ciudad de Puebla.
Puedes comparar estaciones, seleccionar rangos personalizados y observar la evolución por año.
""")

# ============================
# 📥 Carga del archivo real
# ============================
@st.cache_data
def cargar_datos_por_anio(anio):
    ruta = f"../app/data/times/datos_Clean_{anio}.csv"
    df = pd.read_csv(ruta, parse_dates=['DateTime'])
    return df




# ============================
# 🎛️ Controles interactivos
# ============================

# Control general
estaciones = {'santa', 'bine', 'ninfas', 'utp', 'vel'}
estaciones_seleccionadas = st.multiselect("Selecciona las estaciones", estaciones, default=estaciones)

# Control de mes

def mes():
    anio = st.selectbox("Selecciona el año", [2021, 2022, 2023, 2024, 2025])
    df = cargar_datos_por_anio(anio)

    # Rango de fechas basado en año seleccionado
    min_fecha = df['DateTime'].min().date()
    max_fecha = df['DateTime'].max().date()
    rango_fechas = st.slider("Selecciona el rango de fechas", min_value=min_fecha, max_value=max_fecha, value=(min_fecha, max_fecha))

    return rango_fechas, df




contaminantes = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
contaminante = st.selectbox("Selecciona el contaminante", contaminantes)



# ============================
# Menu por seleccion de periodos (dia, mes, anio, comparacion anual)
# ============================

periodo = st.radio("Selecciona el periodo", ["Dia", "Mes", "Anio", "Comparacion Anual"], horizontal=True)

if periodo == "Dia":
    st.success("Dia")

    d = st.date_input("Selecciona la fecha de interés (Recuerda que las fechas limites son 2021-fecha actual)", datetime.date(2025, 5, 13))

    df = cargar_datos_por_anio(d.year)


    st.markdown(f"### Fecha seleccionada: {d}")


    # Plot por dia seleccionado
    df_filtrado = df[
        (df['Estacion'].isin(estaciones_seleccionadas)) &
        (df['DateTime'].dt.date == d)
    ]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        concentracion_horaria(df_filtrado, contaminante)

elif periodo == "Mes":
    st.success("Mes")

    # Controles
    rango_fechas, df = mes()

elif periodo == "Anio":
    st.success("Anio")

    # Controles
    rango_fechas, df = mes()
    # ============================
    # Gráfico comparativo
    # ============================
    df_filtrado = df[
        (df['Estacion'].isin(estaciones_seleccionadas)) &
        (df['DateTime'].dt.date >= rango_fechas[0]) &
        (df['DateTime'].dt.date <= rango_fechas[1])
    ]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        st.markdown(f"### 📈 Evolución de {contaminante} entre {rango_fechas[0]} y {rango_fechas[1]}")

        # Eleccion de plots
        tipo_plot = st.selectbox("Selecciona el tipo de gráfico", ["Gráfico de líneas", "Mapa de calor", "Evolución promedio"])

        if tipo_plot == "Gráfico de líneas":
            concentracion_horaria(df_filtrado, contaminante)
        elif tipo_plot == "Mapa de calor":
            concentracion_horaria_heatmap(df_filtrado, contaminante)
        elif tipo_plot == "Evolución promedio":
            evolucion_promedio(df_filtrado, contaminante, estaciones_seleccionadas)

elif periodo == "Comparacion Anual":
    st.success("Comparacion Anual")







# ============================
# 📥 Opción de exportación
# ============================
st.download_button(
    label="⬇️ Descargar datos filtrados",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name=f"historico.csv",
    mime='text/csv'
)
