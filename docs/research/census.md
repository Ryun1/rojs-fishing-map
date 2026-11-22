# Dive-census and port-survey records around Pico

Compiled 2026-11-22. Follows up section 4 of `species.md`, which left the raw Darwin Core archive of the IMAR/DOP visual census unopened. Labels as in the other notes: **[V]** verified by reading the data or page myself, **[I]** my inference, **[U]** unverified or a guess.

Script: `scripts/census.py` (downloads, filters, prints every table below). Derived data: `data/census/pico_census_sites.json` (about 11 KB).

## Headline

1. **The raw archive has no counts, depth, transect IDs, site names or sizes.** It is presence only, exactly like the GBIF view. [V]
2. Treating each unique date + coordinate as one dive gives **93 dives in the Pico box**, but **64 are at two offshore channel sites**, 5 are on the Faial side, 1 has an on-land coordinate. Only **23 dives (9 sites) are near the Pico shore, all on the west coast between Areia Larga and Formosinha, 17 of them in August 1999.** [V counts, I classification]
3. Nothing at all on the south, east or north coasts. The census cannot give per-spot checklists for most of the app's spots.
4. The ports & marinas Rapid Assessment Survey (2023-2024) has **no Pico records**: it covers Horta, Lajes das Flores and Ponta Delgada only. Horta marina (12 km across the channel) is the nearest proxy. [V]

## 1. Sources

| Dataset | Publisher | Licence | DOI / link | What I fetched |
|---|---|---|---|---|
| Underwater fish visual census in the Azores 1997 to 2015 | IMAR / DOP, University of the Azores (Afonso P, 2016) | CC BY 4.0 [V, eml.xml] | 10.14284/210; https://ipt.vliz.be/eurobis/archive.do?r=scuba_diving_visual_census | DwC-A zip (102 KB), v1.0; plus the OBIS copy via `api.obis.org/v3/occurrence?datasetid=df1970cb-fd9a-440a-9547-7ee6ec2605bc&extensions=MeasurementOrFact` |
| Marine Species Rapid Assessment Survey of Azorean Ports and Marinas (2023-2024) | Universidade dos Açores | CC BY 4.0 [V, GBIF API] | 10.15468/jwasph (GBIF dataset 9fe4e241-5b6b-46e3-a1f2-3c5d94478868) | all 216 records via GBIF occurrence API |

Attribution for anything shipped from these: "Data: IMAR/DOP Azores visual census 1997-2015 (doi 10.14284/210), CC BY 4.0" and, if the port data is used, "Universidade dos Açores RAS of Azorean ports and marinas 2023-2024 (doi 10.15468/jwasph), CC BY 4.0".

## 2. What fields exist

### 2.1 Visual census archive [V]

- `meta.xml` declares an **Occurrence core only, no extensions**. Files: `occurrence.txt`, `eml.xml`, `meta.xml` (dated 2016-06-02).
- 5,775 rows, 48 columns, of which 19 are populated: id / occurrenceID / catalogNumber (`Underwater_visual_census_N`), basisOfRecord, institutionCode, collectionCode, samplingProtocol (one constant value), eventDate (single day), habitat (`marine`), continent, waterBody, country, stateProvince, decimalLatitude, decimalLongitude, coordinateUncertaintyInMeters (`10` for every row), identifiedBy (observer names), scientificName, scientificNameID (WoRMS LSID).
- **Empty**: individualCount (column not even present), organismQuantity, recordNumber, fieldNumber, eventRemarks, locality, minimum/maximumDepthInMeters, sex, year/month/day (derivable from eventDate), all higher taxonomy.
- The IPT resource page (republished 2025-09-17, still version 1.0) shows an "ExtendedMeasurementOrFact" bar with 5,775 records, but the downloadable archive does not contain it. The OBIS copy does carry an eMoF: **every one of the 5,773 eMoF rows is `Sampling instrument = Underwater visual census using SCUBA diving gear`**. No abundance, depth or size facts anywhere. OBIS flags all 5,773 records `NO_DEPTH` and 64 `ON_LAND`.
- The EML methods say the counts exist: 50 m x 5 m belt transects to 40 m, depth strata every 10 m, "all mobile fish were identified ... and counted". They were not published. The EML says "For more detailed information on the dataset please contact contact point" (IMAR/DOP, Horta). Published uses of the count data: Schmiing et al. 2013 (MEPS 474: 201-216), Schmiing et al. 2014 (MEPS 513: 187-199), Zuur et al. 2012 (parrotfish abundance chapter).
- **Events**: there is no event ID, but each date + coordinate is unique to a small set of rows (522 combinations, 518 distinct coordinates in the whole archive), so a date + coordinate behaves like one dive or transect. Repeat visits to the same site show GPS scatter of tens of metres, never identical coordinates. [V counts; I interpretation]
- **Depth proxy**: OBIS attaches its own `bathymetry` (seabed depth at the coordinate from a gridded product) and `shoredistance`. These are not the transect depth; at 30 to 50 m depth they may still be right for the site, but a coarse grid near shore smooths cliffs. Reported below as ranges, label [I].

