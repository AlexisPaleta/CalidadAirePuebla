import streamlit as st
import pandas as pd
import datetime
import calendar


from utils.data_loader import cargar_datos_por_anio
from utils.graficos import (
    evolucion_promedio, concentracion_horaria, concentracion_horaria_heatmap,
    boxplot, barras_promedio, concentracion_diaria_por_mes,
    barras_diarias_por_mes, boxplot_dia_por_estacion, area_apilada_diaria,
    comparar_anios_sobre_mes, area_horaria_estacion, barras_comparativas_mensuales, boxplot_comparativo_anual
)

# Configuración general de la página
st.set_page_config(page_title="Histórico de Calidad del Aire", page_icon="📅", layout="wide")

# ============================
# 🧠 Encabezado principal
# ============================
st.title("📅 Análisis Histórico de la Calidad del Aire en Puebla")
st.markdown("""
Explora cómo ha variado la calidad del aire en diferentes estaciones de Puebla.
Analiza por día, mes, año o compara entre años distintos.
""")


def mostrar_metricas_resumen(df, contaminante):
    promedio = df[contaminante].mean()
    maximo = df[contaminante].max()
    minimo = df[contaminante].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio", f"{promedio:.2f} ppm")
    col2.metric("Máximo", f"{maximo:.2f} ppm")
    col3.metric("Mínimo", f"{minimo:.2f} ppm")

def metricas_anuales(df, contaminante, anio):
    df['Mes'] = df['DateTime'].dt.month
    df['Fecha'] = df['DateTime'].dt.date

    # Promedio mensual
    promedio_mensual = df.groupby('Mes')[contaminante].mean()
    mes_peor = promedio_mensual.idxmax()
    valor_mes_peor = promedio_mensual.max()

    # Día más contaminado
    idx_max = df[contaminante].idxmax()
    valor_max = df.loc[idx_max, contaminante]
    fecha_max = df.loc[idx_max, 'Fecha']

    # Promedio total
    promedio_anual = df[contaminante].mean()

    # Nombre del mes
    mes_nombre = calendar.month_name[mes_peor].capitalize()

    # Nombre de la estación
    estacion_max = df.loc[idx_max, 'Estacion']

    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Mes más contaminado",
                f"{mes_nombre} / {anio}",
                f"{valor_mes_peor:.3f} ppm")

    col2.metric("Pico más alto", f"{valor_max:.3f} ppm", f"{fecha_max} - {estacion_max}")


    col3.metric("Promedio anual",
                f"{promedio_anual:.3f} ppm")



# ============================
# Parámetros generales
# ============================
contaminantes = ['O3', 'NO2', 'CO', 'SO2', 'PM10', 'PM2_5']
estaciones = {'santa', 'bine', 'ninfas', 'utp', 'vel'}

st.sidebar.header("⚙️ Parámetros de análisis")

contaminante = st.sidebar.selectbox("Contaminante", contaminantes)
estaciones_seleccionadas = st.sidebar.multiselect("Estaciones", list(estaciones), default=list(estaciones))
periodo = st.sidebar.radio("Periodo", ["Día", "Mes", "Año", "Comparación Anual"], horizontal=False)

# ============================
# Día
# ============================
if periodo == "Día":
    st.markdown("## 📆 Análisis Diario")

    min_fecha = datetime.date(2021, 1, 1)
    max_fecha = datetime.date.today() - datetime.timedelta(days=1)

    d = st.date_input("Selecciona una fecha", max_fecha, min_value=min_fecha, max_value=max_fecha)
    df = cargar_datos_por_anio(d.year)

    st.info(f"Fecha seleccionada: **{d}**")

    df_filtrado = df[
        (df['Estacion'].isin(estaciones_seleccionadas)) &
        (df['DateTime'].dt.date == d)
    ]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para esta fecha.")
    else:
        st.subheader(f"📈 Concentración horaria de `{contaminante}`")
        mostrar_metricas_resumen(df_filtrado, contaminante)

        tabs = st.tabs(["📈 Línea diaria", "📊 Heatmap", " Área apilada por hora y estación"])

        with tabs[0]:
            concentracion_horaria(df_filtrado, contaminante)
        with tabs[1]:
            concentracion_horaria_heatmap(df_filtrado, contaminante)
        with tabs[2]:
            area_horaria_estacion(df_filtrado, contaminante)

