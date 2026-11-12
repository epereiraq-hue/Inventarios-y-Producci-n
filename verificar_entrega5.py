# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 5: reglas R3 y R4."""
from inventarios_produccion.app.services.reglas import clasificacion, sugerido_pedido

print("=== R4: Clasificación ===")

# Caso 1: stock < target_min -> CRITICO
c = clasificacion(0.5, 1.5, 2.5)
print("Caso 1 - stock=0.5, min=1.5, max=2.5:", c)
assert c == "CRÍTICO"

# Caso 2: target_min <= stock <= target_max -> SALUDABLE
c = clasificacion(2.0, 1.5, 2.5)
print("Caso 2 - stock=2.0, min=1.5, max=2.5:", c)
assert c == "SALUDABLE"

# Caso 3: stock > target_max -> SOBRESTOCK
c = clasificacion(3.0, 1.5, 2.5)
print("Caso 3 - stock=3.0, min=1.5, max=2.5:", c)
assert c == "SOBRESTOCK"

# Caso 4: stock None -> SIN_DATOS
c = clasificacion(None, 1.5, 2.5)
print("Caso 4 - stock=None, min=1.5, max=2.5:", c)
assert c == "SIN_DATOS"

# Caso 5: target ausente -> SIN_DATOS
c = clasificacion(1.0, None, 2.5)
print("Caso 5 - stock=1.0, min=None, max=2.5:", c)
assert c == "SIN_DATOS"

print("\n=== R3: Sugerido de pedido ===")

# Caso 6: stock critico -> sugerido > 0
s, v = sugerido_pedido(0.5, 1.5, 2.5, 10)
print("Caso 6 - stock=0.5, min=1.5, max=2.5, prom=10:", s, v)
assert abs(s - 20.0) < 1e-9
assert v == []

# Caso 7: stock saludable -> sugerido 0
s, v = sugerido_pedido(2.0, 1.5, 2.5, 10)
print("Caso 7 - stock=2.0, min=1.5, max=2.5, prom=10:", s, v)
assert s == 0.0
assert v == []

# Caso 8: stock sobrestock -> sugerido 0
s, v = sugerido_pedido(3.0, 1.5, 2.5, 10)
print("Caso 8 - stock=3.0, min=1.5, max=2.5, prom=10:", s, v)
assert s == 0.0
assert v == []

# Caso 9: SIN_TARGET
s, v = sugerido_pedido(1.0, None, 2.5, 10)
print("Caso 9 - stock=1.0, min=None, max=2.5, prom=10:", s, v)
assert s == 0.0
assert "SIN_TARGET" in v

# Caso 10: PROMEDIO_CERO
s, v = sugerido_pedido(1.0, 1.5, 2.5, 0)
print("Caso 10 - stock=1.0, min=1.5, max=2.5, prom=0:", s, v)
assert s == 0.0
assert "PROMEDIO_CERO" in v

print("\nTodas las pruebas de R3 y R4 pasaron correctamente.")
