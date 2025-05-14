import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Graficas importadas
from utils.graficos import grafico_sobre_medicion, evolucion_promedio

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
    ruta = f"app/data/times/datos_Clean_{anio}.csv"
    df = pd.read_csv(ruta, parse_dates=['DateTime'])
    return df

anio = st.selectbox("Selecciona el año", [2021, 2022, 2023, 2024, 2025])
df = cargar_datos_por_anio(anio)

# ============================
# 🎛️ Controles interactivos
# ============================

# Filtrar por año
df_anio = df[df['Anio'] == anio]

estaciones = sorted(df_anio['Estacion'].unique())
estaciones_seleccionadas = st.multiselect("Selecciona las estaciones", estaciones, default=estaciones)

contaminantes = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
contaminante = st.selectbox("Selecciona el contaminante", contaminantes)

# Rango de fechas basado en año seleccionado
min_fecha = df_anio['DateTime'].min().date()
max_fecha = df_anio['DateTime'].max().date()
rango_fechas = st.slider("Selecciona el rango de fechas", min_value=min_fecha, max_value=max_fecha, value=(min_fecha, max_fecha))


# Modo de visualización [Por hora, Por día, Por mes, Comparar años]

modo = st.radio(
    "¿Cómo quieres visualizar los datos?",
    ["Por hora", "Por día", "Por mes", "Comparar años"],
    horizontal=True
)

if df.empty:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
else:
    if modo == "Por hora":
        st.markdown(f"### 🕒 Promedio horario de `{contaminante}`")

    elif modo == "Por día":
        st.markdown(f"### 📅 Promedio diario de `{contaminante}`")

    elif modo == "Por mes":
        st.markdown(f"### 🗓️ Promedio mensual de `{contaminante}`")
        # df['Mes'] = df['DateTime'].dt.month
        # resumen = df.groupby(['Mes', 'Estacion'])[contaminante].mean().unstack()

        # fig, ax = plt.subplots(figsize=(10, 5))
        # resumen.plot(kind='bar', ax=ax)
        # ax.set_title(f"{contaminante} promedio mensual por estación")
        # ax.set_ylabel(f"{contaminante} (ppm)")
        # ax.set_xlabel("Mes")
        # ax.grid(True, linestyle='--', alpha=0.4)
        # st.pyplot(fig)

    elif modo == "Comparar años":
        st.markdown(f"### 📊 Comparación de `{contaminante}` entre años")

        # anios_comparar = st.multiselect("Selecciona los años a comparar", [2021, 2022, 2023, 2024, 2025], default=[anio])

        # fig, ax = plt.subplots(figsize=(10, 5))
        # for a in anios_comparar:
        #     df_a = cargar_datos_por_anio(a)
        #     df_a = df_a[
        #         (df_a['Estacion'].isin(estaciones_seleccionadas)) &
        #         (df_a['DateTime'].dt.date >= rango_fechas[0]) &
        #         (df_a['DateTime'].dt.date <= rango_fechas[1])
        #     ]
        #     df_a['Fecha'] = df_a['DateTime'].dt.date
        #     promedio = df_a.groupby('Fecha')[contaminante].mean()
        #     ax.plot(promedio.index, promedio.values, label=str(a))

        # ax.set_title(f"Comparación de {contaminante} entre años")
        # ax.set_ylabel(f"{contaminante} (ppm)")
        # ax.set_xlabel("Fecha")
        # ax.grid(True, linestyle='--', alpha=0.4)
        # ax.legend()
        # st.pyplot(fig)




# ============================
# 📥 Opción de exportación
# ============================
st.download_button(
    label="⬇️ Descargar datos filtrados",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"historico_{anio}_{contaminante}.csv",
    mime='text/csv'
)
