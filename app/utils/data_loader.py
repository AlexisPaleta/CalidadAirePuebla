import pandas as pd
from datetime import datetime, timedelta

def cargar_datos(path):
    df = pd.read_csv(f"app/data/times/{path}")
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df


def cargar_datos_dia_anterior():
    df = pd.read_csv(f"app/data/times/datos_Clean_2025.csv")
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    ayer = (datetime.today() - timedelta(days=1)).date()
    df_ayer = df[df['DateTime'].dt.date == ayer]

    return df_ayer

def cargar_datos_por_anio(anio):
    ruta = f"app/data/times/datos_Clean_{anio}.csv"
    df = pd.read_csv(ruta, parse_dates=['DateTime'])
    return df

