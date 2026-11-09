#!/usr/bin/env python3
"""Consolida el TTL mínimo, la v0.1, evidencia audiovisual, anotaciones y legados.
NO hace equivalencias OWL con el grafo 2025, ni publica originales audiovisuales.
Reproduce el mismo archivo desde los insumos locales descritos en README.
"""
from pathlib import Path
import csv, io, re, collections, zipfile, hashlib
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DCTERMS, SKOS

ROOT=Path('/mnt/data')
INV=ROOT/'inventario_fotografico_qoylluriti'
OUT=ROOT/'Qoyllur_Riti_2025_2026_TTL_INTEGRAL_v02'
OUT.mkdir(exist_ok=True)
BASE=ROOT/'qoylluriti_ontologia_etnografica_2025_2026_propuesta_v01.ttl'
CSV=INV/'INVENTARIO_FOTOGRAFICO_QOYLLURITI_2025_2026_CONCILIADO_180.csv'
LEGACY=ROOT/'Anotaciones_Candidatas_Qoylluriti_2025_para_2026_Protege.zip'
G=Graph().parse(BASE,format='turtle')
Q=Namespace('urn:qoylluriti:registro2026:')
G.bind('qr',Q); G.bind('dcterms',DCTERMS);G.bind('skos',SKOS)

# Properties and classes without hard domains/ranges: do not imply identities or certainty.
classes={
 'RegistroAudiovisual':'Registro audiovisual individual',
 'AnotacionEtnografica':'Anotación etnográfica contextual',
 'ReferenciaLegado':'Referencia de entidad en TTL histórico',
 'CandidatoConciliacion':'Relación del legado por conciliar',
 'PreguntaPendiente':'Pregunta de verificación etnográfica',
 'EtapaNarrativa':'Etapa del itinerario relatado',
 'DocumentoFuente':'Documento o matriz documental',
}
for k,lab in classes.items():
 G.add((Q[k],RDF.type,OWL.Class));G.add((Q[k],RDFS.label,Literal(lab,lang='es')))
for a,b in [('RegistroAudiovisual','Evidencia'),('AnotacionEtnografica','Evidencia'),('ReferenciaLegado','Evidencia'),('CandidatoConciliacion','Evidencia'),('DocumentoFuente','Evidencia')]: G.add((Q[a],RDFS.subClassOf,Q[b]))
obj_props={
 'incluyeMedio':'Un lote audiovisual incluye este registro',
 'formaParteDeLote':'Registro indexado dentro de un lote audiovisual',
 'contextualizaActividad':'El lote proporciona contexto audiovisual para una actividad; no garantiza visibilidad de todos sus detalles',
 'contextualizaFestividad':'El lote permite contextualizar la festividad, sin atribuir un evento preciso',
 'tieneAnotacion':'Una entidad está descrita mediante anotación de procedencia',
 'describeActividad':'Anotación referida a una actividad documentada',
 'seRefiereALugar':'Hito de referencia mencionado por una anotación; no implica coordenadas verificadas',
 'tienePreguntaPendiente':'Asocia el registro con verificación todavía abierta',
 'refiereAEntidad':'Referencia de legado propuesta sin implicar identidad OWL',
 'enEtapaNarrativa':'Actividad asociada a una etapa del relato',
 'parteDeItinerario':'Una etapa forma parte del itinerario situado',
 'etapaSiguiente':'Siguiente etapa en el orden narrado, no inferencia de hora exacta',
 'conectaLugarNarrativo':'Etapa que recorre o conecta un lugar de manera general',
 'esSustentadoPor':'Conecta una descripción con el testimonio o medio que la respalda',
 'participacionRelatadaDe':'Colectivo al que el narrador se refiere; no una identificación visual de personas',
 'vinculadoAObjeto':'Relación contextual con objeto documentado',
 'anotacionFuente':'Fuente en donde se registró la anotación',
 'vinculadoALugarContextual':'Asignación contextual de lugar basada en fuente, no georreferenciación puntual',
 'documentaRol':'Referencia al rol de participación descrito por el narrador',
}
for k,lab in obj_props.items():G.add((Q[k],RDF.type,OWL.ObjectProperty));G.add((Q[k],RDFS.label,Literal(lab,lang='es')))
data_props={
 'descripcionNarrativa':'Descripción de testimonio o actividad', 'estadoValidacion':'Estado de revisión o evidencia',
 'incertidumbre':'Restricción de interpretación o confirmación', 'anioRegistro':'Año expresamente confirmado para un evento o medio',
 'anioOriginalEnInventario':'Campo de año sin normalización; puede ser tentativa', 'identificadorAnotacion':'Identificador de anotación',
 'nombreArchivoOriginal':'Nombre original de archivo', 'nombreConjunto':'Nombre de conjunto en inventario',
 'nombreZIPFuente':'Archivo ZIP original', 'rutaMedioArchivo':'Ruta del medio indicada en inventario',
 'hashSHA256':'Digest SHA-256 registrado en inventario', 'descripcionVisual':'Descripción de lo visible',
 'permisoDifusion':'Estado de permiso de difusión', 'nivelAcceso':'Recomendación de acceso',
 'permisoIA':'Condiciones de reutilización en IA; no equivalen a autorización',
 'tipoMedio':'Fotografía o video según inventario', 'duracionEstimativaTexto':'Duración de video aproximada o no numérica preservada sin tipado decimal', 'fuenteIdentificacion':'Base testimonial o de identificación',
 'contextoRelatado':'Contexto narrado, separado de la observación visual', 'lugarContextualTexto':'Lugar contextual declarado',
 'nombreToponimoAlternativo':'Variante de topónimo testimoniada o registrada', 'condicionDocumental':'Condición documental del recurso',
 'predicadoLegado':'Predicado nominal de una relación histórica que NO se afirma en 2026',
 'sujetoLegado':'Sujeto nominal de relación histórica NO afirmada',
 'objetoLegado':'Objeto nominal de relación histórica NO afirmada',
 'restriccionesLegado':'Advertencias del grafo original', 'estadoMigracion':'Estado de migración y revisión',
 'fuenteLote':'CSV o conjunto ZIP asociado', 'relacionConMaterial':'Referencia textual a otra anotación o archivo',
 'textoPregunta':'Pregunta por investigar', 'prioridadRevision':'Prioridad de revisión',
}
for k,lab in data_props.items(): G.add((Q[k],RDF.type,OWL.DatatypeProperty));G.add((Q[k],RDFS.label,Literal(lab,lang='es')))

def lit(s,p,v,lang='es'):
 if v is None: return
 v=str(v).strip()
 if not v:return
 G.add((s,p,Literal(v,lang=lang) if lang else Literal(v)))
def obj(s,p,o):G.add((s,p,o))
def year(s,y):
 if str(y) in ('2025','2026'):
  G.add((s,Q.anioRegistro,Literal(str(y),datatype=XSD.gYear)))
  G.add((s,DCTERMS.date,Literal(str(y),datatype=XSD.gYear)))
def set_entity(name,cls,label,description=None,yr=None,place=None,practice=None,group=None,source=None,state='contextual_revisar',restriction=None):
 s=Q[name];obj(s,RDF.type,Q[cls]);lit(s,RDFS.label,label)
 lit(s,Q.descripcionNarrativa,description);year(s,yr)
 if place:obj(s,Q.ocurreEn,Q[place])
 if practice: obj(s,Q.instanciaDePractica,Q[practice])
 if group:
  for q in (group if isinstance(group,(list,tuple)) else [group]): obj(s,Q.participaColectivo,Q[q])
 if source:lit(s,DCTERMS.source,source)
 lit(s,Q.estadoValidacion,state,lang=None);lit(s,Q.incertidumbre,restriction)
 return s

