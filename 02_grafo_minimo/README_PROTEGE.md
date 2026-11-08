# Cómo ampliar el grafo de Qoyllur Rit’i 2026 en Protégé

**Guía de trabajo para [`proyecto_qoyllurity_2026`](https://github.com/javier-vz/proyecto_qoyllurity_2026)**  
**Versión de la guía:** 1.0 · 8 de noviembre de 2026  
**Programa recomendado:** Protégé Desktop 5.x (interfaz OWL)  
**Archivo original, que NO se reemplaza:** [`qoylluriti_ruta_2026_minimo.ttl`](./qoylluriti_ruta_2026_minimo.ttl)  
**Copia destinada a edición en Protégé:** [`qoylluriti_ruta_2026_protege.ttl`](./qoylluriti_ruta_2026_protege.ttl)

> **Objetivo.** Ampliar el registro de la campaña 2026 sin adelantar clasificaciones sobre los significados rituales. La ruta documentada es el centro del grafo: solo se agregan entidades, lugares, grupos y relaciones cuya fuente y regla de evidencia puedan identificarse. Protégé facilita la edición; **no valida por sí solo la verdad etnográfica**.

## 0. Antes de comenzar: comprobar la publicación del repositorio

El repositorio es **público**. En la revisión del 8/11/2026 aparece un PDF en `05_manuscrito_aportado/` identificado expresamente como **NO PUBLICAR / NO ENTRENAR**. Si el manuscrito sigue en evaluación y no tiene autorización de publicación, se debe gestionar su retirada **también del historial Git**, no solo del árbol actual. Este problema es independiente de Protégé y debe tratarse prioritariamente. Guía oficial: [GitHub — Eliminar datos confidenciales de un repositorio](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

**No subas** GPX con coordenadas sensibles, datos personales, fotografías identificables sin permisos, entrevistas privadas ni anotaciones de acceso restringido. Las rutas originales permanecen en el archivo de investigación; el TTL público no tiene geometrías GPS.

## 1. Qué hay exactamente en el grafo actual

| Elemento | Identificadores reales | Para qué sirve |
|---|---|---|
| `Recorrido` | `qr26:RecorridoRegistrado2026` | Agrupa los registros documentales de 2026; **no** equivale al itinerario oficial de una Nación. |
| `Tramo` | `qr26:Tramo01` a `qr26:Tramo12` | Registros asociados a los 12 archivos GPX (8 a pie, 4 vehiculares). |
| `LugarReferencia` | `qr26:Mahuayani`, `qr26:Santuario`, `qr26:ColquePunku`, etc. | Topónimos o waypoints de referencia; no límites oficiales. |
| `Grupo` | `qr26:NacionPaucartambo` | Denominación documentada de un colectivo; no presume pertenencia individual. |

Las **cinco relaciones ya definidas** son:

| Propiedad | Sujeto esperado | Objeto esperado | Regla de uso |
|---|---|---|---|
| `contieneTramo` | `Recorrido` | `Tramo` | El archivo GPX existe y está incluido en el inventario. |
| `mencionaLugar` | `Tramo` | `LugarReferencia` | El **nombre del archivo** consigna ese topónimo, sin afirmar paso exacto. |
| `proximoAReferencia` | `Tramo` | `LugarReferencia` | Hay cálculo espacial guardado en el CSV de evidencia y referencia revisada. El umbral inicial es **menos de 200 m**. |
| `vinculadoALugar` | `Grupo` | `LugarReferencia` | La fuente concreta documenta una vinculación; no necesariamente propiedad o territorialidad. |
| `asociadoAGrupo` | `Tramo` o `Recorrido` | `Grupo` | **No tiene afirmaciones en la versión inicial.** Solo añadir con evidencia de adscripción del *registro específico*, no por el nombre del archivo ni por quién llevaba el GPS. |

En el fichero original hay **181 triples**, **cuatro clases RDFS**, **cinco propiedades RDF** y 12 aristas `contieneTramo`. Las relaciones `mencionaLugar` (18), `proximoAReferencia` (12) y `vinculadoALugar` (1) se documentan en [`vinculos_2026_y_evidencia.csv`](./vinculos_2026_y_evidencia.csv). **No reinterpretar esas 43 relaciones como si todas indicaran presencia física o pertenencia ritual.**

## 2. Preparar Protégé sin modificar el original

### 2.1. Descargar la carpeta adecuada

1. En GitHub, abre [`02_grafo_minimo/`](https://github.com/javier-vz/proyecto_qoyllurity_2026/tree/main/02_grafo_minimo).
2. Conserva localmente los siguientes archivos con **exactamente esos nombres**:
   - `qoylluriti_ruta_2026_minimo.ttl` — versión inicial **intocable**.
   - `qoylluriti_ruta_2026_protege.ttl` — copia compatible con las vistas OWL (adjunta a esta guía).
   - `vinculos_2026_y_evidencia.csv` — registro de respaldo de relaciones.
   - `plantilla_anotaciones.csv` — filas nuevas antes de añadir relaciones.
   - `candidatas_NO_incorporadas.csv` — hipótesis que **no** debes afirmar todavía.
   - `tramos_2026.csv` — correspondencia entre `GPX-01…12` y sus archivos.
3. Abre la versión compatible en Protégé con **File → Open… → `qoylluriti_ruta_2026_protege.ttl`**. Si aparece un cuadro de sintaxis, elige **Turtle** (o permite la detección automática).
4. Ve a **Active Ontology** y comprueba que se abrió el archivo correcto; el prefijo `qr26:` corresponde a `urn:qoylluriti:registro2026:`. Una URI con esquema `urn:` es un **identificador**, no un enlace web.

### 2.2. ¿Por qué dos TTL?

El TTL original declara `rdfs:Class` y `rdf:Property`. Eso es RDF/RDFS válido, pero puede no aparecer como esperas en las pestañas **Classes** y **Object properties** del editor OWL. La copia de trabajo declara las mismas clases como `owl:Class` y las cinco relaciones como `owl:ObjectProperty`, registra `inicioUTC`, `longitudKm` y `modalidad` como propiedades de datos y deja expresos los metadatos de Dublin Core como anotaciones. **No cambia ningún individuo ni agrega relaciones culturales, topónimos o coordenadas**. La declaración de esquema sí es distinta y debe versionarse como tal.

> No intentes abrir el TTL original y «arreglarlo» borrando clases que no se vean. Utiliza la copia para Protégé y guarda las mejoras en esa copia.

### 2.3. Preparar el espacio de trabajo

1. Abre la pestaña **Entities**: agrupa clases, propiedades e individuos.
2. En **File → Preferences → Renderer**, selecciona **Render entities using annotation values** y elige `rdfs:label` (idioma `es`) para ver nombres legibles. Si alguna clase parece llamarse «Grupo o colectivo» en lugar de `Grupo`, es solo su etiqueta: **no cambió su IRI**.
3. En **Classes**, confirma que aparezcan `Recorrido`, `Tramo`, `LugarReferencia` y `Grupo`.
4. En **Object properties**, confirma las cinco propiedades enumeradas arriba.
5. En **Data properties**, confirma `inicioUTC`, `longitudKm` y `modalidad`.
6. En **Individuals by class**, selecciona `Tramo` y confirma `Tramo01…Tramo12`; selecciona `LugarReferencia` para ver los diez lugares.
7. Si no ves una pestaña, puedes activarla en **Window → Tabs**. Los nombres de los botones pueden variar ligeramente entre versiones de Protégé 5.x.

## 3. Primer ejercicio: leer antes de añadir

1. Abre **Individuals by class** y selecciona la clase `Tramo`.
2. Selecciona `Tramo04` (o búscalo con la búsqueda global de Protégé).
3. En **Object property assertions** verás, entre otras, estas dos afirmaciones existentes:

   ```turtle
   qr26:Tramo04 qr26:mencionaLugar qr26:Mahuayani .
   qr26:Tramo04 qr26:proximoAReferencia qr26:Mahuayani .
   ```

4. Lee su diferencia: la primera se apoya en el **nombre del GPX**; la segunda procede de un **cálculo de proximidad**. Revisa en `vinculos_2026_y_evidencia.csv` las filas `R-NOM-GPX-04-Mahuayani` y `R-GEO-GPX-04-Mahuayani`.
5. En **Data property assertions**, observa `inicioUTC`, `longitudKm` y `modalidad` del tramo. En **Annotations** (si están visibles), consulta `rdfs:label`, `dcterms:identifier` y `dcterms:source`.

**Resultado esperado:** poder explicar el origen de cada afirmación sin añadir nada. Repite con `Tramo05`/`ColquePunku`: el archivo **menciona** Colque Punku, pero la proximidad a su waypoint no se incorporó como hecho confirmado.

## 4. Flujo obligatorio antes de crear una nueva relación

**Primero anota, después edita la ontología.** Abre `plantilla_anotaciones.csv` y crea una fila por cada afirmación propuesta. Los encabezados reales del archivo son:

`ID_anotacion, ID_fuente, Localizador_en_fuente, Año_de_evidencia, ID_entidad_origen, Relacion_propuesta, ID_lugar_o_grupo_destino, Criterio_evidencia, Estado, Anotador, Fecha_anotacion, Nivel_acceso, Revisado_por, Observaciones`.

Registra como mínimo: identificación inequívoca de fuente, **localizador concreto** (GPX + hora, foto, página, minuto de audio), nodo origen, predicado, nodo destino, criterio, autor de la anotación y estado. Para una frase etnográfica, agrega **quién la sostiene** y en qué contexto; si la interpretación no está respaldada, debe permanecer en el CSV.

Estados de revisión del proyecto:

- **Registrado:** el dato aparece directamente en el registro (por ejemplo, topónimo del nombre GPX).
- **Calculado:** se obtuvo mediante un procedimiento repetible, con parámetros (proximidad a waypoint).
- **Atribuido:** una fuente identificada sostiene la relación (autor, participante, documento institucional).
- **Propuesto:** todavía sin revisión suficiente. **No exportar a RDF.**
- **Rechazado:** mantener la razón de rechazo, sin triple afirmativo.

**Control de acceso:** usa `publico`, `solo_equipo`, `restringido_comunidad` o `revisar`. No pongas en un repositorio público anotaciones restringidas. Esta hoja es el **registro de procedencia por afirmación**; una anotación general sobre el nodo no sustituye al CSV.

## 5. Operaciones exactas en Protégé

### A. Crear un lugar de referencia, sin afirmar todavía su pertenencia

**Realiza esto solo cuando hayas documentado el topónimo en una fuente concreta.**

1. **Individuals by class** → selecciona `LugarReferencia`.
2. En el panel de individuos, usa **Add individual (+)** e introduce un ID único en formato ASCII sin espacios, por ejemplo `SectorCampo13` **solo como plantilla**. No lo subas al repositorio con ese nombre de ejemplo.
3. En **Annotations**, añade `rdfs:label` con el nombre original tal como aparece en la fuente y etiqueta de idioma `es` cuando corresponda. Guarda variantes ortográficas como notas o etiquetas alternativas **atribuidas**, no fusionando lugares automáticamente.
4. Añade `rdfs:comment` únicamente si puedes describir la **fuente y el alcance** (por ejemplo, «Topónimo consignado en cuaderno de campo 2026, entrada XX»); no añadas «sagrado», «central» o «estación ritual» sin fuente interpretativa autorizada.
5. Agrega la referencia a la fuente en la anotación y en `plantilla_anotaciones.csv` antes de enlazarlo con un tramo.
6. Guarda. El individuo puede quedar **sin conexiones por ahora**: es preferible a inventar una relación para evitar nodos aislados.

### B. Crear un tramo nuevo a partir de un GPX real

**No ejecutes esto si todavía no existe un archivo GPX adicional verificado.**

1. Comprueba en `tramos_2026.csv` que el GPX no está registrado y asígnale el próximo código libre (`GPX-13` sería solo el siguiente si no se añadió ninguno antes).
2. En **Individuals by class** → `Tramo` → **Add individual (+)**: utiliza `Tramo13` únicamente si corresponde a un archivo real.
3. En **Annotations**, registra `rdfs:label` (nombre legible), `dcterms:identifier` (`GPX-13`) y `dcterms:source` (nombre **exacto** del GPX, sin adjuntar públicamente su geometría).
4. En **Data property assertions**, añade `modalidad` (`pie` o `vehiculo`, según el archivo); `inicioUTC` con tipo **`xsd:dateTime`** si el GPX registra tiempo, y `longitudKm` con tipo **`xsd:decimal`** si esa distancia fue calculada y documentada. No rellenes fechas, modos ni distancias por analogía.
5. Selecciona ahora el individuo `RecorridoRegistrado2026` (clase `Recorrido`).
6. En **Object property assertions → Add (+)**: propiedad `contieneTramo`, destino `Tramo13`.
7. Abre el nuevo `Tramo13` y comprueba que aparece el enlace; documenta en CSV la relación `RecorridoRegistrado2026 → contieneTramo → Tramo13`.
8. Añade filas en `tramos_2026.csv` y en `vinculos_2026_y_evidencia.csv` con **identificadores consistentes**. Las dos tablas deben mantenerse sincronizadas con el TTL.

### C. Vincular un tramo con un lugar ya existente

Ejemplo **de lectura**, no relación nueva: `Tramo04 → mencionaLugar → Mahuayani` ya existe.

1. Elige la fila aprobada en `plantilla_anotaciones.csv`; comprueba la fuente.
2. En Protégé → **Individuals by class** → `Tramo` → selecciona el tramo real.
3. En **Object property assertions → Add (+)** elige **la propiedad correcta** y después el lugar existente:
   - `mencionaLugar`, si el nombre aparece en el archivo;
   - `proximoAReferencia`, si existe cálculo y está en el CSV de evidencia.
4. Verifica el sentido: **Tramo → Lugar**, no al revés.
5. Si la misma afirmación ya existe, **no la dupliques**. En Protégé un axioma duplicado no documenta «dos evidencias»; conserva las dos evidencias como dos filas con sus fuentes en el CSV.
6. Guarda el identificador de la anotación aprobada en el registro de vínculos y vuelve a abrir la ficha de ambos individuos para inspeccionar el resultado.

### D. Incorporar un grupo, sin inventar membresía

1. `Grupo` → **Add individual (+)** solo si hay una denominación y fuente verificables. No crees una entidad nueva para una simple variación ortográfica sin revisar su identidad.
2. Añade `rdfs:label` y un `dcterms:source` a partir de la fuente concreta.
3. Si esa fuente documenta una vinculación territorial, desde el grupo usa `vinculadoALugar` hacia un `LugarReferencia`; describe en el CSV qué entiende la fuente por esa vinculación.
4. **No uses `asociadoAGrupo` para toda la ruta 2026** por el hecho de haber participado junto a la Nación Paucartambo. Una persona portadora de GPS no equivale al desplazamiento colectivo completo.
5. Para asociar **un tramo particular** con un grupo, exige una fuente específica que demuestre esa adscripción durante ese tramo. Hasta entonces deja la relación en `candidatas_NO_incorporadas.csv`.

### E. Incorporar fotografías: primero catálogo, después grafo

Las fotografías de dron `DJI_0009.JPG` a `DJI_0028.JPG` y el archivo fotográfico de 2026 **todavía no son individuos de este TTL**. No basta con ver personas, glaciar o santuario en una imagen para asignarla a un lugar o grupo.

1. Registra en el inventario fotográfico `ID_foto`, nombre de archivo, año, autoría/derechos, fecha y localización **solo cuando estén verificadas**, descripción puramente visual y restricciones de acceso.
2. Si una fotografía documenta una relación, crea primero una anotación en `plantilla_anotaciones.csv` con `ID_fuente` igual al código de foto y `Localizador_en_fuente` con el sector/fragmento relevante.
3. Si falta correspondencia verificable con GPX o lugar, mantén el vínculo como `Propuesto` y **no lo representes como triple**.
4. Por ahora, las fotografías pueden servir de evidencia **externa**, referida en el catálogo y en el CSV. Si más adelante necesitas consultar fotos como nodos del grafo, propone la clase documental `RegistroFotografico` y una relación de evidencia propia, mediante una versión explícita del esquema (v0.2), **sin mezclarla con categorías rituales**.

## 6. Lo que NO debemos agregar todavía

- `EventoRitual`, `LugarSagrado`, `Apu`, `EventoDual` ni `tieneImportancia` para esta proyección minimalista.
- Relaciones de causalidad, precedencia ceremonial, jerarquía cultural o pertenencia individual **inferidas solo del recorrido o de una fotografía**.
- `owl:sameAs` para topónimos semejantes sin control de identidad.
- `rdfs:domain`, `rdfs:range`, `owl:FunctionalProperty`, transitividad o simetría por simple conveniencia visual. Si se declaran, tienen consecuencias lógicas y requieren justificación.
- Coordenadas exactas de puntos sensibles, datos de identificación de participantes o materiales cuya circulación no esté autorizada.

## 7. Cómo revisar y guardar cambios sin perder el historial

1. Asegúrate de que las afirmaciones nuevas están en el CSV de anotaciones y de que sus fuentes pueden localizarse.
2. En Protégé: **File → Save As…**; selecciona **Turtle / RDF Turtle** si se ofrece como formato; guarda la versión de trabajo en `02_grafo_minimo/qoylluriti_ruta_2026_protege.ttl` (la copia, **no** `qoylluriti_ruta_2026_minimo.ttl`).
3. Si Protégé guardó en RDF/XML u otro formato, **no cambies solo la extensión**. Repite **Save As** y selecciona Turtle; el formato debe coincidir con el contenido.
4. Cierra y vuelve a abrir el archivo guardado en Protégé. Verifica los individuos, el tipo y el sentido de cada relación.
5. Comprueba que el archivo usa el prefijo original `urn:qoylluriti:registro2026:`. No cambies IRIs para traducir etiquetas.
6. Guarda junto al TTL: `plantilla_anotaciones.csv` actualizado, `vinculos_2026_y_evidencia.csv` actualizado y, si incorporaste tramos, `tramos_2026.csv` actualizado. Mantén archivos con acceso restringido **fuera de GitHub público**.
7. Actualiza `AUDITORIA.json` con la nueva versión y los **conteos recalculados**: individuos por clase, triples, enlaces por propiedad, número de anotaciones aprobadas, propuestas y rechazadas. **No copies el 181 inicial** a la nueva versión.
8. Haz un commit específico y revisable, por ejemplo: `docs: ampliar grafo ruta 2026 desde anotaciones verificadas`. **No uses una confirmación genérica que mezcle fotos, GPX y documentos privados.**

### Comprobación RDF sin programación avanzada

En el visor de entidades de Protégé, comprobar:

- El recorrido contiene **los 12 tramos iniciales** (más los nuevos **solo si** hay GPX añadido).
- Cada individuo nuevo tiene un tipo claro, `rdfs:label`, identificador y fuente.
- Cada enlace `proximoAReferencia` tiene una fila de cálculo en `vinculos_2026_y_evidencia.csv`; el umbral original fue **<200 m**, no universal.
- Ninguna relación `asociadoAGrupo` se añadió sin una anotación aprobada y una fuente identificable.
- Los topónimos se relacionaron por su IRI estable, no por similitud de cadenas.

Para validación externa del fichero final, puedes usar Python con `rdflib`:

```bash
python -m pip install rdflib
python -c "from rdflib import Graph; p='02_grafo_minimo/qoylluriti_ruta_2026_protege.ttl'; g=Graph().parse(p,format='turtle'); print('Triples:', len(g))"
```

Si ese comando falla, **no publiques** el TTL hasta corregir la sintaxis.

## 8. Consultas SPARQL para verificar la edición

Si tienes un panel de consulta SPARQL habilitado en Protégé, ejecútalas allí. Si no está disponible, pueden correrse con `rdflib` o un entorno SPARQL local. **DL Query no es SPARQL**.

**A. ¿Qué tramos existen?**

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tramo ?nombre WHERE {
  qr26:RecorridoRegistrado2026 qr26:contieneTramo ?tramo .
  ?tramo rdfs:label ?nombre .
}
ORDER BY ?tramo
```

**B. ¿Qué lugares menciona cada tramo?**

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
SELECT ?tramo ?lugar WHERE {
  ?tramo qr26:mencionaLugar ?lugar .
}
ORDER BY ?tramo ?lugar
```

**C. ¿Qué adscripciones colectivas se han documentado?**

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
SELECT ?tramo ?grupo WHERE {
  ?tramo qr26:asociadoAGrupo ?grupo .
}
```

**Resultado inicial esperado:** la consulta C devuelve **cero filas**. Esto es correcto: evita fingir una adscripción no documentada.

**D. ¿Qué tramos no tienen metadatos de archivo?**

```sparql
PREFIX qr26: <urn:qoylluriti:registro2026:>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?tramo WHERE {
  ?tramo a qr26:Tramo .
  FILTER NOT EXISTS { ?tramo dcterms:source ?archivo . }
}
```

Esta consulta debería devolver **cero filas** en la versión inicial; si añadiste un tramo incompleto, aparecerá aquí.

## 9. Checklist de una sesión de trabajo

- [ ] Trabajé sobre la copia `qoylluriti_ruta_2026_protege.ttl` y no sobre el TTL original.
- [ ] Registré en CSV la evidencia, el estado y el control de acceso de cada afirmación nueva.
- [ ] No confundí `mencionaLugar`, `proximoAReferencia` y `vinculadoALugar`.
- [ ] No inventé `asociadoAGrupo` por deducción a partir de la ruta individual.
- [ ] Dejé las fotografías como documentos externos hasta validar sus asociaciones.
- [ ] Guardé el archivo como Turtle verdadero y lo volví a abrir.
- [ ] Revisé los conteos y actualicé auditoría y CSV vinculados.
- [ ] Comprobé que no había material confidencial en el commit.

## 10. Incorporar esta guía a GitHub (sin reemplazar el README existente)

El repositorio ya tiene `README.md` en raíz y `02_grafo_minimo/README.md`. **No hace falta sustituir ninguno.**

1. En GitHub entra en `proyecto_qoyllurity_2026` → `02_grafo_minimo`.
2. Elige **Add file → Upload files** y sube `README_PROTEGE.md` y `qoylluriti_ruta_2026_protege.ttl` desde esta entrega (sin el ZIP).
3. Antes de confirmar, comprueba los **nombres y rutas exactos** y que no estás subiendo documentos de trabajo internos.
4. Confirma con un mensaje como `docs: guía de ampliación del grafo en Protégé`.
5. Opcionalmente, edita el `README.md` raíz y añade esta línea:

   ```markdown
   **Edición del grafo en Protégé:** [guía paso a paso](02_grafo_minimo/README_PROTEGE.md).
   ```

No necesitas crear ramas ni modificar el TTL original para añadir documentación. Para una ampliación grande de datos, sí conviene una rama de trabajo revisable antes de fusionar.

## 11. Fuentes de la guía y del proyecto

- [Protégé Desktop — guía oficial de inicio](https://protegeproject.github.io/protege/getting-started/).
- [Protégé Desktop — menús, Save / Save As](https://protegeproject.github.io/protege/menus/).
- [Protégé Desktop — vistas y paneles](https://protegeproject.github.io/protege/views/).
- [W3C — Turtle](https://www.w3.org/TR/turtle/).
- [GitHub — Eliminar datos confidenciales](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
- Inventario y reglas del propio proyecto: `02_grafo_minimo/README.md`, `GUIA_ANOTACION_Y_PROYECCION.md`, `AUDITORIA.json`, `plantilla_anotaciones.csv`, `vinculos_2026_y_evidencia.csv` y `candidatas_NO_incorporadas.csv`.
