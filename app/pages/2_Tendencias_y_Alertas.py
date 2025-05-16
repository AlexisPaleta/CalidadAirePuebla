import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos_por_anio
from utils.levels_contaminacion import menu_contaminante
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tendencias y Alertas", page_icon="🔥", layout="wide")

st.title("🔥 Tendencias Recientes y Alertas de Calidad del Aire")
st.markdown("""
Monitorea rápidamente los niveles más recientes de contaminación para identificar estaciones críticas,
valores fuera de norma o tendencias ascendentes.
""")

# ============================
# Cargar datos de los últimos 7 días
# ============================
from datetime import datetime, timedelta

hoy = datetime.now().date()
ultimos_dias = [(hoy - timedelta(days=i)) for i in range(6, -1, -1)]

df_all = pd.concat([cargar_datos_por_anio(d.year) for d in ultimos_dias], ignore_index=True)
df_all['Fecha'] = df_all['DateTime'].dt.date

# ============================
# Parámetros
# ============================
contaminantes = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
contaminante = st.selectbox("Selecciona el contaminante para monitorear:", contaminantes)

# ============================
# Promedio diario por estación
# ============================
df_filtrado = df_all[df_all['Fecha'].isin(ultimos_dias)]

promedios = df_filtrado.groupby(['Fecha', 'Estacion'])[contaminante].mean().reset_index()
pivot = promedios.pivot(index='Fecha', columns='Estacion', values=contaminante)

# ============================
# Detección de alertas (valores por encima de nivel 3)
# ============================
def detectar_alertas(valor):
    if pd.isna(valor):
        return False
    _, nivel, _ = menu_contaminante(contaminante, valor)
    return nivel >= 4  # Muy mala o extremadamente mala

alertas = promedios.copy()
alertas['Alerta'] = alertas[contaminante].apply(detectar_alertas)
alertas_detectadas = alertas[alertas['Alerta'] == True]

# ============================
# Mostrar alertas
# ============================
st.markdown("### ⚠ Alertas de alta contaminación (Nivel 4 o superior)")
if alertas_detectadas.empty:
    st.success("No se detectaron alertas graves en los últimos 7 días.")
else:
    st.dataframe(alertas_detectadas[['Fecha', 'Estacion', contaminante]], use_container_width=True)

# ============================
# Visualización de tendencias
# ============================
st.markdown("### 📊 Tendencia de concentración en los últimos 7 días")
fig, ax = plt.subplots(figsize=(12, 5))
pivot.plot(marker='o', ax=ax)
ax.set_title(f"Tendencia de {contaminante} por estación")
ax.set_ylabel(f"{contaminante} (ppm)")
ax.set_xlabel("Fecha")
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(title="Estación", bbox_to_anchor=(1.02, 1), loc='upper left')
fig.autofmt_xdate()
st.pyplot(fig)

# ============================
# Descarga
# ============================
st.download_button(
    label="⬇️ Descargar datos de los últimos 7 días",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name=f"ultimos_7_dias_{contaminante}.csv",
    mime='text/csv'
)
