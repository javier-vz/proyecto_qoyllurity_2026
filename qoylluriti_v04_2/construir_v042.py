"""Reconstruye semánticamente la v0.4.1 (reparación de medios) y aplica auditoría 2026.

BASE: ontología completa v0.4 preservada en Library.
REPARACIÓN EXACTA de hechos añadidos en GitHub v0.4.1: QR-MED-2026-050-11 y dos enlaces.
Nota: se conserva el grafo RDF, no el orden ni la indentación de la serialización de GitHub.
"""
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD, URIRef
from pathlib import Path
import json, hashlib

ROOT=Path('/mnt/data/qoylluriti_auditoria')
G=Graph().parse('/mnt/data/base/qoylluriti_ontologia_etnografica_v04.ttl',format='turtle')
QR=Namespace('http://example.org/festividades#')
DC=Namespace('http://purl.org/dc/terms/')
G.bind('qr',QR);G.bind('dcterms',DC)
BASE_SIZE=len(G)

def es(text):return Literal(text,lang='es')
def replace_comment(id,content):
    subj=QR[id]
    for o in list(G.objects(subj,RDFS.comment)):G.remove((subj,RDFS.comment,o))
    G.add((subj,RDFS.comment,es(content)))
def replace_label(id,content):
    subj=QR[id]
    for o in list(G.objects(subj,RDFS.label)):G.remove((subj,RDFS.label,o))
    G.add((subj,RDFS.label,es(content)))
def src(id,source):G.add((QR[id],DC.source,source))

# 0. Restitución de la última versión del repositorio: v0.4.1 (v0.4 + parche de medios)
MED=QR.Medio_QR_MED_2026_050_11
for p,o in [
    (RDF.type,OWL.NamedIndividual),
    (RDF.type,QR.MedioVisual),
    (QR.archivoRelativo,Literal('medios/QR-MED-2026-050-11.jpg')),
    (QR.sha256,Literal('7e9be149a940d43579e3ded5877b9ad7b55501293fd36e8bb0e810b53999cef2')),
    (QR.anioRegistro,Literal('2026',datatype=XSD.gYear)),
    (QR.identificadorMedio,Literal('QR-MED-2026-050-11')),
    (QR.tipoMedio,es('Fotografía')),
]:G.add((MED,p,o))
for id in ['IntiAlabado','Tayancani']:
    G.add((QR[id],QR.tieneRegistroVisual,MED))
GITHUB_V041_SIZE=len(G)
assert len(list(G.subjects(RDF.type,QR.MedioVisual)))==181
assert len(list(G.triples((None,QR.tieneRegistroVisual,None))))==336

# 1. Fuentes: una investigación publicada de contexto, una tesis de campo 2017,
# y testimonio del investigador participante; las fuentes externas NO se atribuyen
# a afirmaciones nuevas de 2025-2026.
TEST=URIRef('urn:qoylluriti:fuente:auditoria_etnografica_participante_2026')
CHAUCCA=URIRef('https://hdl.handle.net/20.500.12918/3606')
TORRES=URIRef('https://doi.org/10.18800/anthropologica.202002.006')
G.add((TEST,DC.description,es('Relato y aclaraciones del investigador participante en la auditoría etnográfica de noviembre de 2026 sobre experiencias 2025-2026. Fuente conversacional no depositada públicamente; las afirmaciones no se generalizan a otras naciones.')))
G.add((TEST,DC.date,Literal('2026-11',datatype=XSD.gYearMonth)))
G.add((CHAUCCA,DC.bibliographicCitation,Literal('Chaucca Mancco, Roger (2018). Los Pablitos de Paucartambo. Tesis de Antropología, Universidad Nacional de San Antonio Abad del Cusco. Sección 5.4.2, pp. 81-83 (wataskama y Qochapata).')))
G.add((TORRES,DC.bibliographicCitation,Literal('Torres Lezama, Vicente (2020). Kallpachakuy: Coca, bebida y cigarro como fuerza y protección en la peregrinación a Qoyllurit’i. Anthropologica, 38(45), 133-159. https://doi.org/10.18800/anthropologica.202002.006')))