# Source and provenance. Additional evidence never automatically verifies unsupported claims.
source_nodes={
 'FuenteTestimonios_2026_11_08':('Relatos de investigador-participante revisados en conversación, noviembre 2026','Testimonios contextualizados de Ukumaris de Nación Paucartambo; distintas memorias de 2025/2026. El archivo de conversación no se distribuye en este paquete.'),
 'FuenteInventario180':('Inventario audiovisual conciliado, 180 medios','180 filas con ID individual, año declarado, descripción visual, límites interpretativos, origen, archivos y permisos.'),
 'FuenteTTLLegado2025':('Ontología histórica 2025, referencia para conciliación','RDF original con 87 individuos y relaciones revisables; no se importan indiscriminadamente sus axiomas ni autorreferencias.'),
 'FuenteGPS2026':('Doce trazas GPX de 2026','Los tramos conservados del núcleo RDF original son trazas; proximidad a waypoints es aproximada, no presencia ritual demostrada.'),
 'FuenteAnotacionesCampo':('Anotaciones QR-AN 030–053 y referencias contextuales','Matriz de trabajo documental con observaciones visuales, testimonios y pendientes.'),
}
for k,(title,descr) in source_nodes.items():
 s=Q[k];obj(s,RDF.type,Q.DocumentoFuente);lit(s,RDFS.label,title);lit(s,Q.descripcionNarrativa,descr)

# Record ontology-level scope.
ont=Q.OntologiaEtnograficaIntegral_v02
obj(ont,RDF.type,OWL.Ontology);lit(ont,RDFS.label,'Qoyllur Rit’i: ontología etnográfica integral 2025–2026, v0.2')
lit(ont,DCTERMS.description,'Conserva núcleo GPS 2026 y nueva v0.1; agrega etapas, observaciones y evidencias individuales, testimonios, candidatos históricos no asertados y verificación incremental. No es descripción normativa u oficial de todas las naciones.')
obj(ont,DCTERMS.source,Q.FuenteTestimonios_2026_11_08);obj(ont,DCTERMS.source,Q.FuenteInventario180);obj(ont,DCTERMS.source,Q.FuenteTTLLegado2025)
G.add((ont,OWL.versionInfo,Literal('v0.2 — 2026-11-08')))

# Toponyms, aliases and place-granularity safeguards.
places={
 'CarpapampaPaucartambo':('Carpapampa, Paucartambo','Barrio donde el participante sitúa el ensayo general; sin coordenadas'),
 'LosaHuascar':('Losa deportiva Huáscar, Carpapampa','Lugar del ensayo general según testimonio; sin coordenada verificada'),
 'IglesiaPaucartambo':('Iglesia de Paucartambo','Misa y paradas en la salida; no asumir mismo espacio para todas las danzas'),
 'CasaCaporalArea':('Sector de reunión en casa del caporal','Referencia contextual; no se publica dirección privada'),
 'CasaPriosteParada':('Casa del prioste, parada del viaje','Lugar de visita/descanso referido; no se publica ubicación residencial'),
 'CeldaUkumarisSantuario':('Celda de ukumaris en el Santuario','Sector alto del Santuario cercano al camino de Colque Punku; referencia etnográfica, sin coordenada'),
 'BofedalSantuario':('Bofedal del sector de acampada','Referencia contextual en el Santuario; variación de humedad por temporada no determinada'),
 'GrutaTayankani':('Gruta asociada al bautizo de moroco en Tayankani','No equiparar sin corroboración con GrutaTayankani del TTL histórico ni precisar una coordenada'),
 'LaderaYanaqancha':('Ladera del cerro en Yanaqancha','Actividad documentada con fotografía de participantes en ladera; nombre de danza pendiente'),
 'ValleWataskama':('Sector de riachuelo en Wataskama','Sector de juegos y cruces descrito por participante; localización fina por verificar'),
 'CanchaOcongate':('Cancha y graderías de Ocongate','El individuo ya existía en la v0.1; nombre oficial del recinto no determinado'),
 'RutaLomada':('Ruta de 24 horas o Lomada','Referencia narrativa del recorrido, NO un polígono ni una línea oficial'),
 'Sinakara':('Sinakara','Paisaje montañoso que alberga el Santuario; carácter de apu atribuido al relato del participante'),
 'ZonaUltimaVistaGlaciar':('Sector de posible última vista del glaciar','Hipótesis en torno a Q’espi Cruz; no confirmar sin contraste espacial/visual'),
}
for k,(lab,desc) in places.items():
 s=Q[k];obj(s,RDF.type,Q.LugarReferencia);lit(s,RDFS.label,lab);lit(s,RDFS.comment,desc)
for k,aliases in [('Wataskama',['Guatascama','Watascama','Wataskama']),('Yanaqancha',['Yanacancha','Llanacanca','Yanaqancha']),('QespiCruz',["Q'espi Cruz",'Quespi Cruz']),('Ccatcca',['Ccatca','Catca','Ccatcca']),('Escalerachayoq',['Escalerayoq'])]:
 for x in aliases:lit(Q[k],SKOS.altLabel,x)

# Participant roles and traditional objects / no individual identity classification.
for k,lab,descr in [
 ('Ukumari','Ukumari / Ukuku','Participante identificado por nomenclatura regional; no inferir por vestimenta de fotografías'),
 ('Moroco','Moroco','Denominación de participante en primeros años, alrededor de dos o tres, según el relato situado'),
 ('Mamawairi','Mamawairi','Personas y familias que colaboran con transporte, alimentos y apoyo; no reducir a único género ni formalizar requisitos'),
 ('Caporal','Caporal','Rol de coordinación ritual/participación; sin identificar personas concretas'),
 ('PortadorCruz','Portador de la cruz','Rol situacional durante el transporte, no designación permanente'),
]:
 s=Q[k];obj(s,RDF.type,Q.RolParticipante);lit(s,RDFS.label,lab);lit(s,RDFS.comment,descr)
for k,lab,desc in [
 ('CruzColquePunku','Cruz trasladada a Colque Punku','Cruz subida a gruta el día anterior y bajada; el testimonio atribuye su carga por turnos a diferentes naciones'),
 ('Queperina','Queperina','Tela o bulto transportado por peregrinos, especialmente morocos en etapa de Yanaqancha; variante oral no implica objetos idénticos'),
 ('Sorriago','Sorriago','Instrumento referido en la descripción de iniciación; rito y atribución pendientes de más detalle'),
 ('BanderasNaciones','Banderas de las naciones','Numerosas banderas visibles durante descenso, concentraciones y marchas; no inferir nación concreta por imagen'),
 ('CargaLeniaMorocos','Leña transportada por morocos','Material de apoyo colectivo descrito en camino Mahuayani–Santuario; no afirmar carga universal'),
]:
 s=Q[k];obj(s,RDF.type,Q.ObjetoDocumentado);lit(s,RDFS.label,lab);lit(s,RDFS.comment,desc)

# Distinguish participation collective and concept. In v01 Nacion and groups already exist.
for nm,lab,desc in [('UkumarisDistintasNaciones','Ukumaris de distintas naciones','Colectivo descriptivo múltiple; no representa una nación única'),('PoblacionOcongate','Población receptora de Ocongate','Personas que reciben a peregrinos, sin convertir testimonios en identidad de participantes de fotos'),('EscolaresLocalesPaucartambo','Escolares de localidades cercanas','Participación referida por testimonio durante Corpus Christi; no atribuir identidad individual')]:
 set_entity(nm,'Grupo',lab,desc,state='testimonio_contextual')

