# NCS Mapmaker

**Live:** https://map.kbak.no/

Lager egendefinerte kart over norsk, britisk, dansk, nederlandsk, tysk og irsk sokkel til PowerPoint-presentasjoner.

Innstillingene ligger i fire faner: **Innhold** (kartlag, selskap/portefølje), **Kart** (utsnitt, bakgrunn,
sektorer og rutenett, forstørrede felt, 3D), **Tekst og pynt** (tittel, tegnforklaring, miniatyrkart,
målestokk, etiketter) og **Lagre**. Én seksjon er åpen om gangen, sjeldne finjusteringer ligger under
«Flere valg», og feltet «Finn innstilling …» søker på norsk og engelsk og åpner riktig fane og seksjon.

- **Kartlag:** felt i produksjon, felt under utbygging, nedstengte felt, funn, aktive lisenser (stiplet eller heltrukket omriss, eller helfarge uten omriss),
  transportrørledninger (filtrert på medium, valgfritt bare de som er knyttet til valgt selskap/portefølje,
  med etiketter langs røret), innretninger og letebrønner (filtrert på år, formål og resultat).
- **Sektorer:** norsk, britisk, dansk, nederlandsk, tysk og irsk sektor kan slås av og på hver for seg.
  Grensen mot fransk sektor tegnes også (Frankrike har ingen offshore produksjon og ingen kartdata her). Sektorgrensene kan få egen
  farge, tykkelse og stil, og landnavn parallelt med linjen på hver side.
- **Selskapsfilter:** velg ett eller flere selskaper som operatør og/eller partner. De kan fremheves
  (andre vises i grått) eller vises alene, med valgfri eierandel i etiketten. Gjelder felt, funn og lisenser.
  Med «Farge per selskap» får hvert valgte selskap sin egen farge, og felt med flere av de valgte
  selskapene som eiere skraveres i deres farger.
- **Egendefinert portefølje:** alternativ til selskapsfilteret. Velg enkeltfelt og -funn ved å søke
  eller klikke i kartet, og gi porteføljen et navn som vises i tegnforklaringen. Fremhev/vis kun
  valgte og «Zoom til utvalg» virker som for selskaper.
- **Farger:** standardfargene følger en fast palett (magenta, oransje, grønn, blå, rød, gul og gråtoner).
  Paletten tilbys som forslag i alle fargevelgere, og «Tilbakestill farger til standardpaletten» under
  Kartlag setter alle farger tilbake uten å endre andre innstillinger.
- **Bakgrunn:** vektorkart med kystlinje, dybdekurver, landegrenser, valg av hvilke land som vises (f.eks. bare Norge og Danmark), byer og kvadrant-/blokknett (kvadranter med eller uten nummer, valgfri farge og linjetykkelse).
  Fire fargetemaer pluss egne farger, og transparent bakgrunn.
- **Forstørrede felt:** felt kan forstørres opptil seks ganger rundt sitt eget midtpunkt, slik at små felt
  blir synlige i oversiktskart. Valgfritt også funn, og valgfritt bare valgte felt og funn.
- **Miniatyrkart:** valgfritt oversiktskart i et hjørne (eller dratt til valgfri plass) som viser hvor utsnittet er hentet fra
  (automatisk område eller Nordsjøen/Skandinavia/Nord-Europa, markert med omriss eller sirkel).
- **3D-effekt:** vipping og rotasjon, felt og funn som klosser, og forhøyet land med kystvegger («Landhøyde»).
- **Profiltemaer:** «Profil – lyst kart» og «Profil – mørkt kart» følger profilens kartfarger (bakgrunn,
  kart, tekst og markør).
- **Markører og ledelinjer:** punkt med strek til en tekst, f.eks. for å vise et sted. Klikk i kartet for å plassere,
  dra teksten eller punktet for å flytte, og høyreklikk teksten for å endre den. Etiketter som dras bort fra
  objektet sitt, får samme strek og punkt. Markørtekst og etiketter har samme tekststørrelse og skrift som
  feltnavnene. Strekvalgene gjelder både markører og flyttede etiketter og står sammen med etikettvalgene
  under «Etiketter og markører»: farge, punktstørrelse og strektype (fri, vannrett med målet eller knekt,
  dvs. vannrett ut fra målet og så skrå i valgfri vinkel). Standardfargen følger temaet.
- **Tegnforklaring:** i et av hjørnene, eller dra den til valgfri plass i kartet («Flyttet manuelt»).
- **Slide-format:** 16:9, halvside, 4:3, kvadrat, stående eller egendefinert. Rammen viser nøyaktig
  det som eksporteres.
- **Eksport:** *Kopier* legger en PNG på utklippstavlen (lim inn i PowerPoint med Ctrl+V), *PNG*
  laster ned i opptil 8K, og *SVG* gir vektorgrafikk. I PowerPoint kan SVG-en konverteres til figur
  ved å høyreklikke og velge «Konverter til figur».