### 2.2 Ports & marinas RAS [V]

Sampling-event dataset with real structure: eventID (`2024-06-26_Horta`), locality, island, samplingEffort ("≤60 min visual survey per event; early stop after 15 min without new detections"), sampleSizeValue 60 minutes, depth 0, and an eMoF row per record with **abundance category on the SACFOR scale** (converted from DAFOR). One event per port per year, June or July.

## 3. Pico subset of the visual census

Box lat 38.35 to 38.60, lon -28.60 to -27.95: 1,080 records of all taxa, 93 dives on 46 distinct days. [V]

- Dives by year: 1997 14, 1998 10, 1999 33, 2000 16, 2002 4, 2004 10, 2013 2, 2014 3, 2015 1.
- Dives by month (Jan to Dec): 2 4 0 2 1 4 13 35 12 8 10 2. August is 38% of the effort. Any monthly pattern per species below mostly reflects this.

### 3.1 Census sites and nearest candidate spots

Sites are dive coordinates clustered within 300 m. Nearest spot uses the 43 candidate points in `scripts/spots_spots.py`. "Islet" is the distance to the nearer of Ilhéu Deitado / Ilhéu em Pé (OSM islet nodes via Nominatim). [V distances; I site interpretation]

| Site | Lat, lon | Dives | Days | Years | Dive months | Nearest spot (m) | OBIS seabed depth m | OBIS shore dist m | Interpretation [I] |
|---|---|---|---|---|---|---|---|---|---|
| S01 | 38.5164, -28.4587 | 1 | 1 | 2013 | Nov | cachorro (4,640) | on land (409 m elevation) | 4,416 inland | Bad coordinate; ignore for location |
| S02 | 38.5618, -28.4992 | 1 | 1 | 2014 | Aug | formosinha (1,203) | 21.5 | 754 | Off Formosinha / Toledos, boat dive |
| S03 | 38.5516, -28.5146 | 2 | 2 | 2014 | Jul, Oct | formosinha (887); barca (1,059) | 15.5-17 | 254-311 | Between Barca and Formosinha |
| S04 | 38.5478, -28.5202 | 3 | 1 | 1999 | Aug | barca (489) | 9-20 | 97-340 | Barca / Ponta da Laje |
| S05 | 38.5463, -28.5242 | 1 | 1 | 1999 | Aug | barca (431) | 13 | 380 | Barca |
| S06 | 38.5342, -28.5391 | 2 | 1 | 1999 | Aug | madalena (578) | 5 | 337-359 | Inshore of the islets, off Madalena |
| S07 | 38.5276, -28.5403 | 3 | 1 | 1999 | Aug | areialarga (490) | 10.5-13 | 109-327 | Areia Larga |
| S08 | 38.5334, -28.5434 | 1 | 1 | 1999 | Aug | madalena (954) | 5.5 | 249 | Between Madalena and the islets |
| S09 | 38.5299, -28.5459 | 1 | 1 | 1999 | Aug | areialarga (1,020) | 17.5 | 558 | Off Areia Larga, toward the islets |
| S10 | 38.5364, -28.5476 | 9 | 5 | 1998-99, 2013, 2015 | Jun, Aug, Oct | madalena (1,271) | 20 | 12-150 (from islet) | Ilhéus da Madalena (185 m from Ilhéu Deitado); regulated area, not shore-accessible |
| S11 | 38.5408, -28.5639 | 27 | 17 | 1997-2004 | 9 months | madalena (2,731) | 38 | 1,439-1,524 | Offshore channel reef 1.7 km W of the islets; possibly a charted baixa [U] |
| S12 | 38.5089, -28.5886 | 37 | 17 | 1997-2004 | 8 months | criacaovelha (4,134) | 29-50.5 | 2,836-2,997 | Mid-channel reef/bank [U which] |
| S13 | 38.5921, -28.5946 | 4 | 1 | 2004 | Jul | madalena (8,200) | 30.5-34 | 270-341 | Faial side (off Ribeirinha) |
| S14 | 38.5478, -28.5999 | 1 | 1 | 1999 | Aug | madalena (5,954) | 16 | 252 | Faial side (near Espalamaca) |