# Practices and recurring patterns. Instance nodes retain year independence.
practice_defs={
 'PracticaEnsayoGeneral':('Ensayo general previo a la peregrinación','Ensayo y preparación en Paucartambo antes de la salida'),
 'PracticaMisaSalida':('Misa previa a la salida','Celebración religiosa previo a romería y partida'),
 'PracticaVestirseUkumari':('Preparación de vestimenta de ukumari','Reunión y vestimenta cerca de zona del caporal, sin dirección'),
 'PracticaRecorridoPueblo':('Recorrido festivo por el pueblo','Desplazamientos y carreras por calles de Paucartambo antes del viaje'),
 'PracticaRomeria':('Romería al cementerio','Visita y recuerdo a antiguos integrantes y familiares; se conserva práctica'),
 'PracticaReciprocidadCcatcca':('Encuentro y entrega de alimentos en Ccatcca','Carne y maíz compartidos según testimonio; fecha del lote de imágenes pendiente'),
 'PracticaParadaPrioste':('Parada en casa del prioste','Encuentro y descanso con ukumaris, Qollas y Chunchus durante el viaje'),
 'PracticaLlegadaMahuayani':('Llegada a Mahuayani','Llegada de vehículos, bultos y organización para caminar'),
 'PracticaCampamentoSantuario':('Acampada en la celda del Santuario','Preparación de descanso, pertenencias y equipo antes del ascenso'),
 'PracticaMisaSantuario':('Misa en el Santuario','Momentos previos al ingreso o al interior de la iglesia documentados en 2025'),
 'PracticaLlegadaGrutaColque':('Llegada a sector de gruta de Colque Punku','Concentración de naciones cerca de gruta y cruz; no equiparar grutas'),
 'PracticaIniciacionColque':('Iniciación de morocos en Colque Punku','Relato de iniciación con sorriago y abrazo; alcance colectivo por precisar'),
 'PracticaReunionBanderas':('Concentración de banderas y ukumaris','Encuentro al final del descenso cerca del Santuario'),
 'PracticaJuegosWataskama':('Juegos de encuentro en Wataskama','Cruces del riachuelo, carreras y bromas descritas, sin inferir rivalidad generalizada'),
 'PracticaDescansoQespiCruz':('Descanso en Q’espi Cruz','Descanso asociado al lugar por testimonio; última visibilidad de glaciar sin confirmar'),
 'PracticaBaileZigzag':('Formación y desplazamiento en zigzag del Inti Alabado','Se vincula al Inti Alabado, no presupone un significado específico'),
 'PracticaCaminoTayankaniOcongate':('Camino de Tayankani a Ocongate','Caminata posterior al Inti Alabado'),
 'PracticaRecepcionChicha':('Recepción y ofrecimiento de chicha','Hospitalidad de la población según testimonio; fotos no demuestran entrega'),
 'PracticaEsperaCancha':('Permanencia en cancha de Ocongate','Permanencia hasta la noche antes del regreso en camión'),
 'PracticaCorpusDanzas':('Danzas en Corpus Christi de Paucartambo','Danzas de regreso y escolares según relato; participación por agrupación por verificar'),
}
for nm,(lab,descr) in practice_defs.items():
 s=Q[nm];obj(s,RDF.type,Q.PracticaCultural);lit(s,RDFS.label,lab);lit(s,RDFS.comment,descr)

# Enrich existing occurrences only with explicitly grounded details.
existing_enrich={
 'RomeriaPaucartambo2025':('La romería en cementerio recuerda a participantes antiguos y familiares, según testimonio; las fotografías de 2025 muestran el contexto.', 'testimonio_participante_y_fotos'),
 'AscensoColquePunku2026':('Ascenso nocturno desde Santuario a Colque Punku, en marco de una peregrinación físicamente exigente.', 'testimonio_y_GPX'),
 'DescensoColquePunku2025':('Descenso en filas, terreno congelado y nieve recordada como abundante; el participante expresa vivencia de bendición, no propiedad objetiva ni medida de nieve.', 'testimonio_y_fotos'),
 'DescensoColquePunku2026':('Regreso al Santuario en día recordado como soleado y con menos nieve visible que 2025; comparación testimonial, no tendencia climática.', 'testimonio_y_fotos'),
 'TrasladoCruz2025':('La cruz subida a la gruta el día anterior es transportada al descender por turnos entre distintas naciones. El video muestra ukumaris de Nación Paucartambo llevando la cruz, NO el instante exacto del relevo. La interacción puede ser lúdica y físicamente áspera.', 'testimonio_participante_video'),
 'EncuentroWataskamaDocumentado':('En un valle con riachuelo, danzas de Nación Paucartambo se encuentran, corren por turnos y se hacen bromas. Falta fotografía propia; el testimonio mantiene su valor documental.', 'testimonio_sin_fotografia'),
 'DanzaCerroYanaqancha2025':('Fila extensa en ladera documentada por imágenes; según testimonio otros ukumaris realizan danza mientras morocos llevan queperinas; nombre e interpretación pendientes.', 'fotos_video_y_testimonio'),
 'QueperinasYanaqancha2025':('Traslado de queperinas por morocos de primeros años, especialmente primeros dos, según experiencia situada; no inferir roles viendo vestimenta.', 'testimonio_participante'),
 'Lomada2025':('Ruta aproximada de 24 horas desde Santuario; fotografía difícil por exigencia física; cambio hacia Yanaqancha y descansos. Ausencia de foto no implica ausencia de práctica.', 'testimonio_y_fotos'),
 'Lomada2026':('Ruta de 24 horas desde Santuario, con secuencia de tramos GPX de 2026; no es toda la fiesta ni todos los itinerarios.', 'testimonio_GPX'),
 'IntiAlabado2025':('Al amanecer en Tayankani se reúnen queperinas, ukumaris forman filas y realizan desplazamientos en zigzag; sentido específico no interpretado.', 'testimonio_y_audiovisual'),
 'IntiAlabado2026':('Formación en filas de ukumaris de diferentes naciones y zigzag al amanecer en Tayankani; medios comparables con 2025 sin suponer identidad de detalles.', 'testimonio_y_audiovisual'),
 'BautizoMorocoTayankani2025':('Bautizo personal al final de Inti Alabado en Tayankani, 2025. Material personal restringido; detalles de la práctica sin describir más allá del relato.', 'testimonio_personal_restringido'),
 'RecepcionOcongateDocumentada':('Al final de caminata desde Tayankani, habitantes ofrecen recibimiento alegre e incluso chicha. La entrega de chicha no se ve inequívocamente en fotos; año de las cinco fotos no confirmado.', 'testimonio_y_fotos_anio_pendiente'),
 'EncuentroCanchaOcongateDocumentado':('El pueblo llena las graderías; hay grupos en la cancha y una permanencia hasta la noche antes del regreso en camión, según testimonio. Nombre del acto no establecido.', 'testimonio_y_fotos_anio_pendiente'),
 'RegresoCamionPrevioCorpus2026':('Después de la espera en Ocongate se viaja en camión de noche, se llega de madrugada a Paucartambo y los participantes descansan.', 'testimonio_personal_sin_foto'),
 'CorpusChristiPaucartamboActividad2026':('Procesión y danzas por las calles de Paucartambo durante la mañana. Según relato, participan escolares de localidades cercanas vestidos como distintas danzas, incluso niños ukumaris. Cierre del itinerario vivido de Nación Paucartambo, sin fusionar festividades.', 'testimonio_y_fotos'),
}
for name,(descr,estado) in existing_enrich.items():
 lit(Q[name],Q.descripcionNarrativa,descr);lit(Q[name],Q.estadoValidacion,estado,lang=None)

