# -*- coding: utf-8 -*-
"""
Reglas de negocio determinísticas para la app de planificación de inventarios.

Toda la lógica de negocio reside aquí: una función por regla, cada una con su
comentario explicativo. No hay IA generativa en estas reglas.
"""


def promedio_mensual(ventas_6m: list[float]) -> float:
    """
    R1: Promedio mensual de ventas (ventana móvil de 6 meses).

    Entrada: lista de 6 números con las ventas en unidades de los últimos 6 meses.
    Salida: promedio mensual (suma / 6).
    Si la lista está vacía, retorna 0.0.
    """
    if not ventas_6m:
        return 0.0
    return sum(ventas_6m) / len(ventas_6m)


def meses_stock_actual(inventario_actual: float, promedio: float) -> float | None:
    """
    R2: Meses de stock actual.

    Entrada: inventario_actual (unidades) y promedio_mensual (unidades/mes).
    Salida: inventario_actual / promedio_mensual.
    Si promedio == 0, retorna None (división por cero).
    """
    if promedio == 0:
        return None
    return inventario_actual / promedio


def clasificacion(meses_stock: float | None, target_min: float | None, target_max: float | None) -> str:
    """
    R4: Clasificación de inventario.

    Entrada: meses_stock_actual, target_min, target_max.
    Salida: SOBRESTOCK / SALUDABLE / CRÍTICO / SIN_DATOS.
    """
    if meses_stock is None:
        return "SIN_DATOS"
    if target_min is None or target_max is None:
        return "SIN_DATOS"
    if meses_stock > target_max:
        return "SOBRESTOCK"
    if meses_stock < target_min:
        return "CRÍTICO"
    return "SALUDABLE"


def sugerido_pedido(meses_stock: float | None, target_min: float | None, target_max: float | None, promedio: float) -> tuple[float, list[str]]:
    """
    R3: Sugerido de pedido (reposición).

    Entrada: meses_stock_actual, target_min, target_max, promedio_mensual.
    Salida: (sugerido, validaciones).
      - si meses_stock < target_min: sugerido = (target_max - meses_stock) * promedio
      - si meses_stock > target_max: sugerido = 0 (sobrestock)
      - otro caso: sugerido = 0 (saludable)
    """
    validaciones: list[str] = []

    if target_min is None or target_max is None:
        validaciones.append("SIN_TARGET")
    if promedio == 0:
        validaciones.append("PROMEDIO_CERO")

    if validaciones:
        return 0.0, validaciones

    if meses_stock is None:
        validaciones.append("MESES_STOCK_INDEFINIDO")
        return 0.0, validaciones

    if meses_stock < target_min:
        sugerido = (target_max - meses_stock) * promedio
    elif meses_stock > target_max:
        sugerido = 0.0
    else:
        sugerido = 0.0

    return sugerido, validaciones


def accion_sugerida(clasificacion_valor: str) -> str:
    """
    R5: Acción sugerida según la clasificación.

    Entrada: clasificación (SOBRESTOCK / SALUDABLE / CRÍTICO / SIN_DATOS).
    Salida: acción sugerida (PRODUCIR / MONITOREAR / CONGELAR PROMOCION / REVISAR MANUALMENTE).
    """
    mapa = {
        "SOBRESTOCK": "CONGELAR / PROMOCION",
        "SALUDABLE": "MONITOREAR",
        "CRÍTICO": "PRODUCIR",
        "SIN_DATOS": "REVISAR MANUALMENTE",
    }
    return mapa.get(clasificacion_valor, "REVISAR MANUALMENTE")


def validar_reporte(ventas_6m: list[float], inventario_actual: float, target_min: float | None, target_max: float | None) -> list[str]:
    """
    R6: Validación obligatoria antes de usar el reporte.

    Entrada: ventas_6m, inventario_actual, target_min, target_max.
    Salida: lista de errores de validación (vacía si todo está correcto).
    - ventas_6m no puede tener todos ceros sin justificación
    - inventario_actual >= 0
    - target_min y target_max deben existir para la familia
    """
    errores: list[str] = []

    if ventas_6m is None or all(v == 0 for v in ventas_6m):
        errores.append("VENTAS_CEROS")

    if inventario_actual is None or inventario_actual < 0:
        errores.append("INVENTARIO_INVALIDO")

    if target_min is None or target_max is None:
        errores.append("SIN_TARGET")

    return errores
