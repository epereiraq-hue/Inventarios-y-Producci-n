# PLAN.md

Plan de entregas del proyecto de planificación y control de inventarios.
Generado por @arquitecto a partir de `AGENTS.md`, `Contexto/` e `Insumos/`.

---

## 1. RESUMEN

Vamos a construir una app de planificación y control de inventarios para una empresa manufacturera y comercializadora.
Entra: dos archivos Excel de `Insumos/` (ventas acumuladas, existencias y requerimientos de producción).
El agente de IA recibe datos ya limpios y devuelve una propuesta de reposición en JSON (promedio mensual, meses de stock, clasificación, acción y sugerido de pedido), recalculado desde ventas acumuladas de 6 meses.
Sale: un reporte automatizado por producto, familia, empresa (EMP1/EMP2) y sucursal, con contadores, tabla con filtro y descarga de resultados.

---

## 2. LO QUE ENCONTRÉ

### Contexto
- `Contexto/Contexto_Mi_App.md`: describe el proceso de planificación, el cálculo manual (ventas 6 meses → promedio → existencias → sugerido), la necesidad del Área Comercial (producto, familia, empresa EMP1/EMP2, sucursal Heredia/Alajuela/Cartago/San José/Limón), ventas en unidades no montos, no hay máximos/mínimos en Alajuela, evitar traslados entre EMP1 y EMP2 por IVA/facturación, sucursales compartidas, y 7 secciones de especificación funcional.

### Insumos
- `Insumos/Meses de inventario x Producto.xlsx`: 20 hojas. Las clave son `Meses ERA ECOTANK`, `Meses Petrini`, `Meses LCDT` (ventas acumuladas may–nov 2026, inventarios al 04-11-2026, promedio mensual, meses stock), además de hojas maestras por sucursal (`Cariari/Coyol/Ocho/Paso/Zurqui LCDT` y `Petrini`), `Ventas ...`, `Homologar`, `Familias`, `Plan de producción`, `Requerimiento`, `Base Datos`, `Dashboard Original`, `Tabla auxiliar`, `Tabla Target`.
- `Insumos/Requerimientos Logística.xlsx`: hoja `Requerimientos` (35 filas × 22 columnas; encabezados reales en fila 11; 24 requerimientos de producción en filas 12–35).

### Coincidencia con AGENTS.md
- Coincide: el contexto pide recalcular promedio mensual (ventana 6 meses), clasificación y sugerido de pedido; AGENTS.md define reglas R1–R6 y contrato JSON.
- Coincide: los insumos ya traen columnas calculadas, pero por decisión del usuario (opción A) el agente recalcula todo desde ventas acumuladas.
- No cuadra / falta:
  - Sucursales del contexto (Heredia, Alajuela, Cartago, San José, Limón) no aparecen tal cual en insumos (ahí están Cariari, Coyol, Ochomogo, Paso Ancho, Zurquí). Mapeo por confirmar (P5).
  - El contexto dice que no hay máximos/mínimos en Alajuela, pero los insumos traen `Target_Min`/`Target_Max` por familia (versión posterior). Se aplican salvo confirmación de excepción para Alajuela.
  - EMP1 = Petrini y EMP2 = LCDT (confirmadas por el usuario).
  - Campos extra en insumos (costos, GTIN, fechas OC, atrasos, etc.) no participan en reglas de negocio hasta validar su uso.

---

