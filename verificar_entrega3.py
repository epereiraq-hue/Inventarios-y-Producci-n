# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 3: regla R1 promedio mensual."""
from inventarios_produccion.app.services.reglas import promedio_mensual

# Caso 1: ventas normales (del ejemplo de AGENTS.md: [0, 22, 16, 0, 0, 0])
resultado = promedio_mensual([0, 22, 16, 0, 0, 0])
esperado = 6.333333333333333
print(f"Caso 1 - ventas [0, 22, 16, 0, 0, 0]: {resultado} (esperado: {esperado})")
assert abs(resultado - esperado) < 1e-9, f"Fallo: {resultado} != {esperado}"

# Caso 2: lista vacía
resultado = promedio_mensual([])
print(f"Caso 2 - lista vacía: {resultado} (esperado: 0.0)")
assert resultado == 0.0

# Caso 3: todos ceros
resultado = promedio_mensual([0, 0, 0, 0, 0, 0])
print(f"Caso 3 - todos ceros: {resultado} (esperado: 0.0)")
assert resultado == 0.0

# Caso 4: ventas positivas
resultado = promedio_mensual([10, 20, 30, 40, 50, 60])
print(f"Caso 4 - [10, 20, 30, 40, 50, 60]: {resultado} (esperado: 35.0)")
assert resultado == 35.0

print("\nTodas las pruebas de R1 pasaron correctamente.")