# 2. Precisión sobre el alcance general y la simultaneidad
replace_comment('FestividadQoylluriti',
    'La peregrinación conecta Paucartambo, Ccatcca, Ocongate, Mahuayani, el Santuario de Sinakara, Colque Punku y el recorrido de la Lomada hasta Tayankani y el regreso. Este grafo documenta principalmente el trayecto y las actividades observadas desde la participación con los ukumaris de Nación Paucartambo en 2025-2026. Otras naciones, danzas y devotos desarrollan numerosas actividades simultáneas que no pudieron ser observadas de manera exhaustiva desde esa posición. Su ausencia en el grafo no implica que no ocurrieran. La secuencia no se interpreta como calendario universal ni como una sucesión lineal de todos los acontecimientos de Qoyllur Rit’i.')
src('FestividadQoylluriti',TEST)
G.add((QR.FestividadQoylluriti,RDFS.seeAlso,TORRES)) # contextual, no prueba de secuencias particulares

replace_comment('DescensoColquePunku',
    'Los ukumaris descienden al amanecer desde Colque Punku hacia el Santuario; en la experiencia relatada la bajada ocurre aproximadamente entre las siete y ocho de la mañana. Primero se encuentran ukumaris de distintas naciones durante el descenso. Más abajo, en el sector alto del Santuario, los ukumaris de Paucartambo encuentran a los Qapaq Qollas de la misma nación. Este encuentro se inserta en un conjunto de celebraciones simultáneas, pero NO constituye el inicio inmediato de la Lomada. En 2025 se registró abundante nieve y suelo congelado; en 2026, un día soleado con menos nieve. Durante el descenso circula también la cruz transportada entre naciones.')
src('DescensoColquePunku',TEST)

replace_comment('Lomada',
    'La Lomada o recorrido de aproximadamente 24 horas comienza desde el Santuario algunas horas después del descenso de los ukumaris de Colque Punku y de su encuentro con los Qapaq Qollas de Nación Paucartambo. Ukumaris, Qapaq Qollas y Qapaq Chunchos participan como agrupaciones de una misma nación, pero parten en momentos cercanos y se desplazan por separado, no como una caravana única. La ruta pasa por Wataskama y Yanaqancha y continúa de noche hacia Tayankani, con el exigente paso por Escalerachayoq. También se reconocen los hitos Machu Cruz, Q’espi Cruz, Qquchiyoc Wayq’o y Yanaqocha; no se asigna aquí un orden completo a todos los hitos secundarios. El trabajo de campo está condicionado por las responsabilidades y los límites de observación de quien realiza el recorrido como danzante.')
src('Lomada',TEST)

# 3. Agrupaciones y distinción entre observar y ejecutar una práctica
replace_label('QollasPaucartambo','Qapaq Qollas de Nación Paucartambo')
replace_comment('QollasPaucartambo',
    'Agrupación de Qapaq Qollas de Nación Paucartambo, identificada antes en el grafo con el rótulo abreviado «Qollas». Se encuentran con los ukumaris de Paucartambo en el sector alto del Santuario durante el descenso de Colque Punku y ejecutan el canto de despedida en Q’espi Cruz. Su caporal aparece al frente del desplazamiento junto con el de los Qapaq Chunchos en algunos momentos observados. Esto no implica una jerarquía general entre danzas.')
src('QollasPaucartambo',TEST)
replace_label('ChunchusPaucartambo','Qapaq Chunchos de Nación Paucartambo')
replace_comment('ChunchusPaucartambo',
    'Agrupación de Qapaq Chunchos de Nación Paucartambo, anteriormente rotulada de forma abreviada «Chunchus». Su caporal recibe la denominación de Rey Chuncho. En algunos momentos del recorrido se le observa encabezando junto al caporal de los Qapaq Qollas. La organización observada no autoriza asignar una primacía ritual o administrativa permanente a la agrupación. Participan en la Lomada desplazándose como agrupación diferenciada.')
src('ChunchusPaucartambo',TEST)
replace_comment('UkumarisPaucartambo',
    'Agrupación de ukumaris de Nación Paucartambo. Entre sus integrantes se reconocen caporales, morocos durante sus tres primeros años y antiguos desde el cuarto. Al solicitar su incorporación, al interesado se le comunica el compromiso de participar en tres peregrinaciones anuales consecutivas; si no puede asumirlo, se recomienda postergar el ingreso. Esta expectativa tiene para el participante una dimensión devocional y de responsabilidad ante los compañeros. La continuidad posterior suele volverse más flexible. La agrupación participa en el ascenso y descenso de Colque Punku, la Lomada, el Inti Alabado y otras actividades; no todas las prácticas son realizadas por todos sus miembros. La descripción es situada y no se generaliza a las demás naciones.')
src('UkumarisPaucartambo',TEST)

