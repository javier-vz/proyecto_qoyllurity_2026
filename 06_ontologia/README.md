# Qoyllur Rit’i: ontología v0.4.1 con medios originales

Esta es una reparación de los enlaces a imágenes y videos de la ontología v0.4. El núcleo cultural se conserva sin cambios.

## Contenido

- `qoylluriti_etnografia_v04_1_CON_MEDIOS.ttl`: grafo completo con rutas a imágenes y videos que **existen en este paquete**.
- `qoylluriti_nucleo_cultural_v04.ttl`: grafo cultural y espacial original v0.4, sin modificaciones.
- `qoylluriti_medios_v04_1.ttl`: relaciones y metadatos de los archivos multimedia.
- `medios/`: 181 archivos originales por identificador (copiados sin alterar los bytes, SHA-256 comprobado).
- `MEDIOS_VINCULADOS.csv`: correspondencia de cada medio con su archivo físico, entidades vinculadas y SHA-256.
- `GALERIA_LOCAL.html`: galería de fotografías y videos para explorar el paquete descargado.
- `consultar_imagenes.py`: ejemplo simple de consulta a los archivos desde una entidad RDF.

## Cómo funciona el vínculo

Las entidades culturales tienen `qr:tieneRegistroVisual` hacia un medio, y cada medio tiene `qr:archivoRelativo`, por ejemplo `medios/QR-MED-2026-050-01.jpg`. Esa ruta se resuelve **desde la carpeta que contiene el TTL**.

Para GraphRAG, la consulta `IntiAlabado → tieneRegistroVisual → Medio → archivoRelativo` permite recuperar directamente los bytes de la imagen. Los nombres de archivo y las ubicaciones no dependen de un servicio de mensajería.

Las fotos de 2026 del Inti Alabado se recuperaron del segundo lote (11 fotografías), sustituyendo los 10 registros que repetían incorrectamente el lote de 2025. El paquete contiene 181 registros multimedia, 180 contenidos binarios distintos. Una misma fotografía se conservó en dos referencias documentales de 2025, con IDs independientes.

## Protección y uso

**Archivo privado de trabajo:** las fotografías y videos muestran participantes y en algunas tomas personas menores. Requieren revisión de autorización para difusión antes de publicarlos en un repositorio público. Se recomienda subir solo el TTL cultural y, si procede, el índice sin datos personales; el archivo multimedia debe tener almacenamiento autorizado.

No se cambió ningún repositorio de GitHub.