## 3. ENTREGAS POR SUBAGENTE

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 1 | @backend | Estructura base MVC con uv: `create_app()`, carpetas `app/controllers` y `app/services`, `wsgi.py`, `iniciar_app.bat`, archivo `.env.example` | `app/__init__.py`, `app/controllers/`, `app/services/`, `wsgi.py`, `iniciar_app.bat`, `.env.example` | — | Ejecutar `iniciar_app.bat` y ver que Flask arranca sin errores y abre el navegador en `http://127.0.0.1:5000/` |
| 2 | @backend | Lectura de insumos: lee `Meses de inventario x Producto.xlsx` y `Requerimientos Logística.xlsx`, expone datos crudos sin modificar nada en `Insumos/` | `app/services/lectura_insumos.py` | Entrega 1 | Ejecutar un script de prueba y ver en consola que lee 3 hojas `Meses ...` (324 productos) y 24 requerimientos de logística |
| 3 | @backend | Regla R1: función `promedio_mensual(ventas_6m)` con comentario, en `app/services` | `app/services/reglas.py` (o nuevo archivo) | Entrega 2 | Ver en pantalla el promedio de un producto de prueba (ej. ventas [0,22,16,0,0,0] → 6.33) |
| 4 | @backend | Regla R2: función `meses_stock_actual(inventario_actual, promedio)` con manejo de división por cero | `app/services/reglas.py` | Entrega 3 | Ver en pantalla meses_stock de un producto con inventario > 0 y promedio > 0 |
| 5 | @backend | Reglas R3+R4: clasificación (SOBRESTOCK/SALUDABLE/CRÍTICO) y sugerido de pedido usando `target_min`/`target_max` de `Tabla Target` | `app/services/reglas.py` | Entrega 4 | Ver en pantalla clasificación CRÍTICO cuando meses_stock < target_min, y sugerido > 0 |
| 6 | @backend | Regla R5: función `accion_sugerida(clasificacion)` → PRODUCIR / MONITOREAR / CONGELAR PROMOCION / REVISAR MANUALMENTE | `app/services/reglas.py` | Entrega 5 | Ver en pantalla la acción asociada a cada clasificación |
| 7 | @backend | Regla R6: validación obligatoria (ventas ceros, inventario inválido, sin target) antes de usar el reporte | `app/services/reglas.py` | Entrega 6 | Ver en pantalla productos con validaciones `VENTAS_CEROS`, `SIN_TARGET` marcados para revisión manual |
| 8 | @backend | Integración del agente de IA: endpoint que recibe JSON de request, aplica reglas R1–R6, devuelve JSON de respuesta con `origen_calculo: "recalculado_desde_ventas_6m"`; llave de API leída de `.env` (nunca escrita en código) | `app/controllers/agente_ia.py`, `app/services/agente_ia.py`, `.env` | Entrega 7 | Enviar JSON de prueba por pantalla/navegador y recibir JSON de respuesta con promedio, clasificación, acción y sugerido |
| 9 | @backend | Descarga de resultados: exportar el reporte a CSV desde la app (o generar archivo descargable) | `app/controllers/reportes.py`, ruta de descarga | Entrega 8 | Hacer clic en "Descargar" y ver que se descarga `Reporte_Inventarios_Automatizado.csv` con las 30 columnas esperadas |
| 10 | @frontend | Pantalla de inicio: título, propósito de la app, botón para ir a resultados, estilo profesional en español | `app/templates/inicio.html`, ajuste en `app/templates/base.html` | Entrega 9 | Abrir la app y ver la pantalla de inicio con título y navegación |
| 11 | @frontend | Pantalla de resultados: tablero con contadores grandes (críticas, saludables, alerta, sobrestock, total inventario, demanda mensual, meses stock global) y tabla con filtro por producto/familia/empresa/sucursal | `app/templates/resultados.html` | Entrega 10 | Ver los contadores grandes y la tabla filtrando por una familia (ej. 01-03) |
| 12 | @frontend | Detalle por registro: al seleccionar un producto, mostrar sus datos completos, clasificación, acción sugerida y requerimiento de logística si existe | Ajuste en `app/templates/resultados.html` o nueva plantilla `detalle.html` | Entrega 11 | Hacer clic en una fila y ver el detalle de ese producto |
| 13 | @frontend | Estilo de la app: CSS dentro de `base.html` (sin librerías externas de JavaScript), diseño sencillo y profesional | `app/templates/base.html`, `app/static/` si es necesario | Entrega 12 | Ver que la app tiene estilos consistentes y no depende de JS externo |
| 14 | @tester | Pruebas en `tests/` con pytest contra las cifras de control y casos límite de `AGENTS.md` (ej. producto con ventas todos ceros → VENTAS_CEROS; producto con meses_stock < target_min → CRÍTICO) | `tests/test_reglas.py`, `tests/test_clasificacion.py`, `conftest.py` con `pythonpath` | Entrega 13 | Ejecutar `pytest` y ver que las pruebas pasan (o listar las fallidas con causa probable) |
| 15 | @tester | `VALIDACION.md`: tabla esperado vs obtenido para cada cifra de control y caso límite | `VALIDACION.md` | Entrega 14 | Abrir `VALIDACION.md` y confirmar que esperado == obtenido o anotar diferencias |
| 16 | @revisor | Revisión de seguridad: llaves no escritas en código, `.env` no se sube, `.gitignore` adecuado, no hay datos sensibles expuestos, todo lo construido está en `AGENTS.md` | Ningún archivo (solo reporte de hallazgos) | Entrega 15 | Ver en pantalla la lista de hallazgos con prioridad y corrección propuesta |

---

## 4. PUNTOS DE CONTROL

