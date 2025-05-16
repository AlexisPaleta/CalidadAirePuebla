import folium
import streamlit as st
from streamlit_folium import st_folium
from utils.levels_contaminacion import menu_contaminante
import pandas as pd



# Cargar estaciones (una sola vez al inicio)
estaciones = pd.read_csv("app/data/estaciones-Puebla_sinaica.csv")


def mapa(df_media, contaminante):
    # Crear mapa centrado en Puebla
    m = folium.Map(location=[19.04, -98.2], zoom_start=12, control_scale=True)

    for _, estacion in estaciones.iterrows():
        lat = estacion['lat']
        lon = estacion['long']
        id_estacion = estacion['Estaciones']
        nombre_estacion = estacion['nombre']

        # Validar existencia del contaminante en la estación
        if id_estacion not in df_media.index or contaminante not in df_media.columns:
            continue

        valor_ppm = df_media.loc[id_estacion, contaminante]

        if pd.isna(valor_ppm):
            calidad, nivel, color = "", "", "gray"
            popup_html = f"""
            <div style="font-size: 14px">
                <b>Estación:</b> {nombre_estacion}<br>
                <b>Contaminante:</b> {contaminante}<br>
                <b>Valor:</b> No se obtuvo información<br>
            </div>
            """

            # Círculo con color según calidad
            folium.CircleMarker(
                location=(lat, lon),
                radius=25,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{nombre_estacion} - {calidad}"
            ).add_to(m)

            # Marcador opcional (puedes quitar si ya se entiende con el círculo)
            folium.Marker(
                location=(lat, lon),
                icon=folium.Icon(color="blue", icon="info-sign"),
                popup=nombre_estacion
            ).add_to(m)
            continue

        calidad, nivel, color = menu_contaminante(contaminante, valor_ppm)

        # Texto detallado del popup
        popup_html = f"""
        <div style="font-size: 14px">
            <b>Estación:</b> {nombre_estacion}<br>
            <b>Contaminante:</b> {contaminante}<br>
            <b>Valor:</b> {valor_ppm:.3f} ppm<br>
            <b>Calidad:</b> {calidad} (Nivel {nivel})
        </div>
        """

        # Círculo con color según calidad
        folium.CircleMarker(
            location=(lat, lon),
            radius=25,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{nombre_estacion} - {calidad}"
        ).add_to(m)

        # Marcador opcional (puedes quitar si ya se entiende con el círculo)
        folium.Marker(
            location=(lat, lon),
            icon=folium.Icon(color="blue", icon="info-sign"),
            popup=nombre_estacion
        ).add_to(m)

    # Mostrar en Streamlit
    return st_folium(m, width="100%", height=550)