replace_comment('Moroco',
    'Denominación del integrante de la agrupación de ukumaris durante sus tres primeros años de participación. Durante este periodo suele asumir encargos, colaboración y transporte de qeperinas y otros bultos. La obligación de participar tres años seguidos se comunica antes del ingreso. Estas tareas no se presentan como idénticas para todos los morocos ni en todas las actividades.')
src('Moroco',TEST)
G.add((QR.Antiguo,RDF.type,OWL.NamedIndividual))
G.add((QR.Antiguo,RDF.type,QR.Rol))
G.add((QR.Antiguo,RDFS.label,es('Antiguo')))
G.add((QR.Antiguo,RDFS.comment,es('Denominación de quien, entre los ukumaris de Paucartambo, ha completado sus tres primeros años y se encuentra desde el cuarto año de participación. Normalmente tiene mayor flexibilidad respecto de algunos encargos de los morocos; no implica ausencia de compromisos con la agrupación.')))
src('Antiguo',TEST)
G.add((QR.UkumarisPaucartambo,QR.incluyeRol,QR.Antiguo))

# 4. Q’espi Cruz: cantar no equivale a observar
replace_comment('CantoQespiCruz',
    'Durante la madrugada, después del paso por Yanaqancha, los Qapaq Qollas de Nación Paucartambo ejecutan un canto de despedida en Q’espi Cruz. Danzantes de otras agrupaciones presentes, incluidos ukumaris y Qapaq Chunchos, observan con respeto. La relación participaEn se reserva aquí a los ejecutantes del canto: no expresa la presencia como observador.')
src('CantoQespiCruz',TEST)
G.add((QR.CantoQespiCruz,QR.sigueA,QR.PermanenciaYanaqancha))
for a in ['UkumarisPaucartambo','ChunchusPaucartambo']:
    G.remove((QR[a],QR.participaEn,QR.CantoQespiCruz))

# 5. Bautizos: conservar URI histórica para Tayankani y separar Colque Punku
# No transferir medios sin inspección visual de qué bautizo representan.
G.remove((QR.BautizoMorocos,QR.ocurreEn,QR.ColquePunku))
G.remove((QR.BautizoMorocos,QR.usaObjeto,QR.Sorriago))
replace_label('BautizoMorocos','Bautizo de morocos en Tayankani')
replace_comment('BautizoMorocos',
    'Bautizo de morocos realizado en la gruta de Tayankani, después del Inti Alabado y al finalizar la Lomada. En la experiencia personal de un danzante de Paucartambo este momento es especialmente significativo para el reconocimiento como integrante de la danza, tras haber compartido las exigencias del recorrido. No se lo confunde con la iniciación que ocurre durante el primer ascenso a Colque Punku. La asignación de las cinco fotografías ya vinculadas a este individuo se mantiene por compatibilidad, pero exige inspección visual antes de emplearse para documentar gestos específicos.')
G.add((QR.BautizoMorocos,QR.sigueA,QR.IntiAlabado))
src('BautizoMorocos',TEST)
G.add((QR.BautizoPrimerAscensoColquePunku,RDF.type,OWL.NamedIndividual))
G.add((QR.BautizoPrimerAscensoColquePunku,RDF.type,QR.PracticaCultural))
G.add((QR.BautizoPrimerAscensoColquePunku,RDFS.label,es('Iniciación durante el primer ascenso a Colque Punku')))
G.add((QR.BautizoPrimerAscensoColquePunku,QR.formaParteDe,QR.FestividadQoylluriti))
G.add((QR.BautizoPrimerAscensoColquePunku,QR.ocurreEn,QR.ColquePunku))
G.add((QR.BautizoPrimerAscensoColquePunku,QR.usaObjeto,QR.Sorriago))
G.add((QR.BautizoPrimerAscensoColquePunku,RDFS.comment,es('Primer momento de bautizo o iniciación de quien llega por primera vez al sector de Colque Punku durante la peregrinación. El registro previo del TTL describe una acción con sorriago y un abrazo del caporal, cuyos detalles gestuales deben reconfirmarse mediante testimonios o evidencia visual. Se distingue del bautizo realizado en Tayankani después del Inti Alabado. El compromiso de continuidad de tres años se comunica desde antes de la primera peregrinación; el momento exacto de su formalización sigue sin confirmarse.')))
src('BautizoPrimerAscensoColquePunku',TEST)
G.add((QR.UkumarisPaucartambo,QR.participaEn,QR.BautizoPrimerAscensoColquePunku))

