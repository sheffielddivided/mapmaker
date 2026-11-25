"""
Bygger tilleggslagene til bakgrunnskartet (lastes først når de slås på i kartet):

- data/bathymetry.json: havdybde som fylte bånd (dypere enn 20, 50, 100, 200, 500,
  1000, 2000 og 3000 m) fra EMODnet Bathymetry (CC BY 4.0), hentet via WCS i ruter
  på 3x3 grader med 0,02° oppløsning. Øst for 43° Ø (utenfor EMODnet) fylles
  rutenettet fra NOAA ETOPO1 via ERDDAP (public domain).
- data/landextra.json: innsjøer, elver og byområder fra Natural Earth 10m (public domain).
- data/places.json: byer med minst 50 000 innbyggere fra Natural Earth, som
  [norsk navn, engelsk navn, lengde, bredde, land (ISO alfa-3), folketall].

Kjøres for hånd (krever numpy, rasterio og shapely; nedlastingen tar noen minutter):

    python build_basemap_extra.py work/
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import rasterio
import rasterio.features as RF
from rasterio.transform import from_origin
from shapely.geometry import MultiPolygon, Polygon, box, mapping, shape
from shapely.ops import unary_union

WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
OUT = 'data'
W, E, S, N, RES = -25, 44, 47, 83, 0.02
LEVELS = (20, 50, 100, 200, 500, 1000, 2000, 3000)
EMODNET = 'https://ows.emodnet-bathymetry.eu/wcs'
ETOPO = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.csv'
NE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson'


def download(url, path):
    if os.path.exists(path) and os.path.getsize(path):
        return path
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'mapmaker-build'}), timeout=300) as r:
                data = r.read()
            with open(path, 'wb') as fh:
                fh.write(data)
            return path
        except Exception:  # noqa: BLE001
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


# ── TopoJSON (enkel koder: hver ring/linje er én bue) ──────────────────────
def topology(layers, q=100000):
    pts = [c for fs in layers.values() for f in fs for c in _coords(f['geometry']['coordinates'])]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    sx, sy = (x1 - x0) / (q - 1), (y1 - y0) / (q - 1)
    arcs = []

    def arc(coords):
        d, px, py = [], 0, 0
        for x, y in coords:
            ix, iy = round((x - x0) / sx), round((y - y0) / sy)
            if d and ix == px and iy == py:
                continue
            d.append([ix - px, iy - py])
            px, py = ix, iy
        arcs.append(d)
        return len(arcs) - 1
    objs = {}
    for name, fs in layers.items():
        geoms = []
        for f in fs:
            t, c = f['geometry']['type'], f['geometry']['coordinates']
            a = {'Polygon': lambda: [[arc(r)] for r in c], 'MultiPolygon': lambda: [[[arc(r)] for r in p] for p in c],
                 'LineString': lambda: [arc(c)], 'MultiLineString': lambda: [[arc(l)] for l in c]}[t]()
            geoms.append({'type': t, 'arcs': a, 'properties': f['properties']})
        objs[name] = {'type': 'GeometryCollection', 'geometries': geoms}
    return {'type': 'Topology', 'transform': {'scale': [sx, sy], 'translate': [x0, y0]}, 'objects': objs, 'arcs': arcs}


def _coords(c):
    if isinstance(c[0], (int, float)):
        yield c
    else:
        for x in c:
            yield from _coords(x)


def write(name, obj):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, separators=(',', ':'))
    print(f'{OUT}/{name}: {os.path.getsize(os.path.join(OUT, name)) // 1024} KB')


# ── Havdybde ────────────────────────────────────────────────────────────────
def bathymetry_grid():
    tiles = os.path.join(WORK, 'emodnet')
    os.makedirs(tiles, exist_ok=True)
    jobs = []
    for x in range(W, E - 1, 3):
        for y in range(S, N, 3):
            params = {'service': 'WCS', 'version': '1.0.0', 'request': 'GetCoverage', 'coverage': 'emodnet:mean',
                      'crs': 'EPSG:4326', 'BBOX': f'{x},{y},{x + 3},{y + 3}', 'format': 'image/tiff', 'resx': RES, 'resy': RES}
            jobs.append((f'{EMODNET}?{urllib.parse.urlencode(params)}', os.path.join(tiles, f't_{x}_{y}.tif')))
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda j: download(*j), jobs))
    grid = np.full((round((N - S) / RES), round((E - W) / RES)), np.nan, np.float32)
    for _, path in jobs:
        with rasterio.open(path) as r:
            a, b = r.read(1).astype(np.float32), r.bounds
        c0, r0 = round((b.left - W) / RES), round((N - b.top) / RES)
        h, w = min(a.shape[0], grid.shape[0] - r0), min(a.shape[1], grid.shape[1] - c0)
        grid[r0:r0 + h, c0:c0 + w] = a[:h, :w]
    # ETOPO1 (1 bueminutt) der EMODnet mangler (øst for 43° Ø).
    q = 'altitude' + urllib.parse.quote(f'[({S}):1:({N})][(42):1:({E})]')
    etopo = download(f'{ETOPO}?{q}', os.path.join(WORK, 'etopo_east.csv'))
    for lat, lon, alt in np.genfromtxt(etopo, delimiter=',', skip_header=2):
        c, r = round((lon - W) / RES), round((N - lat) / RES)
        if lon >= 43 and 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and np.isnan(grid[r, c]):
            grid[r, c] = alt
    for _ in range(3):  # tett småhull mellom rutenettene
        m = np.isnan(grid)
        if not m.any():
            break
        grid[m] = np.nanmean(np.stack([np.roll(grid, s, ax) for ax in (0, 1) for s in (1, -1)]), 0)[m]
    p = np.pad(grid, 1, mode='edge')  # lett utjevning mot trappetrinn
    return sum(p[1 + dy:p.shape[0] - 1 + dy, 1 + dx:p.shape[1] - 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9


def build_bathymetry():
    g = bathymetry_grid()
    T = from_origin(W, N, RES, RES)
    layers = {}
    for L in LEVELS:
        m = (g < -L).astype(np.uint8)
        u = unary_union([shape(s) for s, _ in RF.shapes(m, mask=m.astype(bool), transform=T, connectivity=8)]).simplify(0.008)
        polys = [Polygon(p.exterior, [h for h in p.interiors if Polygon(h).area >= 0.004])
                 for p in (u.geoms if hasattr(u, 'geoms') else [u]) if p.area >= 0.004]
        layers[f'b{L}'] = [{'type': 'Feature', 'properties': {'d': L}, 'geometry': mapping(MultiPolygon(polys))}]
    write('bathymetry.json', topology(layers))


# ── Natural Earth ───────────────────────────────────────────────────────────
def ne(name):
    with open(download(f'{NE}/{name}.geojson', os.path.join(WORK, f'{name}.geojson')), encoding='utf-8') as fh:
        return json.load(fh)['features']


def build_landextra():
    clip = box(W, S, 50, N)

    def clipped(feats, tol, min_area=0, keep=lambda p: True):
        out = []
        for f in feats:
            if not f.get('geometry') or not keep(f['properties']):
                continue
            g = shape(f['geometry'])
            if g.intersects(clip):
                g = g.intersection(clip).simplify(tol, preserve_topology=True)
                if not g.is_empty and (not min_area or g.area >= min_area):
                    out.append(g)
        return out

    def feats(geoms):
        return [{'type': 'Feature', 'properties': {}, 'geometry': mapping(p)}
                for g in geoms for p in (g.geoms if hasattr(g, 'geoms') else [g])
                if not p.is_empty and p.geom_type in ('Polygon', 'LineString')]
    lakes = unary_union(clipped(ne('ne_10m_lakes') + ne('ne_10m_lakes_europe'), 0.004, 0.003))
    rivers = clipped(ne('ne_10m_rivers_lake_centerlines') + ne('ne_10m_rivers_europe'), 0.004,
                     keep=lambda p: (p.get('min_zoom') or 9) <= 6)
    urban = unary_union(clipped(ne('ne_10m_urban_areas'), 0.004, 0.002))
    write('landextra.json', topology({'lakes': feats(lakes.geoms), 'rivers': feats(rivers), 'urban': feats(urban.geoms)}))


# Norske navn: svensk navn fra Natural Earth der det er nærmest norsk, ellers disse.
NO_NAMES = {'Copenhagen': 'København', 'Prague': 'Praha', 'Brussels': 'Brussel', 'Kyiv': 'Kyiv', 'Helsinki': 'Helsingfors',
            'Saint Petersburg': 'St. Petersburg', 'Antwerp': 'Antwerpen', 'Ghent': 'Gent', 'Zaporizhzhia': 'Zaporizjzja',
            'Kharkiv': 'Kharkiv', 'Rostov-on-Don': 'Rostov ved Don', 'Arkhangelsk': 'Arkhangelsk', 'Dnipro': 'Dnipro',
            'Lviv': 'Lviv', 'Odesa': 'Odesa'}


def build_places():
    out = []
    for f in ne('ne_10m_populated_places'):
        p = f['properties']
        lon, lat = f['geometry']['coordinates'][:2]
        if not (W <= lon <= 50 and S <= lat <= N) or (p['POP_MAX'] or 0) < 50000:
            continue
        en = p['NAME_EN'] or p['NAME']
        no = p['NAME'] if p['ADM0_A3'] in ('NOR', 'DNK', 'SWE', 'FIN', 'ISL', 'FRO') else NO_NAMES.get(en) or p['NAME_SV'] or p['NAME']
        out.append([no, en, round(lon, 3), round(lat, 3), p['ADM0_A3'], int(p['POP_MAX'])])
    out.sort(key=lambda r: -r[5])
    write('places.json', out)


if __name__ == '__main__':
    os.makedirs(WORK, exist_ok=True)
    build_places()
    build_landextra()
    build_bathymetry()