Effort warning: 11 of the 14 sites have 1 to 3 dives, mostly from a single day. Their species lists are a single snapshot, and absence from a 1-dive site means nothing.

### 3.2 Species across all 93 Pico-box dives

"Dives" = dives where the species was recorded at least once (frequency of occurrence, not abundance). Archive synonyms merged: *Balistes carolinensis*, *Pomatomus saltator*, *Seriola dumerilii*, *Trachynotus ovatus*, *Kyphosus sectator*, *Pseudolepidaplois scrofa*, *Scomber japonicus*, *Belone belone gracilis*; and *Centrolabrus trutta* is mapped to the Azorean endemic *C. caeruleus* (trutta does not occur in the Azores; older Azorean records used that name) [I].

| Species | App tier | Dives (of 93) | % | Sites (of 14) | Dive months Jan..Dec |
|---|---|---|---|---|---|
| *Diplodus sargus* | core | 80 | 86% | 14 | 2 4 0 2 1 4 13 28 9 6 10 1 |
| *Sparisoma cretense* | core | 49 | 53% | 13 | 0 0 0 0 0 1 5 26 5 5 5 2 |
| *Sphyraena viridensis* | core | 38 | 41% | 5 | 2 3 0 1 1 1 6 10 5 2 7 0 |
| *Sarda sarda* | core | 14 | 15% | 6 | 0 1 0 0 0 0 6 4 0 1 2 0 |
| *Gymnothorax unicolor* | core | 7 | 8% | 3 | 0 0 0 0 1 0 0 2 0 2 2 0 |
| *Muraena helena* | core | 5 | 5% | 4 | 0 0 0 0 0 0 2 1 1 0 1 0 |
| *Muraena augusti* | core | 4 | 4% | 3 | 0 0 0 0 0 0 0 1 0 2 1 0 |
| *Seriola rivoliana* | core | 1 | 1% | 1 | Aug |
| *Seriola dumerili* | core | 0 | 0% | 0 | (1 record Azores-wide) |
| *Pomatomus saltatrix* | core | 0 | 0% | 0 | (5 records Azores-wide) |
| *Thalassoma pavo* | secondary | 92 | 99% | 14 | |
| *Coris julis* | secondary | 91 | 98% | 14 | |
| *Serranus atricauda* | secondary | 82 | 88% | 12 | 2 4 0 2 1 4 12 29 11 6 9 2 |
| *Boops boops* | secondary | 73 | 78% | 12 | |
| *Sarpa salpa* | secondary | 57 | 61% | 11 | |
| *Abudefduf luridus* | secondary | 56 | 60% | 12 | |
| *Trachurus picturatus* | secondary | 46 | 49% | 8 | 2 3 0 2 1 3 7 11 6 4 6 1 |
| *Sphoeroides marmoratus* | secondary | 41 | 44% | 12 | |
| *Mullus surmuletus* | secondary | 30 | 32% | 11 | |
| *Labrus bergylta* | secondary | 27 | 29% | 9 | |
| *Centrolabrus caeruleus* | secondary | 23 | 25% | 12 | |
| *Bodianus scrofa* | secondary | 20 | 22% | 4 | |
| *Epinephelus marginatus* | secondary (release) | 13 | 14% | 6 | |
| *Balistes capriscus* | secondary | 12 | 13% | 9 | 0 0 0 0 0 0 2 4 0 2 3 1 |
| *Pagellus bogaraveo* | secondary | 9 | 10% | 5 | |
| *Pseudocaranx dentex* | secondary | 9 | 10% | 5 | 0 0 0 0 0 0 1 2 4 1 1 0 |
| *Pagellus acarne* | secondary | 6 | 6% | 3 | |
| *Phycis phycis*, *Scorpaena maderensis* | secondary | 5 each | 5% | 4, 2 | |
| *Trachinotus ovatus* | secondary | 4 | 4% | 4 | |
| *Pagrus pagrus* | secondary | 3 | 3% | 2 | |
| *Conger conger* | secondary | 2 | 2% | 1 | |
| *Scomber colias*, *Octopus vulgaris* | secondary | 1 each | 1% | 1 | |
| *Chelon labrosus*, *Kyphosus sectatrix*, *Belone belone*, *Loligo forbesii*, *Katsuwonus pelamis* | secondary | 0 | | | |

