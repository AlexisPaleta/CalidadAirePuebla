# ==========================
# Colores asociados por nivel
# ==========================

colores_por_nivel = {
    1: 'green',
    2: 'yellow',
    3: 'orange',
    4: 'red',
    5: 'purple'
}

# ==========================
# Clasificación general
# ==========================

def menu_contaminante(contaminante, valor_ppm):
    clasificadores = {
        'O3': clasificar_o3,
        'NO2': clasificar_no2,
        'CO': clasificar_co,
        'SO2': clasificar_so2,
        'PM10': clasificar_pm10,
        'PM2_5': clasificar_pm25
    }

    clasificar = clasificadores.get(contaminante)
    if clasificar:
        categoria, nivel = clasificar(valor_ppm)
        color = colores_por_nivel.get(nivel, "gray")
        return categoria, nivel, color
    else:
        return "Desconocido", 0, "gray"

# ==========================
# Funciones por contaminante (valores inalterados)
# ==========================

def clasificar_o3(valor):
    if valor <= 58:
        return "Buena", 1
    elif valor <= 90:
        return "Aceptable", 2
    elif valor <= 135:
        return "Mala", 3
    elif valor <= 175:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5

def clasificar_no2(valor):
    if valor <= 53:
        return "Buena", 1
    elif valor <= 106:
        return "Aceptable", 2
    elif valor <= 160:
        return "Mala", 3
    elif valor <= 213:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5

def clasificar_co(valor):
    if valor <= 500:
        return "Buena", 1
    elif valor <= 900:
        return "Aceptable", 2
    elif valor <= 1200:
        return "Mala", 3
    elif valor <= 1600:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5

def clasificar_so2(valor):
    if valor <= 35:
        return "Buena", 1
    elif valor <= 75:
        return "Aceptable", 2
    elif valor <= 185:
        return "Mala", 3
    elif valor <= 304:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5

def clasificar_pm10(valor):
    if valor <= 45:
        return "Buena", 1
    elif valor <= 60:
        return "Aceptable", 2
    elif valor <= 132:
        return "Mala", 3
    elif valor <= 213:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5

def clasificar_pm25(valor):
    if valor <= 15:
        return "Buena", 1
    elif valor <= 25:
        return "Aceptable", 2
    elif valor <= 79:
        return "Mala", 3
    elif valor <= 130:
        return "Muy Mala", 4
    else:
        return "Extremadamente Mala", 5
