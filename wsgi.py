# -*- coding: utf-8 -*-
"""Punto de entrada WSGI para despliegue."""

from inventarios_produccion.app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
