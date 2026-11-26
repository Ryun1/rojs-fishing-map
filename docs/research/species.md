# Evidence base for shore-fishing species forecasts on Pico (Azores)

Research notes compiled 2026-11-22. Web research only; no app code touched.

Conventions used below:

- **[V]** = verified in this session: I fetched the source and read the fact in it (or queried the API).
- **[S]** = seen only in a search-engine snippet or summary; source page itself not opened (blocked, paywalled or not tried).
- **[U]** = not verified; from memory or inference. Treat as a lead only.
- "Pico box" = lat 38.35 to 38.60, lon -28.60 to -27.95. "Azores box" = lat 36.8 to 39.8, lon -31.4 to -24.9.

Access problems worth knowing about (all hit in this session):

- `jo.azores.gov.pt/api/public/ato/<uuid>/pdfOriginal` (the links search engines return for the Azores official journal) sit behind a Cloudflare challenge and return 403 to scripts. The alternative path `https://jo.azores.gov.pt/pdf/atos/<number>-I-Portaria-<yyyy-mm-dd>.pdf` works with plain curl for recent acts (2019 onward tested) but not for 2014 to 2016 acts.
- `lotacor.pt` refused connections entirely from this machine (ECONNREFUSED on 443 and 80), so the Lotaçor "pescado descarregado" page could not be inspected. A Wayback snapshot exists (2025-02-16) but the fetch tool cannot open web.archive.org.
- `pescaludica.azores.gov.pt`, `core.ac.uk`, `repositorio.uac.pt`, `revistas.rcaap.pt` block automated clients (403 or bot wall).
- `reports-estatistica.azores.gov.pt` (SREA report viewer) is behind a Cloudflare challenge; fine in a browser, not scriptable.
- No `pdftotext` on this machine; PDFs were converted with Ghostscript `txtwrite`.

---

## 0. Headline findings

1. **The single best quantitative source for the 12-month season curves is SREA's monthly Excel table of landings by species and island** (derived from Lotaçor auction data). It is a direct download, it has a Pico block, and it breaks out six of the app's seven species by their local names (Veja, Sargo/Sarguete, Bicuda, Serra, Írio/Lírio, Anchova). Moray is not broken out. See section 2, including the actual Pico numbers for Mar 2025 to Oct 2026.
2. **Local names need fixing in the app.** In the Azores "bonito" means skipjack tuna (*Katsuwonus pelamis*); *Sarda sarda* is "serra". Seriola is "írio / lírio"; "charuteiro" is a mainland/Madeira/EU trade name and does not appear in the Azores fisheries directorate's own species list or in FishBase's Azores names. [V]
3. **FishBase is usable as data (parquet dumps, no API) but is weak for this purpose**: its temperature "preferences" are global AquaMaps envelopes, and its diel-activity fields are empty for every species checked. It is good for names, depth ranges, max length, and some spawning months. [V]
4. **Occurrence databases are too sparse and too effort-biased to drive predictions.** Around Pico the app's seven species have between 3 and 97 GBIF records each, mostly from one summer-biased dive-survey dataset. Useful for a presence checklist per stretch of coast, not for seasonality. [V]
5. **Regulation facts an app can safely show** (verified in the legal texts): shore angling needs no licence; minimum sizes exist for veja (30 cm), sargo (15 cm), garoupa (30 cm), mero (60 cm) and others; veja has a per-island commercial quota whose exhaustion immediately closes recreational veja fishing on that island; Lajes do Pico, Ponta da Ilha and the Madalena side of the Faial-Pico channel are all inside coastal "resource management" protected areas. Details and caveats in section 6.

---

## 1. What a shore angler realistically catches on Pico / Faial

### 1.1 Scientific sources

| Source | URL | What it contains | Granularity | Access | Confidence |
|---|---|---|---|---|---|
| Diogo & Pereira 2014, *J. Fish Biol.*, "Assessing the potential biological implications of recreational inshore fisheries on sub-tidal fish communities of Azores using catch and effort data" | https://doi.org/10.1111/jfb.12336 | The key study: recreational shore angling, spearfishing and intertidal collecting surveyed **on Faial and Pico**, Oct 2004 to Sep 2005. Abstract [V via OpenAlex]: shore angling had the highest effort and the most diverse catch (38 species, 7 techniques); annual catch about 51.2 t for shore angling vs 6.3 t spearfishing vs 442 t commercial artisanal; mean trophic level 3.1 (shore) vs 3.4 (spear). | Two islands, one year; species table and per-technique breakdown are in the full text | Paywalled (Wiley). **I could not obtain the species composition table.** | High that it exists and is the right paper; species percentages NOT verified |
| Diogo & Pereira 2013, *Acta Ichthyol. Piscat.* 43(4), recreational BOAT fishing, Faial and Pico | https://doi.org/10.3750/aip2013.43.4.02 (PDF: https://aiep.pensoft.net/article/26400/download/pdf/) | Boat angling (secondary for this app). 87 anglers / 46 boats, 2004 to 2005. Demersal handlining was 87.5% of operations; 32 fish species; about 163 t/yr; *Serranus atricauda* was the top species (24.6% by weight, 45.9% by number), then *Pagellus bogaraveo* (about 12%). 57.4% of anglers fished year round. [V] | Two islands | Open access | High |
| Diogo et al. 2017, *Fish. Manag. Ecol.*, spearfisher experience, São Miguel | https://doi.org/10.1111/fme.12206 | Catch composition depends on fisher skill; relevant caveat for any catch-based model. Abstract only [V] | One island | Paywalled | Medium |
| DRP / ICES "Sampling Design of Azorean Recreational Fishing Data Collection (ICES Xa)", Horta, May 2022 | https://www.dgrm.pt/documents/20143/124668/17_Azores_ICES_RecreationalSamp..pdf/7863f6bf-23ee-e6de-0425-d68403671742 | Describes the official data programme. States that shore angling and hand harvesting need no licence and are **not covered** by the logbook / licence-recall surveys (only boat angling, spearfishing and charter boats are). Names *Sparisoma cretense* and *Serranus atricauda* as highly targeted by recreational fishing. [V] | Region | Open PDF | High |
| DRP "Manual de Utilizador do Inquérito de Licenciamento da Pesca Lúdica" (annex: "Espécies mais comuns na Região Autónoma dos Açores") | https://pescador.azores.gov.pt/Sto/Documentos/Documento_3012202116253622717714461.pdf | Official picture list of the species most caught by recreational fishers, with the local names used on the licence survey. This is the best authority for local names. [V] | Region | Open PDF | High |
| Martínez-Escauriaza et al. 2020, *Scientia Marina* 84(4):331-341, shore angling in Madeira | https://doi.org/10.3989/scimar.05046.30a | Closest open-access analogue with a full species table. 734 anglers; CPUE 0.35 ± 0.26 kg/angler/hour; 43 teleosts. Estimated share of recreational shore catch: *Diplodus sargus* 15.7%, *Sparisoma cretense* 10.8%, *Pagrus pagrus* 7.8%, *Sarpa salpa* 7.3%, *Chelon* spp. 6.9%, *Oblada melanura* 6.6%, *Boops boops* 6.3%, *Trachinotus ovatus* 4.3%, *Abudefduf luridus* 2.8%, *Sphyraena* spp. 2.5%, *Diplodus vulgaris* 2.4%, *Pagellus acarne* 2.4%, *Pomatomus saltatrix* 2.1%, *Thalassoma pavo* 1.7%, *Serranus atricauda* 1.6%, *Balistes capriscus* 1.5%, *Seriola rivoliana* 0.8%, morays 0.4%. Time of day: about 40% no preference, 31% day, 14.7% night, 8.6% "depending on the tides". [V] | Madeira archipelago, 2017 | Open access | High for Madeira; a reasonable prior for Pico, not a measurement of it |
| Santos, Medeiros-Leal & Pinho 2020, *Arquipelago Life and Marine Sciences* Supplement 12, "Synopsis of biological, ecological and fisheries-related information on priority marine species in the Azores region" | https://repositorio.uac.pt/bitstreams/62988913-b722-45eb-bcd4-128aab0b019b/download (145 pages) | Azores-specific species sheets (biology, spawning months, size at maturity, regulations timeline, landings series) for commercial priority species including veja, Seriola spp., *Serranus atricauda*, *Scomber colias*, *Trachurus picturatus*, *Pagellus bogaraveo*, *Phycis phycis*, *Conger conger*. [V for veja and Seriola sections] | Region | Open PDF (repository blocks curl; the fetch tool could download it) | High |
| Schmiing, Afonso, Tempera & Santos 2013, *MEPS* 474:201-216, "Predictive habitat modelling of reef fishes with contrasting trophic ecologies" | https://doi.org/10.3354/meps10099 (PDF: https://archimer.ifremer.fr/doc/00396/50773/51525.pdf) | GAMs of abundance / presence for 11 reef fishes from 462 dive transects (0 to 40 m) around **Faial and western Pico**. Predictors: depth, distance to sediment, slope, exposure to swell, exposure to currents. Table 1 [V]: *Diplodus sargus* mean 35.1 ± 4.1 fish per transect, max 500, zero on 16% of transects; *Sparisoma cretense* 4.9 ± 0.6, zero on 47%; *Serranus atricauda* 3.2 ± 0.2, zero on 25%; *Sphyraena viridensis* 3.2 ± 0.9, max 180, zero on 81% (schooling, presence / absence model only); *Sarpa salpa* 21.6, *Coris julis* 25.3, *Labrus bergylta* 0.6. Depth and distance to sediment mattered for nearly all species; herbivores and omnivores (veja, salema, sargo) had decreasing predicted abundance at the most swell-exposed sites, planktivores the opposite. Models explained 34 to 68% of deviance. Note "exposure" here is a long-term site index, not the swell on the day. [V] | Spatial (per-site habitat), summer data only | Open access | High. This is the only source found that supports per-spot differences on Pico, but only for the west coast and only as a static habitat effect |

### 1.2 Weak evidence (guides, forums, charters)

Searches in Portuguese and English for Pico shore-angling reports turned up almost nothing specific: charter listings (boat only), generic travel guides ("grouper, trevally, jacks nearshore"; "mullet, dentex, maybe amberjack from shore"), and no local forum threads with months or spots. I did not find a usable angler-report corpus for Pico. **Gap.** Local knowledge (tackle shops in Madalena / Lajes, Clube Naval, Facebook groups) would have to be collected by hand.

### 1.3 Local names (verified)

From the DRP licence-survey manual annex [V] and FishBase country code 620B = Azores [V]:

