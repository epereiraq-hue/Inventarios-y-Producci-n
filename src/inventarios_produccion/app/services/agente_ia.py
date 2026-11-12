# -*- coding: utf-8 -*-
"""Servicio del agente de IA para la app de planificación de inventarios.

Recibe datos ya limpios y devuelve una propuesta de reposición en JSON,
aplicando las reglas de negocio R1-R6 determinísticas. No inventa reglas ni
columnas. La llave de la IA se lee de .env (nunca escrita en el código).
"""

import os
from typing import Any

from inventarios_produccion.app.services.reglas import (
    promedio_mensual,
    meses_stock_actual,
    clasificacion,
    sugerido_pedido,
    accion_sugerida,
    validar_reporte,
)


def leer_llave_ia() -> str | None:
    """Lee la llave de la IA desde el archivo .env o variable de entorno."""
    return os.environ.get("IA_API_KEY")


def procesar_producto(datos: dict) -> dict:
    """Procesa un producto aplicando las reglas de negocio R1-R6."""
    producto_id = datos.get("producto_id")
    codigo_best = datos.get("codigo_best")
    descripcion = datos.get("descripcion")
    familia = datos.get("familia")
    empresa = datos.get("empresa")
    sucursal = datos.get("sucursal")
    ventas_6m = datos.get("ventas_6m") or []
    inventario_actual = datos.get("inventario_actual") or 0
    target_min = datos.get("target_min")
    target_max = datos.get("target_max")

    # Validación obligatoria R6
    validaciones = validar_reporte(ventas_6m, inventario_actual, target_min, target_max)

    # R1: promedio mensual
    promedio = promedio_mensual(ventas_6m)

    # R2: meses de stock actual
    meses_stock = meses_stock_actual(inventario_actual, promedio)

    # R4 + R3: clasificación y sugerido de pedido
    clasificacion_valor = clasificacion(meses_stock, target_min, target_max)
    sugerido, validaciones_calc = sugerido_pedido(
        meses_stock, target_min, target_max, promedio
    )

    # Unir validaciones de R6 y de cálculo
    todas_validaciones = list(set(validaciones + validaciones_calc))

    # R5: acción sugerida
    accion = accion_sugerida(clasificacion_valor)

    return {
        "producto_id": producto_id,
        "codigo_best": codigo_best,
        "descripcion": descripcion,
        "familia": familia,
        "empresa": empresa,
        "sucursal": sucursal,
        "promedio_mensual": round(promedio, 4),
        "meses_stock_actual": round(meses_stock, 4) if meses_stock is not None else None,
        "clasificacion": clasificacion_valor,
        "accion_sugerida": accion,
        "sugerido_pedido": round(sugerido, 4),
        "validaciones": todas_validaciones,
        "origen_calculo": "recalculado_desde_ventas_6m",
    }
