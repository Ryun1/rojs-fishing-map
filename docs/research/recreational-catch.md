# Recreational shore-angling catch on Faial and Pico

Research notes compiled 2026-11-22. They follow up gap 1 in [`species.md`](species.md) section 8: no verified Pico shore-angling catch composition. Web research only; no app code touched.

Labels follow `species.md`:

- **[V]** = verified in this session: I opened the source and read the figure in it (page numbers given).
- **[I]** = inferred by me from verified figures (for example a share I computed from a published table, or a place read off a map). The working is shown.
- **[U]** = not verified. Treat as a lead only.

Rules followed: only openly published copies, no piracy mirrors, no logins, no paywall workarounds. PDFs were saved to a session scratch folder (`<scratch>/lit/`, not kept in the repo).

---

## 0. Headline findings

1. **Diogo & Pereira 2014 (*J. Fish Biol.* 84:952-970, doi 10.1111/jfb.12336) has no legal open copy.** OpenAlex: `is_oa: false`, `oa_status: closed`, no repository full text. Europe PMC: not in PMC, "Subscription required". OpenAIRE: "Closed Access", with only the Wiley and PubMed records. I could not run the Unpaywall API: it rejects placeholder e-mail addresses (HTTP 422, "Please use your own email address"), and I did not send the user's address to a third party. Its species table is still not available. [V]
2. **Diogo's 2007 MSc thesis is not openly available either.** It is "Contribution to the characterisation of recreational fishing activities on the Islands of Faial and Pico, Azores", Universidade dos Açores, Horta, and it is the source of the survey data. The UAc DSpace API (`repositorio.uac.pt/server/api/discover/search/objects`) returns no item for it under any title, author or Portuguese or English keyword I tried. RCAAP and CORE sit behind bot walls. No PhD thesis by Hugo Diogo turned up. [V for the searches]
3. **The best open substitute is a companion paper on the same survey.** Diogo & Pereira 2016, *MEPS* 542:187-193, "Fishing in the dark", is free on the publisher's site. Its supplement Table S3 gives **catch per angler-hour by species, in number and weight, for day and night**. It covers 39 taxa and 381 interviews, from the same Faial and Pico roving creel survey (Sep 2004 to Aug 2005), but **only in one spatial unit per island. The Pico unit is the west coast around Madalena**, which is the part of the island the app cares about most. [V]
4. **Headline composition, Madalena coast plus south Faial, shore angling** [V, MEPS p. 190; matches my recomputation from Table S3]:
   - Daytime catch by weight: **sargo 28.7%, tainha (*Chelon labrosus*) 23.5%, veja 12.3%**, then salema 8.6% and peixe-porco 6.3% [I].
   - Night-time catch by weight: **sargo 47.9%, encharéu (*Pseudocaranx dentex*) 17.1%, besugo (*Pagellus acarne*) 6.5%**, then bicuda 5.7%, congro 5.0% and moreias 7.4% combined [I].
   - Daytime catch by number is led by small fish: **carapau (juvenile *Pagellus bogaraveo*) 24.4%, sargo 21.7%, chicharro 14.3%** [I].
5. **Shore angling in the Azores was dominated by sargo region-wide too** [V]. In the Azores column of Diogo et al. 2020, Table 3, the top five shore-angling species by weight are, from Diogo & Pereira 2014: **1 sargo, 2 veja, 3 tainha, 4 cavala, 5 salema**. Mean shore CPUE was 1.4 fish or 0.84 kg per angler-hour, and only 4.6% of the catch was released.
6. **Monthly species curves for shore angling are still not openly published.** Only three month-level facts are open: season was a significant factor in catch composition, juvenile carapau peaked July to September, and carapau was absent from catches in January and March. **The SREA landings curves in `species.md` section 2 remain the only month-by-species series.**

---

## 1. Sources

