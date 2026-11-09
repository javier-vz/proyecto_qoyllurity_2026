# Ontología etnográfica Qoyllur Rit’i 2025–2026 — v0.3

**Archivo de trabajo:** `qoylluriti_ontologia_etnografica_2025_2026_v03.ttl`

## Qué representa

Modelo integrado de **festividades, prácticas culturales recurrentes, actividades situadas, lugares, naciones y colectivos, roles, objetos y recorridos**, con relaciones espaciales y temporales. La base conceptual y de instancias es `qoyllurity.ttl` (2025), enriquecido con testimonios de campo de 2025–2026 y los 12 tramos del TTL mínimo de 2026.

**Una práctica se conserva como concepto continuo** (`PracticaIntiAlabado`). Sus realizaciones de 2025 y 2026 son individuos relacionados mediante `instanciaDePractica`. `IntiAlabado_2025` del grafo original se conserva como individuo histórico; no se creó un duplicado. Los 12 GPX se conservaron en el espacio de nombres `qr26:`.

## Dimensión etnográfica

Se incorporan las explicaciones del participante sobre la preparación, romería, transporte en camión, apoyo de mamawairis, subida y bajada de Colque Punku, transporte colectivo de la cruz, encuentro de Wataskama, Lomada, Yanaqancha y queperinas, paso nocturno por Escalerachayoq, Inti Alabado, bautizo de moroco, recibimiento de Ocongate, regreso nocturno y Corpus Christi.

Los contenidos se consignan **en las actividades mismas**, mediante `detalleEtnografico`, `ocurreEnLugar`, `participaColectivo`, `involucraRol`, `involucraObjeto`, `instanciaDePractica`, `sigueA` y `asociadaAFestividad`.

## Relación con la fotografía y el audiovisual

El inventario audiovisual de 180 medios se mantiene **por separado** como catálogo de investigación. El TTL cultural **no genera individuos por fotografía**. La transmisión de archivos por WhatsApp no se presenta como fuente: las fuentes pertinentes son el trabajo de campo, los testimonios y las observaciones. El canal de envío no equivale al origen documental. La publicación de fotografías se decide por separado, en especial las fotos personales del bautizo y las de menores.

## Criterios de conciliación

- Se preservan los individuos y relaciones culturales del TTL histórico salvo errores de modelado explícitos.
- `IntiAlabado_2025`, `Lomada_2025` y el viaje vehicular 2025 son actividades, no lugares.
- `Escalerachayoq` y `Pachakunapata` quedan como lugares; se crean actividades separadas para los acontecimientos allí descritos.
- Se retiran cinco autoenlaces y la propiedad `tieneImportancia` para evitar jerarquías culturales impuestas.
- Las coordenadas puntuales del TTL 2025 quedan en el **archivo original** hasta su auditoría espacial, evitando afirmaciones geográficas exactas no validadas. Los GPX 2026 conservan sus metadatos y criterios de proximidad.
- El TTL de 2025 contiene afirmaciones de su propia fuente; se conservan como conocimiento previamente documentado. Solo se marcan como pendientes cuestiones específicas: visibilidad del glaciar en Q’espi Cruz, denominación de danza de Yanaqancha, significado del zigzag y año de las fotografías de Ocongate.
- Corpus Christi figura como festividad diferenciada; el vínculo con Qoyllur Rit’i describe **el cierre del itinerario de Nación Paucartambo**.

## Principales métricas verificadas

{
  "triples": 1986,
  "clases_owl": 34,
  "practicas_individuos": 30,
  "eventos_rituales": 34,
  "otras_actividades": 51,
  "lugares": 44,
  "tramos_gps": 12,
  "colectivos": 7,
  "relaciones_objeto_owl": 50,
  "nodos_imagen_individual": 0,
  "triplas_removidas_de_baseline": 132
}

## Para Protégé

Abrir `qoylluriti_ontologia_etnografica_2025_2026_v03.ttl` con Protégé Desktop como RDF/Turtle. Prefijos: `qr:` = `http://example.org/festividades#` (grafo histórico y ampliación cultural) y `qr26:` = `urn:qoylluriti:registro2026:` (GPX). El TTL se puede cargar y consultar con RDFLib.

## Registro de versiones

- **v0.1**: primera ampliación propuesta.
- **v0.2**: integración audiovisual extensa. Se reemplaza como línea de trabajo ontológica.
- **v0.3**: modelo cultural integrado, sin individuos por fotografía, con continuidad interanual y distinción entre lugar/evento.

El repositorio GitHub **no se modificó automáticamente**.
