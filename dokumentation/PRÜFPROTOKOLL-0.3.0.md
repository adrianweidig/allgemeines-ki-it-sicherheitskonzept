# Prüfung der Referenzfassung 0.3.0

Die Fassung vom 17.09.2026 umfasst einen OSCAL-Katalog mit 34 Kontrollen in 22 Gruppen, neun Risiken mit getrennten Air-Gap- und Cloud-Bewertungen sowie Konzept und Nutzerbelehrung als DOCX/PDF. Sie enthält keine betriebliche Freigabe oder Aussage über die Umsetzung in einer konkreten Organisation.

## Fachliche Prüfung

- Gemeinsame KI-Regeln und getrennte Datenwege für Air-Gap und Cloud. Cloud umfasst ausschließlich die zugelassene Modellverarbeitung mit internem Dokumentbestand und interner Rechteprüfung.
- Produktneutrale Festlegungen, reguläre Nutzersitzung für Agentenaktionen und ausschließlich administrative Verwaltung serverseitiger KI-Funktionen.
- KI-ARC-001, KI-CON-001, KI-CON-002 und KI-ASS-001 entfallen ohne Neunummerierung. Keine zusätzlichen Nachweisblöcke im Fachkonzept.
- Die neun Risiko-IDs behalten ihren Fachgegenstand. Eine organisationsspezifische Bewertung oder Risikoakzeptanz wurde nicht übernommen.
- Die DSK-Orientierungshilfe wurde für Trainingsausschluss, Speicherung, Löschung und Cloud-Datenverarbeitung erneut geprüft. Quellenkennungen und Rückverweise sind zugeordnet.

## Dokumenterzeugung

Acht PlantUML-Abbildungen wurden lokal als SVG und PNG erzeugt. Das Manifest verbindet Quellen und Ableitungen. Die Konzeptfassung wurde als DOCX erzeugt, in Word mit aktualisiertem Inhaltsverzeichnis gespeichert und daraus als PDF exportiert. Die Nutzerbelehrung wird ebenfalls über den Generator erzeugt und nach dem Word-Export um echte Formularfelder ergänzt.

## Abschließende Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Strenge lokale Projektvalidierung | 0 Fehler, 0 Warnungen, einschließlich lokaler Quellenfassungen |
| Regression | Alle 33 Tests bestanden. Szenariozuordnung, Risikomatrix, Dokumentableitung, Formular und persönliche Metadaten sind einbezogen |
| Online-Quellenprüfung | 0 Fehler, 10 Abrufwarnungen. Q-BMI-001 antwortete für die Fundstelle und den PDF-Abruf mit HTTP 400, acht ISO-Seiten mit HTTP 403. Diese Abrufe bestätigen keine aktuelle Erreichbarkeit. Vorhandene Quellenfassungen und bibliografische Angaben bleiben erhalten |
| Katalog und Editor | 34 Kontrollen, 22 Gruppen, 247 eindeutige IDs und neun Risiken. Import, gezielte Bearbeitung, Export, Wiederöffnung und unveränderte Rückgabe in Chromium und Firefox bestanden. 0 Schemafehler, 0 Fachfehler, 0 Seitenfehler und 0 Netzabrufe. Ein Hinweis betrifft den separat auswählbaren Markdown-Inhaltsindex |
| Dokumente und Darstellung | 36 Konzeptseiten und eine Seite Belehrung. Alle Seiten nach dem endgültigen Word-Export gerendert und visuell geprüft. Acht beschriftete Grafiken mit Alternativtexten, wiederholte Tabellenköpfe, aktualisiertes Inhaltsverzeichnis und vollständige Seitenzählung |
| Quellen und Glossar | 41 vollständige Literaturangaben einmalig im Quellenverzeichnis. Kurze verlinkte Verweise im Fachtext. 31 Begriffe und Abkürzungen im abschließenden Glossar |
| Formular und Signatur | Drei Textfelder und ein leeres Zertifikatssignaturfeld. Ausfüllen mit Umlauten, Speichern, Wiederöffnung und Darstellung geprüft. Lokaler Signaturtest mit flüchtiger Testidentität bestanden, gesamte Datei erfasst und Feldsperre eingehalten. Ausgelieferte Vorlage leer und unsigniert |
| Inhaltsgrenzen | Allgemeine Formulierungen ohne Organisationsbezeichnungen, individuelle Betriebsangaben oder personenbezogene Bearbeitermetadaten übernommen. Quelldateien, DOCX-Inhalte und PDF-Metadaten geprüft. Lokale Eingaben und Arbeitsdaten bleiben ausgeschlossen |
| Lokale Verweise | 70 lokale Links in den geänderten Markdown-Dateien geprüft. Katalog- und Indexverweise sind zusätzlich Bestandteil der Projektvalidierung |

Die Editorprüfung verwendet Commit `eee0aa912a6f6425471c838fa2193976fdba8fc4` in einem unveränderten Editorarbeitsbaum. Das lokale Ergebnis liegt unter `.arbeitsdaten/struktur-v0.3.0/editor-kompatibilitaet.json`. Seitenbilder, Formularprüfung und Signaturergebnis liegen unter `.arbeitsdaten/qa-0.3.0/`. Diese Hilfsdateien gehören nicht zum Git-Bestand.

Die Prüfungen betreffen die Referenzdokumente und ihre Erzeugung. Eine Prüfung produktiver Systeme ist nicht Bestandteil dieser Bearbeitung. Der Status entfernter GitHub-Actions-Läufe wird getrennt vom lokalen Prüfergebnis geführt.

| Datei | SHA-256 |
|---|---|
| `katalog/ki-it-sicherheitskatalog.oscal.json` | `78a25142c9334a6a15b69cf26e6629254ff7daff28d14442a18cbc9fda3ab769` |
| `diagramme/diagramm-manifest.json` | `e44743fe7256518b22464815c5493f4ef136981d68c6e8e9d02b8a4f500bcc97` |
| `konzept/ki-it-sicherheitskonzept.docx` | `5c62bdcb111cc7b1274b1739558819f04bcc3d5b887ae962b9fdf15b79ac324c` |
| `konzept/ki-it-sicherheitskonzept.pdf` | `0c7ec56a237f4e110f1df0a2cdca5e915ba7a3e1abbdcda4753cbb8cc7045e61` |
| `konzept/anlage-1-nutzerbelehrung.docx` | `ee37f7465cb0fc4a1bf303985c4d4f93d66d0aa3114b1899a7d791be38eee976` |
| `konzept/anlage-1-nutzerbelehrung.pdf` | `f80d372e4cbadc265e426789e16f90e9a789459890016d895d1beba5bbb0aefd` |
