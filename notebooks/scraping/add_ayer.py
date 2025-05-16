from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time
import os

# Configuración
URL = 'https://calidaddelaire.puebla.gob.mx/views/reportes_monitoreo.php'
ESTACIONES = ['santa', 'bine', 'ninfas', 'utp', 'vel']
COLUMNS = ['Fecha', 'Hora', 'O3', 'O3 8hrs', 'NO2', 'CO', 'SO2', 'PM-10', 'PM-2.5', 'Estacion']
OUTPUT_CSV = 'datos_2025.csv'

# Solo el día de ayer
ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
FECHAS = [ayer]

def abrir_modal(page):
    page.click('#nv_IAS')
    page.wait_for_selector('[data-bs-target="#modal_historialIAS"]')
    page.click('[data-bs-target="#modal_historialIAS"]')

def configurar_filtros(page, fecha, estacion):
    page.check('#his_filtro_IAS1')
    page.fill('#his_fecha_IAS', fecha)
    page.select_option('#his_estacion_IAS', estacion)
    page.click('#btnHistorial_IAS')

def extraer_datos(page, fecha, estacion):
    page.wait_for_selector('#div_historial_IAS')
    time.sleep(1.5)
    rows = page.locator('table.table.table-bordered tbody tr').all()
    data = []

    for row in rows:
        celdas = row.locator('td').all_inner_texts()
        if len(celdas) == 8:
            data.append([fecha] + celdas + [estacion])
        elif len(celdas) == 7:
            celdas.insert(2, "NA")
            data.append([fecha] + celdas + [estacion])

    if len(data) != 24:
        print(f"⚠️ {fecha} - {estacion}: {len(data)} registros encontrados (esperados: 24)")
        return []
    return data

def scrap_estacion(estacion):
    print(f"\n🚀 Iniciando estación: {estacion.upper()}")
    datos_estacion = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        abrir_modal(page)

        for fecha in FECHAS:
            try:
                configurar_filtros(page, fecha, estacion)
                registros = extraer_datos(page, fecha, estacion)
                if registros:
                    datos_estacion.extend(registros)
                    print(f"✅ {fecha} - {estacion} ({len(registros)} filas)")
                else:
                    print(f"❌ {fecha} - {estacion}: Datos incompletos o vacíos")
            except Exception as e:
                print(f"🛑 Error en {fecha} - {estacion}: {e}")

        browser.close()
    return datos_estacion

def main():
    all_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        resultados = list(executor.map(scrap_estacion, ESTACIONES))
        for datos in resultados:
            all_data.extend(datos)

    if all_data:
        df = pd.DataFrame(all_data, columns=COLUMNS)
        existe = os.path.exists(f'data/Crudos/{OUTPUT_CSV}')
        df.to_csv(f'data/Crudos/{OUTPUT_CSV}', mode='a', index=False, header=False)
        print(f"\n✅ Día agregado a 'data/Crudos/{OUTPUT_CSV}' con {len(df)} nuevas filas.")
    else:
        print("\n⚠️ No se recuperaron datos.")

if __name__ == '__main__':
    main()