Month columns are left blank where they add nothing beyond the effort curve. The census never sampled March and barely sampled January, May and December, so a zero in those months is no evidence of absence. [V]

### 3.3 By shore-spot group (the only part usable per spot)

Dives where recorded / dives in group. Groups follow the nearest-spot column above. [V counts]

| Species | Formosinha S02-03 (3) | Barca S04-05 (4) | Madalena S06, S08 (3) | Areia Larga S07, S09 (4) | Ilhéus S10 (9) | Channel reefs S11-12 (64) |
|---|---|---|---|---|---|---|
| Sargo | 3 | 3 | 3 | 4 | 9 | 52 |
| Veja | 3 | 4 | 3 | 4 | 8 | 24 |
| Bicuda | | | 1 | 1 | 3 | 33 |
| Serra | 1 | | | 1 | 1 | 10 |
| Írio (*S. rivoliana*) | | | | 1 | | |
| Moreias (any of 3) | 1 | | | | 2 | 6 |
| Garoupa | 3 | 4 | | 3 | 8 | 58 |
| Chicharro | 2 | 1 | 1 | 3 | 4 | 35 |
| Salema | 3 | 2 | 3 | 3 | 9 | 32 |
| Boga | 3 | 3 | 1 | 4 | 8 | 49 |
| Salmonete | 1 | 1 | 3 | 2 | 5 | 15 |
| Peixe-porco | 2 | | 1 | 1 | 1 | 4 |
| Encharéu | | | 1 | 1 | | 6 |
| Prombeta | | 1 | | 1 | 1 | 1 |
| Bodião (*L. bergylta*) | 3 | 1 | 2 | | 4 | 14 |
| Peixe-rei / rainha (*C. julis*, *T. pavo*) | 3 | 4 | 3 | 4 | 9 | 63 |
| Mero (release) | | 1 | | | 1 | 9 |

Readable patterns, with the effort caveat: [I]

- Shallow west-coast dives (S02-S10) have veja in 22 of 23 dives versus 24 of 64 at the deeper channel reefs. Consistent with veja being a shallow-reef species.
- Bicuda is in 33 of 64 channel-reef dives but 5 of 23 shallow dives. The channel reefs are boat sites, so this does not say much about shore odds, except that bicuda is resident in the channel year round in the dive record (seen there in 10 of 12 months, including January, February and November; not in March, which was never sampled, or December).
- *C. caeruleus* is in 18 of 23 shallow dives but 1 of 64 channel dives. This looks like an observer naming or protocol difference between survey teams, not ecology; another reason not to compare sites closely.

