# -*- coding: utf-8 -*-
"""Punto de entrada WSGI para despliegue (Render, Gunicorn, etc.)."""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe (desarrollo local)
load_dotenv()

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