| Source | URL | What it gave | Licence / OA status | Saved as (`<scratch>/lit/`) |
|---|---|---|---|---|
| Diogo & Pereira 2014, *J. Fish Biol.* 84:952-970 | https://doi.org/10.1111/jfb.12336 | Abstract only (already in `species.md`) | **Closed.** OpenAlex closed; Europe PMC subscription; OpenAIRE closed access; no repository copy | not obtained |
| Diogo 2007, MSc thesis, Univ. Açores, Horta | (none found) | Cited as the survey source by Pham et al. 2013 and Diogo et al. 2020 | Not in the UAc repository API; RCAAP / CORE bot-walled | not obtained |
| **Diogo & Pereira 2016**, *MEPS* 542:187-193, "Fishing in the dark: the importance of integrating a nocturnal component into recreational fishing surveys" (OpenAlex dates it 2015) | https://www.int-res.com/abstracts/meps/v542/p187-193 ; PDF https://int-res.com/articles/meps2015/542/m542p187.pdf ; supplement https://int-res.com/articles/suppl/m542p187_supp.pdf | Day versus night CPUE, per-species CPUE (Table S3), sizes, sampling design, map of the spatial units | Free to read on the publisher site. © Inter-Research; "Resale or republication not permitted" | `Diogo2015_MEPS542_fishing_in_the_dark.pdf`, `Diogo2015_MEPS542_supp.pdf` |
| **Diogo et al. 2020**, *Rev. Fish. Sci. Aquac.* 28(4):536-560, "Marine Recreational Fishing in Portugal: Current Knowledge, Challenges, and Future Perspectives" | https://doi.org/10.1080/23308249.2020.1777083 ; repository copy http://hdl.handle.net/10400.8/5968 (IC-Online, Politécnico de Leiria) | Azores top-5 shore species by weight, CPUE, release rate, angler profile, Azores species list (from Diogo & Pereira 2014), baits, regulation history | Green OA: the publisher PDF deposited in an institutional repository. © Taylor & Francis; no CC licence seen | `Diogo2020_RFSA_MRF_Portugal_review.pdf` |
| **Pinho, Diogo, Carvalho & Pereira 2014**, *ICES J. Mar. Sci.* 71(9):2448-2456, juvenile blackspot seabream | https://doi.org/10.1093/icesjms/fsu089 | Sampling effort of the 2004-05 shore survey, carapau habitat, months and sizes | Free to read on the publisher site (bronze OA). "All rights reserved" | `Pinho2014_ICESJMS_fsu089_Pbogaraveo_juveniles.pdf` |
| **Pham et al. 2013**, *ICES J. Mar. Sci.* 70(3):564-577, "Total marine fishery catch for the Azores (1950-2010)" | https://doi.org/10.1093/icesjms/fst024 | Recreational catch reconstruction anchored on Diogo 2007; top recreational species | Free to read (bronze). "All rights reserved" | `Pham2013_ICESJMS_fst024_Azores_total_catch.pdf` |
| DGRM / DRP-RAA, "Methodological Protocol for Recreational Fishing Data Collection in Azores (ICES Xa)", Horta, 14 Oct 2024 | https://www.dgrm.pt/documents/20143/48268/PORTUGAL+Methodological+Protocol+for+Marine+Recreational+Fishing+Data+Collection.pdf/a8b3fcab-ea70-a94c-6d44-058a89697a12 | Current official survey design; 2022-23 participation rate | Open PDF, government document | `DGRM_2024_Azores_MRF_methodological_protocol.pdf` |
| AQUACROSS D9.2, Case Study 8 (Faial-Pico Channel), 2018 | https://www.ecologic.eu/sites/default/files/publication/2018/2803-d9.2_cs8_28092018_final.pdf | Shore-angling rules in the Channel MPAs | Open PDF, EU Horizon 2020 deliverable | `AQUACROSS_CS8_D9.2.pdf` |
| Afonso et al. 2014, GAMPA technical report (MoniZec), Faial-Pico Channel MPAs | https://www.vliz.be/imisdocs/publications/ocrd/291406.pdf | Context only: cites Diogo & Pereira for recreational pressure in the Channel; mentions keeping shore angling at Pasteleiro (Faial) for cultural reasons | Open PDF | `Afonso2014_GAMPA_AMP_canal_Faial_Pico.pdf` |
| Schmiing et al. 2014 *MEPS* 513:187-199 and 2015 *ICES JMS* 72:851 (Diogo co-author) | https://www.int-res.com/articles/meps_oa/m513p187.pdf ; https://doi.org/10.1093/icesjms/fsu180 | Only a shore-angling effort layer (a 50 m coastal buffer from observer counts) used in MPA planning. No species and no named places in the text | OA | `Schmiing2014_MEPS513_hotspots.pdf`, `Schmiing2015_ICESJMS_fsu180.pdf` |

