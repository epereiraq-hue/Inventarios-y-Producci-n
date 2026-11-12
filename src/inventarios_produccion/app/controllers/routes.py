# -*- coding: utf-8 -*-
"""Rutas principales de la app."""

import os
from functools import wraps
from flask import render_template, redirect, url_for, request, session, flash
from inventarios_produccion.app.controllers import main_bp

APP_USUARIO = os.environ.get("APP_USUARIO", "")
APP_CLAVE = os.environ.get("APP_CLAVE", "")


def login_required(f):
    """Decorador que exige autenticación para acceder a una ruta."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """Página de inicio de sesión."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")
        if usuario == APP_USUARIO and clave == APP_CLAVE:
            session["usuario"] = usuario
            flash("Bienvenido, " + usuario, "success")
            return redirect(url_for("main.inicio"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")


@main_bp.route("/salir")
def salir():
    """Cerrar sesión."""
    session.pop("usuario", None)
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("main.login"))


@main_bp.route("/")
@login_required
def inicio():
    """Página de inicio."""
    return render_template("inicio.html")
