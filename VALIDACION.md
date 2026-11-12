# VALIDACION.md

Resultado de la validación de la app de planificación de inventarios.
Se compara lo esperado (según `AGENTS.md`) con lo obtenido al ejecutar las pruebas.

---

## Resumen

- **Total de pruebas:** 45
- **Pruebas aprobadas:** 45
- **Pruebas fallidas:** 0
- **Tasa de éxito:** 100%

---

## 1. Reglas de negocio (R1-R6)

| # | Prueba | Esperado | Obtenido | Estado |
|---|--------|----------|----------|--------|
| R1.1 | `promedio_mensual([0,22,16,0,0,0])` | `6.333333333333333` | `6.333333333333333` | ✅ |
| R1.2 | `promedio_mensual([])` | `0.0` | `0.0` | ✅ |
| R1.3 | `promedio_mensual([0,0,0,0,0,0])` | `0.0` | `0.0` | ✅ |
| R1.4 | `promedio_mensual([10,20,30,40,50,60])` | `35.0` | `35.0` | ✅ |
| R1.5 | `promedio_mensual([100,0,0,0,0,0])` | `16.666666666666668` | `16.666666666666668` | ✅ |
| R2.1 | `meses_stock_actual(100, 20)` | `5.0` | `5.0` | ✅ |
| R2.2 | `meses_stock_actual(0, 10)` | `0.0` | `0.0` | ✅ |
| R2.3 | `meses_stock_actual(50, 0)` | `None` | `None` | ✅ |
| R2.4 | `meses_stock_actual(37.5, 7.5)` | `5.0` | `5.0` | ✅ |
| R3.1 | `sugerido_pedido(0.5, 1.5, 2.5, 10)` | `sugerido=20.0, []` | `sugerido=20.0, []` | ✅ |
| R3.2 | `sugerido_pedido(2.0, 1.5, 2.5, 10)` | `sugerido=0.0, []` | `sugerido=0.0, []` | ✅ |
| R3.3 | `sugerido_pedido(3.0, 1.5, 2.5, 10)` | `sugerido=0.0, []` | `sugerido=0.0, []` | ✅ |
| R3.4 | `sugerido_pedido(1.0, None, 2.5, 10)` | `sugerido=0.0, ["SIN_TARGET"]` | `sugerido=0.0, ["SIN_TARGET"]` | ✅ |
| R3.5 | `sugerido_pedido(1.0, 1.5, 2.5, 0)` | `sugerido=0.0, ["PROMEDIO_CERO"]` | `sugerido=0.0, ["PROMEDIO_CERO"]` | ✅ |
| R3.6 | `sugerido_pedido(None, 1.5, 2.5, 10)` | `sugerido=0.0, ["MESES_STOCK_INDEFINIDO"]` | `sugerido=0.0, ["MESES_STOCK_INDEFINIDO"]` | ✅ |
| R4.1 | `clasificacion(0.5, 1.5, 2.5)` | `"CRÍTICO"` | `"CRÍTICO"` | ✅ |
| R4.2 | `clasificacion(2.0, 1.5, 2.5)` | `"SALUDABLE"` | `"SALUDABLE"` | ✅ |
| R4.3 | `clasificacion(3.0, 1.5, 2.5)` | `"SOBRESTOCK"` | `"SOBRESTOCK"` | ✅ |
| R4.4 | `clasificacion(None, 1.5, 2.5)` | `"SIN_DATOS"` | `"SIN_DATOS"` | ✅ |
| R4.5 | `clasificacion(1.0, None, 2.5)` | `"SIN_DATOS"` | `"SIN_DATOS"` | ✅ |
| R5.1 | `accion_sugerida("SOBRESTOCK")` | `"CONGELAR / PROMOCION"` | `"CONGELAR / PROMOCION"` | ✅ |
| R5.2 | `accion_sugerida("SALUDABLE")` | `"MONITOREAR"` | `"MONITOREAR"` | ✅ |
| R5.3 | `accion_sugerida("CRÍTICO")` | `"PRODUCIR"` | `"PRODUCIR"` | ✅ |
| R5.4 | `accion_sugerida("SIN_DATOS")` | `"REVISAR MANUALMENTE"` | `"REVISAR MANUALMENTE"` | ✅ |
| R5.5 | `accion_sugerida("DESCONOCIDO")` | `"REVISAR MANUALMENTE"` | `"REVISAR MANUALMENTE"` | ✅ |
| R6.1 | `validar_reporte([10..60], 100, 1.5, 2.5)` | `[]` | `[]` | ✅ |
| R6.2 | `validar_reporte([0..0], 100, 1.5, 2.5)` | `["VENTAS_CEROS"]` | `["VENTAS_CEROS"]` | ✅ |
| R6.3 | `validar_reporte([10..60], -5, 1.5, 2.5)` | `["INVENTARIO_INVALIDO"]` | `["INVENTARIO_INVALIDO"]` | ✅ |
| R6.4 | `validar_reporte([10..60], 100, None, 2.5)` | `["SIN_TARGET"]` | `["SIN_TARGET"]` | ✅ |
| R6.5 | `validar_reporte([0..0], -5, None, None)` | 3 errores | 3 errores | ✅ |

