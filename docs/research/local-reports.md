# Local shore-angling reports for Pico (and Faial / São Jorge)

Gathered 2026-11-22. Follows up the gap in `species.md` section 1.2 ("no usable angler-report corpus for Pico").

Labels as in the other notes: **[V]** read in the source; **[I]** my inference; **[A]** anecdotal (forum, blog, one angler); **[S]** seen only as a search-engine snippet, page not opened (blocked or behind a licence gate).

Rules followed: no logins, no Facebook/Instagram, robots.txt checked, nothing fetched past Cloudflare challenges or TollBit licence redirects. Names of private individuals (competition winners, forum users) are left out on purpose.

## Verdict

- **Pico itself: still almost nothing structured.** Pico has competitions: the Associação de Pesca Desportiva da Ilha do Pico (APDIP) runs an island championship (at least nine rounds a season, per Clube Náutico das Lajes) and the Semana dos Baleeiros tournament in Lajes (since at least 2004; numbered "IV Torneio Regional de Pesca Desportiva de Costa" in 2025). Madalena added a tournament in 2025 at Porto Velho. But results are published only on Facebook, or not at all. The one Pico catch figure I found is from a Faial club's report: biggest fish at the 2012 Semana dos Baleeiros was a **veja of 2.21 kg** [V].
- **Faial: a small, good corpus exists.** Clube de Pesca Ilha Azul (CPIA) published a report for every shore-championship round in 2012-2014 on the Praia do Almoxarife parish site. Each gives date, coast, hours, target-species rule, groundbait allowed or not, fish count, total kg and the biggest fish. **22 rounds** are in `data/reports_found.json`. Clube Naval da Horta also runs a shore championship (2017-2022 news exists) but its site is behind a Cloudflare challenge.
- **São Jorge: nothing found** beyond an RTP headline about a "1º Torneio do Triângulo: 24 Horas a Pescar" at the Calheta Festival de Julho [S], with no results.
- **Forums and blogs: thin and anecdotal.** A few English and Portuguese threads name species and lures for the "triangle" islands. Most are behind TollBit or Cloudflare, so only snippets were usable.
- **Tackle shops: no public web presence on Pico.** One retailer appears only in a business directory snippet. No Lajes or São Roque shop was found.

**How usable for the app:** the Faial records are good enough to sanity-check **size ranges** and to show that **north-coast venues get swapped for the south coast in winter swell**. They **cannot** support species seasonality, because the club rules set which species count in each month (sargo rounds in Jan/Sep, veja rounds in Jun/Jul, wrasse rounds in Feb-Apr). They are also one sample per month, all daytime 4-hour rounds except two night rounds. Treat them as calibration anecdotes, not a training set. The real route to Pico data is still by hand: ask APDIP and the Lajes / Madalena clubs for their round sheets (contacts below).

## What the Faial records say (I, from the 22 rounds)

- **Biggest fish per round, by species** [V]: sargo 0.90-1.49 kg (7 rounds); veja 1.31-1.77 kg on Faial (6 rounds), 2.21 kg at Lajes do Pico (1); bodião / bodião vermelho 0.65-1.03 kg; garoupa 0.54 kg; rays 2.2-3.3 kg (both on mixed or night rounds); anchova 0.59 kg (October, Feteira); peixe-porco 0.93 kg (October).
- **Catch volume follows the rule set, not the month** [I]: groundbaited sargo rounds gave the biggest bags (114 kg / 11 anglers Jan 2012; 71 kg / 8 anglers Sep 2012; 35-36 kg Jan 2013 and Jan 2014). Veja rounds gave very few fish (18-30) of large average weight (0.6-0.8 kg each). Wrasse rounds gave many tiny fish (278-430 fish, 15-21 kg).
- **Night beach rounds were poor** [V]: Porto Pim in May, 26-38 fish both years. One night produced only a 3.3 kg ray as standout.
- **Sea state moves venues** [V]: five of 22 rounds were postponed (2) or moved (3) for sea or weather, all between October and March. Moves: Fajã (NW coast) to Lajinha (S coast), Jan 2013; Castelo Branco / Fajã to Laginha (S), Oct 2013; but Castelo Branco (SW) to Fajã (NW), Oct 2012. So the club moved to whichever side was sheltered on the day, which is the exposure logic in `spots.md`. The sources do not give the swell direction, so this is a qualitative check only [I].
- **No-groundbait rule matters** [V]: the club notes that only 3 of 9 championship rounds allow engodo (the two sargo rounds and the night round), and calls the no-groundbait rounds "much harder".

