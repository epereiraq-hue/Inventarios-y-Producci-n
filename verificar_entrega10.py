# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 10: pantalla de inicio."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 10: Pantalla de inicio ===")

# Caso 1: Ruta principal carga correctamente
resp = client.get("/")
print("\nCaso 1 - Página de inicio:")
print("  Status:", resp.status_code)
html = resp.data.decode("utf-8")
print("  Tiene título:", "Planificación y Control de Inventarios" in html)
print("  Tiene propósito:", "Reporte automatizado" in html)
print("  Tiene botón resultados:", "Ver Reporte de Inventarios" in html)
print("  Tiene enlace agente IA:", "Agente de IA" in html)
print("  Tiene empresas:", "EMP1" in html and "EMP2" in html)
assert resp.status_code == 200
assert "Planificación y Control de Inventarios" in html
assert "Reporte automatizado" in html
assert "Ver Reporte de Inventarios" in html
assert "Agente de IA" in html

# Caso 2: Navbar funciona
assert "Inicio" in html
assert "Resultados" in html

# Caso 3: CSS embebido en base.html
assert "<style>" in html
assert "navbar" in html.lower()
assert "btn-primary" in html

print("\nTodas las pruebas de la entrega 10 pasaron correctamente.")
