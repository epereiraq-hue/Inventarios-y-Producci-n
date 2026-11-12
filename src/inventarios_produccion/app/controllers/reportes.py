# -*- coding: utf-8 -*-
"""Controlador de reportes. Endpoint para descargar el reporte de inventarios
en formato CSV, generado aplicando las reglas de negocio R1-R6."""

import csv
import io
import os
from flask import Blueprint, request, jsonify, send_file

from inventarios_produccion.app.services.lectura_insumos import (
    leer_todos_los_insumos,
    leer_requerimientos_logistica,
)
from inventarios_produccion.app.services.reglas import (
    promedio_mensual,
    meses_stock_actual,
    clasificacion,
    sugerido_pedido,
    accion_sugerida,
    validar_reporte,
)

reportes_bp = Blueprint("reportes", __name__)


def _obtener_targets() -> dict:
    """Lee Target_Min / Target_Max por familia desde la hoja 'Tabla Target'."""
    import openpyxl
    import os

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    BASE_DIR = os.path.dirname(BASE_DIR)
    ARCHIVO_MESES = os.path.join(BASE_DIR, "Insumos", "Meses de inventario x Producto.xlsx")

    targets = {}
    wb = openpyxl.load_workbook(ARCHIVO_MESES, data_only=True)
    if "Tabla Target" in wb.sheetnames:
        ws = wb["Tabla Target"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            familia = row[0]
            tmin = row[1]
            tmax = row[2]
            if familia is not None and str(familia).strip() != "":
                try:
                    targets[str(familia).strip()] = (float(tmin), float(tmax))
                except (TypeError, ValueError):
                    targets[str(familia).strip()] = (None, None)
    wb.close()
    return targets


def _procesar_fila(fila: dict, hoja: str, empresa: str, sucursal: str, targets: dict) -> dict:
    """Aplica las reglas R1-R6 a una fila de producto y retorna el registro del reporte."""
    codigo = fila.get("codigo")
    descripcion = fila.get("descripcion")
    familia = fila.get("familia")
    ventas_mensuales = []
    for i in range(1, 8):
        v = fila.get(f"ventas_mes_{i}")
        ventas_mensuales.append(float(v) if v is not None else 0.0)

    ventas_6m = ventas_mensuales[-6:] if len(ventas_mensuales) >= 6 else ventas_mensuales
    inventario_actual = float(fila.get("inventario_04_11_2026") or 0)

    tmin, tmax = targets.get(str(familia).strip() if familia else "", (None, None))

    validaciones = validar_reporte(ventas_6m, inventario_actual, tmin, tmax)
    promedio = promedio_mensual(ventas_6m)
    meses_stock = meses_stock_actual(inventario_actual, promedio)
    clasificacion_valor = clasificacion(meses_stock, tmin, tmax)
    sugerido, validaciones_calc = sugerido_pedido(meses_stock, tmin, tmax, promedio)
    todas_validaciones = list(set(validaciones + validaciones_calc))
    accion = accion_sugerida(clasificacion_valor)

    return {
        "origen_hoja": hoja,
        "empresa": empresa,
        "sucursal": sucursal,
        "item": fila.get("item"),
        "codigo": codigo,
        "descripcion": descripcion,
        "familia": familia,
        "ventas_mes_1": ventas_mensuales[0] if len(ventas_mensuales) > 0 else 0,
        "ventas_mes_2": ventas_mensuales[1] if len(ventas_mensuales) > 1 else 0,
        "ventas_mes_3": ventas_mensuales[2] if len(ventas_mensuales) > 2 else 0,
        "ventas_mes_4": ventas_mensuales[3] if len(ventas_mensuales) > 3 else 0,
        "ventas_mes_5": ventas_mensuales[4] if len(ventas_mensuales) > 4 else 0,
        "ventas_mes_6": ventas_mensuales[5] if len(ventas_mensuales) > 5 else 0,
        "promedio_mensual": round(promedio, 4),
        "meses_stock_actual": round(meses_stock, 4) if meses_stock is not None else "",
        "clasificacion": clasificacion_valor,
        "accion_sugerida": accion,
        "sugerido_pedido": round(sugerido, 4),
        "validaciones": ";".join(todas_validaciones) if todas_validaciones else "",
        "origen_calculo": "recalculado_desde_ventas_6m",
    }


def _empresa_de_hoja(nombre_hoja: str) -> str:
    nombre = (nombre_hoja or "").upper()
    if "PETRINI" in nombre:
        return "EMP1"
    if "LCDT" in nombre:
        return "EMP2"
    return "POR_CONFIRMAR"


def _sucursal_de_hoja(nombre_hoja: str) -> str:
    nombre = (nombre_hoja or "").upper()
    if "ERA ECOTANK" in nombre:
        return "Coyol (por confirmar)"
    return "POR_CONFIRMAR"


def generar_reporte_csv() -> str:
    """Genera el contenido CSV del reporte aplicando R1-R6 a todos los productos."""
    datos = leer_todos_los_insumos()
    targets = _obtener_targets()

    filas_reporte = []
    for hoja, filas in datos["meses"].items():
        empresa = _empresa_de_hoja(hoja)
        sucursal = _sucursal_de_hoja(hoja)
        for fila in filas:
            filas_reporte.append(_procesar_fila(fila, hoja, empresa, sucursal, targets))

    filas_reporte.sort(key=lambda r: (r["empresa"], str(r["familia"] or ""), str(r["item"] or "")))

    fieldnames = [
        "origen_hoja", "empresa", "sucursal", "item", "codigo", "descripcion",
        "familia",
        "ventas_mes_1", "ventas_mes_2", "ventas_mes_3",
        "ventas_mes_4", "ventas_mes_5", "ventas_mes_6",
        "promedio_mensual", "meses_stock_actual",
        "clasificacion", "accion_sugerida", "sugerido_pedido",
        "validaciones", "origen_calculo",
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for r in filas_reporte:
        writer.writerow(r)

    return output.getvalue()


@reportes_bp.route("/api/reportes/descargar", methods=["GET"])
def descargar_reporte():
    """Endpoint para descargar el reporte de inventarios en CSV."""
    csv_contenido = generar_reporte_csv()
    return send_file(
        io.BytesIO(csv_contenido.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="Reporte_Inventarios_Automatizado.csv",
    )


@reportes_bp.route("/api/reportes/preview", methods=["GET"])
def preview_reporte():
    """Endpoint para obtener una vista previa del reporte en JSON."""
    csv_contenido = generar_reporte_csv()
    lineas = csv_contenido.splitlines()
    preview = lineas[1:11] if len(lineas) > 1 else []
    return jsonify({
        "total_registros": max(0, len(lineas) - 1),
        "preview": preview,
    })


@reportes_bp.route("/resultados", methods=["GET"])
def resultados():
    """Pantalla de resultados con contadores y tabla con filtro."""
    from flask import render_template
    csv_contenido = generar_reporte_csv()
    lineas = csv_contenido.splitlines()
    if len(lineas) <= 1:
        return render_template("resultados.html", registros=[], contadores={})

    import csv as csv_mod
    reader = csv_mod.DictReader(io.StringIO(csv_contenido))
    registros = list(reader)

    # Calcular contadores (cifras de control)
    total = len(registros)
    críticas = sum(1 for r in registros if r["clasificacion"] == "CRÍTICO")
    saludables = sum(1 for r in registros if r["clasificacion"] == "SALUDABLE")
    sobrestock = sum(1 for r in registros if r["clasificacion"] == "SOBRESTOCK")
    alerta = sum(1 for r in registros if r["validaciones"] and "SIN_TARGET" in r["validaciones"])
    inventario_total = sum(float(r["meses_stock_actual"] or 0) * float(r["promedio_mensual"] or 0) for r in registros if r["promedio_mensual"] and r["meses_stock_actual"])
    demanda_mensual = sum(float(r["promedio_mensual"] or 0) for r in registros if r["promedio_mensual"])
    meses_stock_global = round(inventario_total / demanda_mensual, 2) if demanda_mensual > 0 else 0

    contadores = {
        "criticas": críticas,
        "saludables": saludables,
        "sobrestock": sobrestock,
        "alerta": alerta,
        "inventario_total": round(inventario_total, 2),
        "demanda_mensual": round(demanda_mensual, 2),
        "meses_stock_global": meses_stock_global,
    }

    return render_template("resultados.html", registros=registros, contadores=contadores)


def _buscar_producto_por_item(item: int) -> dict | None:
    """Busca un producto por su número de item en todas las hojas de insumos."""
    datos = leer_todos_los_insumos()
    targets = _obtener_targets()

    # Construir ruta al archivo de requerimientos (misma lógica que _obtener_targets)
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    BASE_DIR = os.path.dirname(BASE_DIR)
    ARCHIVO_REQ = os.path.join(BASE_DIR, "Insumos", "Requerimientos Logística.xlsx")

    for hoja, filas in datos["meses"].items():
        for fila in filas:
            if fila.get("item") == item:
                empresa = _empresa_de_hoja(hoja)
                sucursal = _sucursal_de_hoja(hoja)
                registro = _procesar_fila(fila, hoja, empresa, sucursal, targets)

                # Buscar requerimiento de logística por código Dynamics o Best
                codigo = registro.get("codigo")
                req = None
                if codigo:
                    datos_req = leer_requerimientos_logistica(ARCHIVO_REQ)
                    for r in datos_req:
                        if str(r.get("codigo_dynamics")) == str(codigo) or str(r.get("codigo_best")) == str(codigo):
                            req = r
                            break

                return {
                    "registro": registro,
                    "hoja": hoja,
                    "requerimiento": req,
                }

    return None


@reportes_bp.route("/detalle/<int:item>", methods=["GET"])
def detalle(item: int):
    """Pantalla de detalle por registro (producto específico)."""
    from flask import render_template, abort

    resultado = _buscar_producto_por_item(item)
    if resultado is None:
        abort(404)

    return render_template(
        "detalle.html",
        registro=resultado["registro"],
        hoja=resultado["hoja"],
        requerimiento=resultado["requerimiento"],
    )