## Sources

| # | URL | Type | Date | Reliability | Used for |
|---|---|---|---|---|---|
| 1 | https://jfpalmoxarife.com/noticias/cpia/ (57 posts; list from `wp-sitemap-posts-post-1.xml`) | Club round reports (CPIA, Faial) hosted on Junta de Freguesia da Praia do Almoxarife site | 2012-01 to 2014-01 | **High** for date, venue, weights (organiser's own weigh-in). No species breakdown beyond biggest fish. | 22 records |
| 2 | https://jfpalmoxarife.com/noticias/cpia/clube-pesca-ilha-azul-vence-torneio-semana-dos-baleeiros/ | Club report of the Pico tournament | 2012-09-07 | High for the 2.21 kg veja; venue not stated (Lajes inferred from the 2013 report) | Pico record |
| 3 | https://jfpalmoxarife.com/noticias/cpia/clube-pesca-ilha-azul-vence-torneio-semana-dos-baleeiros-2013/ | Club report | 2013 (event 23 Aug 2013, Friday afternoon, "orla marítima das Lajes do Pico") | High; no weights | Event only |
| 4 | https://cm-lajesdopico.pt/25027/iv-torneio-regional-de-pesca-desportiva-de-costa---semana-dos-baleeiros-2025 | Municipal announcement | 2025-08-27 (event 30 Aug 2025, 08:00, Baía das Lajes) | High for the event; no results published | Event only |
| 5 | https://festasdamadalena.com/evento/i-torneio-regional-de-pesca-desportiva/ | Festival programme | 2026 (II edition 19 Jul 2026, 08:00-12:00; organisers CM Madalena + "Associação de Pescas da Ilha do Pico") | High for the event; shore/boat not stated | Event only |
| 6 | festasdamadalena.com 2025 listing (snippet) | Festival programme | I edition 20 Jul 2025, 07:00, Porto Velho (Madalena) [S] | Medium (page now shows nothing for that date) | Event only |
| 7 | http://www.cnlajesdopico.org/ | Club website | undated | Medium; confirms the APDIP championship has ≥9 rounds and Pico/Faial anglers; no venues or weights | Context, contact |
| 8 | https://www.oldsite.cm-lajesdopico.pt/conteudo/dinamico/documentos/boletim_municipal/2005/boletim_2005_07.pdf ; .../2004/boletim_2004_07.pdf | Municipal bulletins | 2004, 2005 | High for event, no catch data: INATEL inter-parish shore round "na costa da Silveira" (spot `fonte`), 2005; Semana dos Baleeiros "Pesca Desportiva de Costa dos Açores" 27 Aug 2004, 14:00 | Event only |
| 9 | https://www.fppd.pt/associacoes-regionais/ | Federation directory | current | High; lists APDIP's seat as São João, Lajes do Pico. The contact given there looks personal and is not copied here | Contact |
| 10 | https://www.opraticante.pt/trofeu-da-ilha-integra-regional/ | News (spearfishing) | 2018-03 | High for zones: Baía de Santo António and Baía de São Roque, reserves Calheta de Nesquim and Ribeiras. Spearfishing, not angling; no results | Context |
| 11 | https://www.allyoucancatch.com/post/the-perfect-key-lime-pie | Angler blog (German angler, trips 2014-2018) | undated | **A.** Pico breakwaters: bluefish on poppers; from the rocks also barracuda, small amberjack, leerfish; best dusk into night; float-fished bait at night; wire for bluefish | 1 record |
| 12 | https://www.pesqueiro.pt/index.php?topic=10155.0 "Spinning Açores" | PT forum | c. 2016 | **A, [S]** only (Cloudflare; content signal `use=reference`). A Pico member says Italian lure testers fished Pico in 2015 and locals now use lures more; species named: bicuda, anchova, írio, cavala, serra | Context |
| 13 | https://www.pesqueiro.pt/index.php?topic=12212.0 "Spinning de bicudas ou barracudas na rocha Açores"; topic=30081.0 "Os meus pesqueiros Faial acores" | PT forum | 2021+ | Not read (blocked). Worth reading by hand | Lead |
| 14 | https://www.worldseafishing.com/threads/faial-azores.42686250/ ; .../azores-shore-spinning.36756431/ ; .../lure-fishing-azores.40063027/ | UK forum | various | **A, [S]** only (TollBit gate). Snippets: Faial harbour / Porto Pim mostly lizardfish and a triggerfish; Faial surf beach bluefish c. 76-77 cm on metal jigs; "south side of Pico" few bluefish but plenty of barracuda one year | Context |
| 15 | https://www.flyfishing.co.uk/threads/swff-on-the-azores-faial-pico-sao-jorge.295166/ | UK fly forum | undated | **A, [S]** (TollBit). Porto Pim: 1-2 lb fish on small poppers and Clousers | Context |
| 16 | https://forums.deeperblue.com/threads/spearfishing-pico-island.118536 | Spearfishing forum | pre-2020 | **A, [S]** (403). Trevally "almost guaranteed" from shore in summer at some spots; 19 kg amberjack speared near São Caetano | Context (spot `saocaetano`) |
| 17 | https://www.cmjornal.pt/portugal/detalhe/policia-maritima-conduz-buscas-por-pescador-desaparecido-na-ilha-do-pico | News | Jan 2024 (per spots.md) | High that Manhenha is fished on foot; no catch data | 1 record |
| 18 | https://www.caisdopico.pt/2021/04/novo-recorde-europeu-na-caca-submarina.html ; https://www.caisdopico.pt/2017/10/ | Local blog-news | 2017, 2021 | High; spearfishing records (Azores waters, no site): e.g. anchova 11.6 kg, bicuda 11.6 kg, írio 40.3 kg. Only useful as a size ceiling | Context |
| 19 | https://www.semanadomar.net/programa/ (via snippet) | Festival programme | 2026 | [S]: shore round "Sargo (com engodo)", Mútua dos Pescadores, 9 Aug 2026, 08:00, Baía da Horta | Event only |
| 20 | https://correiodosacores.pt/2025/01/23/calendario-conhecido-do-clube-acoriano-de-pesca-desportiva/ | News (São Miguel club calendar) | 2025-01-23 | High, but São Miguel; no Pico/Faial content | Ruled out |

