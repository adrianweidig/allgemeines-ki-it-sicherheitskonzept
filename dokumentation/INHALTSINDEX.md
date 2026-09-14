# Inhaltsindex für Menschen und KI-Agenten

Dieser Index führt zu den maßgeblichen Inhalten. Er enthält keine zusätzlichen Sicherheitsanforderungen. Alle Pfade gelten innerhalb der jeweiligen Repository-Fassung; private Informationen werden nicht mit der öffentlichen Referenz verknüpft.

**Stand:** Fachtexte von Katalog und DOCX/PDF: Version 0.1.0. A01–A08, A10 und A11 sind beschlossen, ihre fachliche Übernahme ist noch offen. A09 zur Auffindbarkeit ist umgesetzt. Die neuen Bewertungen R-01–R-09 stehen noch zur Abstimmung; R-06 berücksichtigt bereits die verbindliche Weiterarbeit ohne KI aus A11. Die ursprünglichen Empfehlungen P01–P12 sind zusammen mit den späteren Entscheidungen zu lesen; bestätigte Entscheidungen haben für die Überarbeitung Vorrang.

## Maßgebliche Dateien

| Gesuchter Inhalt | Quelle und Suchkennzeichen |
|---|---|
| Anforderungen, Begründung, Umsetzung, Prüfziel, Nachweise | [OSCAL-Katalog](../katalog/ki-it-sicherheitskatalog.oscal.json), `catalog.groups[].controls[]`, Auswahl über `id` |
| Einzelner Kontrollabschnitt | `parts[].id`, beispielsweise `ki-gov-003-statement`; Zuordnung unten |
| Beschlossene Vorgaben und offene Empfehlungen | [Praxisprüfung](PRAXISPRÜFUNG-2026-09-14.md#entscheidungen), A- und P-Kennungen |
| Vorgeschlagene Ausgangs- und Restrisiken | [Vorbereitete Risikobewertungen](PRAXISPRÜFUNG-2026-09-14.md#risikobewertungen), R-01–R-09 |
| Abgleich mit den normalen IT-Sicherheitsprozessen | [Zuordnung aller 38 Kontrollen](PRAXISPRÜFUNG-2026-09-14.md#basisprozesse) |
| Derzeitige Konzeptfassung | [DOCX](../konzept/ki-it-sicherheitskonzept.docx) und [PDF](../konzept/ki-it-sicherheitskonzept.pdf); Kapitel und Kontroll-IDs verwenden |
| Konzeptaufbau und derzeitiges Risikoregister | [Dokumentgenerator](../validierung/erzeuge_dokumente.py), `kapitel_eins_bis_acht`, `kapitel_neun`, `kapitel_zehn_bis_dreizehn` |
| Öffentliche Belege | [Quellenregister](../quellen/quellenregister.json), `quellen[].id` und `oscal_uuid`; Verknüpfung über `controls[].links[].href` und `catalog.back-matter.resources[].uuid` |
| Architektur, Datenflüsse, Entscheidungen | [Diagrammübersicht](../diagramme/README.md) und dort verlinkte PlantUML-Quellen |
| Bearbeitungsregeln und Gestaltung | [AGENTS.md](../AGENTS.md), [Layoutregeln](LAYOUTREGELN.md), [Übernahmeleitfaden](ÜBERNAHMELEITFADEN.md) |
| Historie und Migration | [Änderungsprotokoll](../CHANGELOG.md) und Git-Historie |

Die sechs Pflichtabschnitte jeder Kontrolle sind dauerhaft adressierbar:

| Abschnitt | OSCAL-Name | Stabile Abschnitts-ID am Beispiel KI-GOV-003 |
|---|---|---|
| Anforderung | `statement` | `ki-gov-003-statement` |
| Begründung | `rationale` | `ki-gov-003-rationale` |
| Umsetzung | `guidance` | `ki-gov-003-guidance` |
| Prüfziel | `assessment-objective` | `ki-gov-003-assessment-objective` |
| Nachweise | `evidence` | `ki-gov-003-evidence` |
| Quellenangabe | `source` | `ki-gov-003-source` |

Die native Abbildung über `id` und `links` richtet sich nach der [NIST-Referenz für OSCAL Catalog 1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/catalog/json-reference/). Der Katalog verweist über `metadata.links` mit `rel: index` auf diesen Index; der Verweis hat ausschließlich redaktionelle Bedeutung.

<a id="entscheidungen"></a>

## Entscheidungen

| ID | Beschlossener Inhalt | Umsetzung |
|---|---|---|
| [A01](PRAXISPRÜFUNG-2026-09-14.md#a01) | Realistische Maßnahmen und vollständig begründete Referenzrisiken | Fachliche Übernahme offen |
| [A02](PRAXISPRÜFUNG-2026-09-14.md#a02) | Selbstständige Projektarbeit mit schneller, einfacher Wiederherstellung | Fachliche Übernahme offen |
| [A03](PRAXISPRÜFUNG-2026-09-14.md#a03) | Bestehende Dokumenten-, Qualitäts- und Sicherheitsprozesse verwenden | Fachliche Übernahme offen |
| [A04](PRAXISPRÜFUNG-2026-09-14.md#a04) | Unternehmensnetz und vorhandene Anmeldung integrieren | Fachliche Übernahme offen |
| [A05](PRAXISPRÜFUNG-2026-09-14.md#a05) | Internetregeln, ausdrückliche KI-Freigabe und zulässige Ausweichziele | Fachliche Übernahme offen |
| [A06](PRAXISPRÜFUNG-2026-09-14.md#a06) | Persönliche Speicherung und freiwillige, sichtbar aktivierte Wissensübernahme | Fachliche Übernahme offen |
| [A07](PRAXISPRÜFUNG-2026-09-14.md#a07) | Neue Wissensbeiträge stoppen; bestehende nach geltenden Nutzungsregeln behandeln | Fachliche Übernahme offen |
| [A08](PRAXISPRÜFUNG-2026-09-14.md#a08) | Mittlere Restrisiken im regulären Prozess begründet akzeptieren | Fachliche Übernahme offen |
| [A09](PRAXISPRÜFUNG-2026-09-14.md#a09) | Stabile Kennungen, Index und gepflegte Querverweise | In Arbeitsregeln, Index und Katalogkennungen umgesetzt |
| [A10](PRAXISPRÜFUNG-2026-09-14.md#a10) | Hohe Restrisiken, betroffene Funktionen und begrenzter Ausnahmebetrieb | Fachliche Übernahme offen |
| [A11](PRAXISPRÜFUNG-2026-09-14.md#a11) | Jede Tätigkeit bleibt auch bei längerem KI-Ausfall möglich; Wiederherstellung über normalen IT-Betrieb | Fachliche Übernahme offen; Bewertung R-06 angepasst |

<a id="kontrollen"></a>

## Kontrollindex

Die OSCAL-ID ist der dauerhafte Suchschlüssel. Die Kapitelangabe bezeichnet die derzeitige Konzeptfassung. Entscheidungen, Risiken und Praxisempfehlungen werden in den entsprechenden Tabellen dieses Index aufgelöst; die Verknüpfung zeigt die betroffenen Inhalte und behauptet keine bereits abgeschlossene Umsetzung.

| OSCAL-ID | Suchthema | Kapitel | Entscheidungen | Risiken | Praxisempfehlungen |
|---|---|---|---|---|---|
| <a id="ki-gel-001"></a>`ki-gel-001` | Basis-Sicherheitskonzept und KI-Ergänzungen | 3, 9.1 | A03 | übergreifend | P12 |
| <a id="ki-gel-002"></a>`ki-gel-002` | Schutzstatus und Dokumentenführung | 1, 9.1 | A03, A09 | übergreifend | P12 |
| <a id="ki-gov-001"></a>`ki-gov-001` | Inventar und Zuständigkeiten | 7, 9.2 | A03 | übergreifend | P12 |
| <a id="ki-gov-002"></a>`ki-gov-002` | Zugelassene Nutzung, Kompetenz und Weiterarbeit ohne KI | 6, 9.2 | A03, A06, A11 | R-06, R-07 | P12 |
| <a id="ki-gov-003"></a>`ki-gov-003` | Risikoakzeptanz und Überprüfung | 8, 9.2 | A01, A08, A10, A11 | R-01–R-09 | P01, P02 |
| <a id="ki-rec-001"></a>`ki-rec-001` | Recht, Datenschutz und Verwendung | 6, 9.3 | A03, A05, A06, A07 | R-03, R-05, R-08 | P11, P12 |
| <a id="ki-rec-002"></a>`ki-rec-002` | Schutzbedarf und besondere Freigaben | 6, 9.3 | A03, A06 | R-03, R-05, R-08 | P12 |
| <a id="ki-arc-001"></a>`ki-arc-001` | Systemgrenzen und KI-Zugang | 4, 5, 9.4 | A04, A11 | R-04, R-06, R-08 | P03, P09 |
| <a id="ki-arc-002"></a>`ki-arc-002` | Unternehmensdienste und Datenflüsse | 4, 5, 9.4 | A04, A05 | R-08 | P09, P11 |
| <a id="ki-con-001"></a>`ki-con-001` | Netz- und Containerkommunikation | 9.5 | A03, A04 | R-04, R-08 | P09 |
| <a id="ki-con-002"></a>`ki-con-002` | Plattformrechte und Laufzeit | 9.5 | A03 | R-01, R-02 | P12 |
| <a id="ki-api-001"></a>`ki-api-001` | Anmeldung und Zugriffsberechtigung | 9.5 | A04 | R-04 | P03, P09 |
| <a id="ki-api-002"></a>`ki-api-002` | Modell-, Kontext- und Werkzeuggrenzen | 9.5 | A02, A04 | R-01, R-04, R-06 | P03, P06 |
| <a id="ki-mod-001"></a>`ki-mod-001` | Modellimport und Herkunft | 9.6 | A03 | R-02 | P12 |
| <a id="ki-mod-002"></a>`ki-mod-002` | Modellstände und Wiederherstellung | 9.6 | A03 | R-09 | P04, P08 |
| <a id="ki-trn-001"></a>`ki-trn-001` | Ausschluss von Training und Gewichtsänderung | 2, 9.7 | A06 | übergreifend | P07 |
| <a id="ki-rag-001"></a>`ki-rag-001` | Aufnahme und Aufbereitung von Dateien | 9.8, 10 | A03, A06 | R-03 | P04, P05 |
| <a id="ki-rag-002"></a>`ki-rag-002` | Durchgängige Rechte und Empfängertrennung | 9.8, 10 | A03, A06, A07 | R-03 | P03, P10 |
| <a id="ki-rag-003"></a>`ki-rag-003` | Aufbewahrung, Löschung und Ableitungen | 9.8, 10 | A03, A06, A07 | R-03 | P04, P05 |
| <a id="ki-rag-004"></a>`ki-rag-004` | Persönliche Dateiübernahmen und Verläufe | 9.8, 10 | A03, A06, A07 | R-03 | P05 |
| <a id="ki-iam-001"></a>`ki-iam-001` | Identitäten, Dienstzugänge und Geheimnisse | 9.9 | A03, A04 | R-01, R-04, R-08 | P09, P10 |
| <a id="ki-agt-001"></a>`ki-agt-001` | Arbeitsbereiche und Wiederherstellbarkeit | 9.10, 11 | A02, A03 | R-01 | P06 |
| <a id="ki-agt-002"></a>`ki-agt-002` | Zugelassene Modellziele für Agenten | 9.10, 11 | A04, A05 | R-08 | P09, P11 |
| <a id="ki-pmt-001"></a>`ki-pmt-001` | Eingeschleuste Anweisungen und unzuverlässige Inhalte | 9.11, 11 | A02 | R-01 | P03, P06 |
| <a id="ki-out-001"></a>`ki-out-001` | Ergebnisqualität und wirkungsbezogene Freigaben | 9.11 | A02, A03 | R-07 | P06, P08 |
| <a id="ki-tol-001"></a>`ki-tol-001` | Werkzeugaktionen und Genehmigungsgrenzen | 9.12, 11 | A02 | R-01 | P06 |
| <a id="ki-tol-002"></a>`ki-tol-002` | Erweiterungen, MCP und Werkzeugprotokolle | 9.12, 11 | A03, A04 | R-01, R-02 | P04 |
| <a id="ki-thr-001"></a>`ki-thr-001` | Bedrohungen und überprüfbare Testabdeckung | 8, 9.13 | A01 | R-01 | P03 |
| <a id="ki-thr-002"></a>`ki-thr-002` | Überlastung, begrenzte Ressourcen und Schutz der übrigen IT | 9.13 | A01, A05, A11 | R-06 | P01 |
| <a id="ki-val-001"></a>`ki-val-001` | Wiederholbare Qualitäts- und Sicherheitstests | 9.14 | A01, A03 | R-07, R-09 | P03, P08 |
| <a id="ki-val-002"></a>`ki-val-002` | Routineänderungen und wesentliche Änderungen | 9.14 | A02, A03 | R-02, R-09 | P04 |
| <a id="ki-ops-001"></a>`ki-ops-001` | Betriebsprotokolle und Inhaltsminimierung | 9.15 | A03, A06, A07 | R-05 | P05 |
| <a id="ki-ops-002"></a>`ki-ops-002` | Überwachung und Vorfallbehandlung | 9.15 | A03, A08, A10, A11 | übergreifend | P02 |
| <a id="ki-ops-003"></a>`ki-ops-003` | Sicherung, Reparatur und konsistenter Wiederanlauf | 9.15, 13 | A02, A03, A07, A11 | R-03, R-06, R-09 | P04, P05 |
| <a id="ki-dec-001"></a>`ki-dec-001` | Außerbetriebnahme | 9.16 | A03, A07 | R-03, R-05 | P05 |
| <a id="ki-ext-001"></a>`ki-ext-001` | Ausdrückliche Freigabe externer KI-Nutzung | 9.17, 12 | A03, A04, A05 | R-08 | P09, P11 |
| <a id="ki-ext-002"></a>`ki-ext-002` | Freigegebene Ausweichziele | 9.17, 12 | A05, A11 | R-06, R-08 | P11 |
| <a id="ki-ass-001"></a>`ki-ass-001` | Nachweiskette und Abweichungsentscheidungen | 9.18, 13 | A01, A03, A08, A09, A10 | übergreifend | P01, P02, P12 |

## Risiken

Alle Links führen zu den neuen Bewertungsvorschlägen. Das noch geltende Register steht in Kapitel 8.3 des Konzepts und in `kapitel_eins_bis_acht` des Generators. Seine Ablösung ist noch offen.

| ID | Szenario |
|---|---|
| [R-01](PRAXISPRÜFUNG-2026-09-14.md#r-01) | Unzulässige Werkzeugaktion durch eingeschleuste Inhalte |
| [R-02](PRAXISPRÜFUNG-2026-09-14.md#r-02) | Manipulierte Modelle, Pakete oder Erweiterungen |
| [R-03](PRAXISPRÜFUNG-2026-09-14.md#r-03) | Unberechtigte Offenlegung über Unternehmenswissen |
| [R-04](PRAXISPRÜFUNG-2026-09-14.md#r-04) | Umgehung von Anmeldung oder Berechtigung |
| [R-05](PRAXISPRÜFUNG-2026-09-14.md#r-05) | Unnötige geschützte Inhalte in Betriebsprotokollen |
| [R-06](PRAXISPRÜFUNG-2026-09-14.md#r-06) | Überlastung und verbindliche Weiterarbeit ohne KI |
| [R-07](PRAXISPRÜFUNG-2026-09-14.md#r-07) | Wirksam eingesetzte fehlerhafte Ergebnisse |
| [R-08](PRAXISPRÜFUNG-2026-09-14.md#r-08) | Übermittlung außerhalb der freigegebenen KI-Nutzung |
| [R-09](PRAXISPRÜFUNG-2026-09-14.md#r-09) | Sicherheits- oder Qualitätsverlust nach Änderungen |

## Ursprüngliche Praxisempfehlungen

| ID | Gegenstand |
|---|---|
| [P01](PRAXISPRÜFUNG-2026-09-14.md#p01) | Begründete Ausgangs- und Restrisiken |
| [P02](PRAXISPRÜFUNG-2026-09-14.md#p02) | Betriebsunterbrechung und Risikoakzeptanz |
| [P03](PRAXISPRÜFUNG-2026-09-14.md#p03) | Überprüfbare Abdeckung statt unerfüllbarer Vollständigkeit |
| [P04](PRAXISPRÜFUNG-2026-09-14.md#p04) | Änderungsklassen und angemessene Wiederfreigabe |
| [P05](PRAXISPRÜFUNG-2026-09-14.md#p05) | Zugriffssperre, persönliche Speicherung und Löschung |
| [P06](PRAXISPRÜFUNG-2026-09-14.md#p06) | Genehmigung nach Auswirkung und Wiederherstellbarkeit |
| [P07](PRAXISPRÜFUNG-2026-09-14.md#p07) | Trainingsverbot über Funktionen und Rechte |
| [P08](PRAXISPRÜFUNG-2026-09-14.md#p08) | Wiederholbare Bewertung trotz variierender Modellantworten |
| [P09](PRAXISPRÜFUNG-2026-09-14.md#p09) | Unternehmensintegration und lokale Betriebsgrenze |
| [P10](PRAXISPRÜFUNG-2026-09-14.md#p10) | Wirksame und zeitlich geregelte Berechtigungsänderungen |
| [P11](PRAXISPRÜFUNG-2026-09-14.md#p11) | Nutzungsfreigabe externer KI und technische Anfrageprüfung |
| [P12](PRAXISPRÜFUNG-2026-09-14.md#p12) | Anwendbarkeit und konkrete Begründung der Anforderungen |

## Suche und Pflege

Für eine konkrete Frage zuerst die Kennung im Index suchen und dann nur die referenzierten Originalstellen lesen. Beispiel:

```powershell
rg -n -i -F 'ki-gov-003' dokumentation/INHALTSINDEX.md katalog/ki-it-sicherheitskatalog.oscal.json
rg -n -F 'ki-gov-003-statement' katalog/ki-it-sicherheitskatalog.oscal.json
rg -n '^### A08' dokumentation/PRAXISPRÜFUNG-2026-09-14.md
```

Nach relevanten Änderungen Kennungen, Zuordnungen, Dateipfade, Anker und Status gemeinsam pflegen. Die Projektvalidierung prüft Kontroll- und Abschnittskennungen, den Katalogverweis sowie lokale Ziele und Anker des Index. Die fachliche Richtigkeit einer Zuordnung und die tatsächliche Umsetzung einer Entscheidung bleiben redaktionell zu prüfen.
