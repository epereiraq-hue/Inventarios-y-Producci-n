# -*- coding: utf-8 -*-
"""Controladores de la app. Se registran como blueprints en create_app()."""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

# Importar rutas para registrar los endpoints
from app.controllers import routes  # noqa: F401