**Tried and blocked or empty (not circumvented):** RTP Açores (`acores.rtp.pt`, HTTP 403 to automated fetch; its search hits were all non-fishing), cnhorta.org (Cloudflare challenge; its "pesca de costa" news page is the best unread Faial source), Ilha Maior (`ilhamaior.pt/Wp/?s=pesca`: no results), Açoriano Oriental and Tribuna das Ilhas (no relevant hits), pescazores.com (no shore-competition items), picoacip.pt (TLS error), portugalio.com (connection refused). YouTube searches returned only boat tuna / bonito videos and dive videos for Pico, no shore-spot titles.

## Extracted records

Full rows (22 Faial competition rounds, the Lajes 2012 tournament, Manhenha, the breakwater blog) are in [`data/reports_found.json`](data/reports_found.json). Summary:

| Date | Place | Nearest spot (spots.md) | Species (biggest fish) | Method | Size / weight | Source |
|---|---|---|---|---|---|---|
| 2012-01-08 | Castelo Branco, Faial | (Faial) | Sargo | shore, sargo round, groundbait | 1.49 kg; 11 anglers, 114.3 kg total | 1 |
| 2012-02-12 | Lajinha, Feteira, Faial | (Faial) | Garoupa | shore, wrasse round | 0.54 kg; 353 fish, 16.6 kg; wind rising | 1 |
| 2012-03-11 | Fajã, Praia do Norte, Faial | (Faial) | Sargo | shore, mixed, no groundbait | 1.17 kg; 80 fish, 16.6 kg; postponed a week for weather | 1 |
| 2012-04-15 | Castelo Branco, Faial | (Faial) | Bodião vermelho | shore, wrasse round | 1.03 kg; 430 fish, 21.1 kg | 1 |
| 2012-05-19 | Porto Pim beach (night), Faial | (Faial) | Ratão (ray) | shore, beach, night | 3.31 kg; 38 fish, 21.0 kg | 1 |
| 2012-06-17 | Castelo Branco, Faial | (Faial) | Veja | shore, veja round | 1.31 kg; 18 fish, 10.5 kg | 1 |
| 2012-07-01 | Castelo Branco, Faial | (Faial) | Veja | shore, veja round | 1.64 kg; 26 fish, 21.5 kg | 1 |
| 2012-08 (I) | Horta, Semana do Mar, Faial | (Faial) | Veja | shore, inter-club | 1.58 kg | 1 |
| 2012-08 (I) | Lajes do Pico shoreline (I) | `lajes` | Veja | shore, inter-club (8 teams) | **2.21 kg** | 2 |
| 2012-09-16 | Comprido, Capelo, Faial | (Faial) | Sargo | shore, sargo round, groundbait | 1.20 kg; 272 fish, 71.2 kg | 1 |
| 2012-10-14 | Varadouro, Capelo, Faial | (Faial) | Raia | shore, mixed | 2.16 kg; 68 fish, 18.2 kg | 1 |
| 2012-10-28 | Fajã, Praia do Norte, Faial | (Faial) | n/s | shore, inter-club incl. 4 Pico clubs | 339 fish, 42.8 kg in 3 h; moved from Castelo Branco (sea) | 1 |
| 2013-01-27 | Laginha, Feteira, Faial | (Faial) | Sargo | shore, sargo round | 1.16 kg; 117 fish, 35.6 kg; moved from Fajã (sea) | 1 |
| 2013-03-03 | Praia do Almoxarife + Pedro Miguel, Faial | (Faial) | Bodião | shore, wrasse round | 0.65 kg; 167 fish, 14.7 kg | 1 |
| 2013-03-10 | Varadouro, Capelo, Faial | (Faial) | Veja | shore, mixed | 1.64 kg; 110 fish, 17.4 kg | 1 |
| 2013-04-07 | Castelo Branco, Faial | (Faial) | Bodião | shore, wrasse round | 0.98 kg; 278 fish, 15.0 kg | 1 |
| 2013-05-18 | Porto Pim beach (night), Faial | (Faial) | Sargo | shore, beach, night | 0.90 kg; 26 fish, 3.9 kg | 1 |
| 2013-06-09 | Castelo Branco, Faial | (Faial) | Veja | shore, veja round | 1.77 kg; 21 fish, 13.0 kg | 1 |
| 2013-07-07 | Castelo Branco, Faial | (Faial) | Veja | shore, veja round | 1.47 kg; 30 fish, 19.7 kg | 1 |
| 2013-09-01 | Comprido, Capelo, Faial | (Faial) | Sargo | shore, sargo round | 1.16 kg; 187 fish, 34.9 kg | 1 |
| 2013-10-06 | Laginha, Feteira, Faial | (Faial) | Anchova | shore, mixed | 0.59 kg; 224 fish, 12.5 kg | 1 |
| 2013-10-20 | Laginha, Feteira, Faial | (Faial) | Peixe-porco | shore, mixed | 0.93 kg; 92 fish, 14.7 kg; moved (sea) | 1 |
| 2014-01-12 | Lajinha, Feteira, Faial | (Faial) | Sargo | shore, sargo round | 1.02 kg; 11 anglers, 135 fish, 35.9 kg | 1 |
| 2024-01 | Manhenha, Pico | `manhenha` | n/a | shore on foot (news of a missing angler) | none | 17 |
| 2014-18 | "wave breakers", Pico | unknown breakwater | Anchova (bluefish) | spinning, popper | not given [A] | 11 |

