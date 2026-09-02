# Validierung und Veröffentlichungsautomatisierung

## Validierungsworkflow

Der Workflow `Projekt validieren` läuft bei Pull Requests, bei Pushes auf `main` und manuell. Er verwendet minimale Leseberechtigungen und prüft:

- Python-Tests einschließlich negativer Fehlerfälle;
- Projektstatus und Ausschlussgrenzen;
- JSON-Syntax, Quellenregister und OSCAL-1.1.3-Schema;
- Kontroll-IDs, Pflichtteile, Quellenverweise und bedingte Kontrollen;
- DOCX-/PDF-Öffnung, Version, Status, Kontrollbestand und Textähnlichkeit;
- unerwünschte Ersatzschreibweisen, Platzhalter, Geheimnismuster und unzulässige Konformitätsbehauptungen;
- öffentliche Quellenlinks mit differenzierter Behandlung temporärer Sperren;
- Ausschluss lokaler Eingaben aus Git und Veröffentlichungsarchiv.

Da `quellen/lokale-eingaben/` absichtlich nicht im Repository liegt, verwendet der CI-Lauf `--ohne-lokale-eingaben`. Er prüft die registrierten Metadaten und lädt die amtlichen Online-PDFs für den Prüfsummenvergleich; die Existenz und Prüfsumme der lokalen Fassungen wird ausschließlich im vollständigen lokalen Lauf ohne diese Option geprüft.

## Veröffentlichungsartefakt

Der Workflow `Veröffentlichungsartefakt erstellen` läuft bei jedem Push auf `main` und manuell. Er erzeugt mit `git archive` ein ZIP des konkreten Commits mit einem eindeutigen Stammverzeichnis sowie maschinenlesbare Prüfsummen und deutsche Veröffentlichungsnotizen. Es werden keine Tags und keine GitHub Releases erzeugt.

## Abhängigkeiten

Dependabot prüft GitHub Actions und die fixierten Python-Abhängigkeiten monatlich. Es existiert kein Docker- oder GHCR-Workflow, weil dieses Repository keine Laufzeitkomponente und kein Containerabbild liefert.

## Schutz des öffentlichen Referenzbestands

Auf GitHub schlägt jede Fassung mit `organisationsspezifisch: true`, aktivem Training, aktiver Feinabstimmung oder externer Inferenz fehl. Die Heuristik ist ein zusätzliches Warnnetz und keine vollständige Klassifizierungsautomatik.