# Add events missing from v0.1. Do not assign year when previous photo set was unconfirmed.
events=[
 ('EnsayoGeneralPaucartambo','Ensayo general en Paucartambo',None,'LosaHuascar','PracticaEnsayoGeneral','El sábado antes de la peregrinación, ensayo general en la losa deportiva Huáscar del barrio Carpapampa. No se presupone participación de todas las danzas del pueblo.',None,'testimonio_participante'),
 ('MisaPreviaSalidaPaucartambo','Misa previa a la partida',None,'IglesiaPaucartambo','PracticaMisaSalida','El domingo antes de salir se celebra misa; no se asigna año a este testimonio general.',None,'testimonio_participante'),
 ('PreparacionPaucartambo2026','Vestimenta para peregrinación en Paucartambo, 2026','2026','Paucartambo','PracticaVestirseUkumari','Fotografía personal con indumentaria de ukumari; fecha de captura individual no verificada, archivo sugiere 2026.', 'UkumarisPaucartambo','fotografia_contextual'),
 ('PreparacionSalidaPaucartambo2025','Preparación de participantes antes de salida, 2025','2025','CasaCaporalArea','PracticaVestirseUkumari','En los alrededores del punto de reunión se visten los ukumaris; no se divulga dirección particular. Contexto de salida en fotos.', 'UkumarisPaucartambo','testimonio_y_fotos'),
 ('RecorridoPuebloPaucartambo2025','Recorrido festivo por Paucartambo, 2025','2025','Paucartambo','PracticaRecorridoPueblo','Desplazamientos por calles del pueblo, carreras y parada junto a iglesia antes del transporte en camiones.', 'UkumarisPaucartambo','testimonio_y_fotos'),
 ('SalidaCamionesPaucartambo2025','Salida en camiones desde Paucartambo, 2025','2025','Paucartambo','PracticaCaminoPeregrinacion','Traslado colectivo en camión hacia Mahuayani, con apoyo de mamawairis y equipajes. No atribuirlo a todas las naciones.', 'UkumarisPaucartambo','testimonio_contextual'),
 ('ViajeVehiculo2026','Desplazamiento vehicular a Mahuayani, 2026','2026',None,'PracticaCaminoPeregrinacion','Tramos GPS 01–03 y 12 documentan recorrido en vehículo; no inferir detalles de paradas por proximidad GPS.', None,'gpx'),
 ('ParadaCcatccaDocumentada','Parada y encuentro alimentario en Ccatcca',None,'Ccatcca','PracticaReciprocidadCcatcca','El participante describe entrega de alimentos a población local (carne y maíz). Las tres fotos del conjunto no tienen año confirmado.',None,'testimonio_fotos_anio_pendiente'),
 ('ParadaCasaPrioste2025','Reunión y descanso en casa del prioste, 2025','2025','CasaPriosteParada','PracticaParadaPrioste','Reunión de ukumaris, Qollas y Chunchus, comida y descanso durante el viaje. No se publica dirección particular.', ['UkumarisPaucartambo','QollasPaucartambo','ChunchusPaucartambo'],'testimonio_y_fotos'),
 ('LlegadaMahuayani2026','Llegada a Mahuayani, 2026','2026','Mahuayani','PracticaLlegadaMahuayani','Concentración de camiones y equipos; peregrinos preparan queperinas y materiales antes de caminar. Se observan fotografías contextuales.', None,'testimonio_y_fotos'),
 ('CaminoMahuayaniSantuario2025','Ruta a pie de Mahuayani al Santuario, 2025','2025',None,'PracticaCaminoPeregrinacion','Se observa el sendero con peregrinos, zonas de comida y panorámica de Mahuayani al poco de comenzar la caminata; el participante relata carga de pertenencias.',None,'testimonio_y_fotos'),
 ('AcampadaSantuarioRelatada','Acampada de ukumaris en el Santuario',None,'CeldaUkumarisSantuario','PracticaCampamentoSantuario','Los ukumaris acampan en sector alto del Santuario, dejan equipo y descansan; no hay foto de su celda en el conjunto.', 'UkumarisPaucartambo','testimonio_sin_fotografia_celda'),
 ('MisaSantuario2025','Misa y visita a iglesia del Santuario, 2025','2025','Santuario','PracticaMisaSantuario','Secuencia de imágenes del exterior antes de entrar y del interior de iglesia. No atribuir a cada fotografía una misa específica.',None,'visual_y_testimonio'),
 ('AscensoColquePunku2025','Ascenso nocturno a Colque Punku, 2025','2025','ColquePunku','PracticaAscensoGlaciar','Salida nocturna desde Santuario; fotografías iniciales de la subida y vistas de luces del Santuario al anochecer. La hora de cada foto no está verificada.',None,'testimonio_y_fotos'),
 ('LlegadaGrutaColquePunku2025','Concentración cerca de gruta de Colque Punku, 2025','2025','GrutaColquePunku','PracticaLlegadaGrutaColque','Grupos y banderas cerca de cruz y gruta, en el contexto de la madrugada del ascenso. No identificar personas por ropa.',None,'testimonio_y_fotos'),
 ('SectorColquePunku2026','Permanencia junto al sector glaciar, 2026','2026','ColquePunku','PracticaLlegadaGrutaColque','Tomas y relato de grupo de ukumaris en paisaje glaciar; comparaciones de nieve con 2025 son cualitativas.',None,'testimonio_y_fotos'),
 ('IniciacionMorocosColqueDocumentada','Iniciación de morocos en Colque Punku',None,'GrutaColquePunku','PracticaIniciacionColque','Según testimonio, novatos se arrodillan, reciben tres golpes rituales con sorriago de caporal y un abrazo; confirmar variabilidad y años, no derivar de fotos.', 'UkumarisPaucartambo','testimonio_requiere_contexto'),
 ('EncuentroBanderasSantuario2026','Concentración de ukumaris y banderas al llegar al Santuario, 2026','2026','Santuario','PracticaReunionBanderas','En el sector de entrada se encuentran ukumaris de distintas naciones y muchas banderas; no identificar otras naciones visualmente.', 'UkumarisDistintasNaciones','fotos_y_testimonio'),
 ('EncuentroBanderasColque2025','Concentración de ukumaris y banderas tras Colque Punku, 2025','2025','Santuario','PracticaReunionBanderas','En la llegada, banderas de distintas naciones, y transporte conjunto de cruz; práctica específica vinculada a traslado de cruz.', 'UkumarisDistintasNaciones','fotos_y_testimonio'),
 ('EncuentroJuegosWataskama','Encuentros y juegos en Wataskama',None,'Wataskama','PracticaJuegosWataskama','Las agrupaciones se encuentran en lados opuestos del riachuelo, cruzan corriendo y realizan bromas; registro testimonial sin fotos.', ['UkumarisPaucartambo','QollasPaucartambo','ChunchusPaucartambo'],'testimonio_directo_sin_foto'),
 ('DescansoQespiCruz2025','Descanso asociado a Q’espi Cruz durante la Lomada, 2025','2025','QespiCruz','PracticaDescansoQespiCruz','Punto mencionado por participante, muy alto, con paradas de descanso. No asignar foto exacta ni última vista de glaciar sin comprobar.',None,'testimonio_toponimo_en_TTL_anterior'),
 ('SalidaNocturnaYanaqancha2025','Reanudación nocturna de la Lomada desde Yanaqancha, 2025','2025','Yanaqancha','PracticaLomada','Tras descanso, los peregrinos vuelven a salir de noche o madrugada; el participante narra dureza del tramo nocturno siguiente.',None,'testimonio_contextual'),
 ('SecuenciaQueperinasInti2025','Queperinas reunidas antes de formación del Inti Alabado, 2025','2025','Tayankani','PracticaBaileZigzag','El participante identifica un momento inicial de queperinas reunidas, seguido de formación en filas y zigzag. No atribuir todas las imágenes a cada gesto.',None,'testimonio_y_fotos'),
 ('ZigzagIntiAlabado2025','Zigzag del Inti Alabado, 2025','2025','Tayankani','PracticaBaileZigzag','Desplazamiento colectivo en zigzag descrito por participante; no se interpreta su significado ritual.', 'UkumarisDistintasNaciones','testimonio_contextual'),
 ('ZigzagIntiAlabado2026','Zigzag del Inti Alabado, 2026','2026','Tayankani','PracticaBaileZigzag','Desplazamiento colectivo al amanecer, documentado en contexto de fotos y videos; el significado queda abierto.', 'UkumarisDistintasNaciones','testimonio_contextual'),
 ('RecibimientoChichaOcongate','Ofrecimiento de chicha en recepción de Ocongate',None,'Ocongate','PracticaRecepcionChicha','Según testimonio, personas de Ocongate reciben alegremente a peregrinos y ofrecen chicha; no visible inequívocamente en fotos.', 'PoblacionOcongate','testimonio_directo'),
 ('EsperaCanchaOcongateDocumentada','Espera en cancha de Ocongate hasta la noche',None,'CanchaOcongate','PracticaEsperaCancha','Participantes permanecen en cancha hasta la noche antes de viajar en camión; testimonio, sin fotografía de espera nocturna.',None,'testimonio_directo'),
 ('ParticipacionDanzasCorpus2026','Participación de danzas en Corpus Christi, Paucartambo, 2026','2026','Paucartambo','PracticaCorpusDanzas','Según testimonio, danzas de Nación Paucartambo vuelven a participar en Corpus Christi; escenas muestran procesión y vestimenta de danza.',None,'testimonio_y_fotos'),
 ('EscolaresCorpus2026','Presencia de escolares vestidos como danzas en Corpus Christi 2026','2026','Paucartambo','PracticaCorpusDanzas','Participación de niños, incluidos niños con vestimenta de ukumari, según testimonio; no identificar escuelas ni niños en fotos.', 'EscolaresLocalesPaucartambo','testimonio_no_identificar_menores'),
]
for nm,lab,yr,place,pr,desc,grp,state in events:
 s=set_entity(nm,'ActividadDocumentada',lab,desc,yr,place,pr,grp,source='Testimonio de investigador-participante y/o conjunto audiovisual contextual de 2025–2026',state=state)
 if 'an[oñ]o_pendiente' in state: lit(s,Q.incertidumbre,'Año de archivos no confirmado')