- **Animasjon (video):** under Lagre lager «Lag video (MP4)» en kameratur der kartet flyr inn til sluttbildet,
  med valgfri sving (rotasjon underveis), bue (hvor mye kameraet løfter seg), varighet og hold på slutten.
  Starten er automatisk (samme midtpunkt, flatt og zoomet ut), et av de faste utsnittene eller et eget utsnitt.
  Slutten følger kartet eller låses. Etiketter og pynt tones inn ved landing (tittelen kan stå hele tiden),
  så den siste ruten er lik PNG-eksporten. Videoen tegnes rute for rute i full kvalitet og kodes som H.264
  med WebCodecs i nettleseren ([mp4-muxer](https://github.com/Vanilagy/mp4-muxer) lastes fra CDN først
  når videoen lages). Forhåndsvisningen bruker forenklet detalj.
- **Etiketter:** overlappende etiketter skjules automatisk. Dra en etikett for å flytte den, og
  dobbeltklikk for å skjule den, og høyreklikk for å endre teksten. Panelet «Etiketter i kartet» lister alle etiketter som vises nå,
  gruppert etter type, med avkrysning for å skjule/vise hver enkelt. Teksten i en etikett kan redigeres
  med ✎ i listen eller ved å høyreklikke etiketten i kartet; tømt felt gir standardteksten tilbake.
- **Språk:** engelsk (standard) eller norsk, både i grensesnittet og i kartet (tegnforklaring, kildehenvisning, verktøytips).
- **Lagring:** hele oppsettet ligger i URL-en, så kart kan bokmerkes og deles. Navngitte maler
  lagres lokalt i nettleseren.

## Data

`fetch_data.py` (kun Python-standardbiblioteket) henter alle lag og skriver `data/*.json`. Hver
feature har `cc` = `no`, `uk`, `dk`, `nl`, `de` eller `ie`.

| Sektor | Kilde | Lag |
| --- | --- | --- |
| Norge | [Sodir FactMaps](https://factmaps.sodir.no) (NLOD 2.0) | felt, funn, lisenser, letebrønner, rørledninger, innretninger, kvadranter, blokker |
| Storbritannia | [NSTA Open Data](https://opendata-nstauthority.hub.arcgis.com) (Open Government Licence v3.0) | felt (med rettighetshavere), uutbygde funn (punkter), lisens-delområder med eierandel, lete-/avgrensningsbrønner, transportrør ≥ 16", plattformer/FPSO/terminaler, havbunnsrammer, kvadranter, blokker |
| Nederland | [NLOG](https://www.nlog.nl) (TNO for Ministerie van Economische Zaken) via [WFS](https://www.gdngeoservices.nl/geoserver/nlog/ows?service=WFS&request=GetCapabilities) | felt (offshore, med operatør og status), uutbygde felt som funn, aktive lete- og utvinningslisenser (uten rettighetshavere: tjenesten oppgir dem ikke), lete-/avgrensningsbrønner med resultat, produksjonsplattformer, satellitter og havbunnsinnretninger. Rørledninger mangler: Rijkswaterstaats rørlag for Nordsjøen er ikke åpent |
| Tyskland | [EMODnet Human Activities](https://emodnet.ec.europa.eu/en/human-activities) | aktive lisenser, letebrønner, plattformer (A6-A og Mittelplate). Det finnes ingen åpne feltavgrensninger. Rørledningene i tysk sektor (Norpipe, Europipe, Zeepipe, Franpipe) ligger i Sodirs rørlag |
| Irland | [Marine Institute](https://basemap.marine.ie/arcgis/rest/services/Physical/OffshoreEnergy/FeatureServer) (Petroleum Affairs Division, CC BY 4.0) og EMODnet | lisenser som ikke er utløpt, lete-/avgrensningsbrønner med resultat (til 2019), Corrib-røret og Corrib (havbunn). Ingen åpne feltavgrensninger; Kinsale-området stengte i 2020 og er utelatt. Gassrørene fra Skottland ligger i NSTA-laget |
| Danmark | Energistyrelsens data via [GEUS WFS](https://data.geus.dk/geusmap/ows/4326.jsp) (feltavgrensninger, rørledninger, brønnresultater) og shapefilene i [sheffielddivided/ens](https://github.com/sheffielddivided/ens) | felt (status fra års- og månedsproduksjonen, eierandeler fra `ownership.json`), rørledninger (gass/olje/flerfase), lisenser, letebrønner med resultat (til 2019), innretninger, blokker |

Selskapsnavn normaliseres til konsernnavn (`GROUPS` i skriptet), så ett valg dekker datterselskaper
i alle land. `data/companies.json` kobler juridiske navn til konsernnavn, slik at eldre lenker og
maler fortsatt virker.

GitHub Action-en `.github/workflows/update-data.yml` kjører skriptet daglig og committer bare
når dataene faktisk er endret. Feiler én kilde, beholdes forrige data for det landet. Skriptet kan
også kjøres lokalt:

```
python fetch_data.py
```

`data/basemap.json` (kystlinje, landegrenser, dybdekurver og sektorgrenser) er statisk. Den er bygget én gang fra
[Natural Earth](https://www.naturalearthdata.com) 10m (public domain) med
[mapshaper](https://github.com/mbloch/mapshaper):

```
mapshaper -i ne_10m_land.shp ne_10m_minor_islands.shp combine-files -merge-layers force \
  -clip bbox=-14,48,50,83 -dissolve2 -simplify 70% weighted keep-shapes \
  -filter-slivers min-area=0.3km2 -rename-layers land -o land.json format=topojson
# tilsvarende for admin_0_boundary_lines_land (borders, med -filter-fields ADM0_A3_L,ADM0_A3_R -rename-fields l=ADM0_A3_L,r=ADM0_A3_R) og bathymetry_K_200/J_1000/I_2000/H_3000
# (d200/d1000/d2000/d3000), deretter:
# landene hver for seg (for landvalget), fra admin_0_countries:
mapshaper -i ne_10m_admin_0_countries.shp -clip bbox=-14,48,50,83 -filter-fields ADM0_A3,NAME \
  -rename-fields c=ADM0_A3 -simplify 70% weighted keep-shapes -filter-slivers min-area=0.3km2 \
  -rename-layers countries -o countries.json format=topojson
mapshaper -i land.json borders.json d200.json d1000.json d2000.json d3000.json sectors.json countries.json \
  combine-files -o basemap.json format=topojson quantization=100000
```

Sektorområdene (`sectorAreas`) for Norge, Storbritannia og Danmark er hvert lands blokknett (Sodir, NSTA og ENS) slått sammen
(`mapshaper -i no.json uk.json dk.json combine-files snap snap-interval=0.0005 -merge-layers force -dissolve2 cc`).
Sektorgrensene (`sectors`, med landene på hver side i `l`/`r`) er den delen av ett lands sektoromriss
som ligger innenfor 0,01° fra nabolandets sektor. Det gir én sammenhengende linje per grense, også
der blokknettene fra ulike kilder ikke deler punkter nøyaktig.

Nederlandsk, tysk, irsk og fransk sektor er lagt til etterpå med `build_sectors.py` (krever shapely), fra de økonomiske
sonene i [Marine Regions](https://www.marineregions.org) (CC BY 4.0), tysk sone avgrenset til Nordsjøen og fransk
til havet nord for 47° N.
Skriptet legger til omriss og grenser mot britisk, dansk og hverandres sektor uten å endre resten av
bakgrunnskartet. `fetch_data.py` bruker omrissene til å skille sokkel fra land i NLOG- og EMODnet-dataene.

Siden må serveres over HTTP(S). Den fungerer ikke åpnet direkte som fil. Lokalt:

```
python3 -m http.server 8000
# -> http://localhost:8000/
```

## Innhold

| Fil | Rolle |
|---|---|
| `index.html` | Hele Mapmaker. Én fil, vanilla JS med d3 og topojson-client fra CDN (og mp4-muxer ved videoeksport), ingen byggesteg |
| `fetch_data.py` | Henter kartlagene fra Sodir, NSTA, Energistyrelsen, NLOG, EMODnet og Marine Institute og skriver `data/*.json` |
| `build_sectors.py` | Legger nederlandsk, tysk, irsk og fransk sektor inn i `data/basemap.json` (kjøres for hånd) |
| `data/` | Kartlagene (`fields`, `discoveries`, `licences`, `pipelines`, `facilities`, `quadrants`, og `wells` og `blocks`, som lastes først når de slås på), `companies.json` (juridiske navn → konsern), `meta.json` (dato og kilder) og det statiske bakgrunnskartet `basemap.json` |
| `.github/workflows/update-data.yml` | Kjører `fetch_data.py` daglig 04:30 UTC og committer bare når dataene er endret |
| `.htaccess` | Apache-oppsett for map.kbak.no: sperrer skript, dokumentasjon og dotfiler, slår av mellomlagring av JSON/HTML og komprimerer |

## Publisering

Push til `main` publiseres på map.kbak.no på samme måte som NCS Insight på energy.kbak.no: en webhook
i GitHub får Plesks Git-utvidelse til å hente repoet til `httpdocs`. Datafilene oppdateres av
workflowen, som committer direkte til `main`, og når siden samme vei.

## Opphav

Mapmaker ble utviklet som `ppt.html` i `sheffielddivided/map` og er flyttet hit, til et eget repo,
så den kan publiseres alene. Utseendet (farger og font i topplinje og menyer) følger NCS Insight
(`sheffielddivided/ncs-production`).
