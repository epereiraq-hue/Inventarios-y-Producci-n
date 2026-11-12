# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 4: regla R2 meses de stock actual."""
from inventarios_produccion.app.services.reglas import meses_stock_actual

# Caso 1: inventario 100, promedio 20 -> 5 meses
resultado = meses_stock_actual(100, 20)
print(f"Caso 1 - inv=100, prom=20: {resultado} (esperado: 5.0)")
assert resultado == 5.0

# Caso 2: inventario 0, promedio 10 -> 0 meses
resultado = meses_stock_actual(0, 10)
print(f"Caso 2 - inv=0, prom=10: {resultado} (esperado: 0.0)")
assert resultado == 0.0

# Caso 3: promedio 0 -> None (división por cero)
resultado = meses_stock_actual(50, 0)
print(f"Caso 3 - inv=50, prom=0: {resultado} (esperado: None)")
assert resultado is None

# Caso 4: inventario 37.5, promedio 7.5 -> 5 meses
resultado = meses_stock_actual(37.5, 7.5)
print(f"Caso 4 - inv=37.5, prom=7.5: {resultado} (esperado: 5.0)")
assert resultado == 5.0

print("\nTodas las pruebas de R2 pasaron correctamente.")
