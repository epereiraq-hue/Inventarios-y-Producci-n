# -*- coding: utf-8 -*-
"""Pruebas para las reglas de negocio R1-R6 del módulo reglas.py."""

from inventarios_produccion.app.services.reglas import (
    promedio_mensual,
    meses_stock_actual,
    clasificacion,
    sugerido_pedido,
    accion_sugerida,
    validar_reporte,
)


class TestReglaR1PromedioMensual:
    """Pruebas para R1: promedio mensual (ventana de 6 meses)."""

    def test_ventas_normales(self):
        """Ventas [0, 22, 16, 0, 0, 0] -> promedio 6.333..."""
        resultado = promedio_mensual([0, 22, 16, 0, 0, 0])
        assert abs(resultado - 6.333333333333333) < 1e-9

    def test_lista_vacia(self):
        """Lista vacía -> 0.0"""
        assert promedio_mensual([]) == 0.0

    def test_todos_ceros(self):
        """Todas las ventas en cero -> 0.0"""
        assert promedio_mensual([0, 0, 0, 0, 0, 0]) == 0.0

    def test_ventas_positivas(self):
        """[10, 20, 30, 40, 50, 60] -> 35.0"""
        assert promedio_mensual([10, 20, 30, 40, 50, 60]) == 35.0

    def test_una_sola_venta(self):
        """[100, 0, 0, 0, 0, 0] -> 16.666..."""
        resultado = promedio_mensual([100, 0, 0, 0, 0, 0])
        assert abs(resultado - 16.666666666666668) < 1e-9


class TestReglaR2MesesStockActual:
    """Pruebas para R2: meses de stock actual."""

    def test_stock_positivo(self):
        """Inventario 100, promedio 20 -> 5.0 meses"""
        assert meses_stock_actual(100, 20) == 5.0

    def test_inventario_cero(self):
        """Inventario 0, promedio 10 -> 0.0 meses"""
        assert meses_stock_actual(0, 10) == 0.0

    def test_promedio_cero(self):
        """Promedio 0 -> None (división por cero)"""
        assert meses_stock_actual(50, 0) is None

    def test_stock_decimal(self):
        """Inventario 37.5, promedio 7.5 -> 5.0 meses"""
        assert meses_stock_actual(37.5, 7.5) == 5.0


class TestReglaR3SugeridoPedido:
    """Pruebas para R3: sugerido de pedido."""

    def test_stock_critico(self):
        """Stock 0.5 < target_min 1.5 -> sugerido = (2.5 - 0.5) * 10 = 20.0"""
        sugerido, validaciones = sugerido_pedido(0.5, 1.5, 2.5, 10)
        assert abs(sugerido - 20.0) < 1e-9
        assert validaciones == []

    def test_stock_saludable(self):
        """Stock 2.0 entre target_min y target_max -> sugerido 0.0"""
        sugerido, validaciones = sugerido_pedido(2.0, 1.5, 2.5, 10)
        assert sugerido == 0.0
        assert validaciones == []

    def test_stock_sobrestock(self):
        """Stock 3.0 > target_max 2.5 -> sugerido 0.0"""
        sugerido, validaciones = sugerido_pedido(3.0, 1.5, 2.5, 10)
        assert sugerido == 0.0
        assert validaciones == []

    def test_sin_target(self):
        """target_min None -> sugerido 0.0 y validacion SIN_TARGET"""
        sugerido, validaciones = sugerido_pedido(1.0, None, 2.5, 10)
        assert sugerido == 0.0
        assert "SIN_TARGET" in validaciones

    def test_promedio_cero(self):
        """promedio 0 -> sugerido 0.0 y validacion PROMEDIO_CERO"""
        sugerido, validaciones = sugerido_pedido(1.0, 1.5, 2.5, 0)
        assert sugerido == 0.0
        assert "PROMEDIO_CERO" in validaciones

    def test_meses_stock_none(self):
        """meses_stock None -> sugerido 0.0 y validacion MESES_STOCK_INDEFINIDO"""
        sugerido, validaciones = sugerido_pedido(None, 1.5, 2.5, 10)
        assert sugerido == 0.0
        assert "MESES_STOCK_INDEFINIDO" in validaciones


class TestReglaR4Clasificacion:
    """Pruebas para R4: clasificación de inventario."""

    def test_stock_debajo_target_min(self):
        """Stock 0.5, min 1.5, max 2.5 -> CRÍTICO"""
        assert clasificacion(0.5, 1.5, 2.5) == "CRÍTICO"

    def test_stock_dentro_rango(self):
        """Stock 2.0, min 1.5, max 2.5 -> SALUDABLE"""
        assert clasificacion(2.0, 1.5, 2.5) == "SALUDABLE"

    def test_stock_sobre_target_max(self):
        """Stock 3.0, min 1.5, max 2.5 -> SOBRESTOCK"""
        assert clasificacion(3.0, 1.5, 2.5) == "SOBRESTOCK"

    def test_stock_none(self):
        """Stock None -> SIN_DATOS"""
        assert clasificacion(None, 1.5, 2.5) == "SIN_DATOS"

    def test_target_ausente(self):
        """target_min None -> SIN_DATOS"""
        assert clasificacion(1.0, None, 2.5) == "SIN_DATOS"


class TestReglaR5AccionSugerida:
    """Pruebas para R5: acción sugerida."""

    def test_sobrestock(self):
        """SOBRESTOCK -> CONGELAR / PROMOCION"""
        assert accion_sugerida("SOBRESTOCK") == "CONGELAR / PROMOCION"

    def test_saludable(self):
        """SALUDABLE -> MONITOREAR"""
        assert accion_sugerida("SALUDABLE") == "MONITOREAR"

    def test_critico(self):
        """CRÍTICO -> PRODUCIR"""
        assert accion_sugerida("CRÍTICO") == "PRODUCIR"

    def test_sin_datos(self):
        """SIN_DATOS -> REVISAR MANUALMENTE"""
        assert accion_sugerida("SIN_DATOS") == "REVISAR MANUALMENTE"

    def test_desconocido(self):
        """Desconocido -> REVISAR MANUALMENTE"""
        assert accion_sugerida("DESCONOCIDO") == "REVISAR MANUALMENTE"


class TestReglaR6Validacion:
    """Pruebas para R6: validación obligatoria."""

    def test_todo_correcto(self):
        """Datos válidos -> lista vacía"""
        assert validar_reporte([10, 20, 30, 40, 50, 60], 100, 1.5, 2.5) == []

    def test_ventas_ceros(self):
        """Ventas todas cero -> VENTAS_CEROS"""
        errores = validar_reporte([0, 0, 0, 0, 0, 0], 100, 1.5, 2.5)
        assert "VENTAS_CEROS" in errores

    def test_inventario_negativo(self):
        """Inventario negativo -> INVENTARIO_INVALIDO"""
        errores = validar_reporte([10, 20, 30, 40, 50, 60], -5, 1.5, 2.5)
        assert "INVENTARIO_INVALIDO" in errores

    def test_sin_target(self):
        """target_min None -> SIN_TARGET"""
        errores = validar_reporte([10, 20, 30, 40, 50, 60], 100, None, 2.5)
        assert "SIN_TARGET" in errores

    def test_todo_mal(self):
        """Ventas ceros + inventario negativo + sin target -> 3 errores"""
        errores = validar_reporte([0, 0, 0, 0, 0, 0], -5, None, None)
        assert "VENTAS_CEROS" in errores
        assert "INVENTARIO_INVALIDO" in errores
        assert "SIN_TARGET" in errores
        assert len(errores) == 3