# Existing event label from legacy v01 is maintained, but annotate relevant old evidential restrictions.
obj(Q.IniciacionMorocosColqueDocumentada,Q.involucraObjeto,Q.Sorriago)
obj(Q.TrasladoCruz2025,Q.involucraObjeto,Q.CruzColquePunku)
obj(Q.QueperinasYanaqancha2025,Q.involucraObjeto,Q.Queperina)
obj(Q.QueperinasYanaqancha2025,Q.incluyeRol,Q.Moroco)
obj(Q.BautizoMorocoTayankani2025,Q.incluyeRol,Q.Moroco)
obj(Q.EscolaresCorpus2026,Q.participaColectivo,Q.EscolaresLocalesPaucartambo)
obj(Q.ZigzagIntiAlabado2025,Q.relacionadaConActividad,Q.IntiAlabado2025)
obj(Q.ZigzagIntiAlabado2026,Q.relacionadaConActividad,Q.IntiAlabado2026)
obj(Q.EncuentroBanderasColque2025,Q.relacionadaConActividad,Q.TrasladoCruz2025)
obj(Q.EsperaCanchaOcongateDocumentada,Q.relacionadaConActividad,Q.EncuentroCanchaOcongateDocumentado)
obj(Q.RecibimientoChichaOcongate,Q.relacionadaConActividad,Q.RecepcionOcongateDocumentada)
for e in ['EncuentroWataskamaDocumentado','EncuentroJuegosWataskama']:
 obj(Q[e],Q.tieneEvidencia,Q.TestimonioWataskama)
# Do not equate event with place or create sameAs link across old 2025 TTL.

# Narrated stages: order as contextual Paucartambo experienced chronology, not minute-accurate.
stages=[
 ('E01_Preparacion','Preparación y ensayo en Paucartambo',['Paucartambo','LosaHuascar']),
 ('E02_MisaRomeria','Misa, romería y salida por calles de Paucartambo',['Paucartambo','CementerioPaucartambo','IglesiaPaucartambo']),
 ('E03_CamionesCcatcca','Camiones, Ccatcca y parada en casa del prioste',['Paucartambo','Ccatcca','CasaPriosteParada']),
 ('E04_Mahuayani','Mahuayani y comienzo del ascenso a pie',['Mahuayani']),
 ('E05_Santuario','Ingreso, misas y campamento en el Santuario',['Santuario','CeldaUkumarisSantuario']),
 ('E06_ColquePunku','Subida nocturna, gruta y prácticas en Colque Punku',['ColquePunku','GrutaColquePunku']),
 ('E07_RegresoSantuario','Descenso, banderas y cruz en torno al Santuario',['ColquePunku','Santuario']),
 ('E08_LomadaInicio','Inicio de la Lomada desde el Santuario',['Santuario','RutaLomada']),
 ('E09_Wataskama','Encuentro, juegos y cruce en Wataskama',['Wataskama']),
 ('E10_QespiCruz','Paso y descanso asociado a Q’espi Cruz',['QespiCruz']),
 ('E11_Yanaqancha','Descanso, queperinas y actividad de ladera en Yanaqancha',['Yanaqancha']),
 ('E12_TramoNocturno','Reanudación nocturna y paso por Escalerachayoq',['Escalerachayoq','Tayankani']),
 ('E13_IntiAlabado','Inti Alabado al amanecer en Tayankani',['Tayankani']),
 ('E14_Bautizo','Bautizo de moroco en Tayankani (2025)',['Tayankani','GrutaTayankani']),
 ('E15_Ocongate','Marcha a Ocongate y recepción en cancha',['Tayankani','Ocongate','CanchaOcongate']),
 ('E16_RegresoNocturno','Retorno nocturno en camión a Paucartambo',['Ocongate','Paucartambo']),
 ('E17_CorpusChristi','Corpus Christi de Paucartambo: cierre de itinerario 2026',['Paucartambo']),
]
for i,(nm,lab,pts) in enumerate(stages):
 s=Q['Etapa_'+nm];obj(s,RDF.type,Q.EtapaNarrativa);lit(s,RDFS.label,lab)
 if nm != 'E10_QespiCruz':
  G.add((s,Q.ordenNarrativo,Literal(i+1,datatype=XSD.integer)))
 else:
  lit(s,Q.incertidumbre,'Orden relativo de Q’espi Cruz respecto de Wataskama y Yanaqancha pendiente; TTL histórico y relato requieren conciliación')
 obj(s,Q.parteDeItinerario,Q.RecorridoNarradoPaucartambo)
 for p in pts:obj(s,Q.conectaLugarNarrativo,Q[p])
 if i+1<len(stages) and nm not in ('E09_Wataskama','E10_QespiCruz'):
  obj(s,Q.etapaSiguiente,Q['Etapa_'+stages[i+1][0]])
obj(Q.Etapa_E09_Wataskama,Q.etapaSiguiente,Q.Etapa_E11_Yanaqancha)
obj(Q.RecorridoNarradoPaucartambo,RDF.type,Q.Recorrido)
lit(Q.RecorridoNarradoPaucartambo,RDFS.label,'Secuencia narrativa de Nación Paucartambo, 2025–2026; reconstrucción no uniforme')
lit(Q.RecorridoNarradoPaucartambo,Q.incertidumbre,'El orden entre ciertos hitos varía o no se ha especificado por año; las 17 etapas son una secuencia editorial general, no una traza de un único año.')
# Map staged episodes, list explicit not automatched.
stage_events={
 'E01_Preparacion':['EnsayoGeneralPaucartambo','PreparacionPaucartambo2026','PreparacionSalidaPaucartambo2025'],
 'E02_MisaRomeria':['MisaPreviaSalidaPaucartambo','RomeriaPaucartambo2025','RecorridoPuebloPaucartambo2025'],
 'E03_CamionesCcatcca':['SalidaCamionesPaucartambo2025','ParadaCcatccaDocumentada','ParadaCasaPrioste2025','ViajeVehiculo2026'],
 'E04_Mahuayani':['LlegadaMahuayani2026','CaminoMahuayaniSantuario2025','CaminoMahuayaniSantuario2026'],
 'E05_Santuario':['MisaSantuario2025','AcampadaSantuarioRelatada'],
 'E06_ColquePunku':['AscensoColquePunku2025','AscensoColquePunku2026','LlegadaGrutaColquePunku2025','SectorColquePunku2026','IniciacionMorocosColqueDocumentada'],
 'E07_RegresoSantuario':['DescensoColquePunku2025','DescensoColquePunku2026','LlegadaSantuario2026','EncuentroBanderasSantuario2026','EncuentroBanderasColque2025','TrasladoCruz2025'],
 'E08_LomadaInicio':['Lomada2025','Lomada2026'],
 'E09_Wataskama':['EncuentroWataskamaDocumentado','EncuentroJuegosWataskama'],
 'E10_QespiCruz':['DescansoQespiCruz2025'],
 'E11_Yanaqancha':['DescansoYanaqancha2025','DanzaCerroYanaqancha2025','QueperinasYanaqancha2025','SalidaNocturnaYanaqancha2025'],
 'E12_TramoNocturno':['PasoEscalerachayoqDocumentado'],
 'E13_IntiAlabado':['IntiAlabado2025','IntiAlabado2026','SecuenciaQueperinasInti2025','ZigzagIntiAlabado2025','ZigzagIntiAlabado2026'],
 'E14_Bautizo':['BautizoMorocoTayankani2025'],
 'E15_Ocongate':['CaminoTayankaniOcongateDocumentado','RecepcionOcongateDocumentada','RecibimientoChichaOcongate','EncuentroCanchaOcongateDocumentado','EsperaCanchaOcongateDocumentada'],
 'E16_RegresoNocturno':['RegresoCamionPrevioCorpus2026'],
 'E17_CorpusChristi':['CorpusChristiPaucartamboActividad2026','ParticipacionDanzasCorpus2026','EscolaresCorpus2026'],
}
for st,names in stage_events.items():
 for name in names:obj(Q[name],Q.enEtapaNarrativa,Q['Etapa_'+st])

