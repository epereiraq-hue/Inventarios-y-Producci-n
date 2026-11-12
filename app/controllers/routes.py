# -*- coding: utf-8 -*-
"""Rutas principales de la app."""

from flask import render_template
from app.controllers import main_bp


@main_bp.route("/")
def inicio():
    """Página de inicio."""
    return render_template("inicio.html")
