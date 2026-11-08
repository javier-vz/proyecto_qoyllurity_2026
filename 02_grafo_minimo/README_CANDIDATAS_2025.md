# Revisión de anotaciones candidatas (grafo 2025 → documentación 2026)

**Proyecto:** [proyecto_qoyllurity_2026](https://github.com/javier-vz/proyecto_qoyllurity_2026)  
**Fecha de corte:** 8 de noviembre de 2026  
**Estado:** material de revisión humana, **no importación RDF automática**.  
**Herramienta de edición final:** Protégé Desktop, sobre `qoylluriti_ruta_2026_protege.ttl`.

## 1. ¿Qué se extrajo realmente?

Se leyó **íntegramente** el archivo original [`qoyllurity.ttl`](https://github.com/javier-vz/qoyllurity/blob/main/qoyllurity.ttl), sin agregar afirmaciones externas. El archivo examinado coincide a nivel de contenido con la versión actualmente disponible en ese repositorio (Git blob `5d3528c137ce2ebede35bb02e6d0f38addcd0267`). Se recuperaron **87 individuos y sus 161 triples entre individuos** (predicados distintos de `rdf:type`); no se seleccionaron solo las relaciones convenientes a la nueva hipótesis.

La lista contiene **cinco autorreferencias** que deben examinarse antes de reutilizarse y **14 pares de relaciones inversas** que podrían describir una misma vinculación en dos direcciones. Se conservaron intencionalmente todas las filas originales. Cada fila tiene un ID (`QR-AN-001`...) y las URI exactas del triple 2025.

**Importante:** que algo esté escrito en el TTL **no demuestra que haya sucedido en 2026**, ni lo convierte en afirmación culturalmente autorizada, ni garantiza una fuente individual independiente. La fuente original es una decisión de codificación de investigación de 2025. La nueva afirmación requiere evidencia propia de 2026.

## 2. Archivos para trabajar

| Archivo | Qué contiene | Qué hacer |
|---|---|---|
| `ANOTACIONES_CANDIDATAS_2025_PARA_2026.csv` | **161 filas**: todas las relaciones originales, su clasificación y campos de revisión | **Principal: revisar sin importar a Protégé todavía** |
| `PRIMERA_REVISION_PRIORIZADA.csv` | **60 filas** de mayor utilidad potencial para espacio, rutas y adscripción | Empezar aquí, después de examinar los cinco casos de calidad |
| `ENTIDADES_2025_PARA_CONCILIAR.csv` | **87 individuos** originales, tipos, nombres locales, comentarios y posible correspondencia con 2026 | Evitar duplicar lugares y fusionar identidades por nombre |
| `METADATOS_2025_NO_GEO.csv` | **107 atributos literales** originales no geográficos, sin repetir etiquetas ni comentarios | Revisar contexto y tiempo; `tieneImportancia` NO migra |
| `AUDITORIA_CANDIDATAS.json` | Conteos y hashes de las fuentes | Control de integridad |

Los CSV usan **UTF-8 con BOM** para acentos y están delimitados por comas (formato RFC 4180). En Excel con configuración regional española, si las columnas aparecen juntas: **Datos → Desde texto/CSV → Delimitador: coma → Codificación: UTF-8**. No reemplaces la `plantilla_anotaciones.csv` del proyecto: estos archivos son un *backlog*, no la tabla de evidencias confirmadas.

## 3. Las columnas que más importan

- `ID_candidata`: identificador estable dentro de esta extracción.
- `Prioridad`: `0 - CORREGIR`, `1 - ALTA`, `2 - MEDIA`, `3 - BAJA`, `4 - NO MIGRAR`.
- `Nombre_2025_sujeto`, `Predicado_TTL_2025`, `Nombre_2025_objeto`: triple en forma legible.
- `Banderas_calidad` e `ID_pareja_inversa`: autorreferencias, tipos dobles y relaciones inversas a no duplicar.
- `Equivalente_2026_sujeto` / `Equivalente_2026_objeto`: **pistas de nombre**, no afirmaciones de identidad. Para `Tayancani`/`Tayankani`, la grafía requiere revisión. `SantuarioQoylluriti`→`Santuario` es una correspondencia editorial candidata, no `owl:sameAs` automático.
- `Que_anotar_en_csv`: qué conviene documentar o verificar.
- `Consejo_para_TTL_minimo`: por qué no se debe copiar el predicado sin revisar el esquema.
- `Decision_revisor`, `ID_registro_2026`, `Fuente_especifica_2026`, `Localizador_evidencia`, `Responsable_revision`, `Fecha_revision`, `Acceso_evidencia`, `Observaciones_revisor`: **campos para completar manualmente**.

**Decisiones de revisión recomendadas:** `REVISAR`, `ANOTAR_SIN_RDF`, `APROBAR_PARA_TTL`, `PEDIR_VALIDACION_COMUNITARIA`, `DESCARTAR`, `POSTERGAR`. La lista de valores es una convención de trabajo, no un resultado automático.

## 4. Priorización: no confundir importante con cierto

| Prioridad | Filas | Qué significa |
|---|---:|---|
| **0 — CORREGIR** | 5 | Triple de un individuo hacia sí mismo; revisar la modelación original, no exportar. |
| **1 — ALTA** | 60 | Relaciones de lugares, recorridos y grupos susceptibles de servir como preguntas para el registro 2026, **siempre con nueva evidencia**. |
| **2 — MEDIA** | 31 | Acontecimientos situados, procedencia documental o participación que pueden enriquecer la anotación, pero no corresponden directamente al vocabulario mínimo. |
| **3 — BAJA** | 42 | Cronología y jerarquía del modelo 2025; no se presume reiteración en 2026. |
| **4 — NO MIGRAR** | 23 | Objetos, vestimenta, danza, periodicidad o interpretación cosmológica fuera del alcance actual. Se conserva para el historial académico. |

La cifra **14 pares inversos** se refiere a pares dirigidos registrados en sentido opuesto (`estaEn`/`contiene`, `esParteDe`/`tieneParte`, etc.), no a 14 nuevos hechos. **No elimines triples del modelo 2025**, pero evita multiplicar anotaciones o inferir dos evidencias independientes de un solo par.

## 5. Procedimiento exacto de revisión, fila por fila

1. **Conserva la lista original:** descarga los CSV desde este paquete a un directorio de trabajo. No sobrescribas el TTL 2025 ni `qoylluriti_ruta_2026_minimo.ttl`.
2. **Abre `PRIMERA_REVISION_PRIORIZADA.csv`** en Excel o Calc. Después revisa el archivo completo por filtros. Los casos `0 - CORREGIR` deben examinarse primero, pero no son adiciones.
3. Para cada fila, lee `sujeto — predicado — objeto`, los tipos originales, `Banderas_calidad`, el comentario de la entidad en `ENTIDADES_2025_PARA_CONCILIAR.csv` y, si hace falta, el triple original (URI).
4. **Pregunta por el año**: ¿habla solo de la participación 2025 o tenemos una fuente específica para 2026? No copies eventos ni secuencias de 2025 por parecido con 2026.
5. **Busca la evidencia de 2026**: GPX y tramo preciso; punto, tiempo o intervalo; imagen con ID original y contexto; página de libro o artículo; nota de campo; testimonio con atribución y condiciones de acceso. Si no existe, escribe `ANOTAR_SIN_RDF` o `POSTERGAR`.
6. Si aparece una correspondencia con los **10 lugares de referencia** o con `NacionPaucartambo`, verifícala en `ENTIDADES_2025_PARA_CONCILIAR.csv` y en el catálogo 2026; no fusiones nombres por ortografía. Confirma el identificador destino real de 2026.
7. Registra `Decision_revisor`, `ID_registro_2026`, `Fuente_especifica_2026`, `Localizador_evidencia`, quién revisó y `Acceso_evidencia` (`publico`, `solo_equipo`, `restringido_comunidad`, `revisar`).
8. **Solo al aprobar** crea una nueva fila en `plantilla_anotaciones.csv` del repositorio, con su fuente y evidencia. No consideres que rellenar este backlog equivale a una afirmación RDF.
9. Si la anotación está aprobada y **encaja semánticamente** en una de las cinco relaciones del TTL mínimo, entonces edita **la copia** `qoylluriti_ruta_2026_protege.ttl` en Protégé. Guarda el archivo Turtle, vuelve a abrirlo y verifica sus afirmaciones.
10. Si el vínculo **no encaja** en `contieneTramo`, `mencionaLugar`, `proximoAReferencia`, `vinculadoALugar` o `asociadoAGrupo`, **no reutilices incorrectamente otro predicado**. Mantén la anotación CSV y plantea una ampliación de vocabulario específica para una versión posterior.
11. **No vuelques este archivo completo a un repositorio público** si en los campos de revisión ingresaste fotos no autorizadas, coordenadas sensibles, nombres privados o extractos de entrevistas restringidas. Publica una copia filtrada para difusión, sin trasladar datos restringidos.

### Cómo añadir una relación aprobada en Protégé

1. Abre `qoylluriti_ruta_2026_protege.ttl` (de la [guía de edición](README_PROTEGE.md)).
2. **Individuals by class →** selecciona `Tramo`, `LugarReferencia`, `Grupo` o `Recorrido`, según corresponda.
3. Elige un **individuo existente**, comprobando que el IRI corresponde exactamente al del registro aprobado.
4. En **Object property assertions → (+)**, elige una de las cinco propiedades **solamente si sus condiciones de uso están cumplidas**. Ejemplo: `Tramo04 → proximoAReferencia → Mahuayani` está **ya en el TTL**: no la añadas otra vez.
5. Anota el ID de la fila aprobada y la fuente específica en la plantilla CSV; cuando se exporta, el TTL de una relación simple no incorpora automáticamente su procedencia a nivel de triple.
6. Guarda como **RDF Turtle**, verifica en Protégé y actualiza el inventario y `AUDITORIA.json`.

**Protégé normalmente no importa directamente las filas de este CSV como axiomas OWL.** La revisión es deliberadamente manual: el CSV controla evidencia y decisiones, Protégé edita el grafo aprobado.

## 6. Cinco ejemplos reales de revisión

**QR-AN-028:** `SantuarioQoylluriti — estaEn → Sinakara`. El TTL 2025 también conserva la relación inversa `Sinakara — contiene → SantuarioQoylluriti` (**QR-AN-011**). Revísalas como una hipótesis espacial, no como dos observaciones independientes. `Sinakara` todavía no figura como `LugarReferencia` en el TTL mínimo 2026; no lo crees sin identificación documentada y decisión de esquema.

**QR-AN-034:** `Lomada_2025 — pasaPor → Escalerachayoq`. Es una relación de un recorrido representado en 2025. No la asignes automáticamente a `Tramo09` de 2026. Contrasta el trazado y la evidencia de campo, y conserva el término local cuando corresponda.

**QR-AN-006:** `Ukumaris_Paucartambo_2025 — perteneceA → NacionPaucartambo`. Es una adscripción colectiva que requiere fuente y contexto. No la conviertas en `RecorridoRegistrado2026 — asociadoAGrupo → NacionPaucartambo`: el GPS es un registro individual, no el itinerario de una nación completa.

**QR-AN-063:** `SubidaColquePunku_2025 — realizadoPor → Ukumaris_Paucartambo_2025`. No se puede usar como prueba de quién realizó el recorrido de 2026. Tampoco infieras adscripciones individuales solo por fotografías de grupos.

**QR-AN-003:** `Pachakunapata — ocurreEnLugar → Pachakunapata`. Es una autorreferencia ligada a la doble tipificación de 2025. **No generar una copia de esta arista en 2026.**

## 7. Política de datos y evidencia

- La lista refleja **lo que los investigadores modelaron en 2025**, no una descripción cultural universal.
- Los nombres de colectivos y actividades deben interpretarse como denominaciones documentadas, no identidades inferidas por apariencia.
- Los datos de 2026 deben continuar centrados en la **ruta efectivamente registrada** y sus registros, no en una ontología de significados rituales predeterminados.
- **No añadir coordenadas sensibles** al TTL de difusión ni publicar información que requiera autorización comunitaria o personal.
- En caso de testimonios discordantes, conserva múltiples anotaciones atribuidas; no impongas una única verdad por comodidad del modelo.
- El comentario `rdfs:comment` de 2025 y las propiedades `tieneImportancia` son material contextual para revisar, **no fuentes verificadas automáticamente**.

## 8. Incorporación al repositorio

Conserva los archivos bajo `02_grafo_minimo/`:

```text
proyecto_qoyllurity_2026/
└── 02_grafo_minimo/
    ├── README_PROTEGE.md                          (ya existente o de la guía anterior)
    ├── README_CANDIDATAS_2025.md                   (nuevo)
    ├── ANOTACIONES_CANDIDATAS_2025_PARA_2026.csv   (nuevo; 161 filas)
    ├── PRIMERA_REVISION_PRIORIZADA.csv              (nuevo; 60 filas)
    ├── ENTIDADES_2025_PARA_CONCILIAR.csv           (nuevo; 87 filas)
    ├── METADATOS_2025_NO_GEO.csv                   (nuevo; 107 filas)
    └── AUDITORIA_CANDIDATAS.json                   (nuevo)
```

En el `README.md` de raíz puedes añadir, sin reemplazarlo:

```markdown
**Revisión de anotaciones del grafo 2025:** [Candidatas para el registro 2026](02_grafo_minimo/README_CANDIDATAS_2025.md).
```

Esta carpeta **no reemplaza** la ontología ni las tablas actuales de 2026. Cualquier edición manual de resultados debe guardar versiones y fecha de revisión. **No se ha modificado GitHub.**