# Chronology for only explicitly grounded sequences, not the entire global event set.
for chain in [
 ['RomeriaPaucartambo2025','RecorridoPuebloPaucartambo2025','SalidaCamionesPaucartambo2025','ParadaCasaPrioste2025','CaminoMahuayaniSantuario2025','MisaSantuario2025','AscensoColquePunku2025','LlegadaGrutaColquePunku2025','DescensoColquePunku2025','TrasladoCruz2025','Lomada2025','DescansoYanaqancha2025','SalidaNocturnaYanaqancha2025','IntiAlabado2025','BautizoMorocoTayankani2025'],
 ['PreparacionPaucartambo2026','ViajeVehiculo2026','LlegadaMahuayani2026','CaminoMahuayaniSantuario2026','AscensoColquePunku2026','DescensoColquePunku2026','LlegadaSantuario2026','Lomada2026','IntiAlabado2026','RegresoCamionPrevioCorpus2026','CorpusChristiPaucartamboActividad2026'],
 ['CaminoTayankaniOcongateDocumentado','RecepcionOcongateDocumentada','EncuentroCanchaOcongateDocumentado','EsperaCanchaOcongateDocumentada']]:
 for a,b in zip(chain,chain[1:]):obj(Q[b],Q.sigueEnSecuenciaA,Q[a])
# Photo chronology unknown for Ocongate; never type 2026 just from following Corpus 2026.

# Explicit GPX relation only where strongly grounded by route title and stage.
for name,nums in [('ViajeVehiculo2026',[1,2,3,12]),('CaminoMahuayaniSantuario2026',[4]),('AscensoColquePunku2026',[5]),('DescensoColquePunku2026',[6]),('Lomada2026',[7,8,9]),('IntiAlabado2026',[9,10])]:
 for n in nums:obj(Q[name],Q.relacionadoConTramoGPS,Q[f'Tramo{n:02d}'])
lit(Q.IntiAlabado2026,Q.incertidumbre,'Tramo 09–10 es contexto de recorrido, NO captación GPS exacta de la carrera en zigzag')

# Dataset 180 media, one individual per original record and one lot per existing group.
with CSV.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==180 and len({r['ID_foto'] for r in rows})==180
lot_map={
 '00_preparacion_2026':('LotePreparacion2026',['PreparacionPaucartambo2026'],'2026'),
 '01_romeria_2025':('LoteRomeria2025',['RomeriaPaucartambo2025'],'2025'),
 '02_salida_paucartambo_2025':('LoteSalidaPaucartambo2025',['RecorridoPuebloPaucartambo2025','PreparacionSalidaPaucartambo2025'],'2025'),
 '03_ccatcca_anio_por_confirmar':('LoteCcatccaAnioPendiente',['ParadaCcatccaDocumentada'],None),
 '04_casa_prioste_2025':('LotePrioste2025',['ParadaCasaPrioste2025'],'2025'),
 '05_mahuayani_2026':('LoteMahuayani2026',['LlegadaMahuayani2026'],'2026'),
 '06_camino_mahuayani_santuario_2025':('LoteCaminoMahuayani2025',['CaminoMahuayaniSantuario2025'],'2025'),
 '07_dron_2026':('LoteDron2026',[],'2026'),
 '08_misas_santuario_2025_interior_iglesia':('LoteMisasInterior2025',['MisaSantuario2025'],'2025'),
 '08_misas_santuario_2025_previo_ingreso_iglesia':('LoteMisasExterior2025',['MisaSantuario2025'],'2025'),
 '09_ascenso_colque_punku_2025_inicio':('LoteAscensoColque2025',['AscensoColquePunku2025'],'2025'),
 '09_ascenso_colque_punku_2025_llegada':('LoteLlegadaColque2025',['LlegadaGrutaColquePunku2025'],'2025'),
 '11_colque_punku_2026_sector_glaciar':('LoteColque2026',['SectorColquePunku2026'],'2026'),
 '12_descenso_colque_punku_2025':('Lote044_2025',['DescensoColquePunku2025'],'2025'),
 '13_regreso_y_llegada_santuario_2026':('Lote045_2026',['LlegadaSantuario2026','EncuentroBanderasSantuario2026'],'2026'),
 '14_descenso_cruz_reunion_naciones_2025':('Lote046_2025',['TrasladoCruz2025','EncuentroBanderasColque2025'],'2025'),
 'Bautizo personal de moroco — después del Inti Alabado, Tayankani, 2025':('Lote051_2025',['BautizoMorocoTayankani2025'],'2025'),
 'Camino Tayankani–Ocongate, recibimiento y encuentro en la cancha — año pendiente de confirmación':('Lote052_AnioPendiente',['CaminoTayankaniOcongateDocumentado','RecepcionOcongateDocumentada','EncuentroCanchaOcongateDocumentado'],None),
 'Corpus Christi de Paucartambo — cierre del recorrido de Nación Paucartambo (2026)':('Lote053_2026',['CorpusChristiPaucartamboActividad2026','EscolaresCorpus2026'],'2026'),
 'Inti Alabado — formación y desplazamiento ritual en Tayankani, 2025':('Lote050_2025',['IntiAlabado2025'],'2025'),
 'Inti Alabado — formación y desplazamiento ritual en Tayankani, 2026':('Lote050_2026',['IntiAlabado2026'],'2026'),
 'Lomada 2025 — recorrido de aproximadamente 24 horas':('Lote047_2025',['Lomada2025'],'2025'),
 'Yanaqancha — descanso y actividad en ladera durante la Lomada; 2025':('Lote049_2025',['DescansoYanaqancha2025','DanzaCerroYanaqancha2025'], '2025'),
}
group_names={r['Conjunto'] for r in rows}
assert set(lot_map)==group_names,(set(lot_map)-group_names,group_names-set(lot_map))
# A lot can contextualize an activity, without proving each described action is visible.
for group,(id,act,yr) in lot_map.items():
 s=Q[id];obj(s,RDF.type,Q.ConjuntoAudiovisual);lit(s,RDFS.label,group);year(s,yr)
 lit(s,Q.fuenteLote,CSV.name,lang=None);obj(s,DCTERMS.source,Q.FuenteInventario180)
 for a in act:obj(s,Q.contextualizaActividad,Q[a]);obj(Q[a],Q.tieneEvidencia,s)
 if group=='07_dron_2026':
  obj(s,Q.contextualizaFestividad,Q.QoyllurRiti2026)
  lit(s,Q.incertidumbre,'No se asigna sector específico de la Lomada ni GPS por imagen aérea sin cotejo')
 if 'Bautizo' in id or 'CorpusChristi' in id:lit(s,Q.nivelAcceso,'restringido hasta consentimiento de participantes y revisión de imágenes')
 if not yr:lit(s,Q.estadoValidacion,'anio_fotografias_pendiente',lang=None)

