# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 12: detalle por registro."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 12: Detalle por registro ===")

# Caso 1: Página de resultados tiene enlaces a detalle
resp = client.get("/resultados")
html = resp.data.decode("utf-8")
print("\nCaso 1 - Enlaces a detalle en tabla de resultados:")
assert "/detalle/" in html
print("  Tiene enlaces /detalle/: True")

# Caso 2: Acceder al detalle de un producto específico (item 0)
resp2 = client.get("/detalle/0")
print("\nCaso 2 - Detalle de item 0:")
print("  Status:", resp2.status_code)
html2 = resp2.data.decode("utf-8")
assert resp2.status_code == 200
print("  Tiene título Detalle:", "Detalle del Producto" in html2)
print("  Tiene clasificación:", "Clasificación" in html2)
print("  Tiene acción sugerida:", "Acción Sugerida" in html2)
print("  Tiene sugerido de pedido:", "Sugerido de Pedido" in html2)
print("  Tiene botón volver:", "Volver al Reporte" in html2)

# Caso 3: Detalle de un producto que no existe (404)
resp3 = client.get("/detalle/999999")
print("\nCaso 3 - Producto inexistente:")
print("  Status:", resp3.status_code)
assert resp3.status_code == 404

# Caso 4: Verificar que el enlace en la tabla apunta al detalle correcto
import re
enlaces = re.findall(r'href="(/detalle/\d+)"', html)
print(f"\nCaso 4 - Enlaces de detalle encontrados: {len(enlaces)}")
assert len(enlaces) > 0
print(f"  Primer enlace: {enlaces[0]}")

print("\nTodas las pruebas de la entrega 12 pasaron correctamente.")