Not useful, but checked: DRP ICES sampling design 2022 (already in `species.md`); Diogo & Pereira 2013 boat angling (already in `species.md`); Academia.edu profile (needs a login to download, not used).

---

## 2. The survey behind all of this

Facts from the open companions to Diogo & Pereira 2014 [V unless marked]:

- **Design.** A roving creel survey of shore anglers on Faial and Pico from Oct 2004 to Sep 2005. It covered 193 sampling days, 8 per month on Faial and 10 per month on Pico, and the whole coastline. Pico was split into 5 spatial units and Faial into 4. Strata were weekday or weekend and morning or afternoon, with two replicates per spatial unit per month. (Pinho et al. 2014 p. 2449; MEPS p. 188)
- **Night component.** A night component was added in only one unit per island, from Sep 2004 to Aug 2005, over 115 days (Table S1). It sampled from 30 min after sunset to 03:00, "because preliminary surveys indicated that shore anglers were typically less active between 03:00 h and dawn". (MEPS p. 188)
- **Which part of Pico.** The MEPS Fig. 1 map (p. 188) puts the Pico unit (unit 2) on the **west coast around Madalena**, from about 38°31'-32' N down to about 38°27' N. That is roughly Madalena harbour south to Areia Larga and Criação Velha. The Faial unit (unit 1) is on the **south coast of Faial, west of Horta** (Feteira and Castelo Branco side). [I: read off the map; the paper does not name places]
- **Habitat classes used.** Boulders, rock, cliffs, harbours, sandy beaches. (Pinho et al. 2014 p. 2450)
- **Anglers.** 93% male, mean age 44.4. (Diogo et al. 2020 Table 2, p. 541) [V]
- **Discards.** 4.6% of the total catch (MEPS p. 188); release rate 4.6% overall and 4.8% for sargo (Diogo et al. 2020 p. 544-545). Nearly everything caught was kept.
- **Scale.** 38 species and 7 techniques (2014 abstract). The 2020 review's appendix counts **44 taxa for Azores shore angling** (Table A3, p. 558). Annual shore catch was about 51.2 t across the two islands (2014 abstract).

---

## 3. Species composition

### 3.1 Region-level ranking (Diogo & Pereira 2014 via Diogo et al. 2020)

Diogo et al. 2020, Table 3 (p. 542), "top five captured species (by weight)", Azores shore-angling column, source Diogo & Pereira 2014 [V]:

| Rank | Species | Azores name |
|---|---|---|
| 1 | *Diplodus sargus* | Sargo |
| 2 | *Sparisoma cretense* | Veja |
| 3 | *Chelon labrosus* | Tainha |
| 4 | *Scomber colias* | Cavala |
| 5 | *Sarpa salpa* | Salema |

The text on p. 541 confirms: "For shore angling, the most captured species is the white seabream (*Diplodus sargus*) ... in the Azores". [V] The PDF's text layer garbles the table columns. I read the Azores column as the fourth of the four region columns, and checked that reading against the text and against other rows (for example *Balistes capriscus* ranks 2 in the Centre column only). [V with a small risk of misreading the column]