Pico competition venues with no published catch data: Baía das Lajes (`lajes`; Semana dos Baleeiros, late August, 2004-2025), Porto Velho, Madalena (`madalena`, I: the old harbour basin by the main port; July 2025 and 2026), costa da Silveira (`fonte`; INATEL round 2005). Spearfishing zones (not angling): Baía de Santo António (`santoantonio`), Baía de São Roque (`saoroque`).

Faial venue names (Castelo Branco, Lajinha/Laginha in Feteira, Fajã in Praia do Norte, Comprido and Varadouro in Capelo, Porto Pim, Praia do Almoxarife, Pedro Miguel) are not in `spots.md`, which covers Pico only.

## Contacts worth approaching by hand (organisations and businesses only)

| Who | Why | Public contact |
|---|---|---|
| Associação de Pesca Desportiva da Ilha do Pico (APDIP), São João, Lajes do Pico | Runs the Pico island championship and Semana dos Baleeiros tournament. Their round sheets (venue, date, weights, biggest fish) would be the Pico corpus | Listed on https://www.fppd.pt/associacoes-regionais/ (the listed email and phone look personal; use the federation or the municipality to reach them) |
| Câmara Municipal das Lajes do Pico | Publishes the Semana dos Baleeiros tournament; could forward to APDIP | geral@cm-lajesdopico.pt, 292 679 700, Convento de São Francisco, 9930-135 Lajes do Pico |
| Câmara Municipal da Madalena | Co-organises the Madalena tournament with the "Associação de Pescas da Ilha do Pico" | geral@cm-madalena.pt, +351 292 628 700 |
| Clube Náutico das Lajes do Pico | Fields a team in every APDIP round | cnlajesdopico@cnlajesdopico.org, Rua Engenheiro Falcão, 9930-147 Lajes do Pico |
| Clube Naval de São Roque do Pico | Hosts spearfishing events on the north coast; may know north-coast angling marks | no public email found |
| Clube Naval da Horta, shore-angling section (Faial) | Shore championship 2017-2022+, island-wide venues; site blocked to bots | https://www.cnhorta.org/index.php/modalidades/pesca-desportiva-costa/noticias.html (read in a browser) |
| Clube de Pesca Ilha Azul (Faial) | Source of the 2012-2014 corpus; may have later seasons | via Junta de Freguesia da Praia do Almoxarife, https://jfpalmoxarife.com |
| DBM Azores (charter, São Roque and Cais da Madalena) | Local guide; not a tackle shop | info@dbmazores.com |
| "Mini Marcos - Marcos Pescas e Náutica", Madalena | Only fishing-tackle retailer found for Pico, from the ACIP business directory [S]; not verified | ACIP directory (picoacip.pt); no web page found |

No tackle shop with a public web page was found in Lajes or São Roque.

## Next steps if more is wanted

1. Ask APDIP (via CM Lajes) for 2023-2025 round sheets: one season would roughly double the Pico data.
2. Open the cnhorta.org shore-angling news page and pesqueiro.pt topics 12212 and 30081 in a normal browser and add facts by hand.
3. Ask whether the Madalena 2025/2026 tournament was shore-based and where it was weighed.
