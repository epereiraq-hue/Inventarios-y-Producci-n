# -*- coding: utf-8 -*-
"""Pruebas para el endpoint del agente de IA (contrato JSON)."""

from inventarios_produccion.app.services.agente_ia import procesar_producto


class TestProcesarProducto:
    """Pruebas para la función procesar_producto del agente de IA."""

    def test_producto_critico(self):
        """Producto con stock crítico -> clasificación CRÍTICO, acción PRODUCIR."""
        datos = {
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
        resultado = procesar_producto(datos)

        assert resultado["producto_id"] == "PROD0000285"
        assert resultado["clasificacion"] == "CRÍTICO"
        assert resultado["accion_sugerida"] == "PRODUCIR"
        assert resultado["sugerido_pedido"] > 0
        assert resultado["origen_calculo"] == "recalculado_desde_ventas_6m"
        assert resultado["validaciones"] == []
        assert abs(resultado["promedio_mensual"] - 6.333333333333333) < 1e-4

    def test_producto_saludable(self):
        """Producto saludable -> clasificación SALUDABLE, acción MONITOREAR, sugerido 0."""
        datos = {
            "producto_id": "PROD0000287",
            "ventas_6m": [50, 60, 55, 70, 65, 80],
            "inventario_actual": 100,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resultado = procesar_producto(datos)

        assert resultado["clasificacion"] == "SALUDABLE"
        assert resultado["accion_sugerida"] == "MONITOREAR"
        assert resultado["sugerido_pedido"] == 0
        assert resultado["origen_calculo"] == "recalculado_desde_ventas_6m"

    def test_ventas_ceros(self):
        """Ventas todas cero -> clasificación SIN_DATOS, validacion VENTAS_CEROS."""
        datos = {
            "producto_id": "PROD0000284",
            "ventas_6m": [0, 0, 0, 0, 0, 0],
            "inventario_actual": 50,
            "target_min": 1.5,
            "target_max": 2.5,
        }
        resultado = procesar_producto(datos)

        assert resultado["clasificacion"] == "SIN_DATOS"
        assert "VENTAS_CEROS" in resultado["validaciones"]
        assert "PROMEDIO_CERO" in resultado["validaciones"]

    def test_sin_target(self):
        """Sin target -> clasificación SIN_DATOS, validacion SIN_TARGET."""
        datos = {
            "producto_id": "PROD0000999",
            "ventas_6m": [10, 20, 30, 40, 50, 60],
            "inventario_actual": 100,
            "target_min": None,
            "target_max": None,
        }
        resultado = procesar_producto(datos)

        assert resultado["clasificacion"] == "SIN_DATOS"
        assert "SIN_TARGET" in resultado["validaciones"]

    def test_campos_opcionales(self):
        """Campos opcionales ausentes -> no rompe, usa valores por defecto."""
        datos = {
            "producto_id": "PROD0000001",
            "ventas_6m": [10, 10, 10, 10, 10, 10],
            "inventario_actual": 50,
        }
        resultado = procesar_producto(datos)

        assert resultado["producto_id"] == "PROD0000001"
        assert resultado["promedio_mensual"] == 10.0
        assert resultado["origen_calculo"] == "recalculado_desde_ventas_6m"
