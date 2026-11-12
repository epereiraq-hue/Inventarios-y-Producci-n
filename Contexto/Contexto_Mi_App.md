# Contexto - Mi App

_Contenido extraído automáticamente del documento `Proceso Planificación Inventarios y Producción.docx`._

Proceso

Planificación y control de inventarios de una empresa manufacturera y comercializadora

Contexto

En la actualidad el cálculo de reposición de inventario y solicitud de requerimientos para el área de producción se hace en un archivo manual que toma ventas acumuladas de seis meses, calcula un promedio mensual, lo contrasta con las existencias y genera un sugerido de pedido. 

El Área Comercial necesita información lista para analizar, desglosada por producto, familia, empresa (EMP1 y EMP2) y sucursal (Heredia, Alajuela, Cartago, San José, Limón). Las ventas se expresan en unidades, no en montos, no existen aún máximos y mínimos en Alajuela. 

También se debe evitar el traslado de inventario entre EMP1 y EMP2 por el impacto de IVA y facturación, algunos espacios de sucursal son compartidos entre empresas. 

Tarea: 

Elaborar una especificación funcional del reporte automatizado de ventas e inventarios para reposición y proyección comercial, con estas secciones: 1. Objetivo y usuarios del reporte. 2. Matriz de datos: campo, descripción, fuente de origen, transformación requerida y responsable de la fuente. 3. Reglas de cálculo: promedio mensual con ventana móvil de seis meses, stock de seguridad, punto de reorden y sugerido de pedido. Señala qué debe validarse antes de usarse. 4. Tratamiento de ventas extraordinarias, estacionalidad y negocios futuros, con escenarios conservador y optimista. 5. Filtros y vistas: por producto, familia, empresa y sucursal, y alertas de capacidad de almacenamiento. 6. Frecuencia de actualización, accesos y perfiles de usuario. 7. Preguntas abiertas y decisiones pendientes que debe resolver el equipo.

# Prompt estructurado: Contexto, Plan, Construir y Cifras

## Contexto

Proceso: planificación y control de inventarios de una empresa manufacturera y comercializadora.

Situación actual: el cálculo de reposición de inventario y la solicitud de requerimientos al área de producción se hacen en un archivo manual que toma las ventas acumuladas de seis meses, calcula un promedio mensual, lo contrasta con las existencias y genera un sugerido de pedido.

Necesidad del Área Comercial: información lista para analizar, desglosada por producto, familia, empresa (EMP1 y EMP2) y sucursal (Heredia, Alajuela, Cartago, San José, Limón).

Particularidades: las ventas se expresan en unidades, no en montos, y aún no existen máximos y mínimos en Alajuela.

Restricciones: se debe evitar el traslado de inventario entre EMP1 y EMP2 por el impacto de IVA y facturación; algunos espacios de sucursal son compartidos entre empresas.

## Plan

Objetivo: elaborar una especificación funcional del reporte automatizado de ventas e inventarios para reposición y proyección comercial.

Reemplazar: el archivo manual actual por un reporte automatizado, con información lista para analizar por el Área Comercial.

Respetar: la separación de inventario entre EMP1 y EMP2 (sin traslados) y los espacios de sucursal compartidos.

Resultado esperado: un documento que cubra las siete secciones indicadas en el apartado Construir, señalando qué debe validarse antes de usar el reporte.

## Construir

Objetivo y usuarios del reporte.

Matriz de datos: campo, descripción, fuente de origen, transformación requerida y responsable de la fuente.

Reglas de cálculo: promedio mensual con ventana móvil de seis meses, stock de seguridad, punto de reorden y sugerido de pedido. Señalar qué debe validarse antes de usarse.

Tratamiento de ventas extraordinarias, estacionalidad y negocios futuros, con escenarios conservador y optimista.

Filtros y vistas: por producto, familia, empresa y sucursal, y alertas de capacidad de almacenamiento.

Frecuencia de actualización, accesos y perfiles de usuario.

Preguntas abiertas y decisiones pendientes que debe resolver el equipo.

## Cifras

6 meses: ventana móvil para el promedio mensual de ventas.

2 empresas: EMP1 y EMP2.

5 sucursales: Heredia, Alajuela, Cartago, San José y Limón.

Unidad de medida: las ventas se expresan en unidades, no en montos.

2 escenarios: conservador y optimista.

7 secciones: las que debe contener la especificación funcional.

Máximos y mínimos: aún no existen en Alajuela.
