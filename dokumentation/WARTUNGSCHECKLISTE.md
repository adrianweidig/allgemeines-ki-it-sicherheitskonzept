# Wartungscheckliste

## Vor jeder fachlichen Fassung

- [ ] `projektstatus.json` erlaubt ausschließlich organisationsneutrale öffentliche Inhalte.
- [ ] Keine Organisationsnamen, realen Hostnamen, IP-Adressen, Domänen, Konten, internen Schwachstellen oder Geheimnisse enthalten.
- [ ] Training und Feinabstimmung bleiben deaktiviert.
- [ ] Externe Inferenz bleibt deaktiviert oder wird nur in einer getrennten organisationsspezifischen Fassung vollständig neu bewertet.
- [ ] Alle verwendeten Quellen sind erreichbar, nicht überfällig und inhaltlich geprüft.
- [ ] Neue Aussagen besitzen genaue Fundstellen und eine nachvollziehbare Autoritätsstufe.
- [ ] Verschärfungen zu `MUSS` sind mit einem KI-spezifischen Risiko begründet.
- [ ] Kontroll-IDs, Querverweise und Zuordnungen sind vollständig.
- [ ] OSCAL-Katalog besteht die offizielle 1.1.3-Schemaprüfung.
- [ ] DOCX und PDF tragen dieselbe Version und denselben Status wie der Katalog.
- [ ] Die maschinellen Regeln aus `dokumentation/LAYOUTREGELN.md` sind vollständig erfüllt.
- [ ] Fließtext, Aufzählungen, Tabellen, Diagramme, Silbentrennung, Kopfzeilen, Fußzeilen und Seitenzahlen entsprechen dem verbindlichen Gestaltungsprofil.
- [ ] Das automatische Inhaltsverzeichnis enthält Ebenen 1 und 2, rechtsbündige aktuelle Seitenzahlen und Punkt-Füllzeichen.
- [ ] Konzepttext enthält keine Übernahme- oder Redaktionsanleitung, keinen pauschalen Beratungsausschluss und keine Erklärung zur Dokumentmechanik.
- [ ] Vermeidbarer Fachjargon wurde ersetzt; unvermeidbare Fachbegriffe sind vor ihrer ersten Verwendung erklärt.
- [ ] Risikoprozess, Risikomatrix und Risikoregister sind widerspruchsfrei; Ausgangs- und Restrisiken besitzen dieselben stabilen Kennungen.
- [ ] Jede Abbildung besitzt eine PlantUML-Quelle, zum Manifest passende SVG- und PNG-Ableitungen, eine unmittelbare Beschriftung und einen vollständigen Alternativtext.
- [ ] Diagramme sind bei 100 Prozent lesbar, nicht gedreht und verwenden Farbe nicht als einzigen Bedeutungsträger.
- [ ] Jede PDF-Seite wurde gerendert und visuell geprüft.
- [ ] DOCX wurde auf Barrierearmut und personenbezogene Metadaten geprüft.
- [ ] `quellen/lokale-eingaben/` ist ignoriert und nicht im Git-Index oder Veröffentlichungsarchiv.

## Einmalige Maintainer-Entscheidungen

- [ ] Passende Lizenz für das Gesamtwerk nach Prüfung der übernommenen und abgeleiteten Inhalte festlegen.
- [ ] Privaten Sicherheitskontakt beziehungsweise GitHub Private Vulnerability Reporting einrichten.
- [ ] Branch Protection nach dem ersten stabilen grünen CI-Lauf aktivieren.
- [ ] Erforderliche Überprüfungen, Statusprüfungen und Administrationsausnahmen für `main` festlegen.
- [ ] Strategie für Tags und GitHub Releases vor der ersten echten Veröffentlichung beschließen.

## Manuelle Fachprüfung

Die Automatisierung ersetzt keine Prüfung durch Informationssicherheit, Datenschutz, Recht, Geheimschutz, Personalvertretung, Betrieb und fachlich verantwortliche Stellen. Das Übernahmeverfahren und die dabei neu festzulegenden Inhalte beschreibt `dokumentation/ÜBERNAHMELEITFADEN.md`.
