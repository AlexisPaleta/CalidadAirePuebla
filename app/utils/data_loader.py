import pandas as pd
from datetime import datetime, timedelta

def cargar_datos(path):
    df = pd.read_csv(f"data/Clean/{path}")
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df


def cargar_datos_dia_anterior():
    """Carga los datos correspondientes al día anterior.

    La función selecciona automáticamente el archivo CSV según el año
    obtenido de ``ayer.year``. Si el archivo no existe, se lanza un
    ``FileNotFoundError`` con un mensaje descriptivo.
    """
    ayer = (datetime.today() - timedelta(days=1)).date()
    ruta = f"data/Clean/datos_Clean_{ayer.year}.csv"

    try:
        df = pd.read_csv(ruta)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"No se encontró el archivo de datos para el año {ayer.year}: {ruta}"
        ) from e

    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df_ayer = df[df['DateTime'].dt.date == ayer]
    return df_ayer

def cargar_datos_por_anio(anio):
    ruta = f"data/Clean/datos_Clean_{anio}.csv"
    df = pd.read_csv(ruta, parse_dates=['DateTime'])
    return df

