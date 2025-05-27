# Análisis de la Calidad del Aire en Puebla

Proyecto de ciencia de datos para analizar, visualizar y predecir la calidad del aire en la ciudad de Puebla, México. Incluye limpieza de datos, análisis exploratorio, visualización geoespacial y modelos predictivos.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías y dependencias](#tecnologías-y-dependencias)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Resultados esperados](#resultados-esperados)
- [Contribución](#contribución)
- [Autor y contacto](#autor-y-contacto)
- [Licencia](#licencia)

---

## Descripción

Este proyecto analiza datos históricos y actuales de la calidad del aire en Puebla, identificando zonas críticas y tendencias, y desarrollando modelos para predecir niveles de contaminación. Incluye visualizaciones interactivas y reportes automáticos.

## Tecnologías y dependencias

- **Lenguaje:** Python 3.10+
- **Librerías principales:** pandas, numpy, matplotlib, seaborn, scikit-learn, streamlit, geopandas, plotly, entre otras.
- Todas las dependencias están en `requirements.txt` y `app/requirements.txt`.

## Estructura del proyecto

- `data/` — Datos crudos y limpios de calidad del aire.
- `notebooks/` — Jupyter Notebooks para análisis, limpieza y modelado.
- `app/` — Aplicación interactiva (Streamlit) para visualización y consulta.
  - `pages/` — Páginas de la app (análisis histórico, tendencias, alertas, etc).
  - `utils/` — Funciones auxiliares para carga, gráficos, mapas y niveles de contaminación.
- `results/` — Visualizaciones y salidas de modelos.
- `requirements.txt` — Dependencias globales del proyecto.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/V1CMA-V/ServicioSocial
   cd ServicioSocial
   ```
2. Instala las dependencias principales:
   ```bash
   pip install -r requirements.txt
   ```
3. (Opcional) Instala dependencias específicas de la app:
   ```bash
   pip install -r app/requirements.txt
   ```

## Uso

- **Notebooks:** Ejecuta los notebooks en `notebooks/` para análisis exploratorio, limpieza y modelado.
- **App interactiva:**
  ```bash
  cd app
  streamlit run Calidad_del_Aire_Puebla.py
  ```
  Accede a la interfaz web para explorar visualizaciones y predicciones.

## Resultados esperados

- Mapas y gráficos de zonas más contaminadas.
- Modelos predictivos de calidad del aire.
- Reportes y visualizaciones interactivas.

## Contribución

¡Las contribuciones son bienvenidas! Puedes abrir issues, enviar pull requests o sugerencias para mejorar el análisis, visualizaciones o modelos.

## Autor y contacto

- **Victor Manuel Martinez Cruz**
- Contacto: [vicma.dev@hotmail.com](mailto:vicma.dev@hotmail.com)

## Licencia

MIT
