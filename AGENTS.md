# AGENTS.md

Documento de especificaciones para la app de planificación y control de inventarios.
Generado a partir de `Contexto/Contexto_Mi_App.md` y los archivos de `Insumos/`.
Sin suposiciones inventadas: lo que falta está marcado como "por confirmar".

---

## Qué es esta app

Aplicación de planificación y control de inventarios para una empresa manufacturera y comercializadora.
Reemplaza un cálculo manual (archivo Excel hecho a mano) que toma ventas acumuladas de seis meses, calcula un promedio mensual, lo contrasta con existencias y genera un sugerido de pedido.

Destinatario principal: Área Comercial.
Objetivo: reporte automatizado de ventas e inventarios para reposición y proyección comercial, con información lista para analizar por producto, familia, empresa y sucursal.

Restricciones del negocio (del contexto):
- Las ventas se expresan en unidades, no en montos.
- Se debe evitar el traslado de inventario entre EMP1 y EMP2 por impacto de IVA y facturación.
- Algunos espacios de sucursal son compartidos entre empresas.
- Aún no existen máximos y mínimos en Alajuela (nota del contexto; ver Cifras de control).

Empresas (confirmadas por el usuario): EMP1 = Petrini, EMP2 = LCDT.
Sucursales del contexto: Heredia, Alajuela, Cartago, San José, Limón.
Sucursales de los insumos: Cariari, Coyol, Ochomogo, Paso Ancho, Zurquí (ver Casos límite / P5 por confirmar).

---

## Datos de entrada

Carpeta `Insumos/` (no se modifica nada dentro de esta carpeta).
Dos archivos Excel (ningún CSV ni PDF).

### Archivo 1: `Meses de inventario x Producto.xlsx`

Contiene múltiples hojas. Resumen de las más relevantes:

| Hoja | Filas | Columnas | Descripción |
|------|-------|----------|-------------|
| `Meses ERA ECOTANK` | 120 | 17 | Ventas acumuladas 7 meses (may–nov 2026), Total, Promedio Mensual, Inventarios al 04-11-2026, Meses Stock (Actual) |
| `INV ERA Coyol` | 2846 | 14 | Maestro de inventario: N°, Descripción, Tipo, Inventario, Existe sustituto, L.M. ensamblado, N.º L.M. producción, N.º ruta, Unidad medida base, Costo ajustado, Costo unitario, Precio unitario, N° proveedor, Plantilla de fraccionamiento predeterminada |
| `Meses Petrini` | 120 | 21 | Igual que Meses ERA ECOTANK con desglose por sucursal: Cariari, Coyol, Ochomogo, Paso Ancho, Zurquí, Saldo Actual |
| `Meses LCDT` | 111 | 26 | Como la anterior con campos adicionales: Precio por Kg Marítimo, Prioridad, Fecha entrega, # Orden de compra, Fecha OC |
| `Cariari LCDT`, `Coyol LCDT`, `Ocho LCDT`, `Paso LCDT`, `Zurqui LCDT` | 3233 c/u | 18 | Maestro por sucursal bloque LCDT: N°, Descripción, Cód. categoría producto, Tipo, Inventario, Existe sustituto, L.M. de ensamblado, N.º L.M. producción, N.º ruta, Unidad medida base, Costo ajustado, Costo unitario, Precio unitario, N° proveedor, Plantilla de fraccionamiento predeterminada, Inventario de seguridad, Familias Código, Columna1 |
| `Cariari Petrini`, `Coyol Petrini`, `Ocho Petrini`, `Paso Petrini`, `Zurqui Petrini` | 3233 c/u | 18 | Igual que las LCDT, bloque Petrini (EMP1) |
| `Ventas Ecotank` | 57 | 9 | N°, Descripción, ventas por mes (may–nov 2026) |
| `Ventas Petrini` | 761 | 10 | N°, Descripción, Familia, ventas por mes |
| `Ventas LCDT` | 784 | 10 | N°, Columna2, Columna3, ventas por mes |
| `Ventas Petrini LCDT y ERA` | 1600 | 10 | N°, Descripción, Familia, ventas por mes |
| `Homologar` | 2566 | 6 | N°, Código alias, Descripción, Descripción alias, Unidad medida base, Cód. categoría producto |
| `Familias` | 3086 | 5 | N°, Descripción, GTIN, Inventario, Cód. categoría producto |
| `Plan de producción` | 79 | 6 | Inicio, Final, Producto, Descripción del material, Días Prog, Requerimiento unidades |
| `Requerimiento` | 25 | 9 | Código Dymanics, Código Best, Descripción, Requerimiento, Justificación, Proceso, Importancia, Detalle, Meses Inventario |
| `Base Datos` | 109 | 16 | Dynamics, Best, Descripción, Familia, Promedio_Mensual, Saldo_Actual, Total_Transito, Meses_Stock_Actual, Producción_Sugerida, Requerimiento, Meses_Stock_Total, Clasificación, Acción_Sugerida, Target_Min, Target_Max, Estado_vs_Target |
| `Dashboard Original` | 16 | 8 | Resumen global: Referencias Críticas, Saludables, Alerta, Sobrestock, Inventario Total, Demanda Total Mensual, Meses Stock Global |
| `Tabla auxiliar` | 97 | 13 | Como Base Datos sin Target_Min/Target_Max/Estado_vs_Target |
| `Tabla Target` | 10 | 3 | Familia, Target_Min, Target_Max (ej. 01-03: 1.5 – 2.5) |

