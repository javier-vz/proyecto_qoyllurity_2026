"""Uso: python consultar_imagenes.py IntiAlabado"""
from pathlib import Path
import sys
from rdflib import Graph, Namespace
root=Path(__file__).resolve().parent
g=Graph().parse(root/'qoylluriti_etnografia_v04_1_CON_MEDIOS.ttl')
qr=Namespace('http://example.org/festividades#')
nombre=sys.argv[1] if len(sys.argv)>1 else 'IntiAlabado'
for medio in g.objects(qr[nombre],qr.tieneRegistroVisual):
    rel=g.value(medio,qr.archivoRelativo)
    if rel:
        ruta=root/str(rel)
        print(g.value(medio,qr.identificadorMedio),ruta,'OK' if ruta.exists() else 'FALTA')