| Después de la entrega | Interviene | Qué debe ver el usuario en pantalla (cifra o resultado exacto) |
|-----------------------|------------|---------------------------------------------------------------|
| 1 | @revisor (rápido) | Flask arranca y abre `http://127.0.0.1:5000/` sin errores |
| 5 | @tester | Clasificación de un producto con meses_stock < target_min muestra `CRÍTICO` y sugerido > 0 |
| 8 | @tester | Endpoint del agente devuelve JSON con `origen_calculo: "recalculado_desde_ventas_6m"` y `clasificacion` / `accion_sugerida` / `sugerido_pedido` |
| 9 | @usuario | Se descarga `Reporte_Inventarios_Automatizado.csv` con 30 columnas y 324 filas de productos |
| 11 | @tester | Contadores grandes coinciden con `AGENTS.md`: Críticas 13, Saludables 38, Alerta 2, Sobrestock 55, Inventario Total 5843, Demanda Total Mensual 2605.5, Meses Stock Global 2.24 |
| 14 | @tester | `pytest` ejecuta todas las pruebas; cada falla reporta diferencia y causa probable |
| 16 | @revisor | Lista de hallazgos de seguridad con prioridad y corrección propuesta; ninguna llave escrita en el código |

---

## 5. RIESGOS

| Riesgo | Qué hará cada subagente si pasa |
|--------|---------------------------------|
| Datos incompletos en insumos (familia vacía, target ausente) | @backend: marca `SIN_TARGET` y `REVISAR MANUALMENTE`; @tester: prueba con familia vacía y reporta que no se rompe la app |
| Archivos PDF escaneados (no hay en este proyecto, pero si aparecen) | @backend: no puede extraer texto; informa al usuario y pide archivo con texto o CSV |
| Respuesta del agente de IA que no es JSON válido | @backend: valida la estructura del JSON de respuesta; si no es válido, devuelve error 400 y pide reintentar |
| Límite de la llave gratis de IA agotado | @backend: lee la llave de `.env`; si falla la conexión, la app debe funcionar sin el agente (solo reglas determinísticas R1–R6) y avisar en pantalla |
| Mapeo de sucursales no confirmado (Heredia/Alajuela/Cartago/San José/Limón vs Cariari/Coyol/Ochomogo/Paso Ancho/Zurquí) | @arquitecto: deja `POR_CONFIRMAR` en sucursal; no asume equivalencia; @usuario debe confirmar antes de usar en producción |
| Máximos/mínimos en Alajuela (contexto dice que no existen, insumos sí tienen targets) | @backend: aplica targets de `Tabla Target` salvo que el usuario confirme excepción para Alajuela; @tester: valida que no se rompa si falta target |

---

## 6. PREGUNTAS PARA MÍ

Antes de empezar a construir, necesito que confirme:

1. **Mapeo de sucursales:** ¿Cómo relaciono las 5 sucursales del contexto (Heredia, Alajuela, Cartago, San José, Limón) con las de los insumos (Cariari, Coyol, Ochomogo, Paso Ancho, Zurquí)? ¿O dejo `POR_CONFIRMAR` hasta que lo decida?
2. **Excepción Alajuela:** ¿Los `Target_Min`/`Target_Max` de `Tabla Target` aplican también a Alajuela, o Alajuela es realmente sin máximos/mínimos como dice el contexto?
3. **Formato de salida:** ¿El reporte descargable debe ser CSV (como ya está generado) o prefieres Excel (`.xlsx`)?
4. **Puerto de la app:** ¿Flask debe correr en el puerto 5000 o en otro?
5. **Nombre de la llave en `.env`:** ¿Cómo se llama la variable de entorno para la llave de la IA (ej. `IA_API_KEY`, `OPENAI_API_KEY`, otra)?

---

### Tabla de entregas (resumen para su aprobación)

| N° | Responsable | Qué debe entregar |
|----|-------------|-------------------|
| 1 | @backend | Estructura base MVC con uv |
| 2 | @backend | Lectura de insumos |
| 3 | @backend | Regla R1: promedio mensual |
| 4 | @backend | Regla R2: meses de stock actual |
| 5 | @backend | Reglas R3+R4: clasificación y sugerido de pedido |
| 6 | @backend | Regla R5: acción sugerida |
| 7 | @backend | Regla R6: validación obligatoria |
| 8 | @backend | Integración del agente de IA (contrato JSON + .env) |
| 9 | @backend | Descarga de resultados (CSV) |
| 10 | @frontend | Pantalla de inicio |
| 11 | @frontend | Pantalla de resultados con contadores y tabla |
| 12 | @frontend | Detalle por registro |
| 13 | @frontend | Estilo de la app |
| 14 | @tester | Pruebas en tests/ con pytest |
| 15 | @tester | VALIDACION.md esperado vs obtenido |
| 16 | @revisor | Revisión de seguridad y AGENTS.md |

**Esperando su aprobación antes de que @backend comience con la entrega 1.**
