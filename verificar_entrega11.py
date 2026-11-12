# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 11: pantalla de resultados."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 11: Pantalla de resultados ===")

# Caso 1: Ruta /resultados carga correctamente
resp = client.get("/resultados")
print("\nCaso 1 - Página de resultados:")
print("  Status:", resp.status_code)
html = resp.data.decode("utf-8")
print("  Tiene título:", "Reporte de Inventarios" in html)
print("  Tiene contadores:", "Tablero de Control" in html)
print("  Tiene filtros:", "Filtros" in html)
print("  Tiene tabla:", "Detalle por Producto" in html)
assert resp.status_code == 200
assert "Reporte de Inventarios" in html
assert "Tablero de Control" in html
assert "Filtros" in html
assert "Detalle por Producto" in html

# Caso 2: Contadores grandes presentes
assert "Críticas" in html
assert "Saludables" in html
assert "Alerta" in html
assert "Sobrestock" in html
assert "Inventario Total" in html
assert "Demanda Mensual" in html
assert "Meses Stock Global" in html

# Caso 3: Tabla con encabezados
assert "Origen" in html
assert "Empresa" in html
assert "Sucursal" in html
assert "Clasificación" in html
assert "Acción Sugerida" in html
assert "Sugerido Pedido" in html

# Caso 4: Datos de registros presentes (debe haber 324 productos)
assert "PROD000" in html  # códigos de producto

# Caso 5: CSS de contadores y badges
assert "contadores-grid" in html
assert "badge-critico" in html
assert "badge-saludable" in html

# Caso 6: JavaScript de filtro
assert "filtrarTabla" in html
assert "limpiarFiltros" in html

# Caso 7: Navbar actualizado
assert "Resultados" in html

print("\nTodas las pruebas de la entrega 11 pasaron correctamente.")
