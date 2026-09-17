# Arbeitsregeln für dieses Repository

## Projektüberblick

Dieses Repository enthält ausschließlich eine öffentliche, organisationsneutrale Referenz für ein KI-Informationssicherheitskonzept mit Air-Gap- und Cloud-Szenario. Fachliche Kernergebnisse sind ein OSCAL-Katalog, ein abgestimmtes DOCX/PDF-Paar und eine allgemein verwendbare Nutzerbelehrung als Anlage. Es entstehen keine Anwendung und keine produktive KI-Komponente.

## Schutz- und Inhaltsgrenzen

- Der Dokumentstatus lautet `ÖFFENTLICH – organisationsneutrale Referenzvorlage`. Die Sichtbarkeit des GitHub-Repositories wird dadurch nicht festgelegt oder geändert.
- Organisationsdaten, reale Hostnamen, IP-Adressen, Domänen, Konten, interne Schwachstellen, Geheimnisse und eingestufte Inhalte sind verboten.
- Organisationsspezifische Anpassungen erfolgen ausschließlich in einer getrennten geschützten Fassung mit eigener Status- und Kennzeichnungsprüfung. Private Inhalte werden nicht zurückübertragen. Allgemeine Formulierungen und Gestaltung dürfen nach ausdrücklicher Freigabe und vollständiger Entfernung organisationsspezifischer Angaben übernommen werden.
- Training, Feinabstimmung, selbsttätiges Lernen und produktive Änderungen von Modellgewichten bleiben ausgeschlossen.
- Der Katalog beschreibt Air-Gap und Cloud als getrennte Referenzszenarien. `externe-inferenz: false` in `projektstatus.json` beschreibt die nicht ausführende Referenzablage und deaktiviert nicht das fachliche Cloud-Szenario.
- `quellen/lokale-eingaben/` bleibt vollständig von Git ausgeschlossen.

## Fachliche Bearbeitung

- Einstieg für die Recherche ist `dokumentation/INHALTSINDEX.md`. Von dort über Entscheidungs-, Risiko-, Kontroll- und Quellenkennungen zur maßgeblichen Stelle navigieren; Seiten- und Zeilennummern sind nur ergänzende Orientierung.
- Kontrollabschnitte besitzen stabile OSCAL-IDs nach dem Muster `ki-gov-003-statement`. Fachliche Texte nur in ihrer maßgeblichen Quelle pflegen; Index und Querverweise bei jeder betroffenen Änderung mitführen und validieren.
- Beschluss und Umsetzung getrennt kennzeichnen. Die Praxisprüfung dokumentiert die Entscheidungshistorie; der Inhaltsindex nennt den aktuellen Übernahmestand. Ein Navigationsverweis allein begründet keine neue Anforderung.

- Der OSCAL-Katalog ist die normative Quelle. Keine zusätzliche Muss-Anforderung ausschließlich im DOCX ergänzen. Auch die neun Risikobewertungen liegen dort unter `ki-gov-003-risk-register`; Text und Risikomatrix werden daraus abgeleitet. Eigene OSCAL-Namen verwenden den dokumentierten Projektnamensraum.
- Das Konzept beschreibt den vorgesehenen Sollzustand wie eine reale Konzeptfassung. Anpassungs-, Redaktions- und Übernahmehinweise gehören ausschließlich in README und `dokumentation/ÜBERNAHMELEITFADEN.md`.
- Jede Kontrolle besitzt `statement`, `rationale`, `guidance` und `source`, eine ausdrückliche Szenariozuordnung sowie öffentliche Fundstellen. Das Fachkonzept druckt Festlegung und Anwendung. Herleitungen bleiben im Katalog. Zusätzliche Nachweisblöcke und Nachweisregister entfallen.
- Version 0.3.0 führt 34 Kontrollen in 22 Gruppen. KI-ARC-001, KI-CON-001, KI-CON-002 und KI-ASS-001 entfallen ohne Neunummerierung. Die neun Risiko-IDs bleiben erhalten, jede mit separater Air-Gap- und Cloud-Bewertung. Historische Prüfberichte sind keine aktuelle Bewertungsgrundlage.
- Funktionen und Schutzgrenzen bleiben unabhängig von Produkten, Hardwaremengen und Kapazitäten. Kein individuelles Betriebswissen in die Referenz übernehmen. Eine Risikoakzeptanz einer konkreten Umgebung gilt nicht für die Referenzszenarien.
- Bei einer inhaltlichen Katalogrevision die Dokument-UUID neu erzeugen und `metadata.last-modified` auf den tatsächlichen Speicherzeitpunkt setzen.
- Quellen-IDs und Kontroll-IDs bleiben stabil. Änderungen erfordern Migrationshinweis und Changelog-Eintrag.
- ISO-Inhalte nur als öffentliche Kennungen und Metadaten referenzieren; keine proprietären Normentexte übernehmen.
- Empfehlungen dürfen nur mit dokumentierter KI-Risikobegründung zu projektinternem `MUSS` verschärft werden.
- Deutsche Texte verwenden korrekte Umlaute. Technisch vorgeschriebene OSCAL- und GitHub-Bezeichnungen bleiben unverändert.

