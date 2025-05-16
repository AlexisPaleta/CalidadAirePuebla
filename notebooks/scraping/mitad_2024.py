from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time

# Configuración
URL = 'https://calidaddelaire.puebla.gob.mx/views/reportes_monitoreo.php'
ESTACIONES = ['santa', 'bine', 'ninfas', 'utp', 'vel']
COLUMNS = ['Fecha', 'Hora', 'O3', 'O3 8hrs', 'NO2', 'CO', 'SO2', 'PM-10', 'PM-2.5', 'Estacion']
OUTPUT_CSV = 'datos_mitad_2024.csv'
FECHAS = ['2024-07-21', '2024-07-22', '2024-07-23', '2024-07-24', '2024-07-25', '2024-07-26', '2024-07-27',
          '2024-07-28', '2024-07-29', '2024-07-30', '2024-07-31', '2024-08-01', '2024-08-02', '2024-08-03',
          '2024-08-04', '2024-08-05', '2024-08-06', '2024-08-07', '2024-08-08', '2024-08-09', '2024-08-10',
          '2024-08-11', '2024-08-12', '2024-08-13', '2024-08-14', '2024-08-15', '2024-08-16', '2024-08-17',
          '2024-08-18', '2024-08-19', '2024-08-20', '2024-08-21', '2024-08-22', '2024-08-23', '2024-08-24',
          '2024-08-25', '2024-08-26', '2024-08-27', '2024-08-28', '2024-08-29', '2024-08-30', '2024-08-31',
          '2024-09-01', '2024-09-02', '2024-09-03', '2024-09-04', '2024-09-05', '2024-09-06', '2024-09-07',
          '2024-09-08', '2024-09-09', '2024-09-10', '2024-09-11', '2024-09-12', '2024-09-13', '2024-09-14',
          '2024-09-15', '2024-09-16', '2024-09-17', '2024-09-18', '2024-09-19', '2024-09-20', '2024-09-21',
          '2024-09-22', '2024-09-23', '2024-09-24', '2024-09-25', '2024-09-26', '2024-09-27', '2024-09-28',
          '2024-09-29', '2024-09-30', '2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05',
          '2024-10-06', '2024-10-07', '2024-10-08', '2024-10-09', '2024-10-10', '2024-10-11', '2024-10-12',
          '2024-10-13', '2024-10-14', '2024-10-15', '2024-10-16', '2024-10-17', '2024-10-18', '2024-10-19',
          '2024-10-20', '2024-10-21', '2024-10-22', '2024-10-23', '2024-10-24', '2024-10-25', '2024-10-26',
          '2024-10-27', '2024-10-28', '2024-10-29', '2024-10-30', '2024-10-31', '2024-11-01', '2024-11-02',
          '2024-11-03', '2024-11-04', '2024-11-05', '2024-11-06', '2024-11-07', '2024-11-08', '2024-11-09',
          '2024-11-10', '2024-11-11', '2024-11-12', '2024-11-13', '2024-11-14', '2024-11-15', '2024-11-16',
          '2024-11-17', '2024-11-18', '2024-11-19', '2024-11-20', '2024-11-21', '2024-11-22', '2024-11-23',
          '2024-11-24', '2024-11-25', '2024-11-26', '2024-11-27', '2024-11-28', '2024-11-29', '2024-11-30',
          '2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05', '2024-12-06', '2024-12-07',
          '2024-12-08', '2024-12-09', '2024-12-10', '2024-12-11', '2024-12-12', '2024-12-13', '2024-12-14',
          '2024-12-15', '2024-12-16', '2024-12-17', '2024-12-18', '2024-12-19', '2024-12-20', '2024-12-21',
          '2024-12-22', '2024-12-23', '2024-12-24', '2024-12-25', '2024-12-26', '2024-12-27', '2024-12-28',
          '2024-12-29', '2024-12-30', '2024-12-31']

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
            # Insertamos "NA" en la posición de 'O3 8hrs'
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
        browser = p.chromium.launch(headless=False)
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

    df = pd.DataFrame(all_data, columns=COLUMNS)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅ Archivo completo guardado: '{OUTPUT_CSV}' con {len(df)} filas.")

if __name__ == '__main__':
    main()