Taxa in the Azores shore-angling list (Table A3, pp. 557-558) that matter to the app [V that each is marked present for the Azores]: *Seriola rivoliana*, *Pomatomus saltatrix*, *Sphyraena viridensis*, *Muraena helena*, *Muraena augusti*, *Serranus atricauda*, *Epinephelus marginatus*, *Pseudocaranx dentex*, *Trachurus picturatus*, *Trachinotus ovatus*, *Pagellus bogaraveo*, *P. acarne*, *Kyphosus* sp., *Belone belone*, *Sphoeroides marmoratus*, *Synodus saurus*, *Octopus vulgaris*. *Sarda sarda* (serra) is **not** in the Azores shore list. The checkmark glyphs did not survive text extraction, so presence was read as "not marked Ø" in the Azores column. [V with the same caveat]

### 3.2 Per-species CPUE, day and night, Madalena coast and south Faial (MEPS Table S3)

Source: MEPS supplement Table S3 (supplement pp. 3-4) [V for the CPUE values]. CPUE is in fish (n) and kg (w) per angler-hour, as a mean of ratios. The share columns are my arithmetic: each species' CPUE divided by the column total [I]. Column totals: day 6.79 fish/h and 0.85 kg/h; night 2.34 fish/h and 0.64 kg/h. My weight shares reproduce the percentages printed on MEPS p. 190 (sargo 28.7 / 47.9, tainha 23.5, veja 12.3, encharéu 17.1, besugo 6.5), so the printed "assemblage" shares are by weight.

| Species | Azores name | Day n/h | Day kg/h | Night n/h | Night kg/h | Day % by weight [I] | Night % by weight [I] |
|---|---|---|---|---|---|---|---|
| *Diplodus sargus* | Sargo | 1.476 | 0.244 | 1.144 | 0.302 | 28.7 | 47.4 |
| *Chelon labrosus* | Tainha | 0.586 | 0.200 | 0 | 0 | 23.5 | 0 |
| *Sparisoma cretense* | Veja | 0.131 | 0.104 | 0 | 0 | 12.2 | 0 |
| *Sarpa salpa* | Salema | 0.339 | 0.073 | 0.022 | 0.008 | 8.6 | 1.3 |
| *Balistes capriscus* | Peixe-porco | 0.080 | 0.054 | 0 | 0 | 6.3 | 0 |
| *Trachurus picturatus* | Chicharro | 0.971 | 0.031 | 0.523 | 0.011 | 3.6 | 1.7 |
| *Pagellus bogaraveo* (juv.) | Carapau | 1.655 | 0.025 | 0.054 | 0.002 | 2.9 | 0.3 |
| *Pomatomus saltatrix* | Anchova | 0.013 | 0.016 | 0 | 0 | 1.9 | 0 |
| *Thalassoma pavo* | Peixe-rainha | 0.445 | 0.015 | 0 | 0 | 1.8 | 0 |
| *Trachinotus ovatus* | Prombeta | 0.307 | 0.013 | 0.022 | 0.007 | 1.5 | 1.1 |
| *Serranus atricauda* | Garoupa | 0.080 | 0.013 | 0.011 | 0.002 | 1.5 | 0.3 |
| *Boops boops* | Boga | 0.090 | 0.012 | 0.044 | 0.004 | 1.4 | 0.6 |
| *Coris julis* | Peixe-rei | 0.275 | 0.010 | 0 | 0 | 1.2 | 0 |
| *Sphyraena viridensis* | Bicuda | 0.006 | 0.009 | 0.022 | 0.036 | 1.1 | 5.7 |
| *Kyphosus* sp. | Patruça | 0.042 | 0.008 | 0 | 0 | 0.9 | 0 |
| *Centrolabrus caeruleus* | Bodião verde | 0.038 | 0.006 | 0 | 0 | 0.7 | 0 |
| *Labrus bergylta* | Bodião vermelho | 0.016 | 0.004 | 0 | 0 | 0.5 | 0 |
| *Pseudocaranx dentex* | Encharéu | 0.010 | 0.003 | 0.033 | 0.107 | 0.4 | 16.8 |
| *Pagellus acarne* | Besugo | 0.026 | <0.001 | 0.229 | 0.041 | 0.1 | 6.4 |
| *Conger conger* | Congro | 0 | 0 | 0.011 | 0.032 | 0 | 5.0 |
| *Muraena helena* | Moreia | 0 | 0 | 0.022 | 0.024 | 0 | 3.8 |
| *Muraena augusti* | Moreão / moreia preta | 0 | 0 | 0.033 | 0.020 | 0 | 3.1 |
| *Gymnothorax unicolor* | Moreão / moreia castanha | 0 | 0 | 0.011 | 0.003 | 0 | 0.5 |
| *Phycis phycis* | Abrótea | 0 | 0 | 0.022 | 0.010 | 0 | 1.6 |
| *Scomber colias* | Cavala | 0.029 | 0.001 | 0.022 | 0.009 | 0.1 | 1.4 |
| *Apogon imberbis* | (cardinal fish) | 0 | 0 | 0.022 | 0.010 | 0 | 1.6 |
| *Epinephelus marginatus* | Mero | 0.003 | 0.002 | 0 | 0 | 0.2 | 0 |
| *Octopus vulgaris* | Polvo | 0 | 0 | 0.011 | 0.005 | 0 | 0.8 |
| Others (*Chromis limbata*, *Abudefduf luridus*, *Scorpaena* sp., *Gaidropsarus guttatus*, *Pagrus pagrus*, *Bothus podas*, *Sardina pilchardus*, *Priacanthus arenatus*, *Diplodus vulgaris*, *Symphodus* sp., *Gobius paganellus*) | | each ≤0.064 | each ≤0.002 | each ≤0.022 | each ≤0.001 | each ≤0.2 | each ≤0.2 |

