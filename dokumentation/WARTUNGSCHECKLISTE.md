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
- [ ] Jede PDF-Seite wurde gerendert und visuell geprüft.
- [ ] DOCX wurde auf Barrierearmut und personenbezogene Metadaten geprüft.
- [ ] `quellen/lokale-eingaben/` ist ignoriert und nicht im Git-Index oder Veröffentlichungsarchiv.

## Einmalige Maintainer-Entscheidungen

- [ ] Passende Lizenz für das Gesamtwerk nach Prüfung der übernommenen und abgeleiteten Inhalte festlegen.
- [ ] Privaten Sicherheitskontakt beziehungsweise GitHub Private Vulnerability Reporting einrichten.
- [ ] Branch Protection nach dem ersten stabilen grünen CI-Lauf aktivieren.
- [ ] Erforderliche Reviews, Statusprüfungen und Administrationsausnahmen für `main` festlegen.
- [ ] Strategie für Tags und GitHub Releases vor der ersten echten Veröffentlichung beschließen.

## Manuelle Fachprüfung

Die Automatisierung ersetzt keine Prüfung durch Informationssicherheit, Datenschutz, Recht, Geheimschutz, Personalvertretung, Betrieb und fachlich verantwortliche Stellen. Vor organisationsspezifischer Nutzung sind Geltungsbereich, Schutzbedarf, Rechtsgrundlagen, Restrisiken und Nachweise neu festzulegen.