# 6. Danza diferenciada durante la permanencia en Yanaqancha
G.remove((QR.PermanenciaYanaqancha,QR.ocurreEn,QR.LaderaYanaqancha))
replace_comment('PermanenciaYanaqancha',
    'Parada durante la Lomada destinada a descanso, alimentación y organización de pertenencias en el sector de Yanaqancha. Los morocos asumen con frecuencia el traslado de qeperinas y otros bultos. En la ladera cercana ocurre además una danza que se documenta como práctica diferenciada, con requisitos de antigüedad para quienes la ejecutan. La simultaneidad de labores no implica que todos los integrantes participen en la danza.')
src('PermanenciaYanaqancha',TEST)
G.add((QR.DanzaLaderaYanaqancha,RDF.type,OWL.NamedIndividual))
G.add((QR.DanzaLaderaYanaqancha,RDF.type,QR.PracticaCultural))
G.add((QR.DanzaLaderaYanaqancha,RDFS.label,es('Danza colectiva en la ladera de Yanaqancha')))
G.add((QR.DanzaLaderaYanaqancha,QR.formaParteDe,QR.Lomada))
G.add((QR.DanzaLaderaYanaqancha,QR.formaParteDe,QR.FestividadQoylluriti))
G.add((QR.DanzaLaderaYanaqancha,QR.ocurreEn,QR.LaderaYanaqancha))
G.add((QR.DanzaLaderaYanaqancha,QR.ocurreEn,QR.Yanaqancha))
G.add((QR.DanzaLaderaYanaqancha,RDFS.comment,es('Durante la parada en Yanaqancha se realiza una danza colectiva en la ladera, con participación de integrantes de las danzas de Nación Paucartambo que cumplen la antigüedad requerida (según testimonio: al menos dos años en la danza). Mientras tanto otros participantes cumplen tareas de transporte de qeperinas y descanso. El nombre local preciso de la danza continúa pendiente de confirmación. La presencia de una agrupación no implica que todos sus miembros dancen.')))
src('DanzaLaderaYanaqancha',TEST)
for a in ['UkumarisPaucartambo','QollasPaucartambo','ChunchusPaucartambo']:
    G.add((QR[a],QR.participaEn,QR.DanzaLaderaYanaqancha))

# 7. Wataskama: grafía confirmada, evento y lugar, ubicación geográfica no identificada
replace_label('Wataskama','Wataskama')
replace_comment('Wataskama',
    'Wataskama es la denominación utilizada por el investigador participante para el sector del encuentro de despedida durante la Lomada; también nombra la práctica misma, representada por un individuo diferente (EncuentroWataskama). Se conserva esta grafía confirmada. La tesis de Chaucca Mancco (2018, pp. 81-83) sitúa un encuentro wataskama en la colina Qochapata junto a un riachuelo. Queda PENDIENTE confirmar si aquel topónimo corresponde exactamente al lugar registrado aquí en 2025-2026; no se establece equivalencia geográfica automática.')
src('Wataskama',TEST);src('Wataskama',CHAUCCA)
replace_comment('EncuentroWataskama',
    'Encuentro de despedida conocido como Wataskama durante la Lomada de Nación Paucartambo. Agrupaciones de danza se saludan sucesivamente en pares y realizan carreras breves de fuerte exigencia física, cruzando el riachuelo en el sector; no forman una sola caravana. Según observación participante, suelen intervenir danzantes jóvenes, sin que esto permita inferir perfiles etarios generales de cada agrupación. Chaucca Mancco (2018, pp. 81-83) registra en Qochapata un encuentro, carreras, abrazos y despedidas con la expresión «wataskama hermano» («hasta el próximo año, hermano») durante su trabajo de campo de 2017. Su descripción de sanciones y su lista de comparsas no deben extrapolarse sin corroboración a 2025-2026. La nómina completa de danzas participantes y el nombre geográfico preciso están pendientes de consulta con un informante.')
src('EncuentroWataskama',TEST);src('EncuentroWataskama',CHAUCCA)

# 8. Cambios en rol genérico caporal (no más clases)
replace_comment('Caporal',
    'Rol de conducción o coordinación en una agrupación de danza, con denominaciones específicas según la comparsa. Entre los Qapaq Chunchos de Nación Paucartambo el caporal es llamado Rey Chuncho; el caporal de los Qapaq Qollas también cumple funciones visibles durante el recorrido. El registro anterior describe intervenciones de caporales en iniciaciones y durante Wataskama; los detalles de prácticas particulares requieren corroboración antes de formalizar relaciones de autoridad o jerarquías.')
