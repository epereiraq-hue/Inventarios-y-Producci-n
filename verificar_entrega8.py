# -*- coding: utf-8 -*-
"""Script de verificación para la entrega 8: integración del agente de IA."""
from inventarios_produccion.app import create_app

app = create_app()
client = app.test_client()

print("=== Entrega 8: Agente de IA (contrato JSON) ===")

# Caso 1: producto crítico (stock por debajo de target_min)
payload = {
    "producto_id": "PROD0000285",
    "codigo_best": "01-000451",
    "descripcion": "TANQUE ECOTANK 450 LTS AZUL TRICAPA",
    "familia": "01-03",
    "empresa": "EMP2",
    "sucursal": "Coyol",
    "ventas_6m": [0, 22, 16, 0, 0, 0],
    "inventario_actual": 0,
    "target_min": 1.5,
    "target_max": 2.5,
}
resp = client.post("/api/agente-ia", json=payload)
print("\nCaso 1 - producto crítico:")
print("  Status:", resp.status_code)
data = resp.get_json()
for k, v in data.items():
    print(f"  {k}: {v}")
assert resp.status_code == 200
assert data["clasificacion"] == "CRÍTICO"
assert data["accion_sugerida"] == "PRODUCIR"
assert data["sugerido_pedido"] > 0
assert data["origen_calculo"] == "recalculado_desde_ventas_6m"
assert data["validaciones"] == []

# Caso 2: producto saludable
payload2 = {
    "producto_id": "PROD0000287",
    "ventas_6m": [50, 60, 55, 70, 65, 80],
    "inventario_actual": 100,
    "target_min": 1.5,
    "target_max": 2.5,
}
resp2 = client.post("/api/agente-ia", json=payload2)
print("\nCaso 2 - producto saludable:")
print("  Status:", resp2.status_code)
data2 = resp2.get_json()
for k, v in data2.items():
    print(f"  {k}: {v}")
assert resp2.status_code == 200
assert data2["clasificacion"] == "SALUDABLE"
assert data2["accion_sugerida"] == "MONITOREAR"
assert data2["sugerido_pedido"] == 0

# Caso 3: sin ventas (ventas ceros)
payload3 = {
    "producto_id": "PROD0000284",
    "ventas_6m": [0, 0, 0, 0, 0, 0],
    "inventario_actual": 50,
    "target_min": 1.5,
    "target_max": 2.5,
}
resp3 = client.post("/api/agente-ia", json=payload3)
print("\nCaso 3 - ventas ceros:")
print("  Status:", resp3.status_code)
data3 = resp3.get_json()
for k, v in data3.items():
    print(f"  {k}: {v}")
assert resp3.status_code == 200
assert "VENTAS_CEROS" in data3["validaciones"]

# Caso 4: sin target
payload4 = {
    "producto_id": "PROD0000999",
    "ventas_6m": [10, 20, 30, 40, 50, 60],
    "inventario_actual": 100,
    "target_min": None,
    "target_max": None,
}
resp4 = client.post("/api/agente-ia", json=payload4)
print("\nCaso 4 - sin target:")
print("  Status:", resp4.status_code)
data4 = resp4.get_json()
for k, v in data4.items():
    print(f"  {k}: {v}")
assert resp4.status_code == 200
assert "SIN_TARGET" in data4["validaciones"]

# Caso 5: petición sin JSON
resp5 = client.post("/api/agente-ia", data="no es json", content_type="text/plain")
print("\nCaso 5 - sin JSON:")
print("  Status:", resp5.status_code)
assert resp5.status_code == 400

# Caso 6: petición sin producto_id
resp6 = client.post("/api/agente-ia", json={"ventas_6m": [1, 2, 3, 4, 5, 6]})
print("\nCaso 6 - sin producto_id:")
print("  Status:", resp6.status_code)
assert resp6.status_code == 400

print("\nTodas las pruebas de la entrega 8 pasaron correctamente.")
