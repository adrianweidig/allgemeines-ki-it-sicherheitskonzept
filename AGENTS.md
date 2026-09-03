# Arbeitsregeln für dieses Repository

## Projektüberblick

Dieses Repository enthält ausschließlich eine öffentliche, organisationsneutrale Referenz für ein KI-IT-Sicherheitskonzept. Fachliche Kernergebnisse sind genau ein OSCAL-Katalog sowie ein inhaltlich abgestimmtes DOCX/PDF-Paar. Es entstehen keine Anwendung und keine produktive KI-Komponente.

## Schutz- und Inhaltsgrenzen

- Der veröffentlichte Status lautet `ÖFFENTLICH – organisationsneutrale Referenzvorlage`.
- Organisationsdaten, reale Hostnamen, IP-Adressen, Domänen, Konten, interne Schwachstellen, Geheimnisse und eingestufte Inhalte sind verboten.
- Vor einer organisationsspezifischen Anpassung ist eine getrennte Offline-Fassung anzulegen und `organisationsspezifisch` auf `true` zu setzen.
- Training, Feinabstimmung, selbsttätiges Lernen und produktive Änderungen von Modellgewichten bleiben ausgeschlossen.
- Externe Inferenz ist im Standardmodell deaktiviert.
- `quellen/lokale-eingaben/` bleibt vollständig von Git ausgeschlossen.

## Fachliche Bearbeitung

- Der OSCAL-Katalog ist die normative Quelle. Keine zusätzliche Muss-Anforderung ausschließlich im DOCX ergänzen.
- Das Konzept beschreibt den vorgesehenen Sollzustand wie eine reale Konzeptfassung. Anpassungs-, Redaktions- und Übernahmehinweise gehören ausschließlich in README und `dokumentation/ÜBERNAHMELEITFADEN.md`.
- Jede Kontrolle benötigt Anforderung, Begründung, Umsetzung, Prüfziel, Nachweis, Anwendbarkeit und konkrete öffentliche Fundstelle.
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
- Deutsche Silbentrennung und die Korrektursprache `de-DE` müssen aktiviert bleiben.
- Die Seitenführung verwendet ab Seite 2 links den kurzen Schutzstatus und rechts `Seite X von Y`.
- Nach einer Dokumentänderung DOCX und jede PDF-Seite rendern und visuell prüfen.
- Keine Behördenlogos, Wappen oder Gestaltungselemente verwenden, die amtliche Herausgeberschaft vortäuschen.
- Barrierearmut, beschreibende Links, Tabellenüberschriften, ausreichenden Kontrast und sinnvolle Lesereihenfolge prüfen.

## GitHub und Automatisierung

- Änderungen müssen Validierung, Negativtests und Veröffentlichungsartefakt berücksichtigen.
- Kein Docker- oder GHCR-Workflow: Dieses Repository liefert keine Laufzeitkomponente.
- Keine Tags oder GitHub Releases ohne beschlossene Veröffentlichungsstrategie.
- Keine Secrets erzeugen, ausgeben oder in Repository, Beispiele, Logs oder Workflows schreiben.
- Bestehende Nutzeränderungen erhalten; keine destruktiven Git-Befehle und keine unbegründeten Formatierungswellen.
