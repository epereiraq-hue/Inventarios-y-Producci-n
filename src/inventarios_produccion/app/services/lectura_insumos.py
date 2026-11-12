# -*- coding: utf-8 -*-
"""
Lectura de insumos para la app de planificación de inventarios.

Lee los archivos Excel de Insumos/ SIN MODIFICAR nada dentro de esa carpeta.
Expone los datos crudos de las hojas 'Meses ...' (324 productos) y de los
requerimientos de logística (24 requerimientos).
"""

import os
from typing import Any

import openpyxl

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
# Un nivel más arriba: raíz del proyecto (Inventarios y Producción)
BASE_DIR = os.path.dirname(BASE_DIR)
INSUMOS_DIR = os.path.join(BASE_DIR, "Insumos")

ARCHIVO_MESES = os.path.join(INSUMOS_DIR, "Meses de inventario x Producto.xlsx")
ARCHIVO_REQ = os.path.join(INSUMOS_DIR, "Requerimientos Logística.xlsx")


def _limpiar(valor: Any) -> Any:
    """Convierte string vacío en None, devuelve el valor en otros casos."""
    if valor is None:
        return None
    if isinstance(valor, str) and valor.strip() == "":
        return None
    return valor


def leer_hoja_meses(ruta_archivo: str, nombre_hoja: str) -> list[dict]:
    """
    Lee una hoja 'Meses ...' del archivo de inventarios.

    Estructura detectada:
      - fila 2: encabezados de columnas
      - fila 3: fechas de los meses (columnas 7-13)
      - fila 4 en adelante: datos de producto

    Retorna una lista de diccionarios con las columnas principales.
    Con values_only=True, cada fila ya es una tupla de valores.
    """
    import os

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    try:
        wb = openpyxl.load_workbook(ruta_archivo, data_only=True)
    except Exception as exc:
        raise RuntimeError(f"No se pudo leer el archivo Excel '{ruta_archivo}': {exc}") from exc

    try:
        ws = wb[nombre_hoja]
    except KeyError:
        wb.close()
        raise KeyError(f"La hoja '{nombre_hoja}' no existe en el archivo") from None

    filas = []
    for row in ws.iter_rows(min_row=4, values_only=True):
        if row is None or row[0] is None:
            continue

        filas.append({
            "item": _limpiar(row[0]),
            "codigo": _limpiar(row[1]) if len(row) > 1 else None,
            "codigo2": _limpiar(row[2]) if len(row) > 2 else None,
            "descripcion": _limpiar(row[3]) if len(row) > 3 else None,
            "familia": _limpiar(row[4]) if len(row) > 4 else None,
            "estandar": _limpiar(row[5]) if len(row) > 5 else None,
            "ventas_mes_1": _limpiar(row[6]) if len(row) > 6 else None,
            "ventas_mes_2": _limpiar(row[7]) if len(row) > 7 else None,
            "ventas_mes_3": _limpiar(row[8]) if len(row) > 8 else None,
            "ventas_mes_4": _limpiar(row[9]) if len(row) > 9 else None,
            "ventas_mes_5": _limpiar(row[10]) if len(row) > 10 else None,
            "ventas_mes_6": _limpiar(row[11]) if len(row) > 11 else None,
            "ventas_mes_7": _limpiar(row[12]) if len(row) > 12 else None,
            "total": _limpiar(row[13]) if len(row) > 13 else None,
            "promedio_mensual": _limpiar(row[14]) if len(row) > 14 else None,
            "inventario_04_11_2026": _limpiar(row[15]) if len(row) > 15 else None,
            "meses_stock_actual": _limpiar(row[16]) if len(row) > 16 else None,
        })

    wb.close()
    return filas


def leer_todas_las_hojas_meses(ruta_archivo: str) -> dict[str, list[dict]]:
    """
    Lee todas las hojas cuyo nombre comienza con 'Meses ' del archivo.
    Retorna un diccionario: {nombre_hoja: [filas]}.
    """
    wb = openpyxl.load_workbook(ruta_archivo, data_only=True)
    resultado: dict[str, list[dict]] = {}
    for nombre in wb.sheetnames:
        if nombre.startswith("Meses "):
            resultado[nombre] = leer_hoja_meses(ruta_archivo, nombre)
    wb.close()
    return resultado


def leer_requerimientos_logistica(ruta_archivo: str) -> list[dict]:
    """
    Lee la hoja 'Requerimientos' del archivo Requerimientos Logística.xlsx.

    Los encabezados reales están en la fila 11; los datos van de la fila 12
    a la 35 (24 requerimientos).
    """
    wb = openpyxl.load_workbook(ruta_archivo, data_only=True)
    ws = wb["Requerimientos"]

    filas = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row is None or row[0] is None:
            continue

        filas.append({
            "codigo_dynamics": _limpiar(row[0]),
            "codigo_best": _limpiar(row[1]),
            "descripcion": _limpiar(row[2]),
            "requerimiento": _limpiar(row[3]),
            "proceso": _limpiar(row[4]),
            "importancia": _limpiar(row[5]),
            "comentario": _limpiar(row[6]),
            "dias_inventario": _limpiar(row[7]),
            "estado": _limpiar(row[8]),
            "responsable_proceso": _limpiar(row[9]),
            "avance": _limpiar(row[10]),
            "fecha_requerida": _limpiar(row[11]),
            "fecha_prog_inicio": _limpiar(row[12]),
            "fecha_prog_fin": _limpiar(row[13]),
            "fecha_real_inicio": _limpiar(row[14]),
            "fecha_real_fin": _limpiar(row[15]),
            "atraso_dias": _limpiar(row[16]),
            "prioridad_operativa": _limpiar(row[17]),
            "riesgo_bloqueo": _limpiar(row[18]),
            "comentarios": _limpiar(row[19]),
            "ultima_modificacion_fecha": _limpiar(row[20]),
            "ultima_modificacion_usuario": _limpiar(row[21]),
        })

    wb.close()
    return filas


def leer_todos_los_insumos() -> dict[str, Any]:
    """
    Lee ambos archivos de insumos y retorna todo en un diccionario.

    Estructura del retorno:
      {
        "meses": { "Meses ERA ECOTANK": [...], "Meses Petrini": [...], "Meses LCDT": [...] },
        "requerimientos_logistica": [...],
      }
    """
    datos_meses = leer_todas_las_hojas_meses(ARCHIVO_MESES)
    datos_req = leer_requerimientos_logistica(ARCHIVO_REQ)

    return {
        "meses": datos_meses,
        "requerimientos_logistica": datos_req,
    }


if __name__ == "__main__":
    datos = leer_todos_los_insumos()
    print("=== Hojas 'Meses ...' ===")
    for nombre, filas in datos["meses"].items():
        print(f"  {nombre}: {len(filas)} productos")
    print("=== Requerimientos de logística ===")
    print(f"  {len(datos['requerimientos_logistica'])} requerimientos")
    print("\nVerificación completada: Insumos leídos sin modificarse.")
