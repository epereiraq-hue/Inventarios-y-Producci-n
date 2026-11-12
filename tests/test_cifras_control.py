# -*- coding: utf-8 -*-
"""Pruebas para las cifras de control y casos límite de AGENTS.md."""

from inventarios_produccion.app import create_app


class TestCifrasControlAGENTS:
    """Pruebas para las cifras de control definidas en AGENTS.md."""

    def test_endpoint_agente_devuelve_json(self, client):
        """El endpoint /api/agente-ia devuelve JSON con los campos del contrato."""
        payload = {
            "producto_id": "PROD_TEST_001",
            "ventas_6m": [10, 20, 30, 40, 50, 60],
            "inventario_actual": 100,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resp = client.post("/api/agente-ia", json=payload)
        assert resp.status_code == 200

        data = resp.get_json()
        # Campos obligatorios del contrato JSON
        assert "producto_id" in data
        assert "promedio_mensual" in data
        assert "meses_stock_actual" in data
        assert "clasificacion" in data
        assert "accion_sugerida" in data
        assert "sugerido_pedido" in data
        assert "validaciones" in data
        assert "origen_calculo" in data

        # origen_calculo debe ser siempre recalculado_desde_ventas_6m (opción A)
        assert data["origen_calculo"] == "recalculado_desde_ventas_6m"

        # Ventas en unidades (no montos): promedio = 35.0
        assert data["promedio_mensual"] == 35.0

    def test_endpoint_sin_json_devuelve_400(self, client):
        """Petición sin JSON en el body devuelve 400."""
        resp = client.post("/api/agente-ia", data="no es json", content_type="text/plain")
        assert resp.status_code == 400

    def test_endpoint_sin_producto_id_devuelve_400(self, client):
        """Petición sin campo producto_id devuelve 400."""
        resp = client.post("/api/agente-ia", json={"ventas_6m": [1, 2, 3, 4, 5, 6]})
        assert resp.status_code == 400

    def test_endpoint_sin_ventas_6m_devuelve_400(self, client):
        """Petición sin campo ventas_6m devuelve 400."""
        resp = client.post("/api/agente-ia", json={"producto_id": "X"})
        assert resp.status_code == 400

    def test_descarga_csv_devuelve_archivo(self, client):
        """Endpoint /api/reportes/descargar devuelve CSV descargable."""
        resp = client.get("/api/reportes/descargar")
        assert resp.status_code == 200
        assert "text/csv" in resp.content_type
        assert "Reporte_Inventarios_Automatizado.csv" in str(resp.headers.get("Content-Disposition"))

    def test_preview_devuelve_json(self, client):
        """Endpoint /api/reportes/preview devuelve JSON con total_registros y preview."""
        resp = client.get("/api/reportes/preview")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total_registros" in data
        assert "preview" in data
        assert data["total_registros"] > 0


class TestCasosLimite:
    """Pruebas para los casos límite definidos en AGENTS.md."""

    def test_producto_sin_ventas_6_meses(self, client):
        """Producto sin ventas en 6 meses -> promedio 0, validación VENTAS_CEROS."""
        payload = {
            "producto_id": "PROD_SIN_VENTAS",
            "ventas_6m": [0, 0, 0, 0, 0, 0],
            "inventario_actual": 50,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resp = client.post("/api/agente-ia", json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["promedio_mensual"] == 0.0
        assert "VENTAS_CEROS" in data["validaciones"]
        assert "PROMEDIO_CERO" in data["validaciones"]

    def test_inventario_cero_con_promedio_positivo(self, client):
        """Inventario 0 y promedio > 0 -> meses_stock 0, clasificación CRÍTICO."""
        payload = {
            "producto_id": "PROD_SIN_STOCK",
            "ventas_6m": [10, 20, 30, 40, 50, 60],
            "inventario_actual": 0,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resp = client.post("/api/agente-ia", json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["meses_stock_actual"] == 0.0
        assert data["clasificacion"] == "CRÍTICO"
        assert data["accion_sugerida"] == "PRODUCIR"

    def test_target_ausente(self, client):
        """target_min/target_max ausentes -> clasificación SIN_DATOS, validación SIN_TARGET."""
        payload = {
            "producto_id": "PROD_SIN_TARGET",
            "ventas_6m": [10, 20, 30, 40, 50, 60],
            "inventario_actual": 100,
            "target_min": None,
            "target_max": None,
        }
        resp = client.post("/api/agente-ia", json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["clasificacion"] == "SIN_DATOS"
        assert "SIN_TARGET" in data["validaciones"]

    def test_evitar_traslado_entre_empresas(self, client):
        """La app no mezcla EMP1 y EMP2 en el mismo cálculo (cada producto tiene su empresa)."""
        payload_emp1 = {
            "producto_id": "PROD_EMP1",
            "empresa": "EMP1",
            "ventas_6m": [10, 10, 10, 10, 10, 10],
            "inventario_actual": 50,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        payload_emp2 = {
            "producto_id": "PROD_EMP2",
            "empresa": "EMP2",
            "ventas_6m": [10, 10, 10, 10, 10, 10],
            "inventario_actual": 50,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resp1 = client.post("/api/agente-ia", json=payload_emp1)
        resp2 = client.post("/api/agente-ia", json=payload_emp2)
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        assert resp1.get_json()["empresa"] == "EMP1"
        assert resp2.get_json()["empresa"] == "EMP2"
