import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from app.utils.levels_contaminacion import (
    menu_contaminante,
    colores_por_nivel,
    clasificar_o3,
    clasificar_no2,
    clasificar_co,
    clasificar_so2,
    clasificar_pm10,
    clasificar_pm25,
)

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (50, "Buena", 1),
        (60, "Aceptable", 2),
        (100, "Mala", 3),
        (150, "Muy Mala", 4),
        (200, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_o3(valor, categoria, nivel):
    assert clasificar_o3(valor) == (categoria, nivel)
    assert menu_contaminante("O3", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (50, "Buena", 1),
        (80, "Aceptable", 2),
        (120, "Mala", 3),
        (200, "Muy Mala", 4),
        (220, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_no2(valor, categoria, nivel):
    assert clasificar_no2(valor) == (categoria, nivel)
    assert menu_contaminante("NO2", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (300, "Buena", 1),
        (800, "Aceptable", 2),
        (1000, "Mala", 3),
        (1500, "Muy Mala", 4),
        (1700, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_co(valor, categoria, nivel):
    assert clasificar_co(valor) == (categoria, nivel)
    assert menu_contaminante("CO", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (10, "Buena", 1),
        (50, "Aceptable", 2),
        (150, "Mala", 3),
        (300, "Muy Mala", 4),
        (310, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_so2(valor, categoria, nivel):
    assert clasificar_so2(valor) == (categoria, nivel)
    assert menu_contaminante("SO2", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (20, "Buena", 1),
        (50, "Aceptable", 2),
        (100, "Mala", 3),
        (200, "Muy Mala", 4),
        (250, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_pm10(valor, categoria, nivel):
    assert clasificar_pm10(valor) == (categoria, nivel)
    assert menu_contaminante("PM10", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

@pytest.mark.parametrize(
    "valor,categoria,nivel",
    [
        (10, "Buena", 1),
        (20, "Aceptable", 2),
        (50, "Mala", 3),
        (120, "Muy Mala", 4),
        (140, "Extremadamente Mala", 5),
    ],
)
def test_clasificar_pm25(valor, categoria, nivel):
    assert clasificar_pm25(valor) == (categoria, nivel)
    assert menu_contaminante("PM2_5", valor) == (
        categoria,
        nivel,
        colores_por_nivel[nivel],
    )

def test_menu_contaminante_desconocido():
    assert menu_contaminante("XYZ", 100) == ("Desconocido", 0, "gray")
