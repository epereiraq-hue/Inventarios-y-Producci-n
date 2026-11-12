# -*- coding: utf-8 -*-
"""Paquete principal de la app Flask. Patrón MVC gestionado con uv."""

import os

from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Las plantillas HTML residen en src/inventarios_produccion/app/templates/
TEMPLATES_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "..", "src", "inventarios_produccion", "app", "templates")
)


def create_app():
    """Crea y configura la aplicación Flask.

    Registra los blueprints de los controladores y carga la configuración
    desde el archivo .env (variables de entorno).
    """
    app = Flask(__name__, instance_relative_config=True,
                template_folder=TEMPLATES_DIR)

    # Configuración básica
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DEBUG=os.environ.get("FLASK_DEBUG", "1") == "1",
    )

    # Registrar blueprints de controladores
    from app.controllers import main_bp
    app.register_blueprint(main_bp)

    return app
