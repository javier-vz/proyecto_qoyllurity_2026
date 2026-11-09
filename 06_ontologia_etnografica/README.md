# Grafo integral Qoyllur Rit’i 2025–2026 — v0.2

**Corte documental:** 8 de noviembre de 2026. **Estado:** borrador integral de trabajo, corregible semana a semana. No se ha reemplazado ningún repositorio ni los TTL originales.

## Archivo principal

- `qoylluriti_2025_2026_integral_v02.ttl`: **10,886 triples** RDF/Turtle. Apertura directa en Protégé, rdflib o SPARQL local.
- 21 clases OWL, 37 propiedades de objeto, 38 propiedades de datos.
- 51 actividades documentadas, 36 prácticas culturales y 28 lugares de referencia.
- 17 etapas del itinerario narrativo, 12 tramos GPX de 2026.
- 180 registros audiovisuales individuales en 23 lotes (por año/actividad).
- 59 nodos de anotación etnográfica (48 entradas transcritas de CSV y 11 referencias consolidadas anteriores).
- 87 referencias de entidades históricas y 161 relaciones históricas candidatas, **no importadas como afirmaciones**.
- 20 preguntas de verificación abiertas.

## Qué está efectivamente incluido

1. **RDF mínimo 2026**: los 12 tramos originales y las relaciones con topónimos y waypoints con sus limitaciones originales.
2. **v0.1**: todas sus 698 afirmaciones originales sin sobrescritura de archivo; sólo se añaden relaciones de las revisiones posteriores.
3. **Ruta completa narrada**: preparación, ensayo, misa, romería, salida, Ccatcca, prioste, Mahuayani, Santuario, Colque Punku, cruz, Lomada, Wataskama, Q’espi Cruz (sin fijar su orden), Yanaqancha, Escalerachayoq, Inti Alabado, bautizo, Ocongate, regreso nocturno y Corpus Christi 2026.
4. **Evidencias**: los 180 ID originales individualizados con nombre del medio, fuente ZIP, SHA256 cuando disponible, descripción visual, advertencias, año cuando está realmente confirmado, nivel de acceso y permisos pendientes.
5. **Anotaciones**: QR-AN-044 a 053 según documentos revisados, corrigiendo QR-AN-046: el video muestra a ukumaris Paucartambo **llevando** la cruz, no necesariamente el inicio del relevo.
6. **Legado 2025**: 87 referencias y 161 relaciones candidatas representadas como registros de revisión, sin activar autorreferencias, doble tipificación lugar/evento ni juicios de importancia.

### Principios de representación

- La práctica cultural y su **ocurrencia por año** son individuos distintos.
- Testimonio directo puede respaldar una actividad **sin fotografía** (por ejemplo Wataskama).
- Una foto contextual NO prueba por sí sola los roles, naciones, escuelas, órdenes rituales ni significados.
- Las comparaciones de nieve 2025–2026 son cualitativas, no mediciones climáticas.
- Q’espi Cruz está situado como hito de la Lomada pero su orden respecto a Yanaqancha y visibilidad del glaciar permanecen **abiertos**.
- Cinco fotografías de Ocongate y tres de Ccatcca tienen **año de captura pendiente**; la secuencia de retorno antes de Corpus Christi sí consta en testimonio.
- Corpus Christi Paucartambo 2026 y Qoyllur Rit’i 2026 son **festividades independientes** vinculadas por la secuencia vivida de Nación Paucartambo.
- El Corpus incluye fotografías con menores: **no se presume consentimiento de publicación**. El bautizo personal también permanece restringido.
- Las fotos, videos y pistas GPX en binario NO se incrustan en el TTL. Este paquete incluye metadatos, matriz de trabajo y referencias a sus nombres originales.

## Otros archivos del paquete

- `SOLO_TRIPLES_AGREGADOS_v02.ttl`: diferencia RDF respecto del TTL v0.1, para auditoría; no cargarlo por separado en lugar del integral.
- `AUDITORIA_VALIDACION_v02.json`: números y SHA-256 del TTL integral.
- `PENDIENTES_DE_VALIDACION.md`: 20 verificaciones abiertas.
- `CONSULTAS_DE_EJEMPLO.rq`: consultas SPARQL para Protégé/rdflib.
- `CHANGELOG_v02.md`: cambios efectuados respecto de v0.1.
- `INVENTARIO_FOTOGRAFICO_180.csv`: copia del inventario maestro conciliado.
- `ANOTACIONES`: documentos de campo usados como evidencia.
- `LEGADO_2025`: copia del TTL original y matrices de referencia para validación. **No se fusionan sus axiomas en el TTL 2026**.
- `construir_ttl_integral_qoylluriti_v02.py`: script de construcción reproducible con archivos fuente ubicados bajo `/mnt/data`; las rutas pueden ajustarse si se usa en otro equipo.

## Cómo continuar la revisión

Abrir el TTL integral en Protégé y usar `PENDIENTES_DE_VALIDACION.md` como lista de decisiones. Una vez confirmada una corrección, anotarla en su CSV fuente y en el constructor, actualizar el estado de validación y exportar una versión `v0.3` sin sobrescribir esta `v0.2`. Mantener identificadores estables de actividades, medios y testimonios. No publicar ni ejecutar `owl:sameAs` sobre referencias históricas no conciliadas.

**No se ha realizado ningún cambio en GitHub.**
