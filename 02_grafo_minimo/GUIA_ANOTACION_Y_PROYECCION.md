# Protocolo de anotación de evidencia → grafo mínimo

## Propósito

La ontología de 2026 se deja deliberadamente pequeña. Los significados, pertenencias y relaciones densas **no se codifican de antemano** como tipos rituales: deben surgir de anotaciones atribuibles a fuentes concretas y, cuando corresponde, revisadas con participantes pertinentes.

## Unidad mínima

Cada anotación debe identificar **qué fuente**, **qué intervalo** (página, segundo de audio, tiempo GPS, número de foto o fragmento documental), **qué entidad**, **qué lugar** o **qué colectivo**, **qué relación se propone**, **quién la anotó**, **qué regla de evidencia aplica** y **cuál es su estado de revisión**. No basta con una frase narrativa sin referencia.

Para datos espaciales, separar la afirmación `el archivo contiene el nombre de lugar`, la medición `esta traza pasa a menos de 200 m de un waypoint`, y la afirmación cultural `el colectivo estuvo allí`. No son equivalentes.

## Estados

- **Registrado:** propiedad documental observada directamente en el archivo (p.ej., topónimo en nombre de GPX).
- **Calculado:** medida reproducible con parámetros y fuente (p.ej., proximidad a waypoint).
- **Atribuido:** afirmación de autor, participante o institución, con lugar y fecha de enunciación.
- **Propuesto:** hipótesis pendiente de revisión, sin triple afirmativo.
- **Rechazado:** hipótesis descartada, conservar razón y versión.

## Control de sensibilidad

Usar `publico`, `solo_equipo`, `restringido_comunidad` y `revisar`. No publicar puntos privados, ubicaciones culturalmente sensibles o testimonios identificables sin permiso. Las fotografías no revelan por sí mismas afiliaciones individuales. Si hay conflicto entre fuentes, guardar **dos anotaciones atribuidas**, no elegir una falsa «verdad global».

## Proyección RDF

Solo se exportan como relación RDF las anotaciones con estado *registrado*, *calculado* o *atribuido* que cumplen las reglas de su predicado; las hipótesis propuestas quedan fuera del TTL, conservadas en CSV. No se agregan clases `EventoRitual`, `LugarSagrado`, ni «importancia central». El grafo representa lo que los documentos permiten afirmar, no el universo de la práctica ritual.

## Flujo sugerido

1. Extraer de forma autorizada fuentes y sus páginas/fragmentos.
2. Identificar nombres alternativos con fecha y fuente; no fusionar identidades por parecido ortográfico.
3. Crear anotaciones con fuente, evidencia y estado.
4. Validar los vínculos geográficos y colectivos pertinentes.
5. Exportar una proyección RDF versionada y auditar vínculos añadidos/rechazados.
6. Probar consultas espaciales y de adscripción con citas; permitir «no disponible» cuando no exista evidencia.

Los campos se encuentran en `plantilla_anotaciones.csv`, preparada para abrirse en Excel.
