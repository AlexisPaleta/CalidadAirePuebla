import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
from utils.levels_contaminacion import menu_contaminante

# ============================
# Concentracion horaria
# ============================

# ============================
# Gráfico de líneas
# ============================
def concentracion_horaria(df, contaminante):
    # Agrupación: promedio horario por estación
    hourly_avg = df.groupby(['Hora', 'Estacion'])[contaminante].mean().unstack()

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Gráfico de líneas con marcadores
    hourly_avg.plot(ax=ax, marker='o', linewidth=2)

    # Personalización visual
    ax.set_title(f"Concentración Horaria Promedio de {contaminante}", fontsize=18, weight='bold')
    ax.set_xlabel("Hora del Día", fontsize=12)
    ax.set_ylabel(f"{contaminante} (ppm)", fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24), fontsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(title="Estación", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, title_fontsize=10)
    fig.tight_layout()

    # Mostrar en Streamlit
    st.pyplot(fig)

# ============================
# Gráfico de calor
# ============================
def concentracion_horaria_heatmap(df, contaminante):
    hourly_avg = df.groupby(['Hora', 'Estacion'])[contaminante].mean().unstack().T
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(hourly_avg, cmap='YlOrRd', annot=False, fmt=".2f", cbar_kws={'label': f'{contaminante} (ppm)'})
    ax.set_title(f"Mapa de Calor: {contaminante} por Hora", fontsize=14)
    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Estación")
    st.pyplot(fig)

# ============================
# Boxplot por hora en el día (variabilidad intradía)
# ============================
# Gráfico alternativo: área apilada por hora y estación (estilo flujo diario)
def area_horaria_estacion(df, contaminante):
    df['Hora'] = df['DateTime'].dt.hour
    resumen = df.groupby(['Hora', 'Estacion'])[contaminante].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 5))
    resumen.plot(kind='area', stacked=True, ax=ax, alpha=0.6)

    ax.set_title(f"Distribución acumulada por hora de {contaminante}")
    ax.set_xlabel("Hora del día")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.legend(title='Estación', bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)




# ============================
# Concentracion anual
# ============================

# ============================
# Grafico de evolucion promedio
# ============================
def evolucion_promedio(df, contaminante, estaciones_seleccionadas):
    fig, ax = plt.subplots(figsize=(12, 5))
    for estacion in estaciones_seleccionadas:
        df_est = df[df['Estacion'] == estacion]
        df_est = df_est.groupby('DateTime')[contaminante].mean()
        ax.plot(df_est.index, df_est.values, marker='o', label=estacion)

    ax.set_xlabel("Fecha")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.set_title(f"{contaminante} promedio diario por estación")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

# ============================
# Boxplot
# ============================

def boxplot(df, contaminante, estaciones_seleccionadas):
    df = df[df['Estacion'].isin(estaciones_seleccionadas)].copy()
    df['Mes'] = df['DateTime'].dt.strftime('%b')  # Abreviaturas de mes
    df['Mes'] = pd.Categorical(df['Mes'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df, x='Mes', y=contaminante, ax=ax, showfliers=False)

    ax.set_title(f"Distribución mensual de {contaminante}")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.set_xlabel("Mes")
    st.pyplot(fig)

# ============================
# Barras promedio
# ============================
def barras_promedio(df, contaminante, estaciones_seleccionadas):
    df['Mes'] = df['DateTime'].dt.month

    fig, ax = plt.subplots(figsize=(12, 5))

    resumen = df[df['Estacion'].isin(estaciones_seleccionadas)].groupby(['Mes', 'Estacion'])[contaminante].mean().unstack()

    resumen.plot(kind='bar', ax=ax)
    ax.set_title(f"{contaminante} promedio mensual por estación")
    ax.set_xlabel("Mes")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(title='Estación')
    st.pyplot(fig)


# ============================
# Concentracion Mensual por dia
# ============================

def concentracion_diaria_por_mes(df, contaminante, estaciones_seleccionadas, mes):
    # Filtrar por mes
    df_mes = df.copy()
    df_mes['Dia'] = df_mes['DateTime'].dt.day

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 5))

    for estacion in estaciones_seleccionadas:
        df_est = df_mes[df_mes['Estacion'] == estacion]
        promedio_dia = df_est.groupby('Dia')[contaminante].mean()
        ax.plot(promedio_dia.index, promedio_dia.values, marker='o', label=estacion)

    ax.set_title(f"Concentración diaria de {contaminante} en el mes {mes:02d}")
    ax.set_xlabel("Día del mes")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(title='Estación')
    plt.tight_layout()
    st.pyplot(fig)