| Species | Azores name(s) | Note |
|---|---|---|
| *Diplodus sargus* (subspecies *cadenati*) | Sargo; small ones "sarguete" (SREA lists "Sargo / Sarguete") | |
| *Sparisoma cretense* | Veja | |
| *Sphyraena viridensis* | Bicuda | |
| *Seriola rivoliana*, *S. dumerili* | Írio / Lírio | "Charuteiro" is NOT an Azores name in either source; it is the mainland / EU commercial designation for Seriola [S]. *Caranx crysos* is "írio de serra" |
| *Pomatomus saltatrix* | Anchova (also Enchova) | |
| *Sarda sarda* | **Serra** | The app currently calls this "bonito" |
| *Katsuwonus pelamis* | **Bonito** (also Gaiado) | Skipjack tuna. Not a shore fish |
| *Muraena helena* | Moreia / moreia pintada (DRP list labels it "moreia amarela") | |
| *Muraena augusti* | Moreão / moreia preta | |
| *Gymnothorax unicolor* | Moreão / moreia castanha | |
| *Enchelycore anatina* | Moreia víbora | |
| *Serranus atricauda* | Garoupa | |
| *Epinephelus marginatus* | Mero | Restricted, see section 6 |
| *Mycteroperca fusca* | Badejo | Restricted, see section 6 |
| *Pagellus bogaraveo* | Carapau (small) / Peixão (medium) / Goraz (large) | Shore-caught juveniles are "carapau" |
| *Pagellus acarne* | Besugo | |
| *Trachurus picturatus* | Chicharro | |
| *Scomber colias* | Cavala | |
| *Pseudocaranx dentex* | Encharéu | |
| *Trachinotus ovatus* | Prombeta / Cabra | |
| *Balistes capriscus* | Peixe-porco | |
| *Kyphosus* spp. | Patruça / Dorminhoca / Salema do Brasil | |
| *Sarpa salpa* | Salema | |
| *Chelon labrosus* | Tainha | |
| *Boops boops* | Boga | |
| *Labrus bergylta* | Bodião vermelho | |
| *Centrolabrus caeruleus* | Bodião verde | |
| *Bodianus scrofa* | Peixe-cão / Gaio / Viola | |
| *Coris julis* | Peixe-rei ("lambaz" for males) | |
| *Thalassoma pavo* | Peixe-rainha | |
| *Phycis phycis* | Abrótea | |
| *Conger conger* | Congro / Safio | |
| *Pagrus pagrus* | Pargo | |
| *Mullus surmuletus* | Salmonete | |
| *Scorpaena maderensis* | Rascaço / Coça | |
| *Belone belone* | Peixe-agulha | |
| *Sphoeroides marmoratus* | Peixe-balão / Sopapo | Nuisance catch |
| *Abudefduf luridus* | Castanheta preta | Nuisance catch |

---

## 2. Seasonality by month

### 2.1 SREA monthly landings by species and island (best source found)

- Landing page: https://srea.azores.gov.pt/area/agricultura-pecuaria-e-pescas/ [V]
- File used: **"Volume (kg) da pesca descarregada nos últimos 12 meses, por espécie e por ilha"** = `https://srea.azores.gov.pt/wp-content/uploads/2026/11/Q4_out_26.xlsx` (68 KB) [V, downloaded and parsed]
- Metadata page: https://srea.azores.gov.pt/relatorio/quantidade-de-pesca-descarregada-nos-ultimos-12-meses-por-categoria-e-especie/
- Contents: one sheet; a block for the Azores total and one block per island (Santa Maria, São Miguel, Terceira, Graciosa, São Jorge, **Pico**, Faial, Flores, Corvo). Rows are about 45 named species or groups; columns are the last 12 months in kg plus a year-on-year change.
- Source of the numbers: Lotaçor first-sale auction records. Excludes rejected fish, "caldeirada" and algae.
- Granularity: **island x species x month**. Not per port.
- Format / licence: xlsx, public statistics, no login. No explicit licence statement seen.
- History: each file is a rolling 12 months. Monthly files follow the pattern `https://srea.azores.gov.pt/wp-content/uploads/<yyyy>/<mm of publication>/Q4_<ref month abbreviation>_<yy>.xlsx`. On 2026-11-22 the files for reference months Feb 2026 through Oct 2026 returned HTTP 200 (`2026/03/Q4_fev_26.xlsx` ... `2026/11/Q4_out_26.xlsx`); Jan 2026 and earlier returned 404, and the Wayback Machine has no copies. So **about 20 months (Mar 2025 to Oct 2026) can be reconstructed today**, and a longer history has to be accumulated by saving the file once or twice a year, or pulled from the report viewer below. The column headers in the files are mangled dates (e.g. "2025-11-20"); the columns are simply consecutive months ending in the reference month (overlapping months agree exactly between files).
- Longer series: "Total da pesca descarregada, por espécie e por ilha" is an interactive monthly pivot at `https://reports-estatistica.azores.gov.pt/Reportserver/Pages/ReportViewer.aspx?%2fRelatoriosVarios%2fPesca-Total+de+Pesca+Descarregada+nos+Portos+dos+A%c3%a7ores&rs:Command=Render`. It sits behind a Cloudflare browser check, so I could not confirm how far back it goes or its export formats. [U] Worth opening by hand in a browser: SQL Server Reporting Services viewers normally offer Excel / CSV export.
- Other SREA files on the same page [V that they exist]: Q1 (monthly summary by island), Q2 (volume by island), Q3 (value by island), Q5 (average price per kg by species and month).
- SREA's monthly "Pescas" bulletin (e.g. https://srea.azores.gov.pt/2026/11/17/pescas-outubro-2026/) only gives island totals and fish / mollusc / crustacean groups, with the table as an image. Not useful for species. [V]

**Pico, landed kg per month, Nov 2025 to Oct 2026** (extracted from the file) [V]:

| Species (as labelled) | Nov | Dec | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | 12-mo total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Veja | 821 | 377 | 681 | 291 | 2592 | 1494 | 2426 | 5713 | 13914 | 5568 | 2915 | 541 | 37333 |
| Sargo / Sarguete | 129 | 138 | 210 | 370 | 47 | 35 | 78 | 12 | 18 | 5 | 36 | 74 | 1152 |
| Bicuda | 1426 | 75 | 17 | 0 | 121 | 134 | 477 | 720 | 891 | 2687 | 3612 | 1720 | 11880 |
| Serra (*Sarda sarda*) | 14 | 13 | 0 | 0 | 35 | 0 | 71 | 46 | 23 | 68 | 94 | 33 | 397 |
| Írio / Lírio | 0 | 1 | 0 | 0 | 1 | 0 | 7 | 508 | 274 | 42 | 150 | 2 | 985 |
| Anchova | 55 | 9 | 0 | 0 | 6 | 2 | 0 | 27 | 358 | 778 | 308 | 37 | 1580 |
| Encharéu | 338 | 13 | 30 | 3 | 153 | 37 | 137 | 459 | 2374 | 700 | 1392 | 1670 | 7306 |
| Chicharro | 2694 | 2456 | 2634 | 2841 | 2793 | 2334 | 2181 | 3093 | 4181 | 1002 | 674 | 321 | 27204 |
| Cavala | 9 | 1 | 9 | 8 | 306 | 68 | 8 | 78 | 136 | 295 | 50 | 28 | 996 |
| Garoupa | 889 | 242 | 57 | 12 | 156 | 178 | 124 | 393 | 326 | 110 | 47 | 59 | 2593 |
| Congro | 902 | 223 | 147 | 256 | 3205 | 1300 | 1210 | 1465 | 1248 | 1242 | 717 | 640 | 12555 |
| Abrótea | 871 | 344 | 103 | 201 | 1035 | 1639 | 1229 | 1204 | 1489 | 1130 | 1511 | 939 | 11695 |
| Peixão | 595 | 99 | 246 | 261 | 1877 | 436 | 552 | 863 | 1600 | 574 | 727 | 575 | 8405 |
| Pargo | 240 | 23 | 9 | 16 | 473 | 533 | 360 | 201 | 154 | 144 | 40 | 165 | 2358 |
| Mero | 0 | 0 | 51 | 10 | 126 | 106 | 338 | 354 | 463 | 191 | 0 | 275 | 1914 |
| Lula (squid) | 889 | 1102 | 2092 | 1829 | 2411 | 1577 | 1407 | 813 | 2086 | 1445 | 1508 | 2543 | 19702 |
| Polvo (octopus) | 9 | 15 | 35 | 10 | 1 | 4 | 16 | 22 | 7 | 16 | 8 | 6 | 149 |
| Lapa (limpets) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11947 | 5200 | 2483 | 2318 | 171 | 22119 |

**Azores total, same months, for the app's species** [V]:

| Species | Nov | Dec | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | 12-mo total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Veja | 7091 | 1315 | 3246 | 2141 | 5409 | 4595 | 6018 | 17691 | 35126 | 15008 | 14969 | 4389 | 116998 |
| Sargo / Sarguete | 2077 | 2195 | 1559 | 2294 | 1694 | 1042 | 686 | 580 | 558 | 1568 | 2045 | 2272 | 18570 |
| Bicuda | 4960 | 512 | 230 | 130 | 1774 | 4917 | 6455 | 9250 | 13291 | 12583 | 15872 | 14904 | 84878 |
| Serra | 524 | 173 | 449 | 67 | 753 | 961 | 1961 | 2104 | 952 | 681 | 1820 | 1174 | 11619 |
| Írio / Lírio | 320 | 66 | 25 | 6 | 40 | 111 | 204 | 2543 | 2892 | 4659 | 1635 | 264 | 12765 |
| Anchova | 269 | 54 | 48 | 16 | 98 | 65 | 139 | 717 | 3658 | 4500 | 2351 | 332 | 12247 |

**Pico, earlier months (Mar to Oct 2025) from `Q4_fev_26.xlsx` / `Q4_mar_26.xlsx`**, giving a second summer [V]:

| Species | Mar 25 | Apr 25 | May 25 | Jun 25 | Jul 25 | Aug 25 | Sep 25 | Oct 25 |
|---|---|---|---|---|---|---|---|---|
| Veja | 2418 | 1854 | 4245 | 9355 | 11788 | 6466 | 2012 | 968 |
| Sargo / Sarguete | 62 | 32 | 85 | 35 | 28 | 31 | 70 | 172 |
| Bicuda | 121 | 117 | 442 | 886 | 1450 | 2298 | 2228 | 1823 |
| Serra | 111 | 22 | 341 | 58 | 61 | 38 | 22 | 21 |
| Írio / Lírio | 2 | 0 | 14 | 34 | 29 | 49 | 4 | 0 |
| Anchova | 1 | 2 | 13 | 214 | 693 | 250 | 134 | 32 |
| Encharéu | 73 | 61 | 148 | 867 | 1133 | 279 | 70 | 129 |
| Garoupa | 511 | 330 | 769 | 566 | 446 | 106 | 0 | 356 |
| Chicharro | 4553 | 3829 | 4273 | 1647 | 3782 | 3325 | 4035 | 2717 |

