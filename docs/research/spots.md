# Pico (Azores) shore-fishing spots: research notes

Compiled 2026-11-22. Web research plus read-only queries to OpenStreetMap (Overpass, Nominatim), EMODnet Bathymetry REST and OpenTopoData (GEBCO 2020). All requests used a generic user agent (`research-script/1.0`) and carried no personal details.

## How to read this file

Every statement carries one of four labels. PDFs, the dive portal, OSM and bathymetry responses were read raw; news, tourism and council pages were read as extracted summaries from a fetch tool, so wording there is paraphrase.

- **[V] Verified**: I fetched the source and read the text or data myself. URL given.
- **[I] Inference**: derived by me from map geometry or bathymetry grids. Reasonable, not confirmed on the ground.
- **[A] Anecdote**: a source associates this with the place, but it is not evidence about angling there (for example dive-site species lists).
- **[S] Snippet only**: seen only as a search-engine summary of a page that refused automated fetching. Treat as a lead, not a fact.

Evidence grade for "is this place actually fished from shore":

- **A** = a fetched source documents angling at or beside this named place.
- **B** = fetched sources document the port, pier, ramp or bathing area; angling there is plausible but I found no online source naming it as a fishing mark.
- **C** = named coastal feature only (cape, bay); included to fill a gap in coverage.

## Headline findings

1. **Online documentation of named shore marks on Pico is thin.** I found no angling forum, blog, Fishbrain/Fishing Points listing or YouTube report that names specific Pico shore marks. Searches in Portuguese and English returned charter-boat marketing, news of missing anglers, and official documents. The list below is therefore built mostly from infrastructure (OSM harbours, piers, slipways; the official bathing-water list; the Instituto Hidrografico pilot text) and only a handful of entries have grade A.
2. **Grade A entries**: three OSM `leisure=fishing` nodes near Sao Caetano (Coxos, Pesqueiro Pedro, Pontinha), Manhenha (2024 missing shore angler), Sao Miguel Arcanjo (2021 angler death), and the Madalena shore (the DOP report on the Ilheus da Madalena site lists "pesca a cana na zona costeira" by recreational fishers from Madalena; Portaria 53/2016 reportedly keeps a shore-fishing exception there, snippet only).
3. **Exposure and facing can be computed automatically** from the OSM coastline (fetch by bearing). Results are in the main table and they differ from the app's current labels in places: Madalena faces NW in open-water terms (due W is a 6 to 8 km fetch to Faial; open ocean lies NW-NE and SSW-WSW), Lajes faces SW, Sao Roque NNE, Ponta da Ilha is open through 190 degrees from ENE to WSW.
4. **Bathymetry lookup works at 1 km, is patchy at 300 m, and fails at 100 m.** Details in the bathymetry section.
5. **Legal**: shore angling needs no licence; 50 m exclusion around bathing spots 1 June to 30 September; a special regime at the Ilheus da Madalena off Madalena; three marine resource-management areas in the Pico Nature Park. The 2024/2026 offshore marine park expansion (RAMPA) does not appear to add coastal no-take zones on Pico yet. I could not fetch the full text of several regional instruments because the Azores government sites return HTTP 403 to automated clients.

## Candidate names from the brief: confirm, correct or drop

| Lead | Outcome | Basis |
|---|---|---|
| Areia Larga | Confirmed as a cove and old-port area just S of Madalena | [V] IH pilot text in DOP report; OSM place node |
| Criacao Velha / Pocinho | Confirmed, but they are two places: Criacao Velha bathing area (Laja das Rosas) and Pocinho cove 1 km further S (parish of Candelaria per tourism page) | [V] bathing-water bulletin 2024; OSM; IH pilot text |
| Porto do Calhau | Confirmed, west coast near Monte, between Pocinho and Candelaria. Note there is a second Porto do Calhau at Piedade | [V] IH pilot text; OSM dock node and leading lights |
| Candelaria | Parish only. No named shore mark verified; its coast is covered by Porto do Calhau and Pocinho. "Ponta do Hospital / Ponta do Espartel" is the cape S of it | [V] IH pilot text. Port names for Candelaria not found |
| Sao Mateus | Confirmed fishing port plus lighthouse point | [V] OSM seamark harbour category=fishing; bathing-water list |
| Sao Caetano | Confirmed: fishing port at Prainha do Galeao; three OSM fishing-spot nodes just W of it | [V] OSM; dive portal |
| Sao Joao | Partly confirmed: bathing areas at Ponta do Admoiro and Arinhas. A named "porto" for Sao Joao was not located | [V] OSM; bathing-water list (Admoiro) |
| Santa Cruz das Ribeiras | Confirmed port with breakwater and light | [V] OSM; bathing-water list |
| Manhenha | Confirmed fishing port; documented shore angling | [V] OSM; CM Jornal Jan 2024 |
| Calhau (Piedade) | Confirmed port with breakwater and slipway, on the NE coast | [V] OSM; bathing-water list |
| Santo Amaro | Confirmed port with launch ramp | [V] OSM harbour node; Sao Roque council trail page |
| Prainha | Confirmed "porto tradicional" with pier and light | [V] OSM; council trail page |
| Santo Antonio | Confirmed: Furna de Santo Antonio pools and slipway | [V] OSM; bathing-water list; dive portal |
| Lajido / Santa Luzia | Confirmed: Lajido, Arcos and Cabrito are three adjacent shore places in Santa Luzia parish | [V] OSM; tourism page |
| Cachorro | Confirmed: lava-arch shore with old cask ramp | [V] dive portal; tourism page |
| Bandeiras | Parish only; its shore places are Cais do Mourato and Cachorro | [V] tourism page; OSM |

Added beyond the brief: Formosinha, Barca, Cais do Mourato, Ponta de Sao Mateus, Coxos, Pesqueiro Pedro, Pontinha, Fonte (Silveira), Ponta do Castelete, Ponta do Arrife, Poca das Mujas, Portinho da Feteira, Baia de Engrade, Porto da Baixa (Ribeirinha), Caisinho (Terra Alta), Baia de Canas, Ponta do Misterio, Sao Miguel Arcanjo, Pocas de Sao Roque, Cais do Pico old quay.

Not confirmed and left out: "Porto da Aguada", "Cais do Galego" (OSM has it only as a locality near Piedade), bathing waters Pontes, Verdoso, Caminho de Baixo (Santa Barbara), Baixas and Poca Branca (on the official list but I did not locate coordinates).

## Table 1: computed geography (all [I] unless stated)

