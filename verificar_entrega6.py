# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 6: regla R5 acción sugerida."""
from inventarios_produccion.app.services.reglas import accion_sugerida

print("=== R5: Acción sugerida ===")

# Caso 1: SOBRESTOCK -> CONGELAR / PROMOCION
a = accion_sugerida("SOBRESTOCK")
print("Caso 1 - SOBRESTOCK:", a, "(esperado: CONGELAR / PROMOCION)")
assert a == "CONGELAR / PROMOCION"

# Caso 2: SALUDABLE -> MONITOREAR
a = accion_sugerida("SALUDABLE")
print("Caso 2 - SALUDABLE:", a, "(esperado: MONITOREAR)")
assert a == "MONITOREAR"

# Caso 3: CRÍTICO -> PRODUCIR
a = accion_sugerida("CRÍTICO")
print("Caso 3 - CRÍTICO:", a, "(esperado: PRODUCIR)")
assert a == "PRODUCIR"

# Caso 4: SIN_DATOS -> REVISAR MANUALMENTE
a = accion_sugerida("SIN_DATOS")
print("Caso 4 - SIN_DATOS:", a, "(esperado: REVISAR MANUALMENTE)")
assert a == "REVISAR MANUALMENTE"

# Caso 5: clasificación desconocida -> REVISAR MANUALMENTE
a = accion_sugerida("DESCONOCIDO")
print("Caso 5 - DESCONOCIDO:", a, "(esperado: REVISAR MANUALMENTE)")
assert a == "REVISAR MANUALMENTE"

print("\nTodas las pruebas de R5 pasaron correctamente.")