src('Caporal',TEST)

# Bibliografía contextual adicional: NO demuestra secuencias particulares del corpus.
FLORES=URIRef('https://doi.org/10.18800/anthropologica.198701.008')
SALAS=URIRef('https://doi.org/10.1017/lar.2025.10085')
G.add((FLORES,DC.bibliographicCitation,Literal('Flores Lizana, J. Carlos (1987). El santuario de Qoyllur-rit’i (una peregrinación andina). Expresión y germen de organización campesina. Anthropologica. https://doi.org/10.18800/anthropologica.198701.008')))
G.add((SALAS,DC.bibliographicCitation,Literal('Salas Carreño, Guillermo (2025, publicación en línea; volumen 2026). How and Why the Quyllurit’i Pilgrimage Is Related to the Tupac Amaru Rebellion. Latin American Research Review, 61(2), 253-271. https://doi.org/10.1017/lar.2025.10085')))
G.add((QR.FestividadQoylluriti,RDFS.seeAlso,FLORES))
G.add((QR.FestividadQoylluriti,RDFS.seeAlso,SALAS))

# Control de auditoría en información del grafo sin cambiar la ontología cultural
G.add((QR.FestividadQoylluriti,DC.description,es('v0.4.2: auditoría etnográfica de noviembre 2026; revisión no exhaustiva, con observaciones situadas y fuentes de distinto alcance.')))

# Comprobaciones para no borrar contenido audiovisual
assert len(list(G.subjects(RDF.type,QR.MedioVisual)))==181
assert len(list(G.triples((None,QR.tieneRegistroVisual,None))))==336
assert len(list(G.subjects(RDF.type,OWL.Class)))==11
assert len(list(G.subjects(RDF.type,OWL.ObjectProperty)))==18
assert len(list(G.subjects(RDF.type,OWL.DatatypeProperty)))==7
assert (QR.QollasPaucartambo,QR.participaEn,QR.CantoQespiCruz) in G
assert (QR.ChunchusPaucartambo,QR.participaEn,QR.CantoQespiCruz) not in G
assert (QR.UkumarisPaucartambo,QR.participaEn,QR.CantoQespiCruz) not in G
assert (QR.BautizoMorocos,QR.ocurreEn,QR.ColquePunku) not in G
assert (QR.BautizoMorocos,QR.ocurreEn,QR.GrutaTayankani) in G
assert (QR.BautizoPrimerAscensoColquePunku,QR.ocurreEn,QR.ColquePunku) in G
assert (QR.EncuentroWataskama,DC.source,CHAUCCA) in G

out=ROOT/'qoylluriti_etnografia_v04_2_AUDITORIA_CON_MEDIOS.ttl'
G.serialize(destination=out,format='turtle',encoding='utf-8')
G2=Graph().parse(out,format='turtle')
assert len(G2)==len(G)
sha=hashlib.sha256(out.read_bytes()).hexdigest()

report={
 'archivo':out.name,
 'git_sha_blob_v041':'e6dbee2775a84ccda836a71b2c60876420ced8d5',
 'proveniencia':'El grafo v0.4.1 se recompone semánticamente desde la copia integral v0.4 y el parche multimedia constatado en el archivo v0.4.1 de GitHub; serialización y orden de triples pueden variar.',
 'triples_v04':BASE_SIZE,
 'triples_v041_reconstruida':GITHUB_V041_SIZE,
 'triples_v042':len(G),
 'clases_owl':11,
 'propiedades_objeto_owl':18,
 'propiedades_datos_owl':7,
 'medios':181,
 'enlaces_medios':336,
 'triple_sujetos_nuevos':['BautizoPrimerAscensoColquePunku','DanzaLaderaYanaqancha','Antiguo'],
 'sha256_v042':sha,
 'pendientes':['Corroborar la localización geográfica y posible correspondencia Wataskama–Qochapata','Confirmar lista de comparsas de Nación Paucartambo en 2025-2026','Verificar imágenes QR-FOT-2025-051-01 a 05 antes de atribuirlas a un bautizo específico','Confirmar detalles gestuales y temporalidad del primer bautizo/compromiso trienal','Confirmar nombre local de la danza colectiva en la ladera de Yanaqancha','Verificar si cada comparsa identificada participa en la danza de Yanaqancha y su criterio exacto de antigüedad','Revisar orden de hitos secundarios de Lomada contra GPS y entrevistas','Verificar detalles del saludo y eventuales sanciones en Wataskama 2025-2026']
}
(ROOT/'validacion_v042.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
