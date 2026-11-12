# -*- coding: utf-8 -*-
"""Controladores de la app. Se registran como blueprints en create_app()."""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

from inventarios_produccion.app.controllers import routes  # noqa: F401
from inventarios_produccion.app.controllers.agente_ia import agente_ia_bp  # noqa: F401
from inventarios_produccion.app.controllers.reportes import reportes_bp  # noqa: F401
