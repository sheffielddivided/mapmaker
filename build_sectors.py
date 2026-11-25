"""
Legger nederlandsk, tysk, irsk, fransk og belgisk sektor inn i bakgrunnskartet
(data/basemap.json): sektoromriss (sectorAreas, cc = nl/de/ie/fr/be) og sektorgrenser
(sectors) mot britisk, dansk og hverandres sektor. Frankrike og Belgia har ingen
kartdata, bare grensene (og omrisset, som avgjør hvilken side landnavnet står på).

Omrissene er de økonomiske sonene fra Marine Regions (VLIZ, CC BY 4.0), tysk sone
avgrenset til Nordsjøen og fransk til havet nord for 47° N, minus det som allerede hører til norsk, britisk og dansk
sektor (bygget fra blokknettene). Grensene er den delen av omrisset som ligger
innenfor 0,02° fra nabosektoren, slik README beskriver for de andre sektorene.

Kjøres for hånd (krever shapely) på bakgrunnskartet slik det var før NL/DE/IE/FR/BE
(git show 9339a8d:data/basemap.json), etter at EEZ-ene er lastet ned:

    for c in NLD DEU IRL FRA BEL; do curl -o dl/eez_$c.json "https://geo.vliz.be/geoserver/MarineRegions/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=MarineRegions:eez&outputFormat=application/json&CQL_FILTER=iso_ter1='$c'"; done
    python build_sectors.py data/basemap.json dl
"""
import json
import sys
def load(path):
    return json.load(open(path))
def arcs_abs(topo):
    sx,sy=topo['transform']['scale'];tx,ty=topo['transform']['translate']
    out=[]
    for a in topo['arcs']:
        x=y=0;pts=[]
        for dx,dy in a:
            x+=dx;y+=dy;pts.append((x*sx+tx,y*sy+ty))
        out.append(pts)
    return out
def arc(A,i):
    return A[i] if i>=0 else A[~i][::-1]
def line(A,idx):
    pts=[]
    for i in idx:
        p=arc(A,i); pts+= p if not pts else p[1:]
    return pts
def geom(A,g):
    t=g['type']
    if t=='LineString': return {'type':t,'coordinates':line(A,g['arcs'])}
    if t=='MultiLineString': return {'type':t,'coordinates':[line(A,l) for l in g['arcs']]}
    if t=='Polygon': return {'type':t,'coordinates':[line(A,r) for r in g['arcs']]}
    if t=='MultiPolygon': return {'type':t,'coordinates':[[line(A,r) for r in p] for p in g['arcs']]}
    return None
def features(topo,name):
    A=arcs_abs(topo)
    return [{'type':'Feature','properties':g.get('properties',{}),'geometry':geom(A,g)} for g in topo['objects'][name]['geometries']]

from shapely.geometry import shape, box, Polygon, MultiPolygon, mapping, LineString
from shapely.ops import linemerge, unary_union
BASEMAP, DL = sys.argv[1], sys.argv[2]
b = load(BASEMAP)
areas = {f['properties']['cc']: shape(f['geometry']).buffer(0) for f in features(b, 'sectorAreas')}

def eez(c, clip=None):
    # Bare selve sonen, ikke felles forvaltningsområder («Joint regime area») som følger med i svaret.
    feats = json.load(open(f'{DL}/eez_{c}.json'))['features']
    g = shape(next(f for f in feats if 'Exclusive Economic Zone' in (f['properties'].get('geoname') or ''))['geometry'])
    if clip: g = g.intersection(clip)
    polys = [Polygon(p.exterior) for p in (g.geoms if hasattr(g, 'geoms') else [g]) if p.area > 0.01]
    return unary_union(polys).simplify(0.001)
new = {'nl': eez('NLD'), 'de': eez('DEU', box(0, 50, 9.3, 58)), 'ie': eez('IRL'),
       # Fransk sone nord for 47° N (Kanalen og nordlige Biscaya); bakgrunnskartet slutter ved 47,4° N.
       'fr': eez('FRA', box(-10, 47, 3, 52)), 'be': eez('BEL')}
