# Qoyllur Rit’i — v0.4.2: auditoría etnográfica y referencias

**Fecha:** 13 de noviembre de 2026. **Estado:** versión de revisión; no subida a GitHub.

## Procedencia de la base

Archivo de referencia en GitHub: `06_ontologia/qoylluriti_etnografia_v04_1_CON_MEDIOS.ttl`, blob SHA `e6dbee2775a84ccda836a71b2c60876420ced8d5`.

Para conservar el contenido RDF de v0.4.1, ante una limitación de descarga directa del archivo remoto, la base se recompuso a partir de la copia integral v0.4 y del parche multimedia verificado en v0.4.1: medio `QR-MED-2026-050-11` y sus enlaces desde `IntiAlabado` y `Tayancani`. Esta v0.4.2 **no es una edición byte a byte de la serialización de GitHub**, sino una reconstrucción semántica de esa base con las modificaciones de la auditoría. La serialización y el orden de triples pueden diferir.

## Cambios etnográficos

1. Grafía confirmada **Wataskama**; el nombre designa el encuentro y el sector en el testimonio. No se da por probada su identidad geográfica con Qochapata.
2. Etiquetas **Qapaq Qollas** y **Qapaq Chunchos** de Paucartambo, manteniendo URIs previas.
3. El canto de Q’espi Cruz se atribuye a los Qapaq Qollas; observadores no se modelan como ejecutantes de esa práctica.
4. Se distinguen dos encuentros durante el descenso de Colque Punku; la Lomada comienza **algunas horas después**, no inmediatamente.
5. Ukumaris, Qapaq Qollas y Qapaq Chunchos parten cerca en el tiempo, pero **por separado**, no en una caravana única.
6. Se documenta el compromiso previo de tres peregrinaciones anuales consecutivas, `Moroco` para tres primeros años y `Antiguo` desde el cuarto (individuo de `Rol`).
7. Dos bautizos: se conserva la URI histórica `BautizoMorocos` para Tayankani y se agrega `BautizoPrimerAscensoColquePunku`. Las cinco imágenes asociadas previamente al bautizo requieren revisión visual.
8. Descanso en Yanaqancha se separa de la danza en la ladera (`DanzaLaderaYanaqancha`, individuo de clase existente); denominación local desconocida.
9. Wataskama: saludos por parejas de agrupaciones y carreras de alta exigencia. No extrapolar castigos ni lista de comparsas de 2017 a 2025–2026.
10. Se explicita el límite de observación del investigador que participa activamente con una agrupación.

## Fuentes y alcance

- **Testimonio de campo y auditoría de noviembre de 2026**: URI `urn:qoylluriti:fuente:auditoria_etnografica_participante_2026`. Es testimonio conversacional situado, no publicado ni depositado formalmente.
- **Chaucca Mancco, Roger (2018)**, *Los Pablitos de Paucartambo*. Tesis UNSAAC, apartado 5.4.2 (pp. 81–83). https://hdl.handle.net/20.500.12918/3606. Referencia pertinente al wataskama y al topónimo Qochapata documentado en 2017.
- **Torres Lezama, Vicente (2020)**, *Kallpachakuy: Coca, bebida y cigarro como fuerza y protección en la peregrinación a Qoyllurit’i*. *Anthropologica*, 38(45), 133–159. https://doi.org/10.18800/anthropologica.202002.006. Contexto, no prueba directa de prácticas 2025–2026.
- **Flores Lizana, J. Carlos (1987)**, *El santuario de Qoyllur-rit’i (una peregrinación andina). Expresión y germen de organización campesina*. *Anthropologica*. https://doi.org/10.18800/anthropologica.198701.008. Contexto de organización de la peregrinación.
- **Salas Carreño, Guillermo (2025/2026)**, *How and Why the Quyllurit’i Pilgrimage Is Related to the Tupac Amaru Rebellion*. *Latin American Research Review*, 61(2), 253–271. https://doi.org/10.1017/lar.2025.10085. Contexto historiográfico.

`dcterms:source` vincula testimonios y fuente directamente pertinente con los individuos modificados; `rdfs:seeAlso` identifica lecturas de contexto. No se han creado clases bibliográficas, jerarquías inferidas ni propiedades de objeto propias de una teoría del ritual.

## Validación automatizada

| Indicador | Valor |
|---|---:|
| Triples v0.4 (copia integral) | 1644 |
| Triples v0.4.1 (base reconstruida) | 1653 |
| Triples v0.4.2 | 1702 |
| Clases OWL | 11 |
| Propiedades de objeto OWL | 18 |
| Propiedades de datos OWL | 7 |
| Medios visuales | 181 |
| Enlaces a medios | 336 |

Se verificó sintaxis Turtle con `rdflib`, análisis de ida y vuelta y conservación cuantitativa de los enlaces a medios. Estas comprobaciones **no sustituyen la revisión etnográfica**.

## Pendientes de verificación

- Corroborar la localización geográfica y posible correspondencia Wataskama–Qochapata.
- Confirmar lista de comparsas de Nación Paucartambo en 2025-2026.
- Verificar imágenes QR-FOT-2025-051-01 a 05 antes de atribuirlas a un bautizo específico.
- Confirmar detalles gestuales y temporalidad del primer bautizo/compromiso trienal.
- Confirmar nombre local de la danza colectiva en la ladera de Yanaqancha.
- Verificar si cada comparsa identificada participa en la danza de Yanaqancha y su criterio exacto de antigüedad.
- Revisar orden de hitos secundarios de Lomada contra GPS y entrevistas.
- Verificar detalles del saludo y eventuales sanciones en Wataskama 2025-2026.

## Próximo paso recomendado

Revisar esta v0.4.2 junto con Dina, recabar el inventario actual de danzas de Nación Paucartambo y contrastar el topónimo del sector Wataskama con informantes. Luego revisar imágenes de los bautizos y considerar un commit separado en GitHub.
