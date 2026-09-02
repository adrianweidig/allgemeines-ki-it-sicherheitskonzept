# Veröffentlichungsprozess

## Bootstrap

Der Bootstrap initialisiert das private Repository auf `main`, enthält keine Tags und erzeugt kein GitHub Release. Die erste gemeinsame fachliche Fassung aus OSCAL-Katalog, DOCX und PDF trägt `0.1.0`.

## Fachliche Fassung

1. Quellen und Wiedervorlagen prüfen.
2. Normative Änderungen im OSCAL-Katalog bearbeiten.
3. Quellenregister und Zuordnungen aktualisieren.
4. Dokumente aus dem abgestimmten Bestand erzeugen.
5. automatisierte und manuelle Prüfungen vollständig durchführen;
6. Versionsgleichheit und Prüfsummen festhalten;
7. Änderungen in `CHANGELOG.md` dokumentieren;
8. über Pull Request und fachliches Review nach `main` übernehmen.

## Actions-Artefakt

Jeder Push auf `main` erzeugt ein Commit-genaues ZIP und Veröffentlichungsnotizen. Der Dateiname enthält Repository, Branch und kurze Commit-SHA. `git archive` schließt `.git`, ignorierte lokale Eingaben und temporäre Arbeitsdaten aus.

## Spätere Releases

Tags und GitHub Releases werden erst nach dokumentierter Maintainer-Entscheidung eingesetzt. Vorher sind Versionsschema, Signaturverfahren, Aufbewahrung, Freigaberollen und Rücknahmeprozess festzulegen.
