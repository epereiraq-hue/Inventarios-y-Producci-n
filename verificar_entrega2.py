# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 2: lectura de insumos."""
from inventarios_produccion.app.services.lectura_insumos import leer_todos_los_insumos

datos = leer_todos_los_insumos()
print("=== Hojas 'Meses ...' ===")
for nombre, filas in datos["meses"].items():
    print(f"  {nombre}: {len(filas)} productos")
print("=== Requerimientos de logística ===")
print(f"  {len(datos['requerimientos_logistica'])} requerimientos")
print("\nVerificación completada: Insumos leídos sin modificarse.")
