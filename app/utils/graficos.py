import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
from utils.levels_contaminacion import menu_contaminante


# ============================
# 📊 Gráfico de líneas
# ============================
def concentracion_horaria(df, contaminante):
    # Agrupación: promedio horario por estación
    hourly_avg = df.groupby(['Hora', 'Estacion'])[contaminante].mean().unstack()

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Gráfico de líneas con marcadores
    hourly_avg.plot(ax=ax, marker='o', linewidth=2)

    # Personalización visual
    ax.set_title(f"📈 Concentración Horaria Promedio de {contaminante}", fontsize=18, weight='bold')
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
# 📊 Gráfico de calor
# ============================
def concentracion_horaria_heatmap(df, contaminante):
    hourly_avg = df.groupby(['Hora', 'Estacion'])[contaminante].mean().unstack().T
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(hourly_avg, cmap='YlOrRd', annot=False, fmt=".2f", cbar_kws={'label': f'{contaminante} (ppm)'})
    ax.set_title(f"Mapa de Calor: {contaminante} por Hora", fontsize=14)
    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Estación")
    st.pyplot(fig)


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
# 📊 Gráfico sobre medicion
# ============================
def grafico_sobre_medicion(df, estacion, contaminante):
    # Filtrar datos de la estación
    df_est = df[df['Estacion'] == estacion].copy()
    if df_est.empty:
        st.warning(f"No hay datos disponibles para la estación '{estacion}'.")
        return

    # Agrupar por día y obtener máximo diario
    df_est['fecha'] = pd.to_datetime(df_est['DateTime']).dt.date
    g = df_est.groupby('fecha')[contaminante].max().reset_index()
    g = g.rename(columns={contaminante: 'valororig'})
    g = g.set_index('fecha')

    # Clasificar cada punto usando menu_contaminante()
    categorias = []
    colores = []
    for val in g['valororig']:
        categoria, _, color = menu_contaminante(contaminante, val)
        categorias.append(categoria)
        colores.append(color)

    g['categoria'] = categorias
    g['color'] = colores

    # Gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot punto a punto con color según categoría
    ax.scatter(g.index, g['valororig'], c=g['color'], edgecolor='black', s=80, label='Mediciones')

    # Crear líneas de referencia
    limites = {
        "Mala calidad": 90,
        "Muy mala calidad": 135,
        "Contingencia": 175
    }
    for etiqueta, valor in limites.items():
        ax.axhline(y=valor, linestyle='--', label=f"Límite: {etiqueta}", alpha=0.5)

    ax.set_title(f"📊 Mediciones máximas diarias de {contaminante} - {estacion}", fontsize=15)
    ax.set_ylabel(f"{contaminante} (ppb)")
    ax.set_xlabel("Fecha")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper left')
    fig.autofmt_xdate()

    st.pyplot(fig)

