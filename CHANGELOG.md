# Änderungsprotokoll

Alle fachlichen Fassungen werden mit semantischer Versionierung dokumentiert. Vor dem ersten fachlichen Entwurf existiert ausschließlich der Bootstrap des Repositorys.

## 0.2.0 – 14.09.2026

- Technische Korrektur am 15.09.2026: Die Statusprüfung des Veröffentlichungsartefakts verwendet das bereits festgelegte Betriebsmodell `unternehmensintegriert`.

- Layoutgrenzen für Diagramme und Tabellenköpfe abgesichert; Standardpfade des Word-Exports erst im Skriptkörper aufgelöst. 29 Tests und vollständige Seitenprüfung im [Prüfprotokoll](dokumentation/PRÜFPROTOKOLL-0.2.0.md) dokumentiert.

- OSCAL-Dokumentinstanzen erhalten gemäß NIST neue, voneinander getrennte UUIDs und den tatsächlichen Änderungszeitpunkt; die stabilen Kontroll-, Quellen- und Abschnittskennungen bleiben erhalten. [NIST-Dokumentstruktur und Revisionsregeln](https://pages.nist.gov/OSCAL/learn/concepts/layer/overview/)

- A01–A11 und P01–P12 in allen 38 Kontrollen, Konzepttexten und sechs Diagrammen umgesetzt: Unternehmensintegration, reguläre Qualitätssicherung, autonome Routinearbeit mit wirksamer Wiederherstellung, freiwillige Wissensbeiträge und uneingeschränkte Weiterarbeit ohne KI.
- Neun Ausgangs- und Restrisiken einschließlich Maßnahmen, Annahmen und Begründung im Katalog unter `ki-gov-003-risk-register` geführt. Konzept und Risikomatrix werden daraus abgeleitet.
- Bedingte Anwendbarkeit konkretisiert; `KI-EXT-002` schützt auch ohne externe Inferenz vor unzulässigen Ausweichzielen. Mittlere Akzeptanz und befristete hohe Ausnahmen getrennt geregelt.
- Migrationshinweis: Die 38 Kontroll-IDs, Quellen-IDs und 228 bisherigen Abschnitts-IDs bleiben erhalten. Neue Risiko-IDs `r-01` bis `r-09` und untergeordnete Abschnitte ergänzen sie. Das Statusfeld `betriebsmodell` lautet jetzt `unternehmensintegriert`; externe Inferenz bleibt im Standard deaktiviert.
- Eigene OSCAL-Eigenschaften und Abschnittsnamen verwenden den Namensraum `https://github.com/adrianweidig/allgemeines-ki-it-sicherheitskonzept/ns/oscal`. Standardnamen bleiben im OSCAL-Namensraum. Verbraucher müssen `ns` berücksichtigen und unbekannte Erweiterungen erhalten.
- Index, Übernahmeleitfaden, Arbeitsregeln und Validierung auf den neuen Stand abgestimmt. Der fachliche Stichtag folgt der Katalogfassung; historische Quellenprüfdaten werden nicht vorgetäuscht aktualisiert.

## Dokumentationsüberarbeitung – 14.09.2026

- A11 festgehalten: Jede betriebliche Tätigkeit bleibt auch bei längerem KI-Ausfall ausführbar; Reparatur und Wiederherstellung erfolgen über reguläre IT-Verfahren. R-06 und die Kontrollzuordnung entsprechend präzisiert; eine Ausnahme nach A10 hebt diese Voraussetzung nicht auf.
- Beschlüsse A01–A10, die noch offenen Risikobewertungen und ihre Zuordnung zu den 38 Kontrollen im Inhaltsindex erschlossen.
- Die empfohlene Akzeptanz mittlerer Restrisiken sowie der begrenzte Ausnahmebetrieb bei hohen und sehr hohen Restrisiken als beschlossene Vorgaben dokumentiert; die fachliche Übernahme steht noch aus.
- Alle 228 Kontrollabschnitte im OSCAL-Katalog mit stabilen IDs versehen und den redaktionellen Index aus den Katalogmetadaten verlinkt.
- Pflege und Prüfung der Kennungen, lokalen Verweise und Zielanker in Arbeitsregeln und Projektvalidierung verankert.
- Migrationshinweis: Kontroll- und Quellenkennungen sowie fachliche Version 0.1.0 bleiben erhalten. Die zusätzlichen Abschnitts-IDs folgen `Kontroll-ID-Abschnittsname`; neue Metadatenverweise begründen keine zusätzliche Anforderung. Normative Texte und das DOCX/PDF-Paar werden durch diese Navigationsergänzung nicht verändert.

## 0.1.0 – 02.09.2026

- Organisationsneutrale lokale Referenzarchitektur festgelegt.
- OSCAL-1.1.3-Katalog mit KI-spezifischen Kontrollen erstellt.
- Quellenregister mit öffentlichen Fundstellen und lokalen Prüfsummen eingeführt.
- Behördenähnliches DOCX-Masterdokument und daraus erzeugte PDF-Lesefassung erstellt.
- Verbindliche Layoutregeln für Typografie, Listen, Tabellen, Silbentrennung und Seitenführung eingeführt.
- Selektiven Blocksatz für zusammenhängenden Fließtext und eigene Ausrichtungen für Tabellen, Listen, Quellen und Beschriftungen eingeführt.
- Die Architektur-, Import-, RAG- und Agentenflüsse als reproduzierbare und barrierearm beschriebene Diagramme ergänzt.
- Diagramme als leicht anpassbare PlantUML-Quellen mit lokaler SVG-/PNG-Erzeugung und SHA-256-Manifest bereitgestellt.
- Organisationsspezifische Übernahmehinweise aus dem Konzept in einen eigenständigen Leitfaden verlagert.
- Referenzbezogene Kontrollformulierungen in reale Anforderungen an Geltungsbereich, Dokumentenführung und Schutzkennzeichnung überführt.
- Maschinelle Layoutprüfung und vollständiger visueller Seitenprüfprozess ergänzt.
- Schutzstatus-, Quellen-, Katalog-, Dokument- und Negativprüfungen eingerichtet.
- Training und Feinabstimmung ausgeschlossen, externe Inferenz als bedingte Variante gekennzeichnet.

### Überarbeitung vom 03.09.2026

- Manuelle Kapitelauflistung durch ein aktualisierbares Word-Inhaltsverzeichnis mit Ebenen 1 und 2, Punkt-Füllzeichen und rechtsbündigen Seitenzahlen ersetzt.
- Redaktionshinweise, pauschale Beratungsausschlüsse und Erklärungen zur Dokumentmechanik aus dem Sicherheitskonzept entfernt.
- Zentrale Fachbegriffe vor ihrer ersten Verwendung erklärt und vermeidbaren englischen Fachjargon durch verständliche deutsche Begriffe ersetzt.
- Risikoverfahren, Risikomatrix und Risikoregister nach BSI-Standard 200-3 ergänzt.
- BSI-Standard 200-2 und BSI-Standard 200-3 mit offiziellen Fundstellen, Prüfsummen und konkreten Seitenbelegen registriert.
- Bearbeitbare PlantUML-Diagramme für Risikoablauf und Risikomatrix ergänzt und die Abbildungsfolge auf sechs Fachdiagramme erweitert.
- Lokalen Word-Schritt zum Aktualisieren der Felder, Speichern des DOCX und Erzeugen der PDF-Lesefassung eingeführt.
- Layoutvalidierung um Inhaltsverzeichnis, Risikokennungen, Redaktionssprache und vermeidbaren Fachjargon erweitert.
- Selbst formulierte Anforderungen, Rollen und Überschriften konsequent auf verständliche deutsche Begriffe umgestellt; unvermeidbare Abkürzungen werden vor ihrer ersten Verwendung erklärt.
- Das Abkürzungsverzeichnis auf zwei Begriffspaare je Zeile umgestellt und eine Prüfung gegen schwach gefüllte Schlussseiten ergänzt.
