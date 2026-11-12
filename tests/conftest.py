# -*- coding: utf-8 -*-
"""Configuración de pytest para el proyecto de planificación de inventarios.

Configura pythonpath para que las pruebas puedan importar el código de la app.
Proporciona fixtures reutilizables (cliente de prueba de Flask).
"""

import os
import sys

# Configurar pythonpath para importar el paquete de la app
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import pytest  # noqa: E402

from inventarios_produccion.app import create_app  # noqa: E402


@pytest.fixture
def app():
    """Crea una instancia de la app Flask para pruebas."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Proporciona un cliente de prueba de Flask."""
    return app.test_client()