# Consolidate identities without regenerating or sharing original media.
for r in rows:
 mid=r['ID_foto'];safe='Medio_'+re.sub(r'[^A-Za-z0-9_]','_',mid)
 m=Q[safe];grp=r['Conjunto'];lot=Q[lot_map[grp][0]]
 obj(m,RDF.type,Q.RegistroAudiovisual);G.add((m,DCTERMS.identifier,Literal(mid)))
 obj(m,Q.formaParteDeLote,lot);obj(lot,Q.incluyeMedio,m)
 for k,p in [('Archivo_original_en_ZIP','nombreArchivoOriginal'),('Conjunto','nombreConjunto'),('Descripcion_visual','descripcionVisual'),('Limite_interpretacion','incertidumbre'),('Lugar_asignado_contextualmente','lugarContextualTexto'),('Tipo_evidencia','condicionDocumental'),('Estado_revision','estadoValidacion'),('Permiso_difusion','permisoDifusion'),('Nivel_acceso_recomendado','nivelAcceso'),('Permiso_IA','permisoIA'),('Tipo_archivo','tipoMedio'),('Archivo_ZIP_fuente','nombreZIPFuente'),('Ruta_archivo_en_paquete','rutaMedioArchivo'),('SHA256','hashSHA256'),('Fuente_de_identificacion','fuenteIdentificacion'),('Contexto_etnografico_relatado','contextoRelatado'),('Observaciones_revision','relacionConMaterial'),('Fecha_envio_no_captura','fechaEnvioNoCaptura'),('ID_anotacion','identificadorAnotacion'),('Año_confirmado_por_usuario','anioOriginalEnInventario')]:
  lit(m,Q[p],r.get(k,''),lang=None if k in ('hashSHA256','nombreZIPFuente','rutaMedioArchivo','nombreArchivoOriginal','identificadorAnotacion','anioOriginalEnInventario','fechaEnvioNoCaptura') else 'es')
 year(m,r.get('Año_confirmado_por_usuario',''))
 for p,datatype in [('Ancho_px',XSD.integer),('Alto_px',XSD.integer),('Duracion_video_s',XSD.decimal)]:
  raw=r.get(p,'').strip()
  if raw:
   try:
    import decimal
    if datatype==XSD.decimal:decimal.Decimal(raw)
    else:int(raw)
    obj(m,Q[p],Literal(raw,datatype=datatype))
   except (ValueError,decimal.InvalidOperation):
    lit(m,Q.duracionEstimativaTexto,raw,lang=None)
 # Only identify contextual place when the canonical ID is already an existing place node.
 place=r.get('ID_lugar_TTL_2026','').strip()
 if place and (Q[place],RDF.type,Q.LugarReferencia) in G:obj(m,Q.vinculadoALugarContextual,Q[place])
 obj(m,DCTERMS.source,Q.FuenteInventario180)
 if 'bautizo' in grp.lower() or 'Corpus Christi' in grp:
  lit(m,Q.nivelAcceso,'Acceso restringido a revisión y permiso; menores/experiencia personal pueden estar presentes')

# Every QR-AN 044–053 sub-annotation, plus corrected 046, in RDF as directly inspectable documents.
ann_files=[
 ('044','QR_AN_044_ANOTACIONES_DESCENSO_2025.csv',['DescensoColquePunku2025']),
 ('045','QR_AN_045_ANOTACIONES_LLEGADA_SANTUARIO_2026.csv',['LlegadaSantuario2026']),
 ('046','QR_AN_046_ANOTACIONES_CRUZ_RELEVO_2025_CORREGIDO.csv',['TrasladoCruz2025']),
 ('047','QR_AN_047_LOMADA_2025_ANOTACIONES.csv',['Lomada2025','DescansoQespiCruz2025']),
 ('049','QR_AN_049_YANAQANCHA_MEDIOS_Y_PENDIENTES_ANIO_CONFIRMADO_2025.csv',['DescansoYanaqancha2025','DanzaCerroYanaqancha2025','QueperinasYanaqancha2025']),
 ('050_2025','QR_AN_050_INTI_ALABADO_2025_ANOTACIONES.csv',['IntiAlabado2025']),
 ('050_2026','QR_AN_050_INTI_ALABADO_2026_ANOTACIONES.csv',['IntiAlabado2026']),
 ('051','QR_AN_051_BAUTIZO_MOROCO_TAYANKANI_2025_ANOTACIONES.csv',['BautizoMorocoTayankani2025']),
 ('052','QR_AN_052_RECEPCION_OCONGATE_Y_RETORNO_PAUCARTAMBO_ACTUALIZADO.csv',['RecepcionOcongateDocumentada','EncuentroCanchaOcongateDocumentado','RegresoCamionPrevioCorpus2026']),
 ('053','QR_AN_053_CORPUS_CHRISTI_PAUCARTAMBO_2026_ANOTACIONES.csv',['CorpusChristiPaucartamboActividad2026']),
]
ann_count=0
for prefix,fn,ev in ann_files:
 p=INV/fn
 if not p.is_file():raise FileNotFoundError(p)
 with p.open(encoding='utf-8-sig',newline='') as f:dr=list(csv.DictReader(f))
 for idx,r in enumerate(dr,1):
  if prefix=='049' and r.get('ID_anotacion')=='QR-AN-024':
   # A pending question, still captured in historical candidate dataset, add here as question.
   pass
  sid='AnotacionCampo_'+prefix+'_'+str(idx).zfill(2)
  s=Q[sid];obj(s,RDF.type,Q.AnotacionEtnografica)
  aid=r.get('ID_anotacion') or r.get('ID') or f'QR-AN-{prefix}-{idx}'
  lit(s,DCTERMS.identifier,aid,lang=None);lit(s,RDFS.label,f'{aid} · {prefix}')
  content=' '.join(r.get(k,'') for k in ('Afirmacion','Anotacion') if r.get(k))
  lit(s,Q.descripcionNarrativa,content)
  for k,v in r.items():
   if k not in ('Afirmacion','Anotacion') and v:
    lit(s,Q['campoAnotacion_'+re.sub(r'[^A-Za-z0-9]','_',k)],v,lang=None)
  lit(s,DCTERMS.source,fn,lang=None);obj(s,Q.anotacionFuente,Q.FuenteAnotacionesCampo)
  for e in ev:obj(s,Q.describeActividad,Q[e]);obj(Q[e],Q.tieneAnotacion,s)
  ann_count+=1

# Earlier annotation groups 030–043 are indexed from the image inventory; reconstruct only group-level pointers.
for annid,rs in collections.defaultdict(list,((id,[]) for id in [])).items():pass
annotations_by_id=collections.defaultdict(list)
for r in rows:
 ids=re.findall(r'QR-AN-0(?:3\d|4[0-3])',r.get('ID_anotacion',''))
 for aid in ids:annotations_by_id[aid].append(r)
for aid, rs in sorted(annotations_by_id.items()):
 s=Q['AnotacionContexto_'+aid.replace('-','_')];obj(s,RDF.type,Q.AnotacionEtnografica)
 lit(s,RDFS.label,aid+' · evidencia asociada en inventario')
 lit(s,DCTERMS.identifier,aid,lang=None)
 lit(s,Q.descripcionNarrativa,'Conjunto registrado con '+str(len(rs))+' medios y referencias de campo; los detalles deben verificarse en el CSV maestro. El hecho de figurar en inventario no concede publicación.')
 for mid in set(r['ID_foto'] for r in rs):obj(s,Q.esSustentadoPor,Q['Medio_'+re.sub(r'[^A-Za-z0-9_]','_',mid)])
 obj(s,Q.anotacionFuente,Q.FuenteInventario180)

# 87 legacy entities + 161 legacy relation candidates preserved as review records (not RDF assertions).
with zipfile.ZipFile(LEGACY) as z:
 def zcsv(suffix):
  path=next(n for n in z.namelist() if n.endswith(suffix))
  return list(csv.DictReader(io.StringIO(z.read(path).decode('utf-8-sig'))))
 old_entities=zcsv('ENTIDADES_2025_PARA_CONCILIAR.csv')
 old_candidates=zcsv('ANOTACIONES_CANDIDATAS_2025_PARA_2026.csv')
assert len(old_entities)==87 and len(old_candidates)==161
for r in old_entities:
 k=r['ID_2025'];s=Q['LegadoEntidad_'+re.sub(r'[^A-Za-z0-9_]','_',k)]
 obj(s,RDF.type,Q.ReferenciaLegado)
 lit(s,RDFS.label,r['Nombre_2025'] or k)
 lit(s,DCTERMS.identifier,k,lang=None)
 lit(s,Q.descripcionNarrativa,r.get('Comentario_original_2025',''))
 lit(s,Q.condicionDocumental,'Tipos en TTL 2025: '+r.get('Tipos_2025',''))
 lit(s,Q.restriccionesLegado,r.get('Advertencias',''))
 lit(s,Q.estadoMigracion,'referencia_historica_no_conciliada',lang=None)
 lit(s,DCTERMS.source,'qoyllurity(6)(1).ttl',lang=None)
 if r.get('ID_equivalente_2026_candidato',''):lit(s,Q.relacionConMaterial,'Posible correspondencia 2026: '+r['ID_equivalente_2026_candidato'])