## Befehle

```powershell
python -m pip install -r validierung/anforderungen.txt
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
python validierung/erzeuge_dokumente.py
powershell -NoProfile -ExecutionPolicy Bypass -File validierung/aktualisiere_word_felder.ps1
```

## Dokumente und Darstellung

- DOCX ist das redaktionelle Masterdokument; PDF wird ausschließlich daraus erzeugt.
- `dokumentation/LAYOUTREGELN.md` ist für Typografie, Absatzrhythmus, Listen, Tabellen, Silbentrennung sowie Kopf- und Fußzeilen verbindlich.
- Dokumente werden ausschließlich über `validierung/erzeuge_dokumente.py` geändert. Manuelle Abweichungen der Binärdateien vom Generator sind unzulässig.
- Aufzählungen verwenden echte Word-Listen. Listenpunkte enden nicht mit einem Strichpunkt.
- Zusammenhängender Fließtext verwendet den Stil `Fließtext` mit Blocksatz und deutscher Silbentrennung. Tabellen, Listen, Quellen, Beschriftungen und kurze Hinweise bleiben linksbündig.
- Tabellen verwenden feste DXA-Geometrie, ausreichende Zellränder, wiederholte Kopfzeilen und keine exakten Zeilenhöhen.
- Architektur, Datenflüsse und Entscheidungswege werden als versionierte PlantUML-Diagramme unter `diagramme/` gepflegt. Tabellen dienen nicht als Ersatz für Diagramme.
- Diagramme werden als SVG für Markdown und als hochauflösendes PNG für das DOCX erzeugt. Sie stehen inline, besitzen eine unmittelbare Beschriftung und einen vollständigen Alternativtext.
- Nach einer Änderung an einer `.puml`-Quelle ist zuerst `validierung/erzeuge_diagramme.py` und danach `validierung/erzeuge_dokumente.py` auszuführen. Quelle und Ableitungen müssen dem Diagrammmanifest entsprechen.
- Das Inhaltsverzeichnis ist ein echtes Word-Feld für die Überschriftsebenen 1 und 2. Vor dem PDF-Export werden Feld und Seitenzahlen aktualisiert und das DOCX gespeichert.
- Redaktionsanleitungen, Erklärungen zur Dokumentmechanik und pauschale Beratungsausschlüsse bleiben außerhalb des Fachkonzepts.
- Fachbegriffe werden im tabellarischen Glossar am Ende erklärt. Abkürzungen werden bei erster Verwendung ausgeschrieben. Quellen stehen vollständig nur im Quellenverzeichnis, mit nummerierten Kurzverweisen im Text.
- Risiken werden nach BSI-Standard 200-3 als Szenarien mit Eintrittshäufigkeit, Schadenshöhe, Ausgangsrisiko, Behandlung und erneut bewertetem Restrisiko geführt.
- Deutsche Silbentrennung und die Korrektursprache `de-DE` müssen aktiviert bleiben.
- Die Konzeptseiten tragen den öffentlichen Referenzstatus und die Seitenzählung. Die Belehrung enthält keine Einstufung und keinen Autor. Sie umfasst höchstens zwei Seiten mit ausfüllbaren Textfeldern und einem digitalen Signaturfeld.
- Nach einer Dokumentänderung DOCX und jede PDF-Seite rendern und visuell prüfen.
- Keine Behördenlogos, Wappen oder Gestaltungselemente verwenden, die amtliche Herausgeberschaft vortäuschen.
- Barrierearmut, beschreibende Links, Tabellenüberschriften, ausreichenden Kontrast und sinnvolle Lesereihenfolge prüfen.

## GitHub und Automatisierung

- Änderungen müssen Validierung, Negativtests und Veröffentlichungsartefakt berücksichtigen.
- Kein Docker- oder GHCR-Workflow: Dieses Repository liefert keine Laufzeitkomponente.
- Keine Tags oder GitHub Releases ohne beschlossene Veröffentlichungsstrategie.
- Keine Secrets erzeugen, ausgeben oder in Repository, Beispiele, Logs oder Workflows schreiben.
- Bestehende Nutzeränderungen erhalten; keine destruktiven Git-Befehle und keine unbegründeten Formatierungswellen.
