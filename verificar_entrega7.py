# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 7: regla R6 validación obligatoria."""
from inventarios_produccion.app.services.reglas import validar_reporte

print("=== R6: Validación obligatoria ===")

# Caso 1: todo correcto -> sin errores
e = validar_reporte([10, 20, 30, 40, 50, 60], 100, 1.5, 2.5)
print("Caso 1 - todo correcto:", e, "(esperado: [])")
assert e == []

# Caso 2: ventas todos ceros -> VENTAS_CEROS
e = validar_reporte([0, 0, 0, 0, 0, 0], 100, 1.5, 2.5)
print("Caso 2 - ventas ceros:", e, "(esperado: ['VENTAS_CEROS'])")
assert "VENTAS_CEROS" in e

# Caso 3: inventario negativo -> INVENTARIO_INVALIDO
e = validar_reporte([10, 20, 30, 40, 50, 60], -5, 1.5, 2.5)
print("Caso 3 - inventario negativo:", e, "(esperado: ['INVENTARIO_INVALIDO'])")
assert "INVENTARIO_INVALIDO" in e

# Caso 4: target ausente -> SIN_TARGET
e = validar_reporte([10, 20, 30, 40, 50, 60], 100, None, 2.5)
print("Caso 4 - target_min ausente:", e, "(esperado: ['SIN_TARGET'])")
assert "SIN_TARGET" in e

# Caso 5: ventas ceros + inventario negativo + sin target -> 3 errores
e = validar_reporte([0, 0, 0, 0, 0, 0], -5, None, None)
print("Caso 5 - todo mal:", e, "(esperado: 3 errores)")
assert "VENTAS_CEROS" in e
assert "INVENTARIO_INVALIDO" in e
assert "SIN_TARGET" in e
assert len(e) == 3

print("\nTodas las pruebas de R6 pasaron correctamente.")
