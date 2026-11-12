# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 9: descarga de resultados CSV."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 9: Descarga de resultados CSV ===")

# Caso 1: Preview del reporte
resp = client.get("/api/reportes/preview")
print("\nCaso 1 - Preview del reporte:")
print("  Status:", resp.status_code)
data = resp.get_json()
print("  Total registros:", data.get("total_registros"))
print("  Preview (primeras 2 líneas):")
for linea in data.get("preview", [])[:2]:
    print("   ", linea[:120])
assert resp.status_code == 200
assert data["total_registros"] > 0
assert len(data["preview"]) > 0

# Caso 2: Descarga del CSV
resp2 = client.get("/api/reportes/descargar")
print("\nCaso 2 - Descarga CSV:")
print("  Status:", resp2.status_code)
print("  Content-Type:", resp2.content_type)
print("  Content-Disposition:", resp2.headers.get("Content-Disposition"))
assert resp2.status_code == 200
assert "text/csv" in resp2.content_type
assert "Reporte_Inventarios_Automatizado.csv" in str(resp2.headers.get("Content-Disposition"))

# Verificar que el CSV tenga las columnas esperadas
csv_texto = resp2.data.decode("utf-8")
lineas = csv_texto.splitlines()
print("  Columnas:", lineas[0])
print("  Filas de datos:", len(lineas) - 1)
assert "origen_hoja" in lineas[0]
assert "empresa" in lineas[0]
assert "clasificacion" in lineas[0]
assert "sugerido_pedido" in lineas[0]

print("\nTodas las pruebas de la entrega 9 pasaron correctamente.")
