# Validierung und Veröffentlichungsautomatisierung

## Validierungsworkflow

Der Workflow `Projekt validieren` läuft bei Pull Requests, bei Pushes auf `main` und manuell. Er verwendet minimale Leseberechtigungen und prüft:

- Python-Tests einschließlich negativer Fehlerfälle.
- Projektstatus und Ausschlussgrenzen.
- JSON-Syntax, Quellenregister und OSCAL-1.1.3-Schema.
- Kontroll-IDs, Pflichtteile, Quellenverweise und beide Szenariozuordnungen.
- Getrennte Air-Gap- und Cloud-Bewertungen aller neun Risiken.
- Nutzerbelehrung mit höchstens zwei Seiten und gespeicherten Formularwerten.
- DOCX-/PDF-Öffnung, Version, Status, Kontrollbestand und Textähnlichkeit.
- Typografie, Absatzabstände, echte Listen, Listeninterpunktion und deutsche Silbentrennung.
- Feste Tabellengeometrie, ausreichende Zellränder, wiederholte Tabellenköpfe und fehlende exakte Zeilenhöhen.
- Echtes, gespeichertes Word-Inhaltsverzeichnis mit Ebenen 1 und 2, Punkt-Füllzeichen und aktuellen Seitenzahlen.
- PAGE- und NUMPAGES-Felder sowie eine korrekte Seitenführung auf jeder PDF-Seite.
- Acht prüfsummengebundene Fachdiagramme einschließlich Risikoprozess und Risikomatrix.
- Ausschluss von Redaktionshinweisen, pauschalen Beratungsausschlüssen und vermeidbarem Fachjargon aus dem Sicherheitskonzept.
- Unerwünschte Ersatzschreibweisen, Platzhalter, Geheimnismuster und unzulässige Konformitätsbehauptungen.
- Öffentliche Quellenlinks mit differenzierter Behandlung temporärer Sperren.
- Ausschluss lokaler Eingaben aus Git und Veröffentlichungsarchiv.

Da `quellen/lokale-eingaben/` absichtlich nicht im Repository liegt, verwendet der CI-Lauf `--ohne-lokale-eingaben`. Er prüft die registrierten Metadaten und lädt die amtlichen Online-PDFs für den Prüfsummenvergleich; die Existenz und Prüfsumme der lokalen Fassungen wird ausschließlich im vollständigen lokalen Lauf ohne diese Option geprüft.

Die Binärdokumente werden vor dem Commit lokal erzeugt. `validierung/aktualisiere_word_felder.ps1` öffnet das generierte DOCX in Microsoft Word, aktualisiert Inhaltsverzeichnis und Seitenfelder, speichert das Masterdokument und erzeugt daraus die PDF-Lesefassung. Der Linux-CI-Lauf verändert diese Artefakte nicht, sondern prüft den gespeicherten Endstand.

## Veröffentlichungsartefakt

Der Workflow `Veröffentlichungsartefakt erstellen` läuft bei jedem Push auf `main` und manuell. Er erzeugt mit `git archive` ein ZIP des konkreten Commits mit einem eindeutigen Stammverzeichnis sowie maschinenlesbare Prüfsummen und deutsche Veröffentlichungsnotizen. Es werden keine Tags und keine GitHub Releases erzeugt.

## Abhängigkeiten

Dependabot prüft GitHub Actions und die fixierten Python-Abhängigkeiten monatlich. Es existiert kein Docker- oder GHCR-Workflow, weil dieses Repository keine Laufzeitkomponente und kein Containerabbild liefert.

## Schutz des öffentlichen Referenzbestands

Auf GitHub schlägt jede Fassung mit `organisationsspezifisch: true`, aktivem Training, aktiver Feinabstimmung oder externer Inferenz fehl. Die automatisierte Inhaltssuche ist ein zusätzliches Warnnetz und keine vollständige Klassifizierungsautomatik.