The two summers agree on timing (anchova June to September; bicuda May to November peaking August to October; sargo rising from October; veja peaking June to July) but not on size: Pico landed 130 kg of írio in summer 2025 and 980 kg in summer 2026. Timing looks robust; amplitude does not.

What these 20 months show (indicative only; still short of a climatology):

- **Anchova (bluefish): sharply seasonal, July to September**, near zero December to May. Same shape on Pico, Faial, São Jorge and region-wide.
- **Írio (Seriola): June to September**, near zero November to May.
- **Bicuda: builds from April / May, peaks August to October, still present in November**, collapses December to February.
- **Serra (Sarda sarda): spring through autumn, small volumes**, noisy.
- **Sargo: the opposite of the pelagics: highest October to February, lowest May to August.** Small volumes (1.2 t on Pico).
- **Veja: March to September with a July spike.** Pico landed 37 t, about a third of the regional total, consistent with Pico holding 32.5% of the regional veja quota (section 6).
- Limpets appear only from June because of the closed season.

Caveats that matter when turning landings into "chance of catching from shore":

- Landings measure commercial effort and market as much as abundance: gear differs (veja is caught with gillnets, Seriola and bicuda by hook and line / trolling from boats), winter weather keeps small boats ashore, and quota management shapes veja (quarterly quota split, per-trip limits) and garoupa / mero.
- Commercial sargo is a tiny, probably net-caught winter by-catch; its winter peak agrees with shore-angling lore but is not independent proof.
- The fish need not be caught near the island they are landed on, though for coastal species landed by Pico's small local fleet this is a fair assumption.
- One year is not a climatology. Several years are needed before fitting a curve, and the July 2026 veja and tuna spikes show how lumpy a single year is.

### 2.2 Lotaçor directly

- Page cited in the literature as the public landings database: https://lotacor.pt/pescado-descarregado (used for 2009 to 2019 by Santos et al.) [S].
- **Could not be reached from this machine** (connection refused), so filters, granularity and export options are unverified. [U] Given that SREA republishes Lotaçor's numbers by island and species, SREA is the practical route.
- Port-level (lota by lota) monthly data by species was not found anywhere public. For per-spot differences within Pico (Madalena vs São Roque vs Lajes vs Calheta) the request would have to go to Lotaçor or Okeanos / University of the Azores. [U]

### 2.3 Other seasonality sources

| Source | URL | Contains | Granularity | Access | Confidence |
|---|---|---|---|---|---|
| Santos et al. 2020 synopsis (above) | repositorio.uac.pt link above | Annual landings series per priority species, spawning months, regulation timeline | Region, annual | Open PDF | High |
| ICES Azores ecoregion fisheries overview | https://www.ices.dk/advice/ESD/Pages/Azores_fish.aspx | Regional fisheries overview | Region, annual | Open | Not opened [S] |
| INE / dados.gov.pt "Capturas nominais de pescado (t) por porto de descarga e espécie; anual" | https://dados.gov.pt/en/datasets/capturas-nominais-de-pescado-t-1/ | Annual landings by port and species, national | Port, annual | Open data | Not opened [S] |
| GBIF "POPA: fish caught to be used as bait in the Azores tuna fishery 1998 to 2013" | https://doi.org/10.14284/9 | Dated, georeferenced bait catches (chicharro, cavala, sardine etc.): 5,747 records, 819 in the Pico box; months May to October only (tuna season) [V] | Point, date | CC BY-NC 4.0, Darwin Core archive | High, but only tells you where bait-fish were netted in summer |
| FishBase `spawning` table | see section 3 | Spawning months by locality; has an Azores row for *Diplodus sargus* (Faial, Mar to Jun, 15 to 17 C) and *Phycis phycis* | Species x locality | CC BY-NC | Medium |

---

## 3. Per-species ecology that maps to conditions

### 3.1 FishBase / SeaLifeBase as a data source

- The old REST API (`fishbase.ropensci.org`) is dead: no response. [V]
- The maintained route is the **parquet snapshots published for the `rfishbase` R package on Source Cooperative**: `https://data.source.coop/cboettig/fishbase/fb/v25.04/parquet/<table>.parquet` (FishBase) and `.../slb/v25.04/parquet/...` (SeaLifeBase). Both returned HTTP 200; I queried them directly with DuckDB over HTTPS. [V] Versions available include v24.07 and v25.04. Snapshots can lag the live site by months.
- Licence: FishBase content is CC BY-NC; fine for a personal non-commercial app, with attribution. [U for exact wording]
- Useful tables: `species` (depth range, max length, habitat class), `estimate` (modelled temperature range, trophic level), `stocks` (climate zone, IUCN), `ecology` (habitat flags, feeding type), `spawning` (months by locality), `comnames` (local names; `C_Code = '620B'` is the Azores).
- **Limits found by actually pulling the 36 candidate species** [V]:
  - `ecology.Circadian1..3` (diel activity) is **empty for every one of them**. FishBase cannot ground the time-of-day weights.
  - `estimate.TempPrefMin/Mean/Max` are AquaMaps model envelopes over the whole global range, and some are clearly not usable as angling bands (e.g. *Sarda sarda* mean 10.7 C, *Trachinotus ovatus* 13.9 C, *Seriola rivoliana* 22.1 to 28.6 C, which would exclude the Azores for most of the year although the species is resident there).
  - Depth ranges are whole-species ranges (e.g. *Sarda sarda* listed 80 to 200 m), not "is it within casting range".
