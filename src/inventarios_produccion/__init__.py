# -*- coding: utf-8 -*-
"""Paquete inventarios_produccion."""

def main():
    """Punto de entrada para el script de consola definido en pyproject.toml."""
    from inventarios_produccion.app import create_app
    app = create_app()
    app.run()