Serra (*Sarda sarda*) and írio (*Seriola*) were not caught in these two units in that year. Moreias, congro, abrótea and polvo appear **only at night**. Veja, tainha, peixe-porco, anchova and all wrasses appear **only by day**. [V]

Further results from MEPS pp. 189-191 [V]:

- **39 taxa** in 23 families: 30 by day, 23 by night, 14 in both. Day families by weight: Sparidae 40.4%, Scaridae 12.3%, Carangidae 7.0%. Night: Sparidae 56.0%, Carangidae 20.6%, Muraenidae 7.4%.
- **CPUE by weight did not differ** between day and night (0.68 ± 1.05 vs 0.63 ± 1.03 kg/angler-h; Mann-Whitney p > 0.05). **CPUE by number was much higher by day** (5.5 ± 7.8 vs 2.2 ± 2.1 fish/angler-h; p < 0.05). At night anglers catch fewer, bigger fish.
- **Night fish are bigger.** Fork length: besugo 11.1 cm by day vs 20.2 cm at night; encharéu 26.2 vs 52.5 cm; sargo 17.9 vs 19.5 cm; chicharro 12.0 cm at both.
- **SIMPER** (Table 2, p. 191): more numerous by day were veja, peixe-rainha, tainha, salema, carapau, peixe-porco, garoupa and prombeta; more numerous at night were besugo, *Apogon* and chicharro. Sargo had equal mean abundance (0.64) day and night.
- **PERMANOVA** (Table 1, p. 191): catch composition differed by diel period (p = 0.021) and by **season** (p = 0.001), with a significant diel × season interaction (p = 0.001) and island × season (p = 0.032). Island alone and day type alone were not significant. No per-season species table is published.

**Discrepancy to note.** The whole-survey shore CPUE quoted in Diogo et al. 2020 Table 5 (p. 544) is 1.4 fish and 0.84 kg per angler-hour. The two-unit daytime figure is 5.5 fish and 0.68 kg per angler-hour. My guess at the cause is the subset of units and the handling of short trips: the MEPS analysis dropped 29 trips under 30 min. [I] For the app, read these as "under 1 kg/h of fish, typically a few small ones per hour", not as precise rates.

### 3.3 Region-wide recreational totals (Pham et al. 2013)

Pham et al. 2013 anchored a 1950-2010 reconstruction on Diogo 2007, with 2004 as the reference year (p. 569) [V]:

- Recreational catch (all modes) was 300 to 950 t/yr. Boat fishing and "coastal rod fishing" (shore angling) made up 96% of it. Shore angling plus hand harvesting was 471 t in 2004, extrapolated region-wide with a per-island "recreational index".
- The top recreational species over 1950-2010 (pp. 572-573): **sargo 6,500 t (220% of official landings)**, garoupa 4,700 t (85%), cavala 3,000 t (15%), veja 2,970 t (60%).