- AquaMaps (https://www.aquamaps.org, site up [V]) gives the same kind of half-degree envelope model. Not useful at the scale of one island.

FishBase values pulled for the app's seven species [V] (temperatures are modelled range envelopes, not preferences measured in the Azores):

| Species | Habitat class | Depth range m | Max length cm | Modelled temp range C (min / mean / max) | Trophic level | IUCN |
|---|---|---|---|---|---|---|
| *Seriola rivoliana* | reef-associated | 5 to 245 (usually 30 to 35) | 160 | 22.1 / 27.3 / 28.6 | 4.5 | LC |
| *Seriola dumerili* | reef-associated | 1 to 385 (usually 18 to 72) | 190 | 16.9 / 27.1 / 29.0 | 4.7 | LC |
| *Pomatomus saltatrix* | pelagic-oceanic | 0 to 200 | 130 | 8.4 / 21.1 / 27.5 | 4.5 | VU |
| *Sphyraena viridensis* | pelagic-neritic | 0 to 100 | 128 | 15.1 / 18.8 / 21.5 | 4.3 | LC |
| *Sarda sarda* | pelagic-neritic | 80 to 200 | 91 | 7.0 / 10.7 / 23.4 (stocks table: 12 to 27) | 4.2 | LC |
| *Diplodus sargus* | demersal | 0 to 50 | 45 | 15.0 / 18.8 / 24.1 | 3.4 | LC |
| *Sparisoma cretense* | reef-associated | 20 to 50 | 50 | 15.1 / 17.1 / 20.3 | 2.9 | LC |
| *Muraena helena* | reef-associated | 1 to 801 (usually 100 to 300) | 150 | 13.1 / 14.4 / 16.2 | 4.2 | LC |
| *Muraena augusti* | demersal | 0 to 250 (usually 0 to 50) | 90 | 16.2 / 19.6 / 20.2 | 4.0 | LC |
| *Gymnothorax unicolor* | demersal | 0 to 20 | 100 | 16.5 / 19.2 / 21.8 | 3.4 | LC |

FishBase spawning rows relevant to the Azores [V]: *Diplodus sargus*, Faial (Aug 1997 to Jul 1999): March to June at 15 to 17 C (this is the Morato et al. study); *Phycis phycis* off the Azores: December to February; *Sparisoma cretense*: July to September (southern Italy, Ria Formosa); *Muraena augusti* and *M. helena* (Canaries): roughly May to September and January to June respectively.

### 3.2 Azores-specific facts verified in this thread

- **Veja (*Sparisoma cretense*)** (Santos et al. 2020 synopsis, citing Afonso et al. 2008a,b) [V]: strictly a **daytime feeder** scraping algae and small invertebrates; **very high site fidelity** and minimal dispersal of adults in Azores tagging / acoustic tracking; rocky bottoms to about 50 m; **spawning July to October in the Azores**; size at maturity 22 cm (males) and 25 cm (females), below the 30 cm legal minimum; territorial males with harems or multi-male groups. Targeted commercially with gillnets. Implication: night weight should be zero; season is not a migration effect (the fish are resident year round), so the landings peak is effort plus behaviour.
- **Írio (*Seriola* spp.)** (same source, citing Fontes et al. 2014, Barreiros et al. 2003) [V]: both species occur and are landed as one group; acoustic telemetry showed **resident behaviour in *S. rivoliana*** in the Azores; habitat is outer reef slopes and seamounts to 360 m, "occasionally entering coastal bays"; mainly piscivorous; no reproductive data for the Azores. Implication: a shore catch is an occasional event at deep-water points, which matches the small landings.
- **Sargo (*Diplodus sargus*)**: Azores spawning March to June at 15 to 17 C (FishBase row from the Faial study) [V]. Habitat model around Faial / west Pico: the most abundant of the modelled reef fishes, present on 84% of transects, shallow, with abundance responding to exposure to swell and currents (Schmiing et al. 2013) [V].
- **Bicuda (*Sphyraena viridensis*)**: modelled as presence / absence only (schooling pelagic) in Schmiing et al. 2013; carnivores including bicuda were associated with deeper parts of the 0 to 40 m range [V].

### 3.3 Diel activity, swell, temperature, tide and moon by species (primary literature)

*Provenance: researched by a delegated sub-agent with a "fetch, do not recall" brief. Its flags are kept: **[V]** = read in a fetched abstract or full text; **[S]** = seen only in a search-result summary, primary page blocked; **[U]** = from memory, not opened. I did not re-open these papers myself, except where noted. Publisher sites (Springer, ScienceDirect, int-res.com) and the Portuguese repositories were blocked; abstracts mostly came from the OpenAlex API (record IDs W...), Europe PMC (PMID), VLIZ marineinfo.org, PLoS full text and two open PDFs (Cybium, ICCAT).*

**Bottom line.** Measurements support the month curves for sargo, veja, bicuda, írio, encharéu and juvenile peixão, and the time-of-day weights for sargo, veja, bicuda, moreia, congro, bodião and polvo. Temperature bands rest on spawning or larval thresholds, not on catchability. Wave, tide and moon terms are almost entirely unmeasured. **No Azores study at all was found for anchova or serra.**

#### Sargo, *Diplodus sargus*

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Season (Azores) | Spawning March to June at 15 to 17 C; settlement late May to July; juveniles leave nurseries late July to September; maturity at 16.7 cm in the second year | Morato, Afonso, Lourinho and Nash 2003, *J Fish Biol*, doi 10.1046/j.1095-8649.2003.00129.x (OpenAlex W1968213038) | V |
| Season analogue | Gulf of Tunis: spawning March to May as water rises from 15 to 18 C | Mouine et al. 2007, *Sci Mar* (W1803535316) | V |
| Depth | 95% of detections at 0.4 to 11 m, rarely below 15 m; home range 0.49 ± 0.26 km2; n = 41 | Aspillaga et al. 2016, *PLoS ONE*, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0159813 (NW Mediterranean MPA) | V (full text) |
| Storms | Sheltering moves to protected places, not necessarily deeper; one fish moved more than 2 km. No wave-height threshold quantified | same | V |
| Spawning excursions | March to April: all no-take-zone fish went below 20 m and 46% below 50 m, so adults are partly out of the shore zone then | same | V |
| Diel: more active by day | Torre Guaceto, Adriatic | Di Lorenzo et al. 2016, *Mar Env Res* (PMID 26922044) | V |
| Diel: hidden by day, foraging at night | n = 4, artificial reef, Sicily | D'Anna et al. 2010/11 (W1991721093) | V |
| Diel: mixed | All fish showed a diel signature but the direction split (39% shallower at night, 30% deeper) | Aspillaga et al. 2016 | V |
| Diel: review verdict | "Diurnal with a few exceptions"; environmental effects named as a research gap. In the Azores feeding starts at sunrise and peaks midday to early afternoon (Figueiredo et al. 2005, as cited in the review) | Giacalone et al. 2022, *Env Biol Fish* (W4224438857) | V |
| Tide | Tide x time-of-day interaction, with "higher and more variable movements during daytime and neap tides" (19 fish, 60 days). The only measured tide effect found for any species | Belo et al. 2016, *Mar Env Res*, Pessegueiro Island, SW Portugal (PMID 26794495) | V |
| Not found | Any measurement of surf / white-water feeding, turbidity or moon. Figueiredo et al. 2005 (Azores diet, *Fish Res*) abstract not retrievable | | |

Two readings of the same papers differ between my two research threads and should be checked against the full texts before use: (a) the section 5 thread, via the Giacalone review, reports that sargo feeding areas are high-hydrodynamic zones used on a rising or high tide (attributed to Belo et al.), whereas the Belo abstract read here speaks of more movement on neap tides in daytime; (b) section 5 summarises Aspillaga et al. as fish going deeper in storms, whereas the full text read here says they shelter in protected places, not necessarily deeper.

#### Veja, *Sparisoma cretense*

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Habitat (Azores) | Haremic territorial fish hold small home ranges in high-energy reef areas; group fish stay on sheltered reefs and make daily migrations to territorial areas in the spawning season; site fidelity up to 30 months | Afonso, Fontes, Holland and Santos 2008, *MEPS* 359, doi 10.3354/meps07272 (W2006599697) | V |
| Depth split | Larger territorial fish on exposed, deeper ledges; group fish in shallower protected habitat; reproduction "in the summer" | Afonso, Morato and Santos 2008, *Fish Res* 90:92-99, https://marineinfo.org/id/publication/258331 | V |
| Spawning months (Azores) | July to October | Santos et al. 2020 synopsis citing Afonso et al. 2008b (read by me, section 3.2) | V |
| Diel | Diurnal with a dominant diel rhythm, resting at night (n = 6; home range 7 to 25.6 ha) | La Mesa et al. 2012, *Mar Env Res*, Lampedusa (PMID 23069664) | V |
| Not found | Tide, moon, swell or temperature response | | |

#### Bicuda, *Sphyraena viridensis*

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Season and habitat (Azores; about 550 h of underwater observation; fish spearfished at Pico, Faial and four other islands) | Large schools form May to October, 88% of them in July to September (n = 67), always at current-swept sites deeper than 20 m near seamounts and cliffs. November to April: no large schools, only 12 small juvenile groups in shallow bays. 98% of small groups, pairs and solitary fish (n = 40) were in shallow-water bays (the shore-relevant component). SST averaged 17.2 ± 1.3 C in winter and 23.7 ± 2.1 C in summer (range 16.3 to 25.4). 82.2% of fed stomachs held juvenile *Trachurus picturatus* | Barreiros, Santos and Borba 2002, *Cybium* 26(2):83-88, https://sfi-cybium.fr/sites/default/files/pdfs-cybium/02-Barreiros%5B262%5D83-88.pdf | V (full text) |
| Residency | Landings are strongly seasonal, but visual census and telemetry at Formigas indicate year-round residency | Fontes and Afonso 2017, *Mar Biol* 164:19 | S |
| Telemetry, season and diel | Over 3 years at a shallow seamount, bicuda and almaco jack were both detected more often in spring and appear more active in daytime | Gandra, Afonso and Fontes 2020, *MEPS* 654:93-107 (W3087798034) | V |
| Angling study | Dawn and dusk lure sessions, May 2016 to November 2018, Catalan Sea. "Crepuscular inshore dweller"; vulnerability to lures significantly influenced by solar and lunar light intensity, highest pre-spawn and during spawning, with a post-spawn drop at dusk. Caveats: only twilight was sampled, and the abstract does not give the direction of the lunar effect | Merciai et al. 2020, *J Fish Biol* (PMID 32383485) | V (abstract) |

This is the one species for which a peer-reviewed shore-lure angling study exists, and its "summer schools at deep current-swept points, juveniles in shallow bays in winter" pattern matches the SREA landings curve in section 2.

#### Írio / lírio, *Seriola rivoliana* and *S. dumerili*

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Residency (Azores seamounts) | Tagged adult almaco jack detected almost continuously for up to 4 years, although census and landings look seasonal. Gaps of 1 to 2 months fell mostly in autumn and winter; mobility rose in spring and summer; current speed was negatively correlated with detection. (This paper covers *S. rivoliana* only) | Fontes, Schmiing and Afonso 2014, *Mar Biol* 161:1349-1360, https://marineinfo.org/id/publication/258319 | V |
| Diet (Azores) | 232 fish of 23 to 134 cm, exclusively piscivorous: juvenile *T. picturatus*, then *Scomber* | Barreiros et al. 2003, *Cybium* (W2284729860) | V |
| *S. dumerili* spawning (Mediterranean) | Wild fish in spawning condition late May to early June, spawning late June to July | Zupa et al. 2017, *PLoS ONE* (W2569151526) | V |
| Not found | Any thermal threshold for inshore presence, any tide or moon effect, or any primary source on inshore juveniles | | |

#### Anchova, *Pomatomus saltatrix* (no Azores study found)

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Temperature and season | NW Mediterranean: spawning June to September; 21 C is the threshold for larvae in the plankton; adults migrate to spawn in April to June | Sabatés, Martín and Raya 2012, *ICES JMS* (W2150021741) | V |
| Season analogue | Sea of Marmara: spawning May to August, peak July | Bal et al. 2018 (W2794027626) | V |
| Distribution vs SST | Australian tag data: non-linear, peaking at 21.5 C | Brodie et al. 2018 (section 5) | V |
| Cold avoidance (lab, juveniles) | Fish avoid cold water, but feeding motivation overrides the avoidance | Olla, Studholme and Bejda 1985, *MEPS* (W2074299251) | V |
| Stress limits 11.9 / 29.8 C | | Olla and Studholme 1971 | U |
| Diel (lab) | Swam faster by day (47 cm/s) than at night (31 cm/s); speed fell as temperature dropped from 20 to 15 C | Stehlik 2009, *Fish Bull* (W2601721417) | V |
| Diel (field, juveniles) | Gut fullness highest in daytime and twilight, declining at night with some night feeding | Buckel and Conover 1997, *Fish Bull* 95:665-679, Hudson River | S |

#### Serra, *Sarda sarda* (no Azores, Madeira or Canaries study found)

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Temperature and habitat | Epipelagic, neritic, schooling; tolerates 12 to 27 C; spawns in coastal areas in the warmer season, 3 to 4 batches | ICCAT Manual ch. 2.1.10.1 (Mourato et al. 2021), https://www.iccat.int/Documents/SCRS/Manual/CH2/2_1_10_1_BON_ENG.pdf | V (the month table is graphical and was unreadable) |
| Season analogue | Black Sea and Marmara: spawning May to August, most intense June to July | Kahraman et al. 2014 (W2068097447) | V |

#### Moreias

| Topic | Finding | Source | Flag |
|---|---|---|---|
| Diel and moon | 19 *Muraena helena* and 6 *Conger conger* tracked for 2 summer months. Morays were active 3.3% of the time and congers 12.0%, "mainly at night and during quarter lunar phases". Home ranges 19.4 and 34.4 ha; morays moved less than 1 km per day | Pereira et al. 2017, *MEPS* 584:213-227, Pessegueiro Island, SW Portugal (W2766766997) | V |
| Season and depth | 193 fish from 5 to 80 m; females and immatures dominate shallow coastal water; gonad index rises in summer, condition lowest in winter; ripe fish apparently leave inshore in summer to spawn deep | Matić-Skoko et al. 2011, *Aquat Biol*, S Adriatic (W2097135385) | V |
| Moon (different species) | Depth of *Gymnothorax moringa* was predicted by lunar illumination | Orrell et al. 2025, *J Fish Biol*, Ascension (PMID 38632858) | V |
| Not found | Any ecology study of *M. augusti* or *G. unicolor* | | |

#### Secondary species (all V, abstracts)

- **Encharéu, *Pseudocaranx dentex* (Azores)**: spawns June to September; immature schools use inshore habitats year round; inshore fish move daily alongshore. Afonso et al. 2008, *Sci Mar* (W1501256897); Afonso et al. 2009, *MEPS* (W2063675144).
- **Carapau / peixão, juvenile *Pagellus bogaraveo* (Azores)**: inshore in all seasons up to 13 cm, with higher catch rates in summer; **shore angling is the main method** for this size class. Pinho et al. 2014, *ICES JMS* (W2316383282).
- **Garoupa, *Serranus atricauda* (Canaries)**: spawns year round, peak March to July. García-Díaz et al. 2006 (W2289460594).
- **Chicharro, *Trachurus picturatus* (Canaries)**: spawns January to April, peak February. Jurado-Ruzafa and Santamaría 2012 (W1963939519).
- **Bodião, *Labrus bergylta* (Galicia)**: 92% of fish were detected more and moved further by day. Villegas-Ríos et al. 2013, *J Sea Res*.
- **Polvo, *Octopus vulgaris* (Galicia)**: crepuscular activity pattern. Papadopoulo et al. 2024, *Anim Biotelemetry* (W4399805908).
- **Tainha, *Chelon labrosus***: presence and depth unrelated to time of day (fish-farm setting). Arechavala-Lopez et al. 2010 (W2096845577).
- Nothing usable retrieved for *Scomber colias*, *Balistes*, *Trachinotus*, *Kyphosus*, *Sarpa salpa*, *Loligo forbesii*. Nash and Santos 1998 (diel catches at Porto Pim, Faial, *ECSS*, doi 10.1006/ecss.1998.0362) exists and is relevant to harbours, but its abstract was not retrievable.

#### Which app parameters have measured support

| Species | Month curve | Temperature band | Wave band | Time of day | Tide | Moon |
|---|---|---|---|---|---|---|
| Sargo | Measured, Azores (spawning Mar to Jun; juveniles Jul to Sep) plus SREA landings (winter peak) | Partial: spawning 15 to 17 C only | Storm sheltering observed, no threshold; surf feeding is folklore | Measured but conflicting (mostly diurnal; nocturnal at some sites) | Measured once (more movement on neaps, daytime) | Unknown |
| Veja | Azores spawning Jul to Oct; resident year round; SREA landings peak Jun to Jul | Unknown | Habitat only (territorial fish on exposed reef) | Measured: strictly diurnal | Unknown | Unknown |
| Bicuda | Measured, Azores (schools May to Oct, peak Jul to Sep; juveniles in bays in winter); SREA landings agree | Descriptive only (17 C winter, 24 C summer) | Unknown; associated with currents | Measured: twilight angling, daytime telemetry | Unknown | Measured effect, direction unknown |
| Írio | Measured, Azores: resident year round, more mobile spring to summer; SREA landings Jun to Sep | Unknown | Unknown | Weak: more daytime detections | Unknown | Unknown |
| Anchova | SREA landings (Jul to Sep) plus Mediterranean analogue (spawning Jun to Sep) | Partial: 21 C larval threshold; 21.5 C distribution peak (Australia); cold avoidance | Unknown | Lab and juvenile field: day and twilight | Unknown | Unknown |
| Serra | SREA landings (spring to autumn, noisy) plus analogue (spawning May to Aug) | Envelope 12 to 27 C only | Unknown | Unknown | Unknown | Unknown |
| Moreia | Partial: Adriatic summer offshore spawning | Unknown | Unknown | Measured: nocturnal | Unknown | Measured once (quarter moons) |
| Congro | Unknown | Unknown | Unknown | Measured: nocturnal | Unknown | Measured once (quarter moons) |
| Encharéu | Measured, Azores (Jun to Sep spawning; juveniles inshore all year) | Unknown | Unknown | Partial | Unknown | Unknown |
| Peixão juveniles | Measured, Azores (summer peak) | Unknown | Unknown | Unknown | Unknown | Unknown |
| Bodião | Unknown | Unknown | Unknown | Measured: diurnal | Unknown | Unknown |
| Polvo | Unknown | Unknown | Unknown | Measured: crepuscular | Unknown | Unknown |

So of the app's five hand-guessed parameter families: the **season curve** can be grounded (landings plus Azores biology) for six of seven species; **time of day** can be grounded for five; the **temperature band** has only indirect support and for the residents (sargo, veja, morays, írio) temperature is probably just a proxy for season; the **wave band** and **tide weights** are folklore with one or two weak measurements; **moon** has no usable support.


---

## 4. Occurrence datasets around Pico

All counts are from live API queries on 2026-11-22. [V]

Endpoints used:

- GBIF: `https://api.gbif.org/v1/occurrence/search?taxonKey=<key>&decimalLatitude=38.35,38.60&decimalLongitude=-28.60,-27.95&limit=0` (key from `/v1/species/match?name=`)
- OBIS: `https://api.obis.org/v3/occurrence?scientificname=<name>&geometry=POLYGON((-28.6 38.35,-27.95 38.35,-27.95 38.6,-28.6 38.6,-28.6 38.35))&size=0`
- iNaturalist: `https://api.inaturalist.org/v1/observations?taxon_name=<name>&swlat=38.35&swlng=-28.60&nelat=38.60&nelng=-27.95&per_page=0`

### 4.1 Record counts

| Species | GBIF Pico box | GBIF Azores box | OBIS Pico box | OBIS Azores box | iNat Pico box (all / research grade) | iNat Azores box |
|---|---|---|---|---|---|---|
| *Seriola rivoliana* | 6 | 45 | 6 | 36 | 6 / 4 | 35 |
| *Seriola dumerili* | 1 | 9 | 1 | 6 | 4 / 1 | 11 |
| *Pomatomus saltatrix* | 3 | 38 | 3 | 29 | 3 / 3 | 23 |
| *Sphyraena viridensis* | 53 | 203 | 50 | 181 | 10 / 8 | 68 |
| *Sarda sarda* | 20 | 61 | 20 | 59 | 8 / 5 | 14 |
| *Diplodus sargus* | 82 | 453 | 80 | 456 | 23 / 16 | 224 |
| *Sparisoma cretense* | 97 | 528 | 92 | 485 | 52 / 47 | 265 |
| *Muraena helena* | 28 | 252 | 28 | 247 | 9 / 8 | 59 |
| *Muraena augusti* | 29 | 130 | 27 | 121 | 30 / 26 | 136 |
| *Gymnothorax unicolor* | 21 | 67 | 20 | 65 | 10 / 10 | 30 |
| *Trachurus picturatus* | 398 | 2250 | 398 | 2242 | 1 / 0 | 11 |
| *Scomber colias* | 170 | 1166 | 170 | 1165 | 1 / 1 | 8 |
| *Serranus atricauda* | 151 | 748 | 151 | 728 | 21 / 17 | 113 |
| *Epinephelus marginatus* | 38 | 151 | 36 | 126 | 29 / 26 | 117 |
| *Pagellus bogaraveo* | 100 | 968 | 99 | 964 | 2 / 2 | 8 |
| *Pagellus acarne* | 39 | 582 | 20 | 251 | 4 / 3 | 21 |
| *Balistes capriscus* | 36 | 213 | 35 | 192 | 26 / 23 | 114 |
| *Trachinotus ovatus* | 14 | 94 | 14 | 79 | 9 / 9 | 60 |
| *Kyphosus sectatrix* | 1 | 16 | 1 | 12 | 1 / 1 | 14 |
| *Sarpa salpa* | 78 | 442 | 75 | 427 | 22 / 22 | 143 |
| *Chelon labrosus* | 24 | 150 | 22 | 131 | 32 / 23 | 185 |
| *Labrus bergylta* | 30 | 205 | 29 | 202 | 4 / 3 | 36 |
| *Bodianus scrofa* | 24 | 114 | 24 | 115 | 1 / 1 | 34 |
| *Phycis phycis* | 129 | 1692 | 54 | 546 | 3 / 3 | 27 |
| *Conger conger* | 29 | 478 | 29 | 471 | 7 / 6 | 43 |
| *Pagrus pagrus* | 27 | 302 | 27 | 301 | 1 / 1 | 7 |
| *Pseudocaranx dentex* | 17 | 102 | 17 | 97 | 8 / 8 | 39 |
| *Mullus surmuletus* | 45 | 366 | 45 | 357 | 14 / 13 | 82 |
| *Scorpaena maderensis* | 37 | 160 | 34 | 148 | 40 / 31 | 151 |
| *Coris julis* | 94 | 436 | 93 | 430 | 4 / 0 | 6 |
| *Thalassoma pavo* | 137 | 659 | 130 | 629 | 44 / 39 | 252 |
| *Boops boops* | 145 | 686 | 131 | 614 | 15 / 12 | 49 |
| *Belone belone* | 1 | 7 | 1 | 7 | 2 / 1 | 18 |
| *Abudefduf luridus* | 58 | 320 | 71 | 390 | 22 / 16 | 118 |
| *Octopus vulgaris* | 19 | 84 | 18 | 71 | 19 / 18 | 94 |
| *Loligo forbesii* | 2 | 18 | 1 | 16 | 0 / 0 | 1 |
| *Katsuwonus pelamis* | 1071 | 14260 | 1071 | 14257 | 1 / 1 | 4 |
| *Centrolabrus caeruleus* | 0 (name not matched in GBIF backbone) | 4 | 28 | 96 | 34 / 32 | 132 |
| *Sphoeroides marmoratus* | 60 | 392 | 59 | 391 | 20 / 17 | 103 |

GBIF and OBIS counts are nearly identical because they mirror the same IMAR / DOP datasets (published through the EurOBIS IPT at VLIZ). They are not independent.

### 4.2 Where the records come from

For 28 target species combined in the Pico box, GBIF holds 1,834 records [V]:

| Dataset | Records in Pico box | Licence | DOI |
|---|---|---|---|
| Underwater fish visual census in the Azores 1997 to 2015 (IMAR / DOP) | 597 | CC BY 4.0 | 10.14284/210 |
| POPA observer programme: bait fish for the tuna fishery 1998 to 2013 | 583 | CC BY-NC 4.0 | 10.14284/9 |
| iNaturalist research-grade observations | 265 | CC BY-NC 4.0 | 10.15468/ab3s5x |
| Demersais (ARQDAÇO) longline survey 1996 to 2013 | 192 | CC BY 4.0 | 10.14284/22 |
| Azorean Biodiversity Portal | 108 | CC BY 4.0 | 10.15468/j0iceo |
| ImagDOP benthic video annotations, Faial-Pico Channel 2011 | 67 | CC BY-NC 4.0 | 10.14284/209 |
| Museum collections and others | about 20 | various | |

- By year: concentrated in 1997 to 2015 (survey years), a gap 2016 to 2022, then iNaturalist growth (169 records in 2025).
- By month: Jan 13, Feb 28, Mar 4, Apr 64, May 301, Jun 296, Jul 332, Aug 348, Sep 139, Oct 92, Nov 89, Dec 11. This is the **survey and diver calendar, not fish seasonality**.
- The visual census dataset as served by GBIF is **presence only**: sample records have date, coordinates (10 m uncertainty) and species but no count or depth. 5,775 records Azores-wide, 1,080 of all taxa in the Pico box. Whole-dataset months: 70% of records fall in July to September. The Darwin Core archive (https://ipt.vliz.be/eurobis/archive.do?r=scuba_diving_visual_census, returns a zip [V]) may carry more fields; not opened.
- Other relevant GBIF datasets noticed: "Marine Species Rapid Assessment Survey of Azorean Ports and Marinas (2023-2024)" (216 records, CC BY), "Azores actinopterygii updated checklist".
- Azores Biodiversity Portal: https://azoresbioportal.uac.pt/ (site up [V]); its records are also in GBIF.

### 4.3 Verdict

Usable for: a per-coast presence checklist; confirming that veja, sargo, garoupa, bicuda, morays, salema, wrasses are recorded right around Pico; rough spatial contrast between the west (channel) coast, which is well surveyed, and the rest. Not usable for: monthly curves, condition response, or abundance. For the pelagic visitors the numbers are tiny (bluefish 3 records, Seriola 6 to 7, serra 20 in the Pico box). The published habitat models (Schmiing et al. 2013, and a 2014 follow-up in MEPS on "hotspots within hotspots" [U]) are a better way to use the same dive data than the raw points.

---

## 5. Do environmental variables actually predict nearshore catch? Solunar theory

*Provenance: this section was researched by a delegated sub-agent with the same "fetch, do not recall" brief. Its flags are kept: **[V]** = it read the finding on a fetched page (abstract or full text); **[S]** = existence confirmed in Crossref but the finding read only from a search-engine rendering. I did not re-open these papers myself. OpenAlex and Semantic Scholar rate-limited it and Elsevier abstracts were not retrievable.*

**Bottom line.** There is real but modest evidence, and almost none of it is from shore angling for the app's species. No peer-reviewed study was found that models rock or shore angling CPUE for *Diplodus*, bluefish, *Seriola*, barracuda or bonito against swell, tide, wind or pressure. Any rule in the app rests on analogues (squid jigging, gamefish, freshwater angling) and on telemetry of fish behaviour.

### 5.1 Studies checked

Reviews

| Study | URL / DOI | Finding | Flag |
|---|---|---|---|
| Stoner 2004, *J Fish Biol* | doi 10.1111/j.0022-1112.2004.00593.x | Baited-gear review: temperature, light, current velocity and prey density have the largest effects, "potentially affecting variation in CPUE by a factor of ten". Pressure and moon are not highlighted | V |
| Lennox et al. 2017, *Fish and Fisheries* | doi 10.1111/faf.12219 | Conceptual review of hook vulnerability (internal state, encounter, gear); no effect sizes | V |
| Hendricksen 2025, PhD thesis, Univ. of Kent | https://kar.kent.ac.uk/110991 | 1,323 English shore and private-boat sea-angling trips, 8 species, zero-inflated Poisson with LASSO. Trip duration, targeting and other fish caught were the important predictors; states that factors driving sea-angling catch "are still not well understood" | V |

Squid

| Study | URL / DOI | Finding | Flag |
|---|---|---|---|
| Cabanellas-Reboredo et al. 2012, *ICES JMS* 69:1823 | https://academic.oup.com/icesjms/article/69/10/1823/632887 | 55 experimental jigging sessions for *Loligo vulgaris*, Palma Bay. SST: -0.059 per C (about -6%). Wind: -0.171 per m/s (about -16%). Pressure: -0.055 per hPa (an implausibly steep -73% across 1008 to 1032 hPa, probably confounded at n = 55). New moon about 2.5x full moon. Sunset about 2.6x and after sunset about 2x the pre-sunset rate. No R2 reported. Percentages computed from the reported log coefficients | V (full text) |
| Cabanellas-Reboredo et al. 2014, *ICES JMS* | doi 10.1093/icesjms/fst206 | About where and when anglers choose to fish, not catch; sea conditions modulate effort | V |
| Masuda et al. 2014, *Fish Sci* | doi 10.1007/s12562-014-0799-6 | Japanese squid jigging: catch "mainly influenced by the lunar cycle", plus tide and wind direction | V (abstract) |
| Winter 2026, *Aquat Living Resour* | doi 10.1051/alr/2026021 | Falklands squid trawl: lunar phase significant in most seasons, explaining up to 26% of daily catch variation; maxima at new moon in winter | V |
| Chokka squid jig fishery, South Africa (Rhodes thesis; Roberts and Sauer) | not given | Catch falls as turbidity rises; easterly (upwelling) winds positive | S |

Moon and solunar

| Study | URL / DOI | Finding | Flag |
|---|---|---|---|
| Quigley et al. 2023, *SN Appl Sci* | https://link.springer.com/article/10.1007/s42452-023-05379-8 | 361 trout trips, 1,355 h, one angler, seven solunar services. No relationship between CPUE and any solunar rating, major / minor period, moon phase or illumination. The only significant peak-time result was negative (-42.5% inside a minor period). Moon phase explained 61% of the solunar ratings themselves. Air temperature was the only predictor. Cites a 1950 Clear Lake (Iowa) gill-net test of Knight's tables, also null | V (full text) |
| Hanson et al. 2008, *Fish Manag Ecol* | doi 10.1111/j.1365-2400.2008.00634.x | Largemouth bass telemetry: no repeatable lunar activity pattern; "solunar tables ... may have little predictive value" | V |
| Shaw, Renik and Sass 2021, *PLoS ONE* | https://pmc.ncbi.nlm.nih.gov/articles/PMC8483380 | 2,005 walleye and 2,771 muskellunge trips. Angler variables dominate. Moon overhead or underfoot (the solunar "major" periods) raised trip success slightly (walleye odds 0.47 vs 0.34; Cohen's d about 0.1). Dusk better than day. Pressure change not significant (p = 0.12 to 0.91) | V |
| Vinson and Angradi 2014, *PLoS ONE* | PMC4037224 | 341,959 muskellunge: lunar cycle significant but maximum effect about 5%; effort confounding not excluded | V |
| Stevenson and Millar 2013, *Environ Ecol Stat* | doi 10.1007/s10651-013-0236-5 | NZ recreational snapper with confounders controlled: lunar and Maori-calendar effects detectable but "magnitudes ... small, casting doubt on practical relevance" | V |
| Ortega-García et al. 2008, *Fish Res* 93:190 | https://repositoriodigital.ipn.mx/handle/123456789/13179 | Striped marlin sport fishing (not dolphinfish, as I had assumed in the brief). Moon under 1% of variance, SST 10%, ENSO 6%, vessel 1.5%, 53% unexplained | V |
| Lowry, Williams and Metti 2007, *Fish Res* 88:15 | not given | 381 tournament days, NSW: 5 of 8 gamefish species showed lunar patterns with different peak phases; 3 null. Effect sizes not obtained | V (secondary summary) / S (abstract) |
| Pulver 2017, *NAJFM* | doi 10.1080/02755947.2017.1293574 | Gulf of Mexico reef fish: lunar effect for 2 of 5 species, with opposite phases and inconsistency between gears | V |
| Poisson et al. 2010, *Fish Bull* 108:268 | https://archimer.ifremer.fr/doc/00011/12237 | 2,009 longline sets: swordfish CPUE higher at the quarters, albacore at full moon | V |
| Kuparinen et al. 2010, *Fish Res* 105:111 | not given | Pike: higher CPUE in cold water, high wind, around full and new moon, and at dusk; recent fishing effort lowers it | S |
| Arlinghaus et al. 2017, *Fish Res* 186 | not given | Pike whole-lake experiment: depth, lure, angler and site matter; explanatory power "only moderate" | S |

Sparids, bluefish, carangids and Macaronesia

| Study | URL / DOI | Finding | Flag |
|---|---|---|---|
| Giacalone et al. 2022, *Environ Biol Fish* | doi 10.1007/s10641-022-01258-0 | Review of 27 *Diplodus sargus* movement papers. Activity is diurnal; in the Azores feeding starts at sunrise and peaks from midday to early afternoon (Figueiredo et al. 2005). Feeding areas are high-hydrodynamic zones on rising or high tide (Belo et al. 2016). Foraging can switch to nocturnal under predation risk | V |
| Aspillaga et al. 2016, *PLoS ONE* | PMC4954665 | 41 tagged *D. sargus*: they leave the shallow wave-exposed zone for deeper water in storms | V (abstract plus the review) |
| Payne et al. 2013, *Proc R Soc B* | doi 10.1098/rspb.2012.2363 | Sparid *Acanthopagrus australis*: rain and turbidity reverse the activity rhythm from diurnal to nocturnal until the water clears | V |
| Brodie et al. 2018, *ICES JMS* | doi 10.1093/icesjms/fsy057 | Tailor (= bluefish, Australia), 20,878 tags: distribution non-linear in SST, peaking at 21.5 C | V |
| Brodie et al. 2015, *Fish Oceanogr* | doi 10.1111/fog.12122 | Recreational data: SST, fronts and eddies predict *Seriola lalandi* and dolphinfish occurrence | V |
| Jurado-Ruzafa et al. 2024, *JMBA* | doi 10.1017/S0025315424000754 | Canary Islands small pelagics: chlorophyll predicts landings one year later; SST not significant | V |
| Veiga et al. 2010; Rangel and Erzini 2007; Font and Lloret 2011; Diogo and Pereira 2014 | abstracts | Creel surveys with baseline CPUE (about 0.5 fish per angler-hour in northern Portugal) and no environmental modelling in the abstracts. Rangel and Erzini mention "factors influencing catches" but full text not obtained | V (abstracts) |
| Alós et al. (Mallorca) | not given | Work found concerns behavioural and morphological vulnerability to angling, not weather | V |
| Heupel et al. 2003, *J Fish Biol* | doi 10.1046/j.1095-8649.2003.00250.x | Juvenile blacktip sharks left the shallows as pressure fell ahead of a tropical storm | V |
| Attwood 2003 (galjoen, South Africa) | not given | Exists; environmental content not retrieved | U |
| Azores bait-boat tuna vs SST | none | No CPUE vs SST paper found; SST appears only as a covariate in dolphin-interaction models | S |

### 5.2 Verdict by variable (shore catch, the app's kind of species)

| Variable | Evidence | Functional form the evidence supports |
|---|---|---|
| SST / season | Moderate to strong, but mostly about presence rather than bite rate | Species-specific band or optimum (bluefish about 21.5 C in Australia; squid better when cold). Use it seasonally, not day to day |
| Time of day | Strong; the best supported variable | Dusk / sunset peak for squid and predators (about 2 to 2.6x). Daytime for *D. sargus*, shifting to night in turbid or risky conditions |
| Moon phase | Contradictory and small | Squid: new moon better (moderate). Fish: species-specific, often null, typically 5% or less, under 1% of variance |
| Wind speed | Weak to moderate | Negative for boat jigging; partly a fishability and effort effect. Direction matters only through local upwelling or exposure |
| Swell / waves | No direct CPUE evidence for shore sparids | Telemetry implies an intermediate band: fish feed in hydrodynamic zones but leave the shallows in storms. Treat the "white water" rule as angler lore plus a storm cut-off |
| Tide | Weak, indirect | Rising or high tide gives *D. sargus* access to feeding areas; no angling CPUE test found |
| Barometric pressure / trend | None to contradictory | Null in the largest test; one small-sample negative; behavioural response only to storm-scale drops (a threshold) |
| Turbidity / rain | Weak to moderate, species-specific | Negative for squid; shifts sparid activity toward night |
| Chlorophyll | No evidence at trip scale | Lagged (about one year) effect on small-pelagic landings only |

### 5.3 Solunar tables

Not supported. The two direct tests of the tables (a 1950 gill-net test and the 2023 trout study) are null, and telemetry shows no repeatable lunar activity pattern. The one positive hint for moon overhead / underfoot (Shaw et al. 2021) is a very small effect in two freshwater species. Solunar ratings are mostly a re-encoding of moon phase. If the app shows them at all, label them as tradition and give them a weight near zero.

### 5.4 How much do such models explain?

- Where reported, single environmental variables explain roughly 0 to 10% of CPUE variance (moon under 1%, SST 10%), with an outlier of up to 26% for the lunar effect on squid trawl catch.
- Half or more stays unexplained even with vessel and year terms (53% in Ortega-García et al.).
- Angler skill, effort, site, bait and targeting consistently outweigh weather (Shaw, Hendricksen, Arlinghaus).
- Honest framing for the app: conditions shift the odds by tens of percent at best (up to about 2x for dusk and for the squid moon effect); the output is a weak prior, not a forecast, and most of the numbers come from other species and gears.


---

## 6. Regulations an app should respect or display

Caveat for the whole section: I read primary legal texts where I could reach them, but **I could not confirm the current consolidated version of every act** (the official journal API blocks scripts). Items marked [V] are verified in the text of the act cited, as of that act's date. Show a "check current rules" link in the app rather than presenting these as authoritative.

### 6.1 Licence, bag limits, gear (Decreto Legislativo Regional 9/2007/A, 19 April 2007)

Source: original text, Diário da República 1.ª série no. 77, 19 Apr 2007, PDF at https://dre.pt/application/conteudo/519398 [V]. Record page: https://diariodarepublica.pt/dr/detalhe/decreto-legislativo-regional/9-2007-519398

- **Licence** (art. 28): recreational fishing needs a licence **except** hand gathering, **fishing from shore** (or from a moored boat / floating platform), sport-fishing competitions and tourist fishing (covered by the operator's licence). Licences exist only for spearfishing (personal) and for use of a boat. [V] The 2022 DRP / ICES document confirms shore angling still needed no licence then. [V]
- **Daily bag limit from shore** (art. 13.1): per angler per day, **7.5 kg of fish under 40 cm total length, plus 5 fish of 40 cm or more**. [V in the 2007 text]
- From a boat (art. 13.2): the same per person, capped at 20 kg under 40 cm plus 15 fish of 40 cm or more per boat. [V]
- Spearfishing (arts. 8 and 16): 10 fish and octopus per day, 2 crustaceans; no spearfishing at night, within 300 m of / inside class A to C ports, within 100 m of class D ports and bathing areas. [V]
- **Gear from shore** (art. 11): hand line, rod, or lure cast from shore, each with **at most 9 hooks**. [V]
- **Bathing areas** (art. 20): no recreational fishing within **50 m of bathing areas from 1 June to 30 September**. [V]
- **Tail marking** (art. 18): every fish of **25 cm or more** must be marked with a cut in the caudal fin (as drawn in the decree's annex, without removing the fin) **before leaving the fishing spot**. [V]
- **Sale of recreational catch is prohibited**; the same article also restricts donation and abandonment (details not extracted). [V for the sale ban]
- Only the angler who caught a fish may keep or carry it (art. 17). [V]
- **Unverified whether these numbers have since changed.** A government proposal to amend the decree (https://servicos-sraa.azores.gov.pt/grastore/SRMCT/Proposta_Alteracao_DLR_9_2007_A.pdf) would cut the shore limit to 3.5 kg under 40 cm plus 3 fish of 40 cm or more [V that the proposal says this]. I found no evidence that it was enacted; 2024 and 2025 portarias cite the decree "na sua redação atual" (as amended), and the only amendment I could identify is DLR 15/2012/A revoking art. 16(5)(b). [U]

### 6.2 Minimum sizes and closed seasons (Portaria 74/2015, as republished by Portaria 52/2020 of 8 May 2020)

Source: https://jo.azores.gov.pt/pdf/atos/52-I-Portaria-2020-05-08.pdf [V]. Applies to commercial **and recreational** fishing. Fish are measured snout to tail tip. Undersized fish must go straight back.

| Local name | Species | Minimum size |
|---|---|---|
| Veja | *Sparisoma cretense* | 300 mm |
| Sargo | *Diplodus* spp. | 150 mm |
| Garoupa | *Serranus* spp. | 300 mm |
| Mero | *Epinephelus marginatus* | 600 mm |
| Badejo | *Mycteroperca fusca* | 500 mm |
| Pargo | *Pagrus pagrus* | 300 mm |
| Goraz / Peixão | *Pagellus bogaraveo* | 330 mm, **but shore anglers using hand lines or rods are exempt** (art. 6.1), so shore-caught "carapau" are legal |
| Besugo | *Pagellus acarne* | 180 mm |
| Salema | *Sarpa salpa* | 180 mm |
| Boga | *Boops boops* | 150 mm |
| Salmonete | *Mullus surmuletus* | 150 mm |
| Congro / Safio | *Conger conger* | 1,400 mm or 5.5 kg |
| Boca-negra | *Helicolenus dactylopterus* | 300 mm |
| Alfonsim / Imperador | *Beryx* spp. | 350 mm |
| Raia | *Raja* / *Leucoraja* spp. | 520 mm |
| Atum-patudo | *Thunnus obesus* | 10 kg |
| Lapa-brava / Lapa-mansa | *Patella aspera* / *P. candei gomesii* | 50 mm / 30 mm |
| Cavaco / Santola | *Scyllarides latus* / *Maja brachydactyla* | 77 mm / 100 mm carapace |

- **No minimum size is listed for bicuda, anchova, írio, serra or morays.** [V for this version]
- **Closed seasons** (annex II): no fish closed season (the fish entry is "revoked"). Limpets 1 October to 31 May; slipper lobsters 1 May to 31 August; spiny lobster and spider crab 1 October to 31 March; clam 15 May to 15 August. [V]
- Whether the annex has been amended since May 2020 is unverified. [U] The Santos et al. 2020 synopsis independently confirms veja went from 25 cm (Portaria 21/2019) to 30 cm (Portaria 63/2019). [V]

### 6.3 Species-specific limits and closures

- **Veja quota closes recreational fishing island by island.** Governing act: Portaria 112/2023 of 15 December 2023, which is still the act in force in 2026: it has been amended five times (113-A/2025, 139-B/2025, 47/2026, 97/2026) and was most recently amended and republished by **Portaria 115/2026 of 23 October 2026** (https://jo.azores.gov.pt/pdf/atos/115-I-Portaria-2026-10-23.pdf) [V]. Current text [V]: annual veja quota 240,005.6 kg, split by island, **Pico 32.499% = 78,000 kg**, Faial 2.5% = 6,000 kg, São Jorge 2.22% = 5,328 kg (figures from the 2025 republication; the Pico figure is unchanged in the October 2026 text). Art. 9: when an island's veja quota is used up, **recreational capture of veja on that island is prohibited immediately**; and exhaustion of any annex I quota (abrótea, badejo, boca-negra, cântaro, garoupa, mero, raia, veja) immediately closes recreational capture of that species region-wide. Recreational capture of mako sharks (*Isurus* spp.) is prohibited. Garoupa annual quota is 50,000 kg in the October 2026 text. An app cannot know closure status without checking the Direção Regional das Pescas notices; I did not find a machine-readable feed of closures. [U]
- **Mero and badejo** (Portaria 1/2024 of 5 Jan 2024, https://pescador.azores.gov.pt/Sto/Documentos/Documento_0102202410472300928352406.pdf) [V]: recreational limit of one mero per boat per trip and one badejo per boat per trip (per spearfisher for badejo); **spearfishing mero is prohibited**. The text is written per boat; how it applies to a shore angler is not explicit. Treat both as release species in the app.
- **Goraz / peixão / carapau**: when the goraz quota for an island closes, recreational capture closes too (Portaria 13/2026 of 11 Feb 2026, art. 10.7, https://jo.azores.gov.pt/pdf/atos/13-I-Portaria-2026-02-11.pdf) [V]. TAC for ICES subarea 10 is 382 t (2026) and 426 t (2027).
- **Bluefin tuna, bigeye, swordfish, marlins**: boat-only, tag / authorisation regime (Portaria 1/2024, Portaria 52/2020 annex IV). Not relevant from shore.
- Prohibited species list in DLR 9/2007/A art. 22 starts with seahorses; I did not extract the full list. [U]

### 6.4 Protected areas around Pico

Network status as of 2026 [V from the legal texts]:

- The Azores MPA network (RAMPA) was created by Decreto Legislativo Regional 14/2024/A of 24 December 2024, amended by DLR 22/2025/A (9 October 2025) and DLR 6/2026/A (3 March 2026, https://jo.azores.gov.pt/pdf/atos/6-A-I-Decreto_Legislativo_Regional-2026-03-03.pdf). The republished text says it **entered into force on 1 January 2026**. (Some press reports say 1 January 2025; the republished law text I read says 2026, apparently after a postponement.)
- It covers 30% of Azorean waters (about 287,000 km2), half fully protected and half highly protected. [S, press] In **oceanic** areas classed as marine nature reserve, all commercial fishing **and all recreational fishing** (leisure, sport, tourist, spearfishing) are prohibited (art. 76). In oceanic habitat / species management and resource management areas, recreational fishing is "conditioned and subject to authorisation" (arts. 81 onward). The March 2026 amendment concerns pole-and-line tuna fishing. [V]
- **These new rules are for the oceanic (roughly 6 to 200 nautical mile) Azores Marine Park.** The one named after Pico is PMA28, a habitat / species management area (the article calls it "Pico Sudeste", the annex "Pico Sudoeste"); I did not map its limits. [U] Relevant to boats, not to shore anglers.
- **Coastal MPAs (0 to 6 nm) have not been redrawn yet.** The law folds the existing island natural park marine areas into RAMPA unchanged (art. 31 to 34), under the park decrees and management plans; a separate participatory revision of the coastal network is announced in the management strategy approved by Resolução do Conselho do Governo 157/2025 of 10 December 2025 (https://jo.azores.gov.pt/pdf/atos/157-I-Resolu%C3%A7%C3%A3o_do_Conselho_do_Governo-2025-12-10.pdf), and the law must be revised within three years to harmonise coastal and oceanic regimes. [V] No Pico-specific coastal proposal or public consultation was found. **Expect coastal no-take zones around Pico to change in the next few years; the app should not hard-code them.**

Existing coastal protected areas on Pico (DLR 20/2008/A, Pico Natural Park, https://dre.pt/application/conteudo/456524; listed again in DLR 6/2026/A art. 31) [V]:

| Code | Area | App spot affected | What the park decree itself says about fishing |
|---|---|---|---|
| PICO20 | Resource management area of Porto das Lajes | Lajes do Pico | No angling ban in the decree; includes a **limpet no-take reserve** zone; overlaps the Lajes do Pico Natura 2000 site |
| PICO21 | Resource management area of Ponta da Ilha | Ponta da Ilha | No angling ban in the decree; bans disturbance of seabird nesting; noise from boats near colonies is conditioned |
| PICO22 | Resource management area of the Faial-Pico Channel, Pico sector | Madalena | No angling ban in the decree; includes the Ilhéus da Madalena Natura 2000 site and a limpet no-take reserve zone |

- "Resource management" is the lightest category: the stated aim includes sustainable fishing. Only these three are listed as Pico's coastal MPAs in art. 31 of the RAMPA law, so São Roque and Calheta de Nesquim are not inside a listed coastal MPA. [V for the list; I did not check boundaries on a map]
- **Faial-Pico Channel fishing restrictions (Portaria 53/2016 of 21 June 2016)** [S only, the act itself could not be opened]: sets specific rules for three zones: Monte da Guia (Faial), **Ilhéus da Madalena** and **Baixa da Barca**. Reported content: around the Ilhéus da Madalena commercial and recreational fishing are prohibited **except shore fishing between two defined vertices and live-bait capture**; at Baixa da Barca (an offshore shoal north of Madalena) all commercial and recreational fishing is prohibited. Check the text and polygon before showing anything on the map; I could not verify whether it has been amended.
- The Pico Natural Park management plan (Decreto Regulamentar Regional 18/2020/A, https://servicos-sraa.azores.gov.pt/grastore/DSCN/PGPNI/Pico/PG_PNI_PIC_DRR_18_2020_A.pdf) lists "recreational fishing" and "fisheries regulation" among management measures but I found no explicit angling prohibitions in the text extracted. [V that the document exists; content only skimmed]

### 6.5 What the app can reasonably display

- "No licence needed for rod fishing from shore" with a link to the fisheries directorate.
- Minimum sizes next to each species (veja 30 cm, sargo 15 cm, garoupa 30 cm, etc.) and "no minimum size set" for bicuda, anchova, írio, serra, morays.
- A release-only flag for mero and badejo.
- A standing warning on veja and garoupa: "closes when the island quota is reached; check current notices".
- Bag limit and tail-marking rule, labelled "as of the 2007 decree; confirm current values".
- Bathing-area exclusion 1 June to 30 September (relevant to harbour spots with bathing zones).
- A note on Madalena that the islets zone has special fishing rules.

---

## 7. Suggested shore species list for Pico

Tiering uses: the DRP "most common recreational species" list, the Madeira shore-catch shares, the Faial / Pico dive-survey abundance, SREA landings on Pico, and GBIF / iNaturalist presence around Pico. It is a judgment built on those sources, not a measured Pico shore catch composition (that sits in the paywalled Diogo & Pereira 2014 tables).

**Core (already in the app; keep, with name fixes)**

1. Sargo, *Diplodus sargus*. Most abundant shallow reef fish around Faial / west Pico; top shore species in Madeira.
2. Veja, *Sparisoma cretense*. Pico is the regional veja island. Daytime only. Min 30 cm; quota closures.
3. Bicuda, *Sphyraena viridensis*. Late spring to November.
4. Anchova, *Pomatomus saltatrix*. July to September.
5. Írio / lírio, *Seriola rivoliana* and *S. dumerili* (rename from "charuteiro"). June to September; occasional from shore.
6. Serra, *Sarda sarda* (rename from "bonito"). Small volumes, spring to autumn.
7. Moreias: *Muraena helena*, *M. augusti*, *Gymnothorax unicolor*. Not in the landings table; presence well recorded.

**Strong candidates to add**

8. Garoupa, *Serranus atricauda*. Named by DRP as heavily targeted by recreational fishers; 151 GBIF records around Pico; min 30 cm; quota species.
9. Chicharro, *Trachurus picturatus*. Harbour and pier staple; biggest small-pelagic landing on Pico, year round with a dip from August.
10. Cavala, *Scomber colias*.
11. Carapau / peixão (juvenile *Pagellus bogaraveo*) and besugo (*Pagellus acarne*). Shore anglers have an explicit size exemption for the former.
12. Encharéu, *Pseudocaranx dentex*. 7.3 t landed on Pico, June to November.
13. Salema, *Sarpa salpa*, and tainha, *Chelon labrosus*. Float / bread fishing in harbours; both common in surveys and in the Madeira shore catch.
14. Prombeta, *Trachinotus ovatus*. Surf-zone pelagic; 4% of the Madeira shore catch.
15. Peixe-porco, *Balistes capriscus*. Summer; common in dive records.
16. Bodiões and peixe-rei (*Labrus bergylta*, *Centrolabrus caeruleus*, *Coris julis*, *Thalassoma pavo*), boga (*Boops boops*). The realistic everyday bait catch.
17. Lula (*Loligo forbesii*) and polvo (*Octopus vulgaris*) if cephalopods are in scope. Squid is landed on Pico all year.

**Occasional or boat-mostly**: pargo, abrótea, congro (night), patruça, salmonete, peixe-agulha, rascaço. **Do not target / release**: mero, badejo.

---

## 8. Biggest gaps

1. **No verified Pico shore-angling catch composition.** Diogo & Pereira 2014 has it for Faial and Pico (2004 to 2005) but only the abstract was accessible. Getting the PDF (author request, library) is the single most valuable follow-up.
2. **Only 20 months of monthly species landings (Mar 2025 to Oct 2026) are retrievable today.** The SREA rolling file must be collected over time, or the report viewer opened in a browser to see how far back the monthly pivot goes. Timing of the seasonal peaks repeated across the two summers; amplitudes did not.
3. **No per-port or per-spot data.** Everything is island level. Differences between the five spots can only be argued from habitat (exposure, depth, harbour vs open rock), using Schmiing et al. 2013 for the west coast.
4. **Anchova, serra and morays have no Azores ecology study at all**; morays also have no landings line. For anchova and serra the SREA landings curve is the only local evidence.
4b. **Swell, tide and moon effects on shore catch are essentially unmeasured** for every species here; nothing in the literature can replace the app's wave band or tide weights with numbers.
5. **Lotaçor's own site** could not be reached, so its filters and export options are unknown.
6. **Current consolidated law**: shore bag limit (7.5 kg + 5 fish) and tail-marking are verified only in the 2007 text; the minimum-size table only as of May 2020; Portaria 53/2016 (Madalena islets) was not opened. There is no machine-readable source for quota closures.
7. **No angler-report corpus** for Pico was found online.

---

## Appendix: files produced in this session

All under `<scratch>/`:

- `occ_counts.txt`: raw GBIF / OBIS / iNaturalist counts (pipe-separated).
- `fishbase_out.txt`: raw FishBase pulls (traits, temperature, ecology flags, spawning rows, Portuguese names).
- `srea/Q4_out_26.xlsx`: SREA landings by species and island, Nov 2025 to Oct 2026 (plus Q1, Q2, Q5 files).
- `scripts/`: `occ.py`, `facets2.py`, `ds.py` (occurrence APIs); `fb2.py` (FishBase parquet via DuckDB); `xl2.py` (SREA extraction); `oa.py` (OpenAlex abstracts).
- `dl/` and `txt/`: downloaded legal texts and papers with Ghostscript text conversions.
- `oa.sh`, `core.sh`, `pdftxt.py`, `r/`: helper scripts and scratch files left by the two delegated research threads (a hook blocked their deletion). Safe to ignore.

## Fish added 2026-11-26 from the owner's catch photos

Identified by eye from the owner's catch photos and added to `data/species.json`: blacktail comber (garoupa, 13 photos), grey triggerfish (peixe-porco, 7), pompano (prombeta, 5), blue jack mackerel (chicharro, 4), red scorpionfish (rocaz, 1 to 2), island grouper (badejo, 1), two-banded seabream (safia, 1), lizardfish (1) and bogue (boga, 1). Left out as too small to target (ornate wrasse, Azores chromis) or not identified with confidence (garfish, ballan wrasse, axillary seabream, a small eel).

- Seasons: SREA Pico landings through `tools/season.py` (Peixe Porco, Prombeta, Rocaz, Badejo and Safia added to `docs/research/scripts/srea.py`). Thin series: prombeta (median 77 kg a year), boga (44), badejo (16) and safia (10 years with landings). Lizardfish has 18 kg in 32 years ("lagarto da costa"), so its season is a flat guess, marked `ev.season: "estimated"`, and the Seasons tab shows it last with no score.
- Time of day: "measured" where the 2004-05 Faial/Pico shore survey separates day and night (recreational-catch.md 3.2: comber, triggerfish and pompano more by day, triggerfish only by day, jack mackerel and bogue both); estimated for the rest (scorpionfish and grouper treated as dusk and night feeders, safia like sargo).
- Base (shore catch rate) [I]: jack mackerel 0.75 and comber 0.8 (common in the survey and in the owner's photos), triggerfish 0.6, pompano 0.55, safia 0.55, bogue 0.45, scorpionfish, grouper and lizardfish 0.5. The lowest are held at a level where the best spot, month and time can still reach Possible (45), as the tests require for every fish.
- Rules: badejo (Mycteroperca fusca) has a 50 cm minimum size and a recreational limit of one per boat per trip (section 6); garoupa 30 cm and boga 15 cm minimums.