Method. Coordinates are from OSM objects as listed [V]. "Facing" is the mean bearing of open water around the point, weighted by fetch capped at 40 km, using the OSM coastline of Pico, Faial and Sao Jorge and rays every 5 degrees. "Open-ocean sector" lists bearings with at least 40 km of open water; "channel sector" lists bearings with 2 to 40 km (water bounded by Faial, Sao Jorge or Pico's own coast). Depths come from the EMODnet DTM (`depth_sample`) at 100, 300 and 1000 m beyond the shoreline along the facing bearing, with GEBCO 2020 (OpenTopoData) for comparison. Distances to the 20, 50 and 100 m depths are read from a 2 km EMODnet `depth_profile` (1000 samples). A `?` after an EMODnet value means the cell is interpolated, GEBCO-filled, or has no survey source, so it is low confidence. Negative numbers are depth below datum; zero or positive values are land or coast-height cells, not real depths.

| id | Spot | lat, lon | coord source | facing (deg) | open-ocean sector (fetch >= 40 km) | channel / fetch-limited sector (2-40 km) | profile bearing | EMODnet depth m @100 / @300 / @1000 m | GEBCO2020 @100/@300/@1000 | dist. to 20 / 50 / 100 m depth (m) | EMODnet source cells |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | **WEST / FAIAL CHANNEL** | | | | | | | | | | |
| formosinha | Porto da Formosinha (Toledos) | 38.55183, -28.50444 | OSM way 1285294388 | 355 (N) | 305-035 (NW-NE) | 040-060 (NE-ENE), 270-300 (W-WNW) | 355 | -8 / -13 / -21? | 4 / -6 / -20 | 785 / 1896 / >2000 | hi057_1983, GEBCO2024(i) |
| barca | Barca / Ponta da Laje (Porto da Barca) | 38.54345, -28.52087 | OSM way 681376175 (swimming area 'Barca') | 329 (NNW) | 235-250 (SW-WSW), 315-030 (NW-NNE) | 255-310 (WSW-NW) | 330 | 0? / -6 / -25? | 4 / -5 / -23 | 677 / >2000 / >2000 | None, hi057_1983, hi057_1983(i) |
| madalena | Madalena harbour breakwater (molhe) | 38.53622, -28.53302 | OSM node 1577208498 (breakwater-head light) | 322 (NW) | 210-250 (SSW-WSW), 320-035 (NW-NE) | 040-045 (NE-NE), 255-260 (WSW-W), 270-315 (W-NW) | 320 | -10 / -12 / -23? | -6 / -12 / -31 | 735 / 1890 / >2000 | hi2102_2009_12, hi2102_2009_12(i) |
| areialarga | Areia Larga cove / old port | 38.52724, -28.53463 | OSM place node 'Areia Larga' | 265 (W) | 245-260 (WSW-W) | 265-315 (W-NW) | 265 | -3 / -7 / -20 | 2 / -6 / -21 | 881 / 1758 / >2000 | hi057_1983 |
| criacaovelha | Criacao Velha - Laja das Rosas | 38.50496, -28.54133 | OSM way 494673055 ('Piscina das Rosas') | 250 (WSW) | 180-275 (S-W), 335-355 (NNW-N) | 280-330 (W-NNW) | 250 | 2? / -12? / -62? | 9 / -2 / -57 | 310 / 773 / 1610 | Coastal_heights_2024(i), GEBCO2024(i) |
| pocinho | Pocinho (Candelaria/Monte) | 38.49570, -28.53928 | OSM node 5979720174 | 273 (W) | 225-275 (SW-W), 335-345 (NNW-NNW) | 280-330 (W-NNW) | 275 | 4? / -6? / -65? | 16 / 3 / -58 | 464 / 815 / 1427 | None, GEBCO2024(i) |
| calhau_w | Porto do Calhau (Monte/Candelaria, west) | 38.48631, -28.53905 | OSM node 5979720178 + light 1577208929 | 233 (SW) | 160-280 (SSE-W), 340-345 (NNW-NNW) | 285-335 (WNW-NNW) | 235 | 2? / -22? / -280 | 1 / -28 / -174 | 202 / 308 / 414 | Coastal_heights_2024(i), GEBCO2024(i), hi-dop_2010 |
| | **SOUTH** | | | | | | | | | | |
| saomateus | Sao Mateus fishing port | 38.43080, -28.46183 | OSM node 3691921561 (seamark harbour, fishing) | 207 (SSW) | 130-285 (SE-WNW) | - | 205 | 2? / -99? / -453 | -73 / -203 / -401 | 258 / 258 / 490 | Coastal_heights_2024(i), Azores_2015_6(i), Azores_2015_6 |
| ptasaomateus | Ponta de Sao Mateus (lighthouse) | 38.42283, -28.44840 | OSM way 592132104 | 217 (SW) | 140-290 (SE-WNW) | 295-300 (WNW-WNW) | 215 | 2? / -50? / -394? | -37 / -108 / -363 | 180 / 306 / 450 | Coastal_heights_2024(i), GEBCO2024(i), Azores_2015_6(i) |
| coxos | Coxos (OSM leisure=fishing) | 38.42019, -28.43587 | OSM node 13148512571 | 183 (S) | 105-265 (ESE-W) | 085-100 (E-E) | 185 | 1? / -184 / -420 | -189 / -242 / -416 | 132 / 132 / 244 | None, Azores_2015_6 |
| pesqpedro | Pesqueiro Pedro (OSM leisure=fishing) | 38.42043, -28.43400 | OSM node 13148512572 | 183 (S) | 105-265 (ESE-W) | 090-100 (E-E) | 185 | 2? / -98 / -449? | -188 / -254 / -408 | 174 / 174 / 356 | Coastal_heights_2024(i), Azores_2015_6, Azores_2015_6(i) |
| pontinha | Pontinha (OSM leisure=fishing) | 38.42152, -28.42677 | OSM node 13148512573 | 179 (S) | 105-255 (ESE-WSW) | 080-100 (E-E) | 180 | 2? / -99 / -462 | -9 / -37 / -513 | 174 / 174 / 396 | Coastal_heights_2024(i), Azores_2015_6 |
| saocaetano | Sao Caetano port / Prainha do Galeao | 38.42631, -28.42111 | OSM node 4440543145 (harbour) | 162 (SSE) | 110-215 (ESE-SW) | 100-105 (E-ESE) | 160 | 0? / 0? / -317? | 11 / -14 / -211 | 320 / 320 / 320 | None, Azores_2015_6(i) |
| admoiro | Ponta do Admoiro (Sao Joao) | 38.41421, -28.34713 | OSM node 5613502207 | 187 (S) | 115-260 (ESE-W) | 105-110 (ESE-ESE) | 185 | 2? / -99 / -401? | -6 / -42 / -634 | 184 / 184 / 294 | Coastal_heights_2024(i), Azores_2015_6, Azores_2015_6(i) |
| arinhas | Sao Joao - Arinhas | 38.41351, -28.32828 | OSM node 11105720289 | 190 (S) | 115-265 (ESE-W) | 110 | 190 | 3? / -100 / -383? | -12 / -51 / -432 | 222 / 222 / 334 | None, Azores_2015_6, Azores_2015_6(i) |
| fonte | Fonte (Silveira) bathing area | 38.41236, -28.28899 | OSM node 9835266224 | 194 (SSW) | 130-260 (SE-W) | 100-125 (E-SE) | 195 | 1? / -100 / -432 | -119 / -153 / -353 | 100 / 100 / 214 | None, Azores_2015_6 |
| lajes | Lajes do Pico harbour breakwater | 38.39780, -28.25637 | OSM way 682098868 (breakwater) | 228 (SW) | 175-275 (S-W) | 280-320 (W-NW) | 230 | 0? / -8 / -100 | -1 / -9 / -70 | 442 / 843 / 1013 | None, hi2102_2009_11, Azores_2015_6 |
| castelete | Ponta do Castelete (Lajes) | 38.38690, -28.25210 | OSM node 6688550810 | 201 (SSW) | 115-280 (ESE-W) | 285-335 (WNW-NNW) | 200 | 0? / -16? / -158? | 1 / -25 / -114 | 384 / 400 / 637 | None, GEBCO2024(i) |
| arrife | Ponta do Arrife | 38.38717, -28.22306 | OSM node 6688550808 | 159 (SSE) | 085-235 (E-SW) | 075-080 (ENE-E) | 160 | 0? / -31? / -100 | 40 / 1 / -310 | 266 / 384 / 973 | None, GEBCO2024(i), Azores_2015_6 |
| ribeiras | Santa Cruz das Ribeiras port | 38.40564, -28.18676 | OSM way 714021722 (breakwater) + light 1577209502 | 141 (SE) | 095-190 (E-S) | 085-090 (E-E) | 140 | 1? / -76 / -361? | -23 / -84 / -401 | 176 / 282 / 320 | None, hi2102_2009_13, Azores_2015_6(i) |
| mujas | Poca das Mujas (Calheta de Nesquim) | 38.40000, -28.08272 | OSM node 5922305186 | 171 (S) | 080-260 (E-W) | 265 | 170 | -109? / -93 / -536 | -163 / -215 / -348 | 80 / 80 / 80 | Azores_2015_6(i), Azores_2015_6 |
| calheta | Calheta de Nesquim port | 38.40257, -28.07973 | OSM way 1297687722 (breakwater) | 150 (SSE) | 095-205 (E-SSW) | - | 150 | 2? / -107? / -363 | -30 / -146 / -301 | 244 / 244 / 244 | None, GEBCO2024(i), Azores_2015_6 |
| feteira | Portinho da Feteira (Calheta de Nesquim) | 38.40283, -28.06860 | OSM way 683786181 (pier) | 165 (SSE) | 080-250 (E-WSW) | - | 165 | 0? / 2? / -407? | -265 / -276 / -280 | 302 / 302 / 416 | None, Coastal_heights_2024(i), Azores_2015_6(i) |
| | **EAST TIP** | | | | | | | | | | |
| manhenha | Manhenha fishing port | 38.41025, -28.03748 | OSM node 4440804619 | 160 (SSE) | 080-240 (E-WSW) | - | 160 | 1? / 0? / -72 | -7 / -40 / -86 | 452 / 689 / 1159 | None, Azores_2015_6 |
| pontadailha | Ponta da Ilha (lighthouse) | 38.41251, -28.03047 | OSM node 614987101 | 147 (SSE) | 060-245 (ENE-WSW) | 040-055 (NE-NE) | 145 | 0? / -21? / -145 | -73 / -75 / -152 | 288 / 374 / 679 | None, GEBCO2024(i), Azores_2015_6 |
| engrade | Baia de Engrade (Piedade, NE of Ponta da Ilha) | 38.42210, -28.03011 | OSM node 3714211606 | 88 (E) | 065-165 (ENE-SSE) | 335-060 (NNW-ENE) | 90 | 2? / -12? / -81 | -37 / -47 / -142 | 342 / 517 / 1213 | Coastal_heights_2024(i), GEBCO2024(i), Azores_2015_6 |
| | **NORTH / SAO JORGE CHANNEL (listed east to west)** | | | | | | | | | | |
| calhau_e | Porto do Calhau (Piedade) | 38.43930, -28.05579 | OSM way 1317460671 (breakwater) | 75 (ENE) | 070-120 (ENE-ESE) | 005-065 (N-ENE) | 75 | 0? / -58? / -43 | 60 / 37 / -43 | 228 / 228 / 1397 | None, GEBCO2024(i), Azores_2015_6 |
| baixa | Porto da Baixa (Ribeirinha) | 38.44560, -28.07869 | OSM way 683786711 (pier) | 357 (N) | 070-080 (ENE-E), 295-325 (WNW-NW) | 280-290 (W-WNW), 330-065 (NNW-ENE) | 355 | -1? / -5? / -60 | 6 / -49 / -254 | 328 / 551 / 1217 | None, GEBCO2024(i), Azores_2015_6 |
| caisinho | Caisinho / Terra Alta (Santo Amaro) | 38.45653, -28.15181 | OSM way 1313302160 | 12 (NNE) | 075-090 (ENE-E), 305-335 (NW-NNW) | 280-300 (W-WNW), 340-070 (NNW-ENE) | 10 | 2? / -23? / -323 | -39 / -133 / -386 | 182 / 294 / 406 | Coastal_heights_2024(i), GEBCO2024(i), Azores_2015_6 |
| santoamaro | Santo Amaro port | 38.45662, -28.16710 | OSM node 4440989977 (harbour) | 5 (N) | 310-335 (NW-NNW) | 300-305 (WNW-NW), 340-075 (NNW-ENE) | 5 | 2? / -77? / -377? | -31 / -94 / -309 | 270 / 270 / 380 | Coastal_heights_2024(i), GEBCO2024(i), Azores_2015_6(i) |
| prainha | Prainha port (Prainha do Norte) | 38.47224, -28.19952 | OSM way 1425387442 (pier) | 58 (ENE) | 080-100 (E-E) | 105-120 (ESE-ESE), 355-075 (N-ENE) | 60 | 0? / -3? / -140? | 30 / 12 / -101 | 458 / 559 / 761 | None, GEBCO2024(i) |
| canas | Baia de Canas | 38.48964, -28.23534 | OSM way 1104288825 | 55 (NE) | 085-105 (E-ESE), 345 | 110-115 (ESE-ESE), 350-080 (N-E) | 55 | 2? / -10? / -93? | 36 / 5 / -121 | 376 / 569 / 1165 | Coastal_heights_2024(i), GEBCO2024(i) |
| misterio | Ponta do Misterio | 38.49830, -28.24208 | OSM node 6688540277 | 23 (NNE) | 085-110 (E-ESE), 300-345 (WNW-NNW) | 115-125 (ESE-SE), 295, 350-080 (N-E) | 25 | 2? / -63? / -376? | -3 / -52 / -387 | 162 / 284 / 529 | Coastal_heights_2024(i), GEBCO2024(i), Azores_2015_6(i) |
| sma | Sao Miguel Arcanjo shore | 38.50700, -28.28900 | approx: shore north of OSM place node 'Sao Miguel Arcanjo' (38.50333,-28.28992) | 17 (NNE) | 090, 315-350 (NW-N) | 355-085 (N-E) | 15 | -4? / -30? / -92? | 54 / 32 / -125 | 262 / 490 / 1065 | GEBCO2024(i) |
| pocassr | Pocas de Sao Roque | 38.51919, -28.30481 | OSM way 1426714236 | 36 (NE) | 090-110 (E-ESE), 320-355 (NW-N) | 000-085 (N-E), 115-135 (ESE-SE) | 35 | 0? / -25? / -166? | -34 / -70 / -225 | 244 / 396 / 753 | None, GEBCO2024(i), Azores_2015_6(i) |
| caisdopico | Cais do Pico old quay (Porto Velho) | 38.52714, -28.31907 | OSM node 5626570343 | 46 (NE) | 090-110 (E-ESE), 335-000 (NNW-N) | 005-085 (N-E), 115 | 45 | -7 / -40 / -313? | -32 / -77 / -358 | 162 / 306 / 462 | hi2102_2009_14, Azores_2015_6(i) |
| saoroque | Sao Roque commercial port breakwater | 38.53147, -28.32136 | OSM way 725143852 (breakwater) | 27 (NNE) | 090-105 (E-ESE), 310-000 (NW-N) | 005-085 (N-E), 115-130 (ESE-SE) | 25 | -112? / -154? / -407? | -68 / -128 / -438 | 48 / 48 / 48 | hi2102_2009_14(i), Azores_2015_6(i) |
| santoantonio | Santo Antonio - Furna | 38.53539, -28.33552 | OSM node 5626570084 (slipway) | 29 (NNE) | 345-000 (NNW-N) | 005-080 (N-E) | 30 | 2? / -5? / -222 | 15 / -5 / -201 | 366 / 388 / 771 | None, GEBCO2024(i), hi2102_2009_8 |
| cabrito | Cabrito (Santa Luzia) | 38.55745, -28.38814 | OSM node 6848482483 (slipway) | 19 (NNE) | 090-110 (E-ESE), 300-015 (WNW-NNE) | 020-085 (NNE-E) | 20 | 2? / -32? / -348 | -40 / -79 / -338 | 218 / 336 / 412 | None, GEBCO2024(i), 201907_Lisboa-Acores |
| arcos | Arcos (Santa Luzia) | 38.56023, -28.40901 | OSM way 621266888 | 3 (N) | 090-095 (E-E), 290-020 (WNW-NNE) | 025-085 (NNE-E), 285 | 5 | 2? / -7? / -84? | 8 / -2 / -62 | 346 / 679 / 1123 | Coastal_heights_2024(i), GEBCO2024(i) |
| lajido | Lajido (Santa Luzia) | 38.55859, -28.42759 | OSM node 6864119798 ('Portinho do Lajido') | 351 (N) | 295-020 (WNW-NNE) | 025-075 (NNE-ENE), 270-290 (W-WNW) | 350 | -3? / -17? / -84? | -13 / -31 / -87 | 310 / 535 / 1097 | GEBCO2024(i) |
| cachorro | Cachorro (Bandeiras) | 38.55700, -28.44650 | approx: shore north of OSM place node 'Cachorro' (38.55570,-28.44646) | 346 (NNW) | 295-025 (WNW-NNE) | 030-055 (NNE-NE), 280-290 (W-WNW) | 345 | -10 / -27 / -56 | 2 / -16 / -55 | 240 / 815 / 1616 | hi0906_1987 |
| mourato | Cais do Mourato (Bandeiras) | 38.55871, -28.48160 | OSM way 1426714237 | 351 (N) | 300-030 (WNW-NNE) | 035-065 (NE-ENE), 260-295 (W-WNW) | 350 | 0? / -2? / -35? | 8 / 1 / -36 | 635 / 1309 / >2000 | None, GEBCO2024(i) |

Reading the depth columns. When the three "distance to depth" numbers are equal (for example Calheta 244/244/244), the grid jumps straight from a coast cell to deep multibeam data, so the true nearshore profile is unknown and only "deep water within roughly that distance" can be concluded. The Sao Roque breakwater value of -112 m at 100 m is from an interpolated cell and should be checked against a chart before use.

## Table 2: which spots are in the lee for each wind or swell direction ([I], from the same fetch data)

Geometry only. Swell refracts around headlands and wraps into "sheltered" coasts, so treat this as a first filter, not a safety assessment.

| Wind / swell FROM | Lee spots (max fetch < 2 km within +/-25 deg) | Fetch-limited (max fetch 2-40 km: channel chop only) |
|---|---|---|
| N | areialarga, saomateus, ptasaomateus, coxos, pesqpedro, pontinha, saocaetano, admoiro, arinhas, fonte, lajes, arrife, ribeiras, calheta, mujas, feteira, manhenha, pontadailha | castelete, engrade, calhau_e, baixa, prainha |
| NE | areialarga, criacaovelha, pocinho, calhau_w, saomateus, ptasaomateus, coxos, pesqpedro, pontinha, saocaetano, admoiro, arinhas, fonte, lajes, castelete, arrife, ribeiras, calheta, mujas, feteira, manhenha | caisinho, santoamaro, prainha, canas, misterio, sma, pocassr, caisdopico, saoroque, santoantonio, cabrito |
| E | madalena, areialarga, barca, criacaovelha, pocinho, calhau_w, saomateus, ptasaomateus, lajes, cachorro, formosinha | fonte, santoamaro, santoantonio, lajido, mourato |
| SE | madalena, areialarga, barca, criacaovelha, pocinho, lajes, baixa, caisinho, santoamaro, sma, santoantonio, arcos, lajido, cachorro, mourato, formosinha | prainha, canas, saoroque |
| S | madalena, areialarga, barca, pocinho, calhau_e, baixa, caisinho, santoamaro, prainha, canas, misterio, sma, pocassr, caisdopico, saoroque, santoantonio, cabrito, arcos, lajido, cachorro, mourato, formosinha |  |
| SW | ribeiras, engrade, calhau_e, baixa, caisinho, santoamaro, prainha, canas, misterio, sma, pocassr, caisdopico, saoroque, santoantonio, cabrito, arcos, lajido, cachorro, mourato, formosinha |  |
| W | saocaetano, arrife, ribeiras, calheta, manhenha, engrade, calhau_e, santoamaro, prainha, canas, sma, pocassr, caisdopico, saoroque, santoantonio, cabrito | caisinho, misterio, mourato, formosinha |
| NW | saomateus, coxos, pesqpedro, pontinha, saocaetano, admoiro, arinhas, fonte, arrife, ribeiras, calheta, mujas, feteira, manhenha, pontadailha, calhau_e, prainha, canas, santoantonio | areialarga, lajes, castelete, engrade |

Practical reading: with the prevailing NW swell the south coast from Sao Mateus to Manhenha is the lee, plus Prainha, Baia de Canas and Santo Antonio on the north coast, which the geometry shows are shadowed from the NW. With S or SW weather the whole north coast is the lee. With E weather the west coast (Madalena to Porto do Calhau) is the lee. With N or NE the south coast is the lee. There is no direction that closes every coast.

## Table 3: per-spot description, access, restrictions, species

Species entries are anecdotal [A] unless marked otherwise. Portuguese names: sargo = white seabream (Diplodus sargus), veja = parrotfish (Sparisoma cretense), garoupa = comber/grouper (Serranus atricauda), chicharro = blue jack mackerel (Trachurus picturatus), bicuda = yellowmouth barracuda (Sphyraena viridensis), enchareu = white trevally (Pseudocaranx dentex), lirio = amberjack/almaco jack (Seriola spp.), tainha = grey mullet, salema = Sarpa salpa, mero = dusky grouper (Epinephelus marginatus).

| id | Grade | Type and shore | Seabed and nearby features | Access and safety | Restrictions specific to the spot | Species associated by sources [A] | Sources |
|---|---|---|---|---|---|---|---|
| formosinha | B | Wide stone ramp (old wine-cask ramp), open rocky shore, Toledos [V] | Arcos da Formosinha reef 150 m offshore: top at 8 m, max 18 m, weak currents [V dive portal]. Very gently shelving: 50 m depth about 1.9 km out [I] | Road access; swimming "depends on sea state", no lifeguard noted [V tourism page]. Open NW to NE | Possibly inside the limpet no-take stretch (Ponta do Cachorro to Pe do Monte) [V, 1993 rule as cited in DOP report] | Enchareu schools and round stingrays near 18 m; wrasses, morays | S1, S4, S9 |
| barca | B | Small cove with ramp ("Porto da Barca") behind Ponta da Laje, 0.7 M N of Madalena; breakwaters and sea pools [V] | Low black rock; "frequent breaking along the shore" from the Baixio Grande shoal [V IH text]. 20 m depth about 680 m out [I] | Town-edge access. Official bathing water "Barca" (PTAJ3X) | 50 m bathing rule 1 Jun to 30 Sep. Check whether inside Ilheus da Madalena regulated area (boundary not retrieved) | none found | S1, S3, S6 |
| madalena | A | Harbour breakwater rooted NE running SW, quay on inner face, large slipway; ferries and fishing boats [V IH text]. Old port (small quay, slipway) 400 m S in a cove N of Ponta do Areeiro [V] | Shallow, foul, rocky ground under 10 m between shore and the islets 0.5 M off; "frequently swept by swell". 20 m about 735 m out, 50 m about 1.9 km (IH 2009 survey cells) [V/I]. Tidal stream in channel: flood NNE, ebb SSW, mean 1 to 2 kn [V]. Reefs offshore: Baixa do Norte (17.5 m, about 0.9 M from Ilheu em Pe), Baixa da Barca (21.5 m, about 2 M N), Baixa do Sul (7 m) [V]. Lights: breakwater head Fl(3)R 8s 10M, plus Fl G 5M [V OSM/NGA] | Easy, urban. Described as the stretch of Pico most exposed to the dominant NW swell [V DOP report]. Class C port [S] | Portaria 53/2016: Ilheus da Madalena area closed to commercial and recreational fishing except shore fishing between two defined vertices (D-E) and live-bait capture [S: vertex coordinates not retrieved]. Baixa da Barca: all fishing banned [S] (offshore, not reachable from shore). Natura 2000 SAC Ilheus da Madalena. Limpet no-take zone. Official bathing water "Madalena" (PTAV7E): 50 m rule in season. Boat-based recreational fishing not allowed inside class A-C ports [V art. 20, proposal text] | [V DOP report, section on Ilheus da Madalena site] recreational fishers from Madalena use the area for rod fishing from the coast ("pesca a cana na zona costeira"), boat trolling for serra/bonito (Sarda sarda), bicuda and cavala, and handlining for garoupa, mero and pargo; the islets are noted as a breeding area for peixe-porco (grey triggerfish). Faial-side text adds sargos, vejas, chicharro for shore lines. Dive records nearby: bicuda, enchareu | S1, S2, S6, S9, S11 |
| areialarga | B | Small cove S of Ponta do Areeiro with stairs at the old harbour; light on Ponta da Areia Larga [V] | "Small but frequently sheltered from bad weather" by the rocky shallows running from Ponta do Areeiro to the islets; good anchorage [V IH text]. -3 / -7 / -20 m at 100 / 300 / 1000 m (IH 1983 survey cells) | Easy; end of the Criacao Velha vineyard trail [V tourism page] | As Madalena: check whether inside the Ilheus da Madalena regulated area | none found | S1, S4 |
| criacaovelha | B | Lava platform with enclosed natural pool and open-sea entry (Laja das Rosas) [V] | Low black cliff coast; 50 m contour about 0.3 M off, "very steep inside it, rocks frequent at the shore" [V IH text] | Bathing facilities, bar. Official bathing water "Criacao Velha" (PTAQ8U) | 50 m bathing rule in season. Limpet no-take stretch | none found | S1, S3, S4 |
| pocinho | B | Small cove with rolled-pebble beach and small quay [V IH text] | Arcos do Pocinho: lava flow sloping to 23 m, starts about 9 m, arches, weak currents [V dive portal]. Ponta do Poio headland to the N | Calm, mostly locals [V tourism page]. Official bathing water "Pocinho" (PTAV2D) | 50 m bathing rule in season. Limpet reserve named "Portinho do Pocinho / Central de Ondas do Cachorro" [S] | Bicuda and enchareu schools; chromis | S1, S3, S4, S9 |
| calhau_w | B | Small port: wall on S side, small quay, slipway, cargo gear [V IH text]; leading lights Oc R 6M [V OSM/NGA] | Steeper than further N: 50 m about 310 m out, 100 m about 415 m, -280 m at 1 km (2010 survey cell) [I] | Road to quay. Open SSE to W | none found | none found | S1, S6 |
| saomateus | B | Fishing port [V OSM seamark]; bathing area | Very steep: 100 m depth about 490 m out, -453 m at 1 km (multibeam) [I] | Village port. Open SE to WNW, no channel shelter. Official bathing water "Sao Mateus" (PTAT2K) | 50 m bathing rule in season | none found | S3, S6 |
| ptasaomateus | C | Rocky point with lighthouse (Fl W 5s 13M) [V OSM/NGA] | 100 m depth about 450 m out [I] | Not assessed | Vineyard-landscape protected area on land (Sao Mateus / Sao Caetano) | none found | S6 |
| coxos, pesqpedro, pontinha | A | Three points tagged `leisure=fishing`, `access=yes` in OSM (added Sept 2025). "Pesqueiro" means fishing mark. The only explicit angling-spot tags on the island [V] | Deepest water close in of any listed spots: about -98 to -184 m at 300 m, -420 to -460 m at 1 km (multibeam) [I] | Not described in any source. Open ESE to W; fully exposed to S and SW swell | Vineyard-landscape protected area on land | none found | S6 |
| saocaetano | B | Fishing port at Prainha do Galeao; light "Cabos Galeao" Fl(2)R 8s 9M [V] | Dive "Corais de Sao Caetano": entry from the fishing port, 3 m on sand and pebble, then a wall from 15 m down to 60 m with black coral; weak currents [V dive portal] | Shore dive site suitable for night dives. Official bathing water "Prainha do Galeao" (PTAE2F) | 50 m bathing rule in season. Mero may not be taken by spearfishing [V] | Morays (three species), mero, barred hogfish, bicuda schools | S3, S6, S9 |
| admoiro | B | Bathing area on lava shore, Sao Joao [V] | 100 m depth about 290 m out [I] | "Sheltered, less frequented" [V tourism page]. Official bathing water "Admoiro" (PTAW8V) | 50 m bathing rule in season. Misterio de Sao Joao protected area nearby (land) | none found | S3, S4, S6 |
| arinhas | B | "Zona Balnear das Arinhas", Sao Joao [V OSM] | 100 m depth about 330 m out [I] | Not described | Likely bathing use in season | none found | S6 |
| fonte | B | Bathing area "Fonte", Silveira [V] | 100 m depth about 210 m out [I] | Official bathing water "Fonte" (PTAV8X) | 50 m bathing rule in season | none found | S3, S6 |
| lajes | B | Harbour with breakwater, slipway, leading lights Oc R 7M; natural pool by the village [V] | Shallow lava shelf: -8 m at 300 m (IH 2009 survey cell), 20 m about 440 m out, 100 m about 1 km [I] | Easy, urban. Whale-watching boat base. Two official bathing waters: "Clube Naval das Lajes" (PTAW7H), "Lajes (Mare)" (PTAD7Q) | Inside Area Protegida de Gestao de Recursos do Porto das Lajes (1.53 km2) and SAC/SPA Lajes do Pico [V list]; angling rules for it not retrieved. 50 m bathing rule in season | none found | S3, S5, S6 |
| castelete, arrife | C | Rocky capes S and SE of Lajes; Arrife has a viewpoint [V OSM] | Castelete 20 m about 385 m out; Arrife -100 m at 1 km [I] | Not assessed. Fully open S | Castelete likely inside the Porto das Lajes area | none found | S6 |
| ribeiras | B | Port with breakwater; light Fl R 3s; municipal sea pool [V] | Steep: -76 m at 300 m (IH 2009 survey cell), -361 m at 1 km [I] | Village port. Open E to S. Official bathing water "Santa Cruz das Ribeiras" (PTAE7J) | 50 m bathing rule in season | none found | S3, S6 |
| mujas | B | Natural rock pool area in vegetation, Calheta de Nesquim [V] | Deep close in (grid gap near shore) [I] | "Most isolated site": no toilets, showers, shade or lifeguard [V tourism page]. Official bathing water "Poca das Mujas" (PTAN8L) | 50 m bathing rule in season | none found | S3, S4, S6 |
| calheta | B | Small port with breakwaters and slipway [V OSM] | Deep close in: -363 m at 1 km (multibeam) [I] | Village port. Open E to SSW | none found | none found | S6 |
| feteira | B | Small pier with picnic area "Zona de Lazer do Portinho" [V OSM] | -407 m at 1 km [I] | Not described | none found | none found | S6 |
| manhenha | A | Fishing port (slipway, dock) and sea pool [V OSM] | Shelf wider than the south coast: 20 m about 450 m out, 100 m about 1.2 km, -72 m at 1 km (multibeam) [I] | Jan 2024: a 77-year-old went missing after leaving to shore-fish "na zona da Manhenha" [V CM Jornal]. Open E to WSW. Official bathing water "Manhenha" (PTAE7H) | Inside or beside Area Protegida de Gestao de Recursos da Ponta da Ilha (5.95 km2), SAC and SPA Ponta da Ilha [V list]; angling rules not retrieved. 50 m bathing rule in season | none found | S3, S5, S6, S7 |
| pontadailha | A (spearfishing) / C (angling) | Low lava point with major lighthouse [V OSM] | 20 m about 290 m out, 100 m about 680 m, -145 m at 1 km [I]. Open ocean through 190 degrees | Aug 2025: search for a recreational spearfisher missing at Ponta da Ilha [S, RR]. Treat as dangerous in any swell | As Manhenha | none found | S6, S8 |
| engrade | C | Bay N of the lighthouse on the east face [V OSM] | -81 m at 1 km [I] | Not assessed. Faces E; sheltered from W and SW | As Manhenha | none found | S6 |
| calhau_e | B | Small port with breakwater, slipway, enclosed basin; bathing area and restaurant [V OSM] | 20 m about 230 m out, 100 m about 1.4 km [I]. "Baixa do Calhau" seamount with top near 15 m is advertised as a north-coast dive [V commercial page; its position relative to this port is not verified] | Official bathing water "Calhau" (PTAE8T). Faces ENE; lee in S, SW, W | 50 m bathing rule in season | Dive page: reef fish, morays, occasional rays | S3, S6, S10 |
| baixa | B | Pier and bathing area, Ribeirinha [V OSM] | 50 m about 550 m out [I] | Official bathing water "Porto da Baixa" (PTAT8V) | 50 m bathing rule in season | none found | S3, S6 |
| caisinho | B | Small harbour-side bathing place with stairs, Terra Alta [V] | Steep: 100 m about 400 m out, -323 m at 1 km [I] | Official bathing water "Caisinho" (PTAD9N) | 50 m bathing rule in season | none found | S3, S4, S6 |
| santoamaro | B | Port with launch ramp; boat-building village, maritime museum [V council trail page] | Steep: 100 m about 380 m out, -377 m at 1 km [I] | Trail PR7 ends at the ramp; nearby coast is "lava platforms where waves break" and cliffs [V] | Shearwater nesting sites along the trail (quiet requested) | none found | S6, S12 |
| prainha | B | "Porto tradicional" with pier; light Fl R 4s 7M [V]. Baia da Areia just E was once a commercial port [V] | Shallow close in: -3 m at 300 m (low confidence), 100 m about 760 m out [I]. Dark-sand patches reported [V tourism page] | Geometry shows shelter from W and NW. Bathing water "Poca Branca" (PTAN7H) nearby | 50 m bathing rule in season near pools. Reserva Natural do Misterio da Prainha on land | none found | S3, S4, S6, S12 |
| canas | B/C | Small pebble beach reached by a short trail; charted anchorage [V] | 50 m about 570 m out [I] | Isolated; trail access [V] | none found | none found | S4, S6, S12 |
| misterio | C | Lava-delta point [V council trail page] | Steep: 100 m about 530 m out, -376 m at 1 km [I] | Rough lava; not assessed | Protected landscape (Ponta do Misterio vineyard area) on land | none found | S6, S12 |
| sma | A | Open rocky shore below Sao Miguel Arcanjo (coordinates approximate) | A press report placed the recovered angler 40 m from shore in 15 m of water [S, RR], which suggests deeper water close in than the grid shows (-4 / -30 m, GEBCO-filled) | Oct 2021: a 66-year-old left home at about 20:00 to fish in the Sao Miguel Arcanjo area, was reported missing and found dead two days later [V DN, Noticias ao Minuto]. Night fishing alone here has a documented fatality | none found | none found | S13 |
| pocassr | B | Wide lava platforms forming large pools; arches offshore [V] | Dive "Arcadas de Sao Roque": 3 m pools, wall to 12 m, arch rising nearly to the surface; average 18 m, max 25 m; weak currents; "quiet, sheltered area" [V dive portal] | Facilities; snorkelling. Official bathing water "Pocas de Sao Roque" (PTAL9T) | 50 m bathing rule in season | Large schools of bicuda; chromis | S3, S4, S9 |
| caisdopico | B | Old whaling-era quay and slipway on the village front; natural pool beside it; light Oc R 6M [V] | Very steep bay: -7 m at 100 m, -40 m at 300 m (IH 2009 survey cells), -313 m at 1 km [I] | Easy, urban. Official bathing water "Piscina do Cais" (PTAV2U) | 50 m bathing rule in season | none found | S3, S6 |
| saoroque | B | Commercial port breakwater, light Fl G [V OSM] | Deep water immediately outside; grid value at 100 m is unreliable [I] | Class B port [S]. Access to a commercial quay may be controlled (not verified) | Boat-based recreational fishing not allowed inside class A-C ports [V art. 20, proposal text]. Port bay has a designated anchorage and fish-keep-cage zone [V Portos dos Acores regulation] | none found | S6, S11, S14 |
| santoantonio | B | Maintained sea pools, slipway, volcanic shore [V] | Dive "Furnas de Santo Antonio": 3 m start, wall leading out of the bay, large rocks at 10 to 15 m, max 17 m, arch 8 m wide; "sheltered and shallow", weak currents [V dive portal] | Family bathing site. Official bathing water "Furna de Santo Antonio" (PTAN3T). Geometry shows shelter from W and NW | 50 m bathing rule in season. Furnas de Santo Antonio is a nature reserve / species-management area / SPA (seabirds) [V list] | Veja, octopus, salema, ornate wrasse, morays | S3, S5, S6, S9 |
| cabrito, arcos, lajido | B | Three adjacent basalt-slab and rock-arch shores in Santa Luzia; slipway at Cabrito; "Portinho do Lajido" [V] | Arcos and Lajido shelve gently (50 m about 540 to 680 m out); Cabrito is steeper (100 m about 410 m out, -348 m at 1 km) [I] | Quiet; few visitors [V tourism page]. Official bathing water "Arcos" (PTAT7V) | 50 m bathing rule in season at Arcos. Vineyard-landscape protected area (north zone) on land | none found | S3, S4, S6 |
| cachorro | B | Lava arches and tunnels, boardwalk, tidal pool, old cask ramp [V] | Dive "Cachorro": gentle descent to 18 m, pebble bottom, maze of arches; weak currents (IH 1987 survey cells: -10 / -27 / -56 m) [V/I] | 5 min by car from Madalena; beginner and night-dive site [V] | Western end of the limpet no-take stretch (Ponta do Cachorro to Pe do Monte) [V as cited] | Veja, tainha (thick-lipped mullet), salema, octopus, black moray, wrasses | S2, S4, S9 |
| mourato | B | Hamlet with a small landing ramp "usable only in favourable weather" [V IH text]; bathing area | Very shallow: -2 m at 300 m, 20 m about 635 m out, 50 m about 1.3 km [I]. Low stony coast with frequent breaking from the Baixio Grande [V IH text] | Changing rooms, showers, parking. Official bathing water "Cais Mourato" (PTAX7C) | 50 m bathing rule in season | none found | S1, S3, S4 |

## Bathymetry lookup: how well it worked

What I ran. For all 43 points: three `depth_sample` calls (100, 300, 1000 m offshore along the computed facing bearing) and one `depth_profile` call (2 km line) against `https://rest.emodnet-bathymetry.eu`, plus the same 129 points against GEBCO 2020 through `https://api.opentopodata.org/v1/gebco2020`. No key needed and no failed calls, with a 0.25 s pause between calls.

Findings.

- **1 km offshore: works.** EMODnet and GEBCO agree in sign everywhere and within 30 percent of each other at 31 of 43 points; the worst disagreements are Porto da Baixa (-60 vs -254 m) and Ponta do Arrife (-100 vs -310 m). It cleanly separates three regimes: Faial channel shelf (about -20 to -35 m at 1 km from Mourato and Formosinha to Areia Larga), moderate (about -40 to -170 m: Criacao Velha, Pocinho, Lajes, Manhenha, Ponta da Ilha, Calhau (Piedade), Prainha, Baia de Canas, Pocas de Sao Roque, Arcos, Lajido, Cachorro), and steep island flank (-220 to -540 m at 1 km: the south coast from Porto do Calhau (W) round to Portinho da Feteira except Lajes, and on the north Caisinho, Santo Amaro, Ponta do Misterio, Cais do Pico, Sao Roque, Santo Antonio and Cabrito).
- **300 m offshore: works only where a harbour survey exists.** EMODnet returns the source dataset per cell. Cells from Instituto Hidrografico surveys (`hi2102_2009_*`, `hi057_1983`, `hi0906_1987`) at Madalena, Areia Larga, Barca, Formosinha, Cachorro, Lajes, Cais do Pico and Santa Cruz das Ribeiras look credible. Elsewhere the cell is GEBCO-filled and interpolated, or sits on the inshore edge of the 2015 multibeam composite where values cluster suspiciously at -99 to -100 m.
- **100 m offshore: does not work.** The grid cell is about 115 m (1/16 arc-minute), so the 100 m point usually falls in a coast or land cell and returns 0 to +4 m. Only five of 43 spots (Madalena, Areia Larga, Formosinha, Cachorro, Cais do Pico) returned a survey-backed depth there.
- **Better derived metric**: distance offshore to the 20, 50 and 100 m depths from the 2 km profile. It is robust to the bad first cell and matches the pilot text: the Instituto Hidrografico description puts the 50 m contour about 1 M (1.85 km) off the coast between Ponta da Areia Larga and Cais do Mourato, and my profile gives 1.9 km at Madalena and Formosinha and 1.3 km at Mourato; for Ponta do Hospital to Areia Larga the text says about 0.3 M (560 m) and the profiles give 310 to 815 m.
- **Use the `reference.identifier` and `interpolationType` fields as a per-spot confidence flag.** That is automatable.
- **Not tested**: Navionics or official ENC soundings, which would be the right source for the first 100 m. No open API for them.

Reusable scripts and raw results are in `scripts/` with a `spots_` prefix (`spots_spots.py`, `spots_fetch.py`, `spots_sectors.py`, `spots_bathy.py`, `spots_prof.py`; the raw `bathy.json` was not kept). The scratchpad is temporary.

## What can be automated and what needs local knowledge

| Attribute | Automatable from open data? | Notes |
|---|---|---|
| Coordinates | Yes | OSM harbours, piers, slipways, breakwaters, capes, bathing areas. Public Overpass mirrors were unreliable today (502/504 on two of three); cache the result |
| Facing bearing and exposure sectors | Yes | Ray-cast fetch against OSM coastline. About 10 s for 43 spots in plain Python |
| Lee/exposed for a forecast wind or swell direction | Yes, first-order | Does not model swell refraction or wrap |
| Steepness (distance to 20/50/100 m) | Yes | EMODnet profile; confidence from source field |
| Depth within casting range (first 100 m) | No | Below grid resolution |
| Type (harbour wall, pier, slipway, pool) | Partly | OSM tags give structure type; not whether it is fishable |
| Navigation lights | Yes | OSM seamarks (from NGA Pub. 113, 2011). These are not the quay floodlights that draw baitfish; those are not mapped |
| Official bathing waters (for the 50 m seasonal rule) | Yes | Annual regional list; 26 on Pico in 2024 |
| Protected-area polygons | Probably | Names and areas verified; I did not obtain polygons. Natura 2000 and WDPA downloads should have them (not tested) |
| Substrate at the mark (rock, sand, mixed) | No | Only where a dive description or the pilot text says so |
| Height above water, footing, walk-in difficulty | No | No source found for any spot |
| Night-fishing practicality, lighting, parking | No | Local knowledge |
| Species by spot | No | Only dive-site species lists and one general statement about the channel fishery |
| Stream mouths | Not checked | I did not query OSM waterways. Pico has little permanent surface drainage (general knowledge, not verified here) |
| Tidal streams | Partly | Verified only for the Faial channel (flood NNE, ebb SSW, 1 to 2 kn mean). Nothing fetched for the Sao Jorge channel |

## Legal and protected-area notes

Verified by reading the text:

- **No licence for shore angling.** Art. 28(1)(b) of DLR 9/2007/A, as reproduced in the regional government's amendment proposal, exempts "pesca ludica exercida de terra firme" from licensing. [V] S11
- **Bathing areas.** Art. 20(2): recreational fishing may not be practised within 50 m of places frequently used for bathing between 1 June and 30 September. The proposal leaves this paragraph unchanged, so it is original 2007 text. [V] S11
- **Ports.** Art. 20(1) in the proposal text bars recreational fishing from a boat or floating structure inside marinas, docks and class A, B and C ports. It does not by itself ban rod fishing from the walls. Whether Portos dos Acores or the Horta harbour master prohibit angling on particular quays was not found. [V for the article; open question for local rules]
- **Shore catch limit.** Art. 13(1): per angler per day from shore, 3.5 kg of fish under 40 cm plus 3 fish of 40 cm or more. [V] S11. Caveat: this is the proposal's republished text; I could not open the consolidated law, so the limits in force in 2026 may differ.
- **Marking.** Art. 18: fish of 25 cm or more must have the upper caudal lobe cut before leaving the spot. Sale is prohibited. [V] S11
- **Gear.** Hand line or rod; no leftovers of bait or groundbait to be abandoned on the shore or in port areas. [V] S11
- **Spearfishing** (for context): not within 300 m of or inside class A-C ports, 100 m for class D ports and "portinhos", 100 m of bathing places, never at night; mero may not be taken. [V] S11
- **Pico Nature Park marine areas**: Area Protegida de Gestao de Recursos do Canal Faial-Pico / Sector Pico (66.89 km2), Ponta da Ilha (5.95 km2), Porto das Lajes (1.53 km2); SACs Ilheus da Madalena, Lajes do Pico, Ponta da Ilha. [V] S5. These are "resource management" category, not strict reserves. Their specific angling rules were not retrieved; art. 21 of DLR 9/2007/A makes recreational fishing in classified areas subject to their own plans. The 2020 park management plan covers terrestrial areas only. [V]
- **Limpets**: Ilheus da Madalena and the adjacent coast from Ponta do Cachorro to Pe do Monte are a no-take zone for limpets under DRR 14/93/A, as cited in the DOP report. [V as cited; current status not checked]

Snippet only, full text not retrieved (official sites returned HTTP 403):

- **Portaria 53/2016 of 21 June** regulates fishing in three areas of the Faial-Pico channel: Monte da Guia (Faial), Ilheus da Madalena and Baixa da Barca. At Ilheus da Madalena commercial and recreational fishing is banned except shore fishing between vertices D and E and capture of live bait; at Baixa da Barca all fishing is banned. [S] I could not obtain the vertex coordinates, so I cannot say which stretch of the Madalena shore is the permitted one or how far the closed area extends along the coast. This is the single most important item to check locally.
- **Offshore marine park (RAMPA)**: the expanded network was approved in October 2024 and took effect 1 January 2026; a December 2025 government resolution lists "revise and designate the coastal network" as future work. [S] On that reading no new coastal no-take zones apply to Pico's shore yet in 2026, but I did not read the instruments.
- **Bathing waters 2026**: 26 identified on Pico. [S]
- **Port classes**: Sao Roque class B, Madalena class C. [S]
- **Goraz**: when an island quota closes, taking it is banned for recreational anglers too. [S]

Whale watching and diving: I found no whale-watching or diving reserve that restricts shore angling. Lajes and Madalena are boat bases only.

## Species context (not spot-specific)

- A 2004-05 survey of Faial and Pico found shore angling to be the recreational method with the most fishing operations, 38 taxa in the catch, seven techniques, about 51 t per year. (Diogo and Pereira 2014, J. Fish Biology, abstract via search summary [S]; full species table not obtained.)
- The DOP channel report describes recreational shore line-fishing as targeting sargos, vejas, garoupas and chicharro, with octopus collected by hand. [V] S2. Written about the Faial side of the channel (Monte da Guia). For the Madalena side the same report lists rod fishing from the coast without naming species, and boat fishing for serra, bicuda, cavala, garoupa, mero and pargo. [V] S2

## Sources

- S1. Instituto Hidrografico (2000) pilot description of the Faial channel, as adapted in the DOP/University of the Azores SIC report: https://www.vliz.be/imisdocs/publications/ocrd/291402.pdf
- S2. Same report, sections on Ilheus da Madalena, recreational fishing and limpet zones: https://www.vliz.be/imisdocs/publications/ocrd/291402.pdf ; MPA scenarios report: https://www.vliz.be/imisdocs/publications/ocrd/291406.pdf
- S3. Azores bathing-water quality bulletin 2024, Pico (26 waters, with codes): https://servicos-sraa.azores.gov.pt/grastore/BALNEARES/boletins_AB_ID/2024_boletim_divulgacao_Pico_AB_ID.pdf
- S4. Tourism page on Pico natural pools (commercial, descriptive only): https://azoresgetaways.com/pt-pt/destinations/azores/pico/piscinas-naturais-ilha-pico
- S5. Classified areas of Pico (SIARAM sheet hosted by Lajes council, updated Oct 2012): https://oldsite.cm-lajesdopico.pt/index.php/documentos-online/ambiente-e-saude-publica/conservacao-da-natureza/479-areas-classificadas-ilha-do-pico/file
- S6. OpenStreetMap via Overpass (queried 2026-11-22; object ids in Table 1). Fishing nodes: https://www.openstreetmap.org/node/13148512571 , /13148512572 , /13148512573
- S7. CM Jornal, 3 Jan 2024, missing shore angler at Manhenha: https://www.cmjornal.pt/portugal/detalhe/policia-maritima-conduz-buscas-por-pescador-desaparecido-na-ilha-do-pico
- S8. Renascenca, 18 Aug 2025, missing spearfisher at Ponta da Ilha (403 on fetch; snippet only): https://rr.pt/noticia/pais/2025/08/18/buscas-por-pescador-desaparecido-na-ilha-do-pico/436558/
- S9. Official Azores dive portal, Pico sites: https://dive.visitazores.com/en/divespots?island=pico (pages for arcos-da-formosinha, arcos-do-pocinho, cachorro, corais-de-sao-caetano, arcadas-de-sao-roque, furnas-de-santo-antonio, baixa-do-norte)
- S10. Commercial dive guide naming Baixa do Calhau and Arcos da Prainha: https://azoresgetaways.com/en-us/destination/azores/pico/pico-island-diving
- S11. Regional government proposal to amend DLR 9/2007/A, with republished text: https://servicos-sraa.azores.gov.pt/grastore/SRMCT/Proposta_Alteracao_DLR_9_2007_A.pdf
- S12. Sao Roque do Pico council trail descriptions: https://www.cm-saoroquedopico.pt/trilho/read/1/social
- S13. DN, 25 Oct 2021: https://www.dn.pt/arquivo/diario-de-noticias/pescador-desparecido-na-ilha-do-pico-encontrado-morto-14255933.html ; Noticias ao Minuto, 24 Oct 2021: https://www.noticiasaominuto.com/pais/1858496/buscas-por-pescador-desparecido-suspensas-e-retomadas-segunda-feira
- S14. Portos dos Acores regulation for the Sao Roque port bay: https://portosdosacores.pt/wp-content/uploads/2023/07/REG11_DPPIC00_Ordenamento_da_Baia_do_Porto-de_Sao_Roque_do_Pico_para_Utilizacao_como_Fundeadouro_para_Colocacao-de-Viveiros-e-Ap-1.pdf
- S15. Faial-Pico channel workshop proceedings 2017 (mentions "decreto de pesca 53/2016" and recreational uses of the channel): https://www.ecologic.eu/sites/default/files/event/2017/2803-faial-pico-channel-workshop-3-october-2017-proceedings-portuguese.pdf
- EMODnet Bathymetry REST: https://rest.emodnet-bathymetry.eu/depth_sample and /depth_profile . GEBCO 2020 via https://api.opentopodata.org/v1/gebco2020

Could not fetch (HTTP 403 or bot challenge; not circumvented): jo.azores.gov.pt (Portaria 53/2016 and other regional acts), portal.azores.gov.pt, pescador.azores.gov.pt, pescazores.com, rr.pt, idealista.pt, forums.deeperblue.com (a Pico spearfishing thread), repositorio.uac.pt (University of the Azores theses, including work on recreational fishing in Faial and Pico). diariodarepublica.pt pages rendered empty.

## Not done

- No Navionics, OpenSeaMap tile or Fishbrain data was inspected; OpenSeaMap content was covered only through OSM seamark tags.
- No YouTube or Facebook content was reviewed; search did not surface any Pico shore-fishing video and I did not browse those sites directly.
- Access difficulty, height above water and night practicality are blank for almost every spot because no source describes them.
