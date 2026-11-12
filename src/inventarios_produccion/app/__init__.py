# -*- coding: utf-8 -*-
"""Paquete principal de la app Flask. Patrón MVC gestionado con uv."""

import os

from flask import Flask


def create_app():
    """Crea y configura la aplicación Flask.

    Registra los blueprints de los controladores y carga la configuración
    desde el archivo .env (variables de entorno).
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DEBUG=os.environ.get("FLASK_DEBUG", "1") == "1",
    )

    from inventarios_produccion.app.controllers import main_bp
    app.register_blueprint(main_bp)

    from inventarios_produccion.app.controllers.agente_ia import agente_ia_bp
    app.register_blueprint(agente_ia_bp)

    from inventarios_produccion.app.controllers.reportes import reportes_bp
    app.register_blueprint(reportes_bp)

    return app
