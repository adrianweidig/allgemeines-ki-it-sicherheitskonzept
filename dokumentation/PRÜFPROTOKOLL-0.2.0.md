# Prüfprotokoll zur Fassung 0.2.0

Prüfdatum: 14.09.2026. Gegenstand sind der [OSCAL-Katalog](../katalog/ki-it-sicherheitskatalog.oscal.json), das daraus abgeleitete [DOCX](../konzept/ki-it-sicherheitskonzept.docx), dessen [PDF-Lesefassung](../konzept/ki-it-sicherheitskonzept.pdf) und die zugehörige Dokumentation. Die Prüfung betrifft die Konzeptfassung, nicht die Wirksamkeit einer Unternehmensumsetzung.

## Fachliche Übernahme

A01–A11 und P01–P12 sind übernommen. Die Zuordnung führt über den [Inhaltsindex](INHALTSINDEX.md) zu den stabilen Kontroll- und Risikokennungen. Alle 38 Kontrollen besitzen Anforderung, Begründung, Umsetzung, Prüfziel, Nachweise, Anwendbarkeit und Quellenbezug.

Die neun Ausgangs- und Restrisiken stehen mit Maßnahmen, Annahmen und Begründung im Katalog unter `ki-gov-003-risk-register`. Dokument und Risikomatrix werden daraus erzeugt. Bewertet wird das schädliche Szenario unter den beschriebenen Bedingungen; eine niedrige Eintrittshäufigkeit ist keine Garantie und verringert nicht automatisch die Schadenshöhe. Insbesondere beruht R-06 auf unabhängiger Weiterarbeit ohne KI, nicht auf einer zugesagten Reparaturzeit.

## Technische und redaktionelle Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Strenge Projektvalidierung im Checkout ohne ignorierte Eingangs-PDFs | 0 Fehler, 0 Warnungen |
| Automatisierte Prüf- und Negativtests | 29 bestanden |
| Offizielles NIST-Katalogschema OSCAL 1.1.3 | Bestanden |
| Eigene Namensräume, eindeutige IDs, neun Risikobewertungen und Kontrollverweise | Bestanden |
| Vollständige Übernahme der normativen Kontroll- und Risikoprosa in das DOCX | Bestanden |
| Abgleich des DOCX- und PDF-Textes | Bestanden |
| Sechs PlantUML-Quellen, SVG-/PNG-Ableitungen und SHA-256-Manifest | Bestanden |
| Word-Inhaltsverzeichnis und Seitenfelder | Aktualisiert; DOCX vor PDF-Export gespeichert |
| Visuelle Kontrolle der Word-Ausgabe über alle gerenderten PDF-Seiten | 73 Seiten geprüft; keine abgeschnittenen Diagramme oder überlagerten Inhalte festgestellt |

Die Sichtprüfung umfasst Deckblatt, Inhaltsverzeichnis, Tabellenfortsetzungen, Risikomatrix, alle sechs Diagramme, Quellen, Kopf- und Fußzeilen. Diagramme werden proportional auf höchstens 20,5 cm Höhe begrenzt; Beschriftungen und Tabellenköpfe bleiben mit ihrem Folgeinhalt verbunden. Die allgemeinen und organisationsspezifischen Fassungen wurden getrennt erzeugt und geprüft. Die technische Prüfung ist kein vollständiges Barrierefreiheitsgutachten.

## Reproduktion und Grenzen

```powershell
python validierung/validiere_projekt.py --streng --ohne-lokale-eingaben
python -m unittest discover -s validierung/testfälle -p "test_*.py"
```

In einer organisationsspezifischen Fassung zusätzlich `--offline-anpassung` verwenden. Die fünf ursprünglichen lokalen Quellen-PDFs sind nicht Teil des Git-Checkouts. Ihre alten Binärfassungen konnten hier deshalb nicht erneut lokal gegen die registrierten Prüfsummen geprüft werden; der Schalter nimmt nur diese Eingangsdateiprüfung aus.

Die zusätzliche Onlineprüfung der öffentlichen Quellen ergab 0 Fehler und 10 Abrufwarnungen: acht ISO-Metadatenseiten antworteten mit HTTP 403; die BMI-Fundstelle und ihr PDF-Abruf scheiterten mit HTTP 400. Diese Abrufe belegen keine erneute Inhaltsprüfung. Die betroffenen Fundstellen bleiben zur manuellen Wiedervorlage offen; historische Abruf- und Inhaltsprüfdaten im Quellenregister wurden nicht vorgetäuscht aktualisiert.

Die Risikobewertungen bleiben begründete Planungsbewertungen. Eine Übernahme in den Betrieb setzt die tatsächlich vorhandenen Basismaßnahmen, die dokumentierten Annahmen und die zuständige Risikoentscheidung voraus. Die ISO-/BSI-Zuordnungen dienen der Orientierung; Schema- und Dokumentprüfungen bestätigen keine Zertifizierung oder organisationsbezogene Normkonformität.
