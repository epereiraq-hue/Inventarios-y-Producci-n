# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 13: Estilo de la app."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 13: Estilo de la app ===")

# Caso 1: base.html tiene CSS embebido
with open("src/inventarios_produccion/app/templates/base.html", encoding="utf-8") as f:
    base_html = f.read()
tiene_style_base = "<style>" in base_html
print("\nCaso 1 - base.html tiene CSS embebido:")
print("  Tiene etiqueta <style>:", tiene_style_base)
assert tiene_style_base

# Caso 2: resultados.html tiene CSS embebido
with open("src/inventarios_produccion/app/templates/resultados.html", encoding="utf-8") as f:
    resultados_html = f.read()
tiene_style_resultados = "<style>" in resultados_html
print("\nCaso 2 - resultados.html tiene CSS embebido:")
print("  Tiene etiqueta <style>:", tiene_style_resultados)
assert tiene_style_resultados

# Caso 3: detalle.html tiene CSS embebido
with open("src/inventarios_produccion/app/templates/detalle.html", encoding="utf-8") as f:
    detalle_html = f.read()
tiene_style_detalle = "<style>" in detalle_html
print("\nCaso 3 - detalle.html tiene CSS embebido:")
print("  Tiene etiqueta <style>:", tiene_style_detalle)
assert tiene_style_detalle

# Caso 4: No hay librerías externas de JavaScript
tiene_js_externo_base = 'src="http' in base_html or 'src="https' in base_html
tiene_js_externo_resultados = 'src="http' in resultados_html or 'src="https' in resultados_html
tiene_js_externo_detalle = 'src="http' in detalle_html or 'src="https' in detalle_html
print("\nCaso 4 - Sin librerías externas de JavaScript:")
print("  base.html sin JS externo:", not tiene_js_externo_base)
print("  resultados.html sin JS externo:", not tiene_js_externo_resultados)
print("  detalle.html sin JS externo:", not tiene_js_externo_detalle)
assert not tiene_js_externo_base
assert not tiene_js_externo_resultados
assert not tiene_js_externo_detalle

# Caso 5: Página de inicio carga con estilos
resp = client.get("/")
html_inicio = resp.data.decode("utf-8")
print("\nCaso 5 - Página de inicio con estilos:")
print("  Status:", resp.status_code)
print("  Tiene <style>:", "<style>" in html_inicio)
assert resp.status_code == 200
assert "<style>" in html_inicio

# Caso 6: Página de resultados carga con estilos
resp2 = client.get("/resultados")
html_resultados = resp2.data.decode("utf-8")
print("\nCaso 6 - Página de resultados con estilos:")
print("  Status:", resp2.status_code)
print("  Tiene <style>:", "<style>" in html_resultados)
assert resp2.status_code == 200
assert "<style>" in html_resultados

# Caso 7: Diseño profesional - elementos clave de estilo
elementos_estilo = [
    "navbar", "btn-primary", "card", "contadores-grid",
    "badge-critico", "badge-saludable", "enlace-detalle",
]
for elem in elementos_estilo:
    presente = elem in html_inicio or elem in html_resultados
    print("  Estilo '%s': %s" % (elem, "OK" if presente else "FALTA"))
    assert presente, "Falta estilo: %s" % elem

print("\nTodas las pruebas de la entrega 13 pasaron correctamente.")