### Archivo 2: `Requerimientos Logística.xlsx`

Hoja `Requerimientos`: 35 filas, 22 columnas.
Filas 5–10: cabecera de título ("SOLICITUD DE REQUERIMIENTOS", "Producción - Logística", periodo "Del 09 al 13 de noviembre 2026", fases 1–3).
Encabezados reales (fila 11):
1. Código Dynamics
2. Código Best
3. Descripción
4. Requerimiento
5. Proceso
6. Importancia
7. Comentario
8. Días de Inventario
9. Estado
10. Responsable del proceso
11. % Avance
12. Fecha requerida
13. Fecha programada inicio
14. Fecha programada fin
15. Fecha real inicio
16. Fecha real fin
17. Atraso (días)
18. Prioridad operativa
19. Riesgo/Bloqueo
20. Comentarios
21. Última modificación (fecha)
22. Última modificación (usuario)

Datos: filas 12–35 (24 requerimientos).

### Notas sobre los insumos
- Los insumos ya traen columnas calculadas (`Promedio Mensual`, `Meses Stock`, `Producción_Sugerida`, `Requerimiento`, `Clasificación`, `Acción_Sugerida`, `Target_Min`, `Target_Max`), pero por decisión de negocio (P2, opción A) el agente de IA **recalcula todo desde las ventas acumuladas** y no toma esas columnas como fuente de verdad.
- Campos extra en insumos no mencionados por el contexto (costos, GTIN, fechas de compra/OC, atrasos, responsable, dashboard, homologación): se documentan aquí porque están en los archivos, pero no participan en las reglas de negocio hasta que se valide su uso.

---

## Reglas de negocio (código, sin IA)

Reglas determinísticas. El agente de IA no las inventa; las aplica.