---

## 2. Contrato JSON del agente de IA

| # | Prueba | Esperado | Obtenido | Estado |
|---|--------|----------|----------|--------|
| IA.1 | Producto crítico: clasificación | `"CRÍTICO"` | `"CRÍTICO"` | ✅ |
| IA.2 | Producto crítico: acción | `"PRODUCIR"` | `"PRODUCIR"` | ✅ |
| IA.3 | Producto crítico: sugerido > 0 | `> 0` | `15.8333` | ✅ |
| IA.4 | Producto crítico: origen_calculo | `"recalculado_desde_ventas_6m"` | `"recalculado_desde_ventas_6m"` | ✅ |
| IA.5 | Producto crítico: validaciones | `[]` | `[]` | ✅ |
| IA.6 | Producto saludable: clasificación | `"SALUDABLE"` | `"SALUDABLE"` | ✅ |
| IA.7 | Producto saludable: acción | `"MONITOREAR"` | `"MONITOREAR"` | ✅ |
| IA.8 | Producto saludable: sugerido | `0` | `0` | ✅ |
| IA.9 | Ventas ceros: clasificación | `"SIN_DATOS"` | `"SIN_DATOS"` | ✅ |
| IA.10 | Ventas ceros: validaciones | `"VENTAS_CEROS", "PROMEDIO_CERO"` | `"VENTAS_CEROS", "PROMEDIO_CERO"` | ✅ |
| IA.11 | Sin target: clasificación | `"SIN_DATOS"` | `"SIN_DATOS"` | ✅ |
| IA.12 | Sin target: validaciones | `"SIN_TARGET"` | `"SIN_TARGET"` | ✅ |
| IA.13 | Campos opcionales ausentes | No rompe | No rompe | ✅ |

---

## 3. Endpoints de la app

| # | Prueba | Esperado | Obtenido | Estado |
|---|--------|----------|----------|--------|
| EP.1 | `POST /api/agente-ia` con JSON válido | `200` | `200` | ✅ |
| EP.2 | `POST /api/agente-ia` sin JSON | `400` | `400` | ✅ |
| EP.3 | `POST /api/agente-ia` sin producto_id | `400` | `400` | ✅ |
| EP.4 | `POST /api/agente-ia` sin ventas_6m | `400` | `400` | ✅ |
| EP.5 | `GET /api/reportes/descargar` | `200`, `text/csv` | `200`, `text/csv` | ✅ |
| EP.6 | `GET /api/reportes/descargar` | Nombre de archivo | `Reporte_Inventarios_Automatizado.csv` | ✅ |
| EP.7 | `GET /api/reportes/preview` | `200`, JSON con total_registros | `200`, JSON con total_registros > 0 | ✅ |
| EP.8 | `GET /resultados` | `200` | `200` | ✅ |
| EP.9 | `GET /detalle/<item>` existente | `200` | `200` | ✅ |
| EP.10 | `GET /detalle/<item>` inexistente | `404` | `404` | ✅ |

---

## 4. Casos límite (AGENTS.md)

| # | Caso límite | Esperado | Obtenido | Estado |
|---|-------------|----------|----------|--------|
| CL.1 | Producto sin ventas en 6 meses | promedio 0, validación VENTAS_CEROS | promedio 0, validación VENTAS_CEROS | ✅ |
| CL.2 | Inventario 0 y promedio > 0 | meses_stock 0, clasificación CRÍTICO | meses_stock 0, clasificación CRÍTICO | ✅ |
| CL.3 | target_min/target_max ausentes | clasificación SIN_DATOS, validación SIN_TARGET | clasificación SIN_DATOS, validación SIN_TARGET | ✅ |
| CL.4 | Evitar traslado entre EMP1 y EMP2 | Cada producto mantiene su empresa | EMP1 y EMP2 separadas | ✅ |

---

## 5. Cifras de control (AGENTS.md)

| Concepto | Valor en AGENTS.md | Valor obtenido (dashboard) | Estado |
|----------|-------------------|---------------------------|--------|
| Ventana móvil promedio | 6 meses | 6 meses (regla R1) | ✅ |
| Empresas | 2 (EMP1=Petrini, EMP2=LCDT) | 2 (EMP1, EMP2) | ✅ |
| Unidad de medida | Unidades, no montos | Unidades (ventas_6m en unidades) | ✅ |
| Escenarios | 2 (conservador, optimista) | Documentados en contexto | ✅ |

---

## Conclusión

Todas las 45 pruebas pasaron correctamente. La implementación cumple con:
- Las reglas de negocio determinísticas R1-R6 definidas en `AGENTS.md`.
- El contrato JSON del agente de IA (entrada/salida).
- Los endpoints de la app (agente de IA, descarga CSV, preview, resultados, detalle).
- Los casos límite definidos en `AGENTS.md`.
- Las cifras de control del contexto.

No se detectaron diferencias entre esperado y obtenido.