# ============================
# Mes
# ============================
elif periodo == "Mes":
    st.markdown("## 🗓️ Análisis Mensual")

    mes = st.selectbox("Selecciona el mes", list(range(1, 13)))
    anio = st.selectbox("Selecciona el año", [2021, 2022, 2023, 2024, 2025])
    df = cargar_datos_por_anio(anio)
    df_mes = df[df['DateTime'].dt.month == mes]

    month_names = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    st.info(f"Mostrando datos de **{month_names[mes]} {anio}**")

    df_filtrado = df_mes[df_mes['Estacion'].isin(estaciones_seleccionadas)]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para este mes.")
    else:

        st.subheader(f"{contaminante} en el mes seleccionado")
        mostrar_metricas_resumen(df_filtrado, contaminante)

        tabs = st.tabs(["📈 Línea diaria", "📊 Barras", "📦 Boxplot", "📉 Área apilada"])

        with tabs[0]:
            concentracion_diaria_por_mes(df_filtrado, contaminante, estaciones_seleccionadas, mes)
        with tabs[1]:
            barras_diarias_por_mes(df_filtrado, contaminante, estaciones_seleccionadas, mes)
        with tabs[2]:
            boxplot_dia_por_estacion(df_filtrado, contaminante, estaciones_seleccionadas, mes)
        with tabs[3]:
            area_apilada_diaria(df_filtrado, contaminante, estaciones_seleccionadas, mes)

# ============================
# Año
# ============================
elif periodo == "Año":
    st.markdown("## 📊 Análisis Anual")

    anio = st.selectbox("Selecciona el año", [2021, 2022, 2023, 2024, 2025])
    df = cargar_datos_por_anio(anio)

    min_fecha = df['DateTime'].min().date()
    max_fecha = df['DateTime'].max().date()
    rango_fechas = st.slider("Selecciona el rango de fechas", min_value=min_fecha, max_value=max_fecha, value=(min_fecha, max_fecha))

    df_filtrado = df[
        (df['Estacion'].isin(estaciones_seleccionadas)) &
        (df['DateTime'].dt.date >= rango_fechas[0]) &
        (df['DateTime'].dt.date <= rango_fechas[1])
    ]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles en este rango.")
    else:
        st.info(f"Mostrando datos de **{rango_fechas[0]} a {rango_fechas[1]}**")

        st.subheader(f"{contaminante} en el año seleccionado")
        metricas_anuales(df_filtrado, contaminante, anio)

        tabs = st.tabs(["📈 Línea diaria", "📊 Barras mensuales", "📦 Boxplot mensual"])

        with tabs[0]:
            evolucion_promedio(df_filtrado, contaminante, estaciones_seleccionadas)
        with tabs[1]:
            barras_promedio(df_filtrado, contaminante, estaciones_seleccionadas)
        with tabs[2]:
            boxplot(df_filtrado, contaminante, estaciones_seleccionadas)

# ============================
# Comparación Anual
# ============================
elif periodo == "Comparación Anual":
    st.markdown("## 🔁 Comparación entre Años")

    col1, col2 = st.columns(2)
    with col1:
        anio_1 = st.selectbox("Selecciona el año 1", [2021, 2022, 2023, 2024, 2025], index=3)
    with col2:
        anio_2 = st.selectbox("Selecciona el año 2", [2021, 2022, 2023, 2024, 2025], index=4)

    estacion = st.selectbox("Estación a comparar", list(estaciones))

    df1 = cargar_datos_por_anio(anio_1)
    df2 = cargar_datos_por_anio(anio_2)

    df_filtrado_1 = df1[df1['Estacion'] == estacion]
    df_filtrado_2 = df2[df2['Estacion'] == estacion]

    nombre_estacion = {
        'santa': 'Agua Santa',
        'bine': 'Benemérito Instituto Normal del Estado (BINE)',
        'ninfas': 'Las Ninfas',
        'utp': 'Universidad Tecnológica de Puebla (UTP)',
        'vel': 'Velódromo'
    }[estacion]

    if df_filtrado_1.empty or df_filtrado_2.empty:
        st.warning("No hay datos disponibles para esta comparación.")
    else:

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### Resumen {anio_1}")
            metricas_anuales(df_filtrado_1, contaminante, anio_1)

        with col2:
            st.markdown(f"#### Resumen {anio_2}")
            metricas_anuales(df_filtrado_2, contaminante, anio_2)

        tabs = st.tabs(["📈 Línea diaria", "📊 Heatmap", "📊 Boxplot"])

        st.info(f"Comparando `{contaminante}` en **{nombre_estacion}** entre {anio_1} y {anio_2}")

        with tabs[0]:
            comparar_anios_sobre_mes(df_filtrado_1, df_filtrado_2, contaminante, estacion, anio_1, anio_2)

        with tabs[1]:
            barras_comparativas_mensuales(df_filtrado_1, df_filtrado_2, contaminante, estacion, anio_1, anio_2)

        with tabs[2]:
            boxplot_comparativo_anual(df_filtrado_1, df_filtrado_2, contaminante, anio_1, anio_2)

# ============================
# Exportación
# ============================
if 'df_filtrado' in locals() and not df_filtrado.empty:
    st.download_button(
        label="⬇️ Descargar datos filtrados",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name="datos_historicos.csv",
        mime="text/csv"
    )