```python
# Regla R1: Promedio mensual (ventana móvil de 6 meses)
# Entrada: ventas acumuladas de los últimos 6 meses (v1..v6)
# Salida: promedio mensual
def promedio_mensual(ventas_6m):
    return sum(ventas_6m) / 6

# Regla R2: Meses de stock actual
# Entrada: inventario_actual, promedio_mensual
# Salida: meses_stock_actual
def meses_stock_actual(inventario_actual, promedio_mensual):
    if promedio_mensual == 0:
        return None  # división por cero
    return inventario_actual / promedio_mensual

# Regla R3: Sugerido de pedido (reposición)
# Entrada: meses_stock_actual, target_min, target_max, promedio_mensual
# Lógica:
#   si meses_stock_actual < target_min: sugerido = (target_max - meses_stock_actual) * promedio_mensual
#   si meses_stock_actual > target_max: sugerido = 0 (sobrestock, congelar/promocionar)
#   otro caso: sugerido = 0 (saludable, monitorear)
def sugerido_pedido(meses_stock, target_min, target_max, promedio_mensual):
    if meses_stock is None:
        return 0
    if meses_stock < target_min:
        return (target_max - meses_stock) * promedio_mensual
    if meses_stock > target_max:
        return 0
    return 0

# Regla R4: Clasificación de inventario
# Entrada: meses_stock_actual, target_min, target_max
# Salida: SOBRESTOCK / SALUDABLE / CRÍTICO
def clasificacion(meses_stock, target_min, target_max):
    if meses_stock is None:
        return "SIN_DATOS"
    if meses_stock > target_max:
        return "SOBRESTOCK"
    if meses_stock < target_min:
        return "CRÍTICO"
    return "SALUDABLE"

# Regla R5: Acción sugerida
# Entrada: clasificación
# Salida: acción
def accion_sugerida(clasificacion):
    mapa = {
        "SOBRESTOCK": "CONGELAR / PROMOCION",
        "SALUDABLE": "MONITOREAR",
        "CRÍTICO": "PRODUCIR",
        "SIN_DATOS": "REVISAR MANUALMENTE"
    }
    return mapa.get(clasificacion, "REVISAR MANUALMENTE")

# Regla R6: Validación obligatoria antes de usar el reporte
#   - ventas_6m no puede tener todos ceros sin justificación
#   - inventario_actual >= 0
#   - target_min y target_max deben existir para la familia (si faltan, marcar SIN_TARGET)
#   - evitar traslados de inventario entre EMP1 (Petrini) y EMP2 (LCDT)
#   - sucursales compartidas: no duplicar stock
def validar_reporte(fila):
    errores = []
    if fila.ventas_6m is None or all(v == 0 for v in fila.ventas_6m):
        errores.append("VENTAS_CEROS")
    if fila.inventario_actual is None or fila.inventario_actual < 0:
        errores.append("INVENTARIO_INVALIDO")
    if fila.target_min is None or fila.target_max is None:
        errores.append("SIN_TARGET")
    return errores
```

Notas:
- Target_Min / Target_Max por familia provienen de la hoja `Tabla Target` (versión posterior al contexto; rigen para todas las sucursales).
- Alajuela: el contexto dice que aún no tiene máximos/mínimos. Como los insumos son versión posterior, se aplican los targets salvo que se confirme lo contrario para Alajuela (ver Casos límite).

---

## Lo que hace el agente de IA (contrato JSON)

El agente de IA recibe datos ya limpios y devuelve una propuesta de reposición. No inventa reglas ni columnas.

### Request (input)
```json
{
  "producto_id": "PROD0000285",
  "codigo_best": "01-000451",
  "descripcion": "TANQUE ECOTANK 450 LTS AZUL TRICAPA",
  "familia": "01-03",
  "empresa": "EMP2",
  "sucursal": "Coyol",
  "ventas_6m": [0, 22, 16, 0, 0, 0],
  "inventario_actual": 0,
  "target_min": 1.5,
  "target_max": 2.5
}
```

### Response (output)
```json
{
  "producto_id": "PROD0000285",
  "promedio_mensual": 6.333333333333333,
  "meses_stock_actual": 0.0,
  "clasificacion": "CRÍTICO",
  "accion_sugerida": "PRODUCIR",
  "sugerido_pedido": 15.833333333333334,
  "validaciones": [],
  "origen_calculo": "recalculado_desde_ventas_6m"
}
```

### Reglas del contrato
- `ventas_6m`: arreglo de 6 números (ventas en unidades, no montos).
- `origen_calculo` siempre `"recalculado_desde_ventas_6m"` (opción A confirmada).
- Si `validaciones` no está vacío, el agente no debe proponer acción; debe marcar el producto para revisión manual.
- El agente no modifica archivos de `Insumos/`.

