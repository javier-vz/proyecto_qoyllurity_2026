# Proyección RDF mínima: ruta registrada de Qoyllur Rit’i en 2026

**No es una sustitución del grafo situado de 2025 ni una descripción ontológica universal de la festividad.**

## Qué contiene

- **12 tramos GPX** de la campaña de 2026, con su archivo de origen, fecha UTC, modo y distancia tabulada.
- **Un nodo central** `RecorridoRegistrado2026`, unido a los 12 tramos por `contieneTramo`.
- **Topónimos** relacionados de dos maneras independientes: `mencionaLugar` cuando el nombre figura en el archivo y `proximoAReferencia` cuando un trazado GPS se acerca a <200 m de un waypoint guardado en favoritos.
- **Una relación de grupo atribuida**: Nación Paucartambo se vincula nominalmente al lugar Paucartambo según UNESCO 00567. No se atribuye todo el GPS a esa Nación.

## Vocabulario mínimo

Cuatro clases (`Recorrido`, `Tramo`, `LugarReferencia`, `Grupo`) y cinco propiedades de objeto (`contieneTramo`, `mencionaLugar`, `proximoAReferencia`, `vinculadoALugar`, `asociadoAGrupo`). La quinta queda definida pero **sin afirmaciones**, pendiente de evidencia de campo. No existen categorías `EventoRitual`, `LugarSagrado`, `Apu`, `EventoDual` ni grados de importancia impuestos.

## Límites probatorios

1. Los nombres de archivos son etiquetas: no prueban que una traza pasara por el centro exacto del lugar.
2. El cálculo de proximidad usa Haversine entre los puntos del GPX y diez referencias no personales de `favoritos_qoyllurity_2026.gpx`. Las referencias PRE pueden ser aproximadas. No prueba presencia ceremonial ni adscripción colectiva.
3. Las trazas son registros de un dispositivo, no un mapa oficial del recorrido de cada nación.
4. Se excluyeron de la selección todos los waypoints privados y los puntos sensibles. **No se redistribuyen coordenadas ni geometrías originales.**
5. No se incorpora ninguna fotografía como ubicada en un sector sin validación documental.
6. La única vinculación entre grupo y lugar procede de UNESCO y se atribuye expresamente a esa fuente, sin presumir que los registros GPS son representativos de la nación.

## Archivos

- `qoylluriti_ruta_2026_minimo.ttl`: datos RDF mínimos.
- `tramos_2026.csv`: inventario de los doce tramos, con fuente y modo.
- `vinculos_2026_y_evidencia.csv`: evidencia específica detrás de cada relación.
- `candidatas_NO_incorporadas.csv`: relaciones tentativas que no deben afirmarse aún.
- `AUDITORIA.json`: conteos e hipótesis de trabajo.

## Consultas SPARQL

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tramo ?nombre WHERE {
  qr26:RecorridoRegistrado2026 qr26:contieneTramo ?tramo .
  ?tramo rdfs:label ?nombre .
}
ORDER BY ?tramo
```

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tramo ?referencia ?nombre WHERE {
  ?tramo qr26:proximoAReferencia ?referencia .
  ?referencia rdfs:label ?nombre .
}
```

Para publicar una versión en abierto: primero revisar la sensibilidad de los enlaces a GPX fuente, revisar derechos de las fotografías y acordar reglas de adscripción con participantes pertinentes.