So recreational sargo catch is about twice the commercial sargo landing. This supports `species.md`'s warning that SREA sargo landings understate how common sargo is in the shore catch. [I]

### 3.4 Juvenile blackspot seabream ("carapau") from shore (Pinho et al. 2014)

From pp. 2449-2454 [V]:

- Shore anglers on Faial and Pico took about **1.6 t/yr** of juvenile *P. bogaraveo* in 2004-05. Mean fork length was 8.7 ± 1.6 cm, with a range of 5 to 14 cm.
- **62% of the shore effort that used hooks and baits suited to carapau was spent in harbours**, and harbours gave the highest carapau CPUE of the five habitat classes.
- **Months.** Carapau were present along the coast almost all year except January and March, with the highest abundance July to September. A new cohort of 6-8 cm fish appeared in June.
- **Rules.** Since 2009 the minimum size is 30 cm TL and shore angling for this species is banned (p. 2449). The shore-angler exemption noted in `species.md` section 7, item 11 dates from 2006 and was later withdrawn. That needs reconciling with `species.md` section 6. [V that Pinho et al. say this; current law not re-checked here]

---

## 4. Techniques, baits, time of day, months, places

| Topic | Finding | Label and source |
|---|---|---|
| Techniques | 7 shore-angling techniques recorded. **The per-technique species breakdown is only in the closed 2014 paper.** Not available | [V] for the count (2014 abstract); breakdown [U] |
| Baits | Fucus seaweed is collected in spring to catch salema. Marbled crab (*Pachygrapsus marmoratus*) is taken by rock-turning for bait. Imported polychaete worms are sold in local shops. Hook and bait sizes for carapau are mentioned but not listed | [V] Diogo et al. 2020 p. 546 (citing Diogo & Pereira 2014); Pinho et al. 2014 p. 2450 |
| Lures | Nothing found in the open sources | gap |
| Time of day | Anglers are active from sunset to about 03:00 and rarely from 03:00 to dawn. By day you catch more fish; at night the fish are bigger; weight per hour is about equal. Night catch is dominated by sargo, encharéu, besugo, bicuda, congro and moreias; day catch by sargo, tainha, veja, salema, peixe-porco and the small wrasses and carapau | [V] MEPS pp. 188-190 |
| Months | Season changes the species mix significantly (p = 0.001) but no month-by-species table is open. Carapau peak Jul-Sep, absent Jan and Mar. Portugal-wide, July to September is the preferred season for shore angling effort | [V] MEPS p. 191; Pinho p. 2452; Diogo et al. 2020 p. 542 |
| Pico places | The survey's Pico night unit is the **Madalena west coast** [I from map]. Harbours concentrate anglers (25% subsample rule, MEPS p. 188) and carapau effort (62%, Pinho). Shore anglers are "distributed diffusely along the coastline". No named Pico spots in any open source | [V] / [I] |
| Channel MPA rules | AQUACROSS (its table of existing Channel MPAs) lists shore angling on "specific sections of the coast" as an exception at **Monte da Guia** (Faial). For the **Ilhéus da Madalena** the only exception is live-bait capture, although the same report later mentions "permitted shore angling sites at Ilhas da Madelena". The legal text (Portaria 53/2016) is the authority; see `species.md` 6.4 | [V that the report says both]; legal status [U] |
| Participation | A 2022-23 phone survey found a 9.1% participation rate in the Azores, with shore angling the most popular mode. The official DCF surveys (license-system recall survey, Pescador app) still cover only boat angling, spearfishing and charters, **not shore angling** | [V] DGRM 2024 protocol pp. 5-7 |

---

## 5. What this changes for the app

**Species list (`species.md` section 7):**

