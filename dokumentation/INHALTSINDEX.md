# Inhaltsindex für Menschen und KI-Agenten

Dieser Index führt zu den maßgeblichen Inhalten. Er enthält keine zusätzlichen Sicherheitsanforderungen. Alle Pfade gelten innerhalb der jeweiligen Repository-Fassung; private Informationen werden nicht mit der öffentlichen Referenz verknüpft.

**Stand:** Version 0.3.0 mit 34 Kontrollen in 22 Gruppen und neun Risiken mit je zwei Bewertungen. A01–A11 und P01–P12 bleiben Entscheidungshistorie der Version 0.2.0. Maßgeblich ist der aktuelle Katalog. Allgemeine Infrastruktur- und Nachweisblöcke sind entfallen.

## Maßgebliche Dateien

| Gesuchter Inhalt | Quelle und Suchkennzeichen |
|---|---|
| Festlegung, methodische Herleitung, Anwendung und Quellen | [OSCAL-Katalog](../katalog/ki-it-sicherheitskatalog.oscal.json), `catalog.groups[].controls[]`, Auswahl über `id` |
| Einzelner Kontrollabschnitt | `parts[].id`, beispielsweise `ki-gov-003-statement`; Zuordnung unten |
| Beschlüsse und historische Empfehlungen | [Praxisprüfung](PRAXISPRÜFUNG-2026-09-14.md#entscheidungen), A- und P-Kennungen |
| Verbindliche Ausgangs- und Restrisiken | [OSCAL-Katalog](../katalog/ki-it-sicherheitskatalog.oscal.json), `ki-gov-003-risk-register`, darin `r-01` bis `r-09`; [Entscheidungshistorie](PRAXISPRÜFUNG-2026-09-14.md#risikobewertungen) |
| Abgleich mit den normalen IT-Sicherheitsprozessen | [Historische Zuordnung der Version 0.2.0](PRAXISPRÜFUNG-2026-09-14.md#basisprozesse) |
| Derzeitige Konzeptfassung | [DOCX](../konzept/ki-it-sicherheitskonzept.docx) und [PDF](../konzept/ki-it-sicherheitskonzept.pdf); Kapitel und Kontroll-IDs verwenden |
| Dokumentableitung aus dem Katalog | [Dokumentgenerator](../validierung/erzeuge_dokumente.py), `kapitel_eins_bis_acht`, `kapitel_neun`, `kapitel_zehn_bis_dreizehn` |
| Öffentliche Belege | [Quellenregister](../quellen/quellenregister.json), `quellen[].id` und `oscal_uuid`; Verknüpfung über `controls[].links[].href` und `catalog.back-matter.resources[].uuid` |
| Architektur, Datenflüsse, Entscheidungen | [Diagrammübersicht](../diagramme/README.md) und dort verlinkte PlantUML-Quellen |
| Bearbeitungsregeln und Gestaltung | [AGENTS.md](../AGENTS.md), [Layoutregeln](LAYOUTREGELN.md), [Übernahmeleitfaden](ÜBERNAHMELEITFADEN.md) |
| Historie und Migration | [Änderungsprotokoll](../CHANGELOG.md) und Git-Historie |
| Prüfstand und bekannte Prüfgrenzen | [Prüfprotokoll 0.3.0](PRÜFPROTOKOLL-0.3.0.md) |

Die vier Pflichtabschnitte jeder Kontrolle sind dauerhaft adressierbar:

| Abschnitt | OSCAL-Name | Stabile Abschnitts-ID am Beispiel KI-GOV-003 |
|---|---|---|
| Anforderung | `statement` | `ki-gov-003-statement` |
| Begründung | `rationale` | `ki-gov-003-rationale` |
| Umsetzung | `guidance` | `ki-gov-003-guidance` |
| Quellenangabe | `source` | `ki-gov-003-source` |

Die native Abbildung über `id` und `links` richtet sich nach der [NIST-Referenz für OSCAL Catalog 1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/catalog/json-reference/). Der Katalog verweist über `metadata.links` mit `rel: index` auf diesen Index; der Verweis hat ausschließlich redaktionelle Bedeutung.

<a id="entscheidungen"></a>

## Entscheidungen

| ID | Beschlossener Inhalt | Umsetzung |
|---|---|---|
| [A01](PRAXISPRÜFUNG-2026-09-14.md#a01) | Realistische Maßnahmen und vollständig begründete Referenzrisiken | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A02](PRAXISPRÜFUNG-2026-09-14.md#a02) | Selbstständige Projektarbeit mit schneller, einfacher Wiederherstellung | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A03](PRAXISPRÜFUNG-2026-09-14.md#a03) | Bestehende Dokumenten-, Qualitäts- und Sicherheitsprozesse verwenden | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A04](PRAXISPRÜFUNG-2026-09-14.md#a04) | Unternehmensnetz und vorhandene Anmeldung integrieren | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A05](PRAXISPRÜFUNG-2026-09-14.md#a05) | Internetregeln, ausdrückliche KI-Freigabe und zulässige Ausweichziele | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A06](PRAXISPRÜFUNG-2026-09-14.md#a06) | Persönliche Speicherung und freiwillige, sichtbar aktivierte Wissensübernahme | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A07](PRAXISPRÜFUNG-2026-09-14.md#a07) | Neue Wissensbeiträge stoppen; bestehende nach geltenden Nutzungsregeln behandeln | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A08](PRAXISPRÜFUNG-2026-09-14.md#a08) | Mittlere Restrisiken im regulären Prozess begründet akzeptieren | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A09](PRAXISPRÜFUNG-2026-09-14.md#a09) | Stabile Kennungen, Index und gepflegte Querverweise | In Arbeitsregeln, Index und Katalogkennungen umgesetzt |
| [A10](PRAXISPRÜFUNG-2026-09-14.md#a10) | Hohe Restrisiken, betroffene Funktionen und begrenzter Ausnahmebetrieb | In Katalog, Konzept und zugehörigen Diagrammen umgesetzt |
| [A11](PRAXISPRÜFUNG-2026-09-14.md#a11) | Jede Tätigkeit bleibt auch bei längerem KI-Ausfall möglich; Wiederherstellung über normalen IT-Betrieb | In KI-GOV-002/003, KI-THR-002, KI-OPS-003 und R-06 umgesetzt |

<a id="kontrollen"></a>

## Kontrollindex

Die OSCAL-ID ist der dauerhafte Suchschlüssel. Die Kapitelangabe bezeichnet Version 0.3.0. Verbleibende Kontrollkennungen wurden nicht neu nummeriert.

| Kontrolle | Gegenstand | Kapitel | Szenario |
|---|---|---|---|
| <a id="ki-gel-001"></a>`ki-gel-001` | KI-spezifische Ergänzung des Informationssicherheitskonzepts | 9.1 | Beide Szenarien |
| <a id="ki-gel-002"></a>`ki-gel-002` | Schutzkennzeichnung und kontrollierte Dokumentenführung | 9.1 | Beide Szenarien |
| <a id="ki-gov-001"></a>`ki-gov-001` | KI-Funktionen und Softwarezuordnung | 9.2 | Beide Szenarien |
| <a id="ki-gov-002"></a>`ki-gov-002` | KI-Nutzung und Nutzerbelehrung | 9.2 | Beide Szenarien |
| <a id="ki-rec-001"></a>`ki-rec-001` | Zulässige Inhalte im Modellkontext | 9.3 | Beide Szenarien |
| <a id="ki-rec-002"></a>`ki-rec-002` | Einstufung und Freigabe von KI-Inhalten | 9.3 | Beide Szenarien |
| <a id="ki-gov-003"></a>`ki-gov-003` | Bewertung KI-spezifischer Risiken | 9.4 | Beide Szenarien |
| <a id="ki-thr-001"></a>`ki-thr-001` | Prüfung KI-spezifischer Fehl- und Missbrauchsszenarien | 9.4 | Beide Szenarien |
| <a id="ki-arc-002"></a>`ki-arc-002` | Verarbeitungsgrenzen der Szenarien | 9.5 | Beide Szenarien |
| <a id="ki-api-001"></a>`ki-api-001` | Anmeldung und KI-Zugriffsrechte | 9.6 | Beide Szenarien |
| <a id="ki-iam-001"></a>`ki-iam-001` | Berechtigungen für KI-Nutzung und KI-Verwaltung | 9.6 | Beide Szenarien |
| <a id="ki-api-002"></a>`ki-api-002` | Serverseitige Grenzen für Modellzugriffe | 9.7 | Beide Szenarien |
| <a id="ki-mod-001"></a>`ki-mod-001` | Prüfung bereitgestellter Modelle | 9.8 | Beide Szenarien |
| <a id="ki-mod-002"></a>`ki-mod-002` | Austauschbare Modellstände mit stabilen Modellaliasen | 9.8 | Beide Szenarien |
| <a id="ki-trn-001"></a>`ki-trn-001` | Keine Änderung von Modellgewichten | 9.9 | Beide Szenarien |
| <a id="ki-rag-001"></a>`ki-rag-001` | Aufnahme von Dokumenten in den KI-Kontext | 9.10 | Beide Szenarien |
| <a id="ki-rag-002"></a>`ki-rag-002` | Durchgängige Berechtigungsprüfung und Indextrennung | 9.10 | Beide Szenarien |
| <a id="ki-rag-003"></a>`ki-rag-003` | Schutz abgeleiteter Daten | 9.10 | Beide Szenarien |
| <a id="ki-rag-004"></a>`ki-rag-004` | Persönliche Inhalte und gemeinsame Wissensbestände | 9.10 | Beide Szenarien |
| <a id="ki-agt-001"></a>`ki-agt-001` | Agentische Projektarbeit im Nutzerkontext | 9.11 | Beide Szenarien |
| <a id="ki-agt-002"></a>`ki-agt-002` | Freigegebene Modellziele für Agenten | 9.11 | Beide Szenarien |
| <a id="ki-pmt-001"></a>`ki-pmt-001` | Abgrenzung von Arbeitsauftrag und Dateninhalt | 9.12 | Beide Szenarien |
| <a id="ki-out-001"></a>`ki-out-001` | Fachliche Prüfung und Verwendung von KI-Ergebnissen | 9.13 | Beide Szenarien |
| <a id="ki-tol-001"></a>`ki-tol-001` | Freigabe von Agentenaktionen | 9.14 | Beide Szenarien |
| <a id="ki-tol-002"></a>`ki-tol-002` | Serverseitige KI-Werkzeuge und interne Ausführung | 9.14 | Beide Szenarien |
| <a id="ki-thr-002"></a>`ki-thr-002` | Begrenzung von KI-Aufträgen | 9.15 | Beide Szenarien |
| <a id="ki-val-001"></a>`ki-val-001` | Erprobung von Modellen und KI-Funktionen | 9.16 | Beide Szenarien |
| <a id="ki-val-002"></a>`ki-val-002` | Fortschreibung bei Änderungen der KI-Nutzung | 9.17 | Beide Szenarien |
| <a id="ki-ops-001"></a>`ki-ops-001` | Umgang mit KI-Inhalten in Protokollen | 9.18 | Beide Szenarien |
| <a id="ki-ops-002"></a>`ki-ops-002` | Behandlung KI-spezifischer Auffälligkeiten | 9.19 | Beide Szenarien |
| <a id="ki-ops-003"></a>`ki-ops-003` | Konsistenz nach Wiederherstellung von KI-Daten | 9.20 | Beide Szenarien |
| <a id="ki-dec-001"></a>`ki-dec-001` | Entfernung nicht mehr benötigter KI-Bestände | 9.21 | Beide Szenarien |
| <a id="ki-ext-001"></a>`ki-ext-001` | Freigegebene Cloud-Verarbeitung | 9.22 | Cloud-Szenario |
| <a id="ki-ext-002"></a>`ki-ext-002` | Zulässige Ausweichziele | 9.22 | Beide Szenarien |

## Risiken

Die folgenden Links dokumentieren die Entscheidungshistorie. Verbindlich sind die gleichnamigen Risikoabschnitte `r-01` bis `r-09` im Katalog unter `ki-gov-003-risk-register` und deren Ableitung in Kapitel 8.3. Jedes Risiko enthält sechs Air-Gap-Einstufungswerte und sechs weitere unter `r-XX-cloud-assessment`. Kontrollverweise, Behandlung, Annahmen und Begründungen bleiben zugeordnet. Die Teile heißen `treatment`, `assumptions` und `residual-reasoning`; ihre IDs folgen beispielsweise `r-06-assumptions`.

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
