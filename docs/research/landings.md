# SREA landings 1994 to 2026: season profiles for Pico

Gathered 2026-11-22. Replaces the 20-month reconstruction in `species.md` section 2.1 as the basis for season curves.

## Source [V]

- Report: SREA "Total da pesca descarregada, por espécie e por ilha" (SQL Server Reporting Services viewer at `reports-estatistica.azores.gov.pt`, linked from https://srea.azores.gov.pt/relatorio/pesca-total-descarregada-nos-portos-dos-acores/).
- The viewer sits behind a browser check, so it was opened in Chrome. Parameters: Ano Inicial 1994, Ano Final 2026, all islands. The viewer's own CSV export was used, then cut to Pico and Faial.
- Contents: island × category × species × year × month, kg and €. Origin is Lotaçor first-sale auction records (commercial landings).
- Coverage: January 1994 to October 2026 with no missing years (2,760 rows a year for the two islands; 2026 runs to October). 113 species or groups appear for Pico.
- Licence: official public statistics; no licence statement seen (same open question as the Q4 files, see the spec's section 12).

## Files

- `data/srea/srea_landings_pico_faial_1994-2026.csv` (4 MB): `island,category,species,year,month,kg,eur`. Months are in Portuguese; a blank means nothing landed.
- `data/srea/season_profiles.json`: per island and target species, annual kg per year and month-of-year profiles for 1994–2009, 2010–2025 and all complete years.
- `scripts/srea.py`: builds the profiles. `python3 -I docs/research/scripts/srea.py <csv> <out_json>`.

Method: each complete year is turned into monthly shares (month kg / year kg), so big years don't swamp small ones. The profile is the mean share per month over the years with any landings, scaled so the top month is 1.

## Pico month-of-year profiles, 1994–2025 [V, computed]

Digits are J F M A M J J A S O N D, 9 = peak month, 0 = under a tenth of the peak.

| Species | Profile | Years with landings | Median kg/yr | Peak 1994–2009 | Peak 2010–2025 |
|---|---|---|---|---|---|
| Veja | `111235941111` | 32 | 46,748 | Jul | Jul |
| Sargo / Sarguete | `975322113898` | 32 | 1,611 | Nov | Jan |
| Bicuda | `002475699520` | 32 | 5,752 | Aug | Sep |
| Serra (*Sarda sarda*) | `235696421220` | 32 | 1,996 | May | May |
| Lírio / Írio | `000002962000` | 32 | 4,482 | Jul | Jul |
| Anchova | `000002984210` | 24 | 840 | Aug | Jul |
| Encharéu | `000013941010` | 32 | 3,335 | Jul | Jul |
| Tainha / Muja | `956852212699` | 32 | 2,912 | Dec | Jan |
| Salema | `056984321330` | 32 | 67 | Feb | Apr |
| Cavala | `144579934431` | 32 | 3,291 | Jun | May |
| Chicharro | `455887986664` | 32 | 40,209 | Jul | May |
| Garoupa | `456898733364` | 32 | 4,557 | May | Jun |
| Congro | `467899985454` | 32 | 7,382 | May | Jun |
| Moreia pintada | `357798996432` | 32 | 3,582 | Jul | May |
| Bonito (skipjack) | `000001995200` | 24 | 522,283 | Aug | Aug |

Salema, boga, besugo and the other morays land under 100 kg a year on Pico, so their profiles are noise.

## Long-term change, Pico median kg per year by 8-year block [V, computed]

| Species | 1994–01 | 2002–09 | 2010–17 | 2018–25 |
|---|---|---|---|---|
| Veja | 2,354 | 45,564 | 56,687 | 72,360 |
| Sargo / Sarguete | 1,035 | 1,714 | 1,438 | 1,764 |
| Bicuda | 4,052 | 5,842 | 6,756 | 11,567 |
| Serra | 2,540 | 2,676 | 2,102 | 768 |
| Lírio / Írio | 1,076 | 5,200 | 3,803 | 14,474 |
| Anchova | 0 | 335 | 1,376 | 1,708 |
| Encharéu | 1,057 | 2,302 | 6,199 | 6,841 |
| Tainha / Muja | 478 | 2,124 | 4,898 | 5,987 |
| Garoupa | 3,592 | 9,444 | 2,962 | 2,626 |

## Reading it [I]

- The seasons are stable across the two halves of the record for every species with real volume, so a single all-years curve is a sound default.
- **Clear summer fish:** lírio (June to August, almost nothing otherwise), anchova (June to October, peak July–August), encharéu (July), bicuda (late summer into October), veja (June–August).
- **Clear winter fish:** sargo (October to February) and tainha (November to February). This matches the shore-angling survey, where sargo dominates the catch (see `recreational-catch.md`).
- **Serra** peaks in spring (April to June) and its landings fell sharply after 2018.
- Rising series (veja, bicuda, lírio, anchova, encharéu, tainha) may reflect fishing effort or market changes as much as fish numbers.

## Caveats

- These are commercial landings, not shore catch. The season reflects when boats target and sell a species, quotas and closures (veja has a per-island quota) and weather days, as well as when the fish are inshore.
- Veja's 1994–2001 figures are tiny compared with later years, probably a change in how it was recorded or marketed; the profile uses shares, so this mainly affects the trend table.
- Moray categories changed names over time ("Moreia Pintada", "Moreia Preta Viúva", "Moreão"); codes before October 2002 included some catch-all groups ("Diversos peixes", "Tunídeos").
- Faial is in the same files and profiles JSON but has not been summarised here.