# Deler med eksisterende sektorer fjernes, så hver sjø bare hører til ett land.
for k in new:
    for o, g in areas.items():
        new[k] = new[k].difference(g)
new['de'] = new['de'].difference(new['nl'])
new['fr'] = new['fr'].difference(new['ie'])
new['be'] = new['be'].difference(new['nl']).difference(new['fr'])
TOL = 0.02
lines = []
def border(a, b_, l, r):
    seg = a.boundary.intersection(b_.buffer(TOL))
    parts = [s for s in (seg.geoms if hasattr(seg, 'geoms') else [seg]) if s.geom_type == 'LineString' and not s.is_empty]
    m = linemerge(parts) if parts else None
    if m is None: return
    ms = sorted((x for x in (m.geoms if hasattr(m, 'geoms') else [m]) if not x.is_ring), key=lambda x: -x.length)
    # Grenser kan være delt (Irland/Storbritannia nord og sør for Nord-Irland); småbiter ved kysten droppes.
    ms = [x for x in ms if x.length >= 0.3] or ms[:1]
    if not ms: return
    print(l, r, [round(x.length, 3) for x in ms], file=sys.stderr)
    g = ms[0] if len(ms) == 1 else {'type': 'MultiLineString', 'coordinates': [list(x.coords) for x in ms]}
    lines.append(({'l': l, 'r': r}, mapping(g) if not isinstance(g, dict) else g))
border(new['nl'], areas['uk'], 'nl', 'uk')
border(new['de'], new['nl'], 'nl', 'de')
border(new['de'], areas['uk'], 'uk', 'de')
border(new['de'], areas['dk'], 'dk', 'de')
border(new['ie'], areas['uk'], 'uk', 'ie')
border(new['fr'], areas['uk'], 'uk', 'fr')
border(new['fr'], new['ie'], 'ie', 'fr')
border(new['be'], new['nl'], 'nl', 'be')
border(new['be'], areas['uk'], 'uk', 'be')
border(new['be'], new['fr'], 'fr', 'be')
# Kod nye buer med bakgrunnskartets transform og legg dem til topologien.
sx, sy = b['transform']['scale']; tx, ty = b['transform']['translate']
def add_arc(coords):
    q = [(round((x - tx) / sx), round((y - ty) / sy)) for x, y in coords]
    d, px, py = [], 0, 0
    for x, y in q:
        if d and x == px and y == py: continue
        d.append([x - px, y - py]); px, py = x, y
    b['arcs'].append(d)
    return len(b['arcs']) - 1
def rings(poly):
    return [[add_arc(poly.exterior.coords)]] + [[add_arc(r.coords)] for r in poly.interiors]
for cc in new:
    g = new[cc]
    polys = list(g.geoms) if hasattr(g, 'geoms') else [g]
    polys = [p for p in polys if p.area > 0.001]
    b['objects']['sectorAreas']['geometries'] = [x for x in b['objects']['sectorAreas']['geometries'] if x['properties']['cc'] != cc]
    b['objects']['sectorAreas']['geometries'].append({'type': 'MultiPolygon', 'arcs': [rings(p) for p in polys], 'properties': {'cc': cc}})
    print(cc, 'area polys', len(polys), round(sum(p.area for p in polys), 3), file=sys.stderr)
secs = b['objects']['sectors']['geometries']
secs[:] = [x for x in secs if not ({x['properties']['l'], x['properties']['r']} & set(new))]
for props, g in lines:
    if g['type'] == 'LineString':
        secs.append({'type': 'LineString', 'arcs': [add_arc(g['coordinates'])], 'properties': props})
    else:
        secs.append({'type': 'MultiLineString', 'arcs': [[add_arc(c)] for c in g['coordinates']], 'properties': props})
json.dump(b, open(BASEMAP, 'w'), separators=(',', ':'))