---

## Qué produce la app

1. Reporte automatizado de ventas e inventarios por producto, familia, empresa (EMP1/EMP2) y sucursal.
2. Sugerido de pedido y clasificación por producto (SOBRESTOCK / SALUDABLE / CRÍTICO).
3. Acciones sugeridas: PRODUCIR / MONITOREAR / CONGELAR PROMOCION / REVISAR MANUALMENTE.
4. Filtros y vistas: por producto, familia, empresa y sucursal; alertas de capacidad de almacenamiento (por definir en vistas).
5. Exportable a Excel/CSV (formato por definir).

---

## Quién decide

- El Área Comercial valida la información lista para analizar.
- El área de Producción valida los requerimientos de pedidos de fabricación.
- El equipo resuelve las preguntas abiertas y decisiones pendientes (ver Contexto, sección "Preguntas abiertas y decisiones pendientes que debe resolver el equipo").
- El agente de IA **no decide**: solo propone cálculos y clasificaciones; un humano valida antes de usar.

---

## Cifras de control

Del contexto:
- Ventana móvil para promedio mensual: 6 meses.
- Empresas: 2 (EMP1 = Petrini, EMP2 = LCDT).
- Sucursales: 5 (Heredia, Alajuela, Cartago, San José, Limón).
- Unidad de medida: unidades, no montos.
- Escenarios: 2 (conservador y optimista).
- Secciones de la especificación funcional: 7.
- Máximos y mínimos: aún no existen en Alajuela (contexto); versión posterior de insumos trae Target_Min/Target_Max por familia.

Del insumo `Dashboard Original` (hoja del Excel):
- Referencias Críticas: 13
- Saludables: 38
- Alerta: 2
- Sobrestock: 55
- Inventario Total: 5843
- Demanda Total Mensual: 2605.5
- Meses Stock Global: 2.242563807330646

Estas cifras son de referencia del dashboard actual, no cifras calculadas por esta app.

---

## Casos límite

| Caso | Comportamiento |
|------|----------------|
| Producto sin ventas en 6 meses (todos ceros) | `promedio_mensual` = 0; `meses_stock_actual` = None si inventario > 0; validación `VENTAS_CEROS` |
| Inventario actual = 0 y promedio > 0 | `meses_stock_actual` = 0 → clasificación CRÍTICO si está por debajo de target_min |
| target_min / target_max ausentes para una familia | `clasificacion` = SIN_DATOS; acción = REVISAR MANUALMENTE; validación `SIN_TARGET` |
| Sucursal compartida entre EMP1 y EMP2 | No trasladar inventario entre empresas; evitar doble conteo (regla de negocio, por definir en vistas) |
| Máximos/mínimos no existen en Alajuela (contexto) vs targets presentes en insumos | Los insumos son versión posterior; aplicar targets salvo confirmación expresa de excepción para Alajuela |
| Nombres de sucursal no coinciden (contexto: Heredia/Alajuela/Cartago/San José/Limón; insumos: Cariari/Coyol/Ochomogo/Paso Ancho/Zurquí) | Mapeo de sucursales por confirmar (P5). No se asume equivalencia sin confirmar. |

---

## Reglas del sistema

1. No modificar nada dentro de `Insumos/`.
2. No crear archivos adicionales sin autorización.
3. Instalación de dependencias de Python solo con `uv` (nunca `pip`).
4. Scripts temporales de extracción/inspección se borran al terminar.
5. No inventar columnas, archivos ni reglas que no estén en `Contexto_Mi_App.md` ni en los insumos. Si falta algo, se deja como "por confirmar" y se pregunta antes de escribir.
6. Las reglas de negocio son código determinístico (sin IA generativa en la lógica de cálculo).
7. El contrato JSON es la interfaz entre el agente de IA y la lógica de negocio.