# ============================
# Barras diarias por mes
# ============================
def barras_diarias_por_mes(df, contaminante, estaciones_seleccionadas, mes):
    df_mes = df.copy()
    df_mes['Dia'] = df_mes['DateTime'].dt.day
    df_mes = df_mes[df_mes['DateTime'].dt.month == mes]

    resumen = df_mes[df_mes['Estacion'].isin(estaciones_seleccionadas)] \
        .groupby(['Dia', 'Estacion'])[contaminante].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 5))
    resumen.plot(kind='bar', ax=ax)

    ax.set_title(f"{contaminante} promedio diario por estación - Mes {mes:02d}")
    ax.set_xlabel("Día del mes")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(title='Estación', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)


# ============================
# Boxplot diario por estacion
# ============================
def boxplot_dia_por_estacion(df, contaminante, estaciones_seleccionadas, mes):
    df_mes = df.copy()
    df_mes['Dia'] = df_mes['DateTime'].dt.day
    df_mes = df_mes[df_mes['DateTime'].dt.month == mes]
    df_mes = df_mes[df_mes['Estacion'].isin(estaciones_seleccionadas)]

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df_mes, x='Dia', y=contaminante, hue='Estacion', ax=ax, showfliers=False)

    ax.set_title(f"Distribución diaria de {contaminante} por estación - Mes {mes:02d}")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.set_xlabel("Día del mes")
    ax.legend(title='Estación', bbox_to_anchor=(1.02, 1), loc='upper left')
    st.pyplot(fig)

# ============================
# Area apilada diaria
# ============================
def area_apilada_diaria(df, contaminante, estaciones_seleccionadas, mes):
    df_mes = df.copy()
    df_mes['Dia'] = df_mes['DateTime'].dt.day
    df_mes = df_mes[df_mes['DateTime'].dt.month == mes]
    df_mes = df_mes[df_mes['Estacion'].isin(estaciones_seleccionadas)]

    resumen = df_mes.groupby(['Dia', 'Estacion'])[contaminante].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 5))
    resumen.plot(kind='area', stacked=True, ax=ax, alpha=0.6)

    ax.set_title(f"Concentración acumulada diaria de {contaminante} por estación - Mes {mes:02d}")
    ax.set_xlabel("Día del mes")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(title='Estación', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)


# ============================
# Comparacion entre años
# ============================
# Re-importar tras el reset
import pandas as pd
import matplotlib.pyplot as plt

# Redefinir función de comparación ensimada por mes
def comparar_anios_sobre_mes(df1, df2, contaminante, estacion, anio1, anio2):

    df1['DiaJuliano'] = df1['DateTime'].dt.dayofyear
    df2['DiaJuliano'] = df2['DateTime'].dt.dayofyear

    df1['Fecha'] = df1['DateTime'].dt.date
    df2['Fecha'] = df2['DateTime'].dt.date

    prom1 = df1.groupby('DiaJuliano')[contaminante].mean()
    prom2 = df2.groupby('DiaJuliano')[contaminante].mean()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(prom1.index, prom1.values, label=f"{contaminante} - {anio1}", color='blue')
    ax.plot(prom2.index, prom2.values, label=f"{contaminante} - {anio2}", color='green')

    ax.set_title(f"📊 Comparación diaria de {contaminante} entre {anio1} y {anio2} en {estacion}", fontsize=14)
    ax.set_xlabel("Mes del año")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_xlim(1, 366)
    ax.set_xticks([15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])
    ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    plt.tight_layout()

    st.pyplot(fig)

# 1. Barras comparativas por mes entre años (resumen mensual claro)
def barras_comparativas_mensuales(df1, df2, contaminante, estacion, anio1, anio2):
    df1['Mes'] = df1['DateTime'].dt.month
    df2['Mes'] = df2['DateTime'].dt.month

    prom1 = df1.groupby('Mes')[contaminante].mean()
    prom2 = df2.groupby('Mes')[contaminante].mean()

    df_plot = pd.DataFrame({
        f'{anio1}': prom1,
        f'{anio2}': prom2
    })

    fig, ax = plt.subplots(figsize=(10, 5))
    df_plot.plot(kind='bar', ax=ax)
    ax.set_title(f'Comparación mensual de {contaminante} entre {anio1} y {anio2} ({estacion})')
    ax.set_xlabel("Mes")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.set_xticks(range(0, 12))
    ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'], rotation=0)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(title="Año")
    plt.tight_layout()
    st.pyplot(fig)

# 2. Boxplot combinado por año (distribución general del año)
def boxplot_comparativo_anual(df1, df2, contaminante, anio1, anio2):
    df1['Año'] = anio1
    df2['Año'] = anio2
    df_comparado = pd.concat([df1, df2], ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df_comparado, x='Año', y=contaminante, color='skyblue', showfliers=False, ax=ax)

    ax.set_title(f"Distribución anual de {contaminante}")
    ax.set_ylabel(f"{contaminante} (ppm)")
    ax.set_xlabel("Año")
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