## 4. Ports & marinas RAS (2023-2024)

No Pico port was surveyed: localities are Horta (Faial) 86 records, Lajes das Flores 70, Ponta Delgada 60. [V] Fish recorded with SACFOR abundance class (identical in both years, so it is one assessment per port, repeated):

| Species | Horta | Lajes das Flores | Ponta Delgada |
|---|---|---|---|
| *Chelon labrosus* (tainha) | Superdominant | Common | Frequent |
| *Diplodus sargus* (sargo) | Common | Common | Abundant |
| *Boops boops* (boga) | Common | Rare | |
| *Thalassoma pavo* | Common | Frequent | |
| *Sparisoma cretense* (veja) | Frequent | | |
| *Similiparma lurida* (= *Abudefduf luridus*) | Frequent | | |
| *Labrus bergylta*, *Symphodus caeruleus*, *Apogon imberbis*, *Chromis limbata*, *Synodus saurus* | Rare | | |
| *Diplodus vulgaris* | | Frequent | |
| *Ophioblennius atlanticus* | | Common | |
| *Sarpa salpa* | | Rare | |
| *Balistes capriscus* | | Rare | Rare |
| *Coris julis* | | | Rare |

Relevance [I]: confirms the harbour assemblage the app assumes (tainha dominant, sargo common, boga and veja present) in a large Azorean marina close to Pico. Pico harbours (Madalena, São Roque, Lajes, Cais do Pico) are smaller and more exposed, so treat it as a plausibility check only. Daytime, June/July, surface visual survey: no data on night species, morays or pelagics.

## 5. Caveats

- Presence only; frequency of occurrence depends on transect area, depth stratum and observer, none of which is recorded per row.
- 69% of Pico-box dives come from two offshore boat sites (S11, S12) and 78% of all dives were in 1997-2000. The whole east, south and north coast has zero dives.
- Coordinates: one Pico dive (S01, Nov 2013) sits 4.4 km inland. The "10 m" uncertainty is a blanket value.
- The census is diver-visible fish by day. Pelagic visitors (anchova, írio, serra) and nocturnal species (congro, moreias out of holes) are under-recorded relative to what an angler meets.
- Depth figures are OBIS's gridded seabed depth at the point, not survey depth.
- RAS port data: one visit per port per year; no Pico ports.

## 6. What this changes for the app

1. **No abundance or depth model can be built from this dataset as published.** Getting the counts (and transect depths) would need a data request to IMAR/DOP, Horta (dataset contact in the EML). For the app, the published habitat models (Schmiing et al. 2013, 2014) remain the better use of these dives. [I]
2. **Per-spot species checklists are only possible for five west-coast spots** (Madalena, Areia Larga, Barca, Formosinha, plus the Ilhéus as an offshore reference), and only as "seen by divers within about 0.5 to 1.2 km". Suggested wording: "Recorded by divers nearby (IMAR/DOP 1997-2015): sargo, veja, salema, garoupa, boga, chicharro, salmonete; occasionally bicuda, serra, peixe-porco." For all other spots, fall back to the island-wide list in `species.md` section 7. [I]
3. **Island-wide ranking support** (93 dives, west Pico channel): sargo, garoupa, boga, salema and the wrasses are near-ubiquitous; veja is ubiquitous in shallow water; chicharro about half of dives; bicuda common on channel reefs and present in winter months; serra regular (15%); morays recorded but under-sampled; anchova and *Seriola* essentially absent from the dive record. This supports the core/secondary split in `species.md` section 7 and argues for adding garoupa and salema as named species. [I]
4. **Do not derive monthly curves from the census**: August is 38% of effort and March has none. Seasonality should stay with SREA landings (`species.md` section 2). [I]
5. **Harbour spots**: the Horta RAS supports listing tainha (mullet) and sargo as the default harbour species, boga and veja as present. Tainha is never recorded in the Pico dive census (it lives in harbours and surf, which divers did not sample), so the census must not be used to rule out species at harbour spots. [I]
6. Attribution string for any checklist shipped from this: see section 1.