for r in old_candidates:
 aid=r['ID_candidata'];s=Q['LegadoCandidata_'+aid.replace('-','_')]
 obj(s,RDF.type,Q.CandidatoConciliacion)
 lit(s,RDFS.label,'Revisión histórica '+aid);lit(s,DCTERMS.identifier,aid,lang=None)
 for old,new in [('ID_2025_sujeto','sujetoLegado'),('Predicado_TTL_2025','predicadoLegado'),('ID_2025_objeto','objetoLegado'),('Banderas_calidad','restriccionesLegado'),('Que_anotar_en_csv','descripcionNarrativa'),('Prioridad','prioridadRevision'),('Verificar_con','textoPregunta'),('Consejo_para_TTL_minimo','relacionConMaterial')]:lit(s,Q[new],r.get(old,''))
 lit(s,Q.estadoMigracion,'NO_ASERTADO_POR_REVISAR',lang=None)
 obj(s,DCTERMS.source,Q.FuenteTTLLegado2025)
 for fld in ('ID_2025_sujeto','ID_2025_objeto'):
  if r.get(fld,''):
   obj(s,Q.refiereAEntidad,Q['LegadoEntidad_'+re.sub(r'[^A-Za-z0-9_]','_',r[fld])])

# Questions remain openly visible. Some are direct triggers for future updates.
questions=[
 ('Q01_AnioOcongate','Confirmar el año de las cinco fotografías de Ocongate','Lote052_AnioPendiente','alta'),
 ('Q02_AnioCcatcca','Confirmar año de las tres fotografías de Ccatcca','LoteCcatccaAnioPendiente','media'),
 ('Q03_UltimaVistaGlaciar','Comprobar último lugar visible del glaciar y posición de Q’espi Cruz respecto a Yanaqancha y Wataskama','DescansoQespiCruz2025','alta'),
 ('Q04_DanzaCerro','Identificar nombre y alcance de la danza/actividades en cerro de Yanaqancha con informante','DanzaCerroYanaqancha2025','alta'),
 ('Q05_Dron','Ubicar individualmente DJI_0009–0028 y si alguna imagen mira hacia Santuario desde ruta Lomada','LoteDron2026','media'),
 ('Q06_PuntoFotografiaLomada','Asignar puntos de las 19 fotos de Lomada a lugares sólo con verificación visual, topográfica o testimonial','Lote047_2025','media'),
 ('Q07_PermisosBautizo','Confirmar permisos y acceso a imágenes personales del bautizo en 2025','Lote051_2025','alta'),
 ('Q08_DifusionMenores','Revisar permisos, privacidad y tratamiento de menores en Corpus Christi','Lote053_2026','alta'),
 ('Q09_GrutaTayankani','Confirmar emplazamiento del bautizo y equivalencia con gruta etiquetada en TTL original','GrutaTayankani','alta'),
 ('Q10_TransporteCruz','Revisar correspondencia temporal de los videos de cruz sin afirmar que se registra el instante de relevo','Lote046_2025','media'),
 ('Q11_MoroscosColque','Precisar alcance y año de la iniciación en Colque Punku; testimonio y otros participantes','IniciacionMorocosColqueDocumentada','media'),
 ('Q12_Escalerachayoq','Conciliar paso por Escalerachayoq con 2026 GPS sin heredar dobles tipos del TTL original','PasoEscalerachayoqDocumentado','media'),
 ('Q13_InicioFiesta2025_2026','Revisar si ensayo, misa, romería y salida se repiten con mismas secuencias en 2025 y 2026','EnsayoGeneralPaucartambo','media'),
 ('Q14_CeludaSantuario','Ubicación de celda de ukumaris en Santuario, sin exponer datos privados','AcampadaSantuarioRelatada','baja'),
 ('Q15_ConfrontacionLegado','Revisar las 161 relaciones candidatas del TTL 2025; no migrar autorreferencias y relaciones incongruentes','FuenteTTLLegado2025','alta'),
 ('Q16_Zigzag','Conservar en revisión el significado del zigzag del Inti Alabado; no inferirlo de forma visual','IntiAlabado2025','baja'),
 ('Q17_RecorridoOcongate','Relacionar regreso nocturno con pruebas documentales sin suponer traza GPX después de Tayankani','RegresoCamionPrevioCorpus2026','media'),
 ('Q18_CorpusNinos','Corroborar participación escolar sin identificar individualmente niños o centros educativos','EscolaresCorpus2026','media'),
 ('Q19_ClimaNieve','Mantener comparación nieve 2025/2026 como percepción cualitativa; no usar como inferencia sobre cambio climático','DescensoColquePunku2025','alta'),
 ('Q20_FotografiasFaltantes','Preservar que Wataskama y otras prácticas sin fotos tienen testimonio y pueden aparecer en el TTL','EncuentroWataskamaDocumentado','alta'),
]
for k,question,target,priority in questions:
 s=Q[k];obj(s,RDF.type,Q.PreguntaPendiente);lit(s,RDFS.label,question)
 lit(s,Q.textoPregunta,question);lit(s,Q.prioridadRevision,priority,lang=None)
 lit(s,Q.estadoValidacion,'abierta',lang=None);obj(Q[target],Q.tienePreguntaPendiente,s)

# Verify desired properties and no live, accidental identity inferences.
# Graph must have no triple imported asserting original namespace self-loops.
oldns='http://example.org/festividades#'
assert all(not(str(s).startswith(oldns) or str(p).startswith(oldns)) for s,p,o in G), 'Unexpected old graph assertions!'
assert len(set(G.subjects(RDF.type,Q.RegistroAudiovisual)))==180
assert len(set(G.subjects(RDF.type,Q.ReferenciaLegado)))==87
assert len(set(G.subjects(RDF.type,Q.CandidatoConciliacion)))==161
assert len(set(G.subjects(RDF.type,Q.PreguntaPendiente)))==20
assert len(set(G.subjects(RDF.type,Q.EtapaNarrativa)))==17
assert (Q.EncuentroWataskamaDocumentado,Q.tieneEvidencia,Q.TestimonioWataskama) in G
assert (Q.BautizoMorocoTayankani2025,Q.ocurreEn,Q.Tayankani) in G
assert not list(G.triples((Q.Lote052_AnioPendiente,Q.anioRegistro,None)))
# Validate no year assigned to unknown photo ID.
for r in rows:
 if r['ID_foto'].startswith('QR-FOT-ANO-PEND'):
  m=Q['Medio_'+re.sub(r'[^A-Za-z0-9_]','_',r['ID_foto'])]
  assert not list(G.triples((m,Q.anioRegistro,None)))

output=OUT/'qoylluriti_2025_2026_integral_v02.ttl'
G.serialize(destination=str(output),format='turtle',encoding='utf-8')
check=Graph().parse(output,format='turtle')
assert len(check)==len(G)

# Cross-link count, collision reporting and metadata for package.
counts={
 'triples':len(G),'clases':len(set(G.subjects(RDF.type,OWL.Class))),
 'prop_objeto':len(set(G.subjects(RDF.type,OWL.ObjectProperty))),
 'prop_dato':len(set(G.subjects(RDF.type,OWL.DatatypeProperty))),
 'actividades':len(set(G.subjects(RDF.type,Q.ActividadDocumentada))),
 'practicas':len(set(G.subjects(RDF.type,Q.PracticaCultural))),
 'lugares':len(set(G.subjects(RDF.type,Q.LugarReferencia))),
 'tramos_gpx':len(set(G.subjects(RDF.type,Q.Tramo))),
 'medios':len(set(G.subjects(RDF.type,Q.RegistroAudiovisual))),
 'lotes':len(set(G.subjects(RDF.type,Q.ConjuntoAudiovisual))),
 'anotaciones':len(set(G.subjects(RDF.type,Q.AnotacionEtnografica))),
 'anotaciones_detalladas':ann_count,
 'referencias_2025':len(set(G.subjects(RDF.type,Q.ReferenciaLegado))),
 'relaciones_2025_candidatas':len(set(G.subjects(RDF.type,Q.CandidatoConciliacion))),
 'preguntas':len(set(G.subjects(RDF.type,Q.PreguntaPendiente))),
 'etapas':len(set(G.subjects(RDF.type,Q.EtapaNarrativa))),
 'archivo':str(output),
 'hash_ttl_sha256':hashlib.sha256(output.read_bytes()).hexdigest()
}
import json
(OUT/'AUDITORIA_VALIDACION_v02.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(counts,ensure_ascii=False,indent=2))
