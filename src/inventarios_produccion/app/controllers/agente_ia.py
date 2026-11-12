# -*- coding: utf-8 -*-
"""Controlador del agente de IA. Endpoint que recibe JSON y devuelve JSON."""

from flask import Blueprint, request, jsonify
from inventarios_produccion.app.services.agente_ia import (
    procesar_producto,
    leer_llave_ia,
)

agente_ia_bp = Blueprint("agente_ia", __name__)


@agente_ia_bp.route("/api/agente-ia", methods=["POST"])
def agente_ia():
    """Endpoint del agente de IA."""
    llave = leer_llave_ia()
    if llave is None:
        pass

    datos = request.get_json(silent=True)
    if datos is None:
        return jsonify({"error": "Se requiere JSON en el cuerpo de la petición"}), 400

    producto_id = datos.get("producto_id")
    if not producto_id or not str(producto_id).strip():
        return jsonify({"error": "Falta campo obligatorio: producto_id"}), 400

    if len(str(producto_id)) > 100:
        return jsonify({"error": "producto_id demasiado largo (máx. 100 caracteres)"}), 400

    if "ventas_6m" not in datos:
        return jsonify({"error": "Falta campo obligatorio: ventas_6m"}), 400

    resultado = procesar_producto(datos)
    return jsonify(resultado), 200