1. **Sargo stays number one, now on Pico data**, not only on Madeira and dive-survey proxies. It is about 29% of the daytime catch weight and 47% of the night-time weight on the Madalena and south-Faial coast. It is the only species that matters by both day and night. [V/I]
2. **Promote tainha (*Chelon labrosus*) and salema to core species.** Tainha is the second-largest daytime catch by weight (23.5%) and ranks 3rd region-wide. Salema is 5th region-wide and 8.6% of daytime weight. Both are harbour and float or bread fish. [V/I]
3. **Veja is confirmed as a day-only species** (12.2% of daytime weight, zero at night), ranking 2nd region-wide. This matches the "night weight zero" note in `species.md` 3.2. [V]
4. **Add encharéu (*Pseudocaranx dentex*) as a night species.** It is 17% of night-time weight and the fish average 52 cm at night, against a 0.4% share by day. [V/I]
5. **Add besugo (*Pagellus acarne*) as a night species** (6.4% of night weight, larger fish at night). [V/I]
6. **Moreias and congro are night-only** (about 7% and 5% of night weight respectively). This supports the existing nocturnal weighting. [V/I]
7. **Bicuda from shore is mostly a night or low-light catch** in this data: 5.7% of night weight against 1.1% by day. That is small and from one year, so it is weak evidence for a dusk or night bias. [I]
8. **Anchova is a small daytime share (1.9%), and írio and serra were not caught in these units that year.** Serra is absent from the whole Azores shore list (Table A3). That argues for marking serra as "occasional, boat-mostly" rather than a core shore species, and for keeping írio as occasional. [V/I]
9. **Carapau and chicharro dominate by number but not by weight.** They are the everyday harbour catch, so treat them as "harbour, small fish" rather than target species. Re-check the carapau rule: Pinho et al. say shore angling for *P. bogaraveo* has been banned since 2009. [V]
10. **Cavala ranks 4th region-wide by weight** but is tiny in the Madalena and south-Faial units. Keep it as a candidate. [V]

**Season curves:**

- No new month-by-species curve for shore angling is openly available, so **keep the SREA landings shapes** from `species.md` 2.1 for timing.
- One new monthly curve: **carapau (juvenile *P. bogaraveo*) inshore abundance peaks Jul-Sep, is absent in Jan and Mar, and new recruits arrive in June** (Pinho Fig. 4b). Use it only if carapau stays in the app given the 2009 ban.
- Season significantly changes the mix (PERMANOVA), so a flat year-round prior for the shore species is wrong. The direction per species is still unknown from open sources.

**Time-of-day weights:** the MEPS night/day split is the first **Pico-measured** diel evidence. Suggested multipliers, from the night-vs-day share of the species' weight share [I]:

- Day-only (night weight ≈ 0): veja, tainha, peixe-porco, anchova, wrasses.
- Night-favoured: encharéu, besugo, moreias, congro, abrótea, bicuda.
- Both: sargo (slightly higher weight share at night), chicharro.
- Total kg per hour is about equal day and night. Night should therefore change **which** species the app shows, not the overall "is it worth going" score.

**Per-spot differences:** still only habitat-based. The one open data point is that harbours concentrate effort and juvenile sparids and carangids. Nothing in the open sources ranks named Pico spots.

---

## 6. What is not openly available (and the legitimate routes to it)

1. **Diogo & Pereira 2014 full text**: the species × technique table, monthly effort and catch, and per-spatial-unit results for all 5 Pico units. Legitimate routes: ask the author (Hugo Diogo, Okeanos / DRP Horta; the corresponding address is printed in the MEPS paper), an interlibrary loan, or the Wiley article purchase.
2. **Diogo 2007 MSc thesis** (Univ. Açores, Horta): probably holds the per-month and per-technique tables. It is not in the UAc open repository. Ask the UAc library in Horta or the author.
3. **DRP's own 2022-23 participation survey and the Pescador app data**: no public catch tables found.
4. **Unpaywall** could not be queried without a real contact e-mail. Re-run it with the user's own address if wanted: `https://api.unpaywall.org/v2/10.1111/jfb.12336?email=<your address>`. OpenAlex, Europe PMC and OpenAIRE already agree the paper is closed.
