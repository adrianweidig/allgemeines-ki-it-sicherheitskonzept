# Allgemeines KI-IT-Sicherheitskonzept

> [!CAUTION]
> **ÖFFENTLICH – organisationsneutrale Referenzvorlage.** Jede Anreicherung mit organisationsspezifischen Informationen beendet diesen Status. Anpassungen dürfen ausschließlich in einer getrennten, angemessen geschützten geschützte Fassung begonnen werden. Dort ist `organisationsspezifisch` in `projektstatus.json` vor der ersten Anpassung auf `true` zu setzen; die Dokumentkennzeichnung wechselt dadurch auf **NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH**. Eine formale Einstufung darf nur die zuständige Organisation durch befugte Stellen vornehmen.

![Lokale KI-Systemarchitektur mit Vertrauenszonen](dokumentation/medien/architektur.svg)

Dieses Repository entwickelt eine prüf- und zertifizierungsvorbereitende Referenz für den sicheren Betrieb unternehmensintegrierter KI mit bevorzugter lokaler Inferenz. Es enthält keine Anwendung, Arbeitsoberfläche, Plattform oder produktive KI-Komponente. Es setzt ein wirksames allgemeines IT-Sicherheitskonzept voraus und ergänzt dieses ausschließlich um KI-spezifische Risiken, Verschärfungen, Prüfziele und Nachweise.

## Kernergebnisse

- [`Inhaltsindex für Menschen und KI-Agenten`](dokumentation/INHALTSINDEX.md): stabile Kennungen, Querverweise und Entscheidungsstand für Kontrollen, Risiken und Überarbeitung.
- [`katalog/ki-it-sicherheitskatalog.oscal.json`](katalog/ki-it-sicherheitskatalog.oscal.json): normativer OSCAL-Katalog nach OSCAL 1.1.3.
- `konzept/ki-it-sicherheitskonzept.docx`: redaktionelles Masterdokument.
- `konzept/ki-it-sicherheitskonzept.pdf`: ausschließlich aus derselben DOCX-Fassung erzeugte Lesefassung.
- [`quellen/quellenregister.json`](quellen/quellenregister.json): nachvollziehbare öffentliche Fundstellen, Prüfsummen und konkrete Belegstellen.

Die aktuelle gemeinsame fachliche Fassung trägt die Version `0.2.0`. Alle abgestimmten Praxisänderungen sind übernommen; neun begründete Ausgangs- und Restrisiken werden direkt im Katalog geführt. Der OSCAL-Katalog ist für normative Anforderungen maßgeblich. Das Konzept erläutert Architektur, Anwendung und Zusammenwirken; es führt keine zusätzlichen, nur dort vorhandenen Muss-Anforderungen ein.

## Konzept und Übernahmeanleitung

Das DOCX/PDF-Paar ist bewusst wie ein tatsächlich geltendes Sicherheitskonzept formuliert. Redaktionshinweise, Platzhalter und Arbeitsanweisungen zur Anpassung stehen nicht im Konzept. Der separate [`Leitfaden zur organisationsspezifischen Übernahme`](dokumentation/ÜBERNAHMELEITFADEN.md) beschreibt Schutzgrenze, Anpassungsreihenfolge, Statuswechsel, Diagrammpflege, Nachweise und Freigaben.

Die öffentliche Fassung darf nicht direkt mit internen Angaben ergänzt werden. Jede organisationsspezifische Bearbeitung beginnt in einer getrennten, angemessen geschützten geschützte Fassung und aktiviert dort vor der ersten realen Angabe das Statusgate.

## Geltungsbereich

Die Standardumgebung umfasst verwaltete Clients, die vorhandene Unternehmensanmeldung und kontrollierte KI-Zugänge. Lokale Inferenz kann zentral oder mit gleichwertigem Schutz auf Endgeräten erfolgen. Container, Wissenssuche und Erweiterungen sind bedingte Funktionen. Bestehende Identitäts-, Entwicklungs-, Daten- und Betriebsdienste werden nach dem allgemeinen IT-Sicherheitskonzept integriert.

Vorausgesetzt werden wirksame Unternehmensprozesse für Identitäten, Endgeräte, Netze, Software, Dokumente, Qualitätssicherung, Protokollierung und Datensicherung. KI-spezifische Kontrollen verweisen auf diese Prozesse und ergänzen deren Schutz. Direkte Schnittstellen dürfen die vorgesehenen Zugriffsregeln nicht umgehen.

Fernzugriff und zugelassene Unternehmensdienste folgen den bestehenden IT-Regeln. Jede betriebliche Tätigkeit bleibt ohne KI möglich, auch bei längerem Ausfall. Persönliche Speicherung ist im normalen Rahmen zulässig; Unternehmenswissen aus persönlicher Agentenarbeit ist freiwillig, sichtbar und standardmäßig ausgeschaltet.

## Verbindliche Architekturgrenzen

- `betriebsmodell` ist `unternehmensintegriert`.
- `externe-inferenz` ist standardmäßig `false`.
- `modelltraining` und `feinabstimmung` müssen `false` bleiben.
- Vortraining, Fine-Tuning, LoRA, PEFT, RLHF, kontinuierliches Lernen und Änderungen produktiver Modellgewichte sind ausgeschlossen.
- Fachwissen bleibt außerhalb der Modellgewichte; freigegebene Wissenssuche, persönliche Arbeitsunterlagen und geregelte freiwillige Beiträge sind möglich.
- Vortrainierte Basismodelle sind austauschbare, versionierte Artefakte; Fachwissen verbleibt außerhalb des Modells.

Die Erzeugung von Suchvektoren, die RAG-Indexierung, Systemanweisungen und vorübergehender Gesprächskontext sind kein Modelltraining, benötigen jedoch eigene Schutzmaßnahmen.

## Bedingte externe Inferenz

Externe Inferenz ist technisch möglich, aber nicht Teil der Standardarchitektur. Bei ihrer Aktivierung werden Eingaben, Systemanweisungen, Gesprächskontexte, RAG-Ausschnitte, übertragene Dateien, Metadaten und angeforderte Ausgaben außerhalb der lokalen Infrastruktur verarbeitet. Transportverschlüsselung verhindert diese Verarbeitung durch den externen Betreiber nicht.

Eine Aktivierung verändert Systemgrenze, Verantwortlichkeiten, Datenflüsse, Rechtslage, Bedrohungsmodell und Nachweispflichten. Zuvor müssen mindestens Datenschutz, Datenklassifikation, Verträge und Auftragsverarbeitung, Drittlandbezug, Anbieter- und Lieferkettenprüfung, Protokollierung, Löschung, Aufbewahrung, Verschlüsselung, Schlüsselverwaltung, Verfügbarkeit, Vorfallprozesse und Ausstiegsszenario neu bewertet und freigegeben werden. Die ausdrückliche KI-Freigabe kann gleichartige Anfragen im genehmigten Nutzungsprofil abdecken. Automatische Wechsel sind nur innerhalb bereits freigegebener Ausweichprofile erlaubt; eine allgemeine Internetfreigabe genügt nicht.

`KI-EXT-001` ist nur bei externer Inferenz anwendbar; `KI-EXT-002` schützt in jeder Betriebsform vor nicht freigegebenen Zielwechseln. Das Setzen von `externe-inferenz` auf `true` ohne eine organisationsspezifische, getrennte Fassung und ohne aktivierte Zusatzkontrollen schlägt in der Validierung fehl.

## Statusmechanismus

`projektstatus.json` ist die maschinenlesbare Prüfschranke. Im öffentlichen Referenzrepository ist ausschließlich folgende Kombination zulässig:

```json
{
  "dokumentstatus": "ÖFFENTLICH",
  "organisationsspezifisch": false,
  "betriebsmodell": "unternehmensintegriert",
  "externe-inferenz": false,
  "modelltraining": false,
  "feinabstimmung": false
}
```

Eine automatische Erkennung beliebiger Organisationsdaten ist technisch nicht vollständig möglich. Die Validierung sucht ergänzend heuristisch nach IP-Adressen, Host- und Domänennamen, Organisationskennzeichen, Geheimhaltungsvermerken und typischen Zugangsdaten. Verantwortlich bleibt der kontrollierte Anpassungsprozess.

## Quellenprinzip

Jede normative Kontrolle besitzt mindestens eine öffentliche, nachvollziehbare Fundstelle oder ist ausdrücklich als organisationsneutrale Projektfestlegung gekennzeichnet. Lokale Dateien allein gelten nicht als Beleg. Das Quellenregister dokumentiert Herausgeber, Titel, Fassung, Datum, URL, Abruf- und Prüfdatum, Seitenzahl, Prüfsumme, Autoritätsstufe, Nachnutzungsstatus, konkrete Fundstellen, Wiedervorlage und abgeleitete Kontrollen.

Die lokal vorhandenen Ausgangs- und Referenzdokumente liegen ausschließlich unter `quellen/lokale-eingaben/`; dieses Verzeichnis wird von Git ausgeschlossen. Ihre offiziellen Fundstellen sind im Quellenregister verzeichnet. Die abweichende Binärfassung des BMVg-PDF wurde nicht ersetzt: Die lokal vorliegende und die am 02.09.2026 erneut geladene offizielle Fassung besitzen unterschiedliche PDF-Prüfsummen, aber dieselbe Seitenzahl und nach normalisierter Extraktion denselben Textinhalt. Beide Prüfergebnisse sind transparent registriert.

Die Zitierform lautet:

> Herausgeber: Titel, Fassung/Stand, Veröffentlichungsdatum, konkrete Seite oder Abschnitt, öffentliche URL, abgerufen am TT.MM.JJJJ.

Im Fließtext werden Quellenkennungen wie `[Q-BSI-001]` verwendet. Rechtsquellen enthalten zusätzlich Artikel beziehungsweise Paragraf und den geprüften konsolidierten Stand. GitHub-Quellen werden auf einen Commit oder Release fixiert.

## Nutzung und Validierung

Voraussetzungen sind Python 3.11 oder neuer, die in [`validierung/anforderungen.txt`](validierung/anforderungen.txt) fixierten Pakete, Java 17 oder neuer für PlantUML, Microsoft Word für die Aktualisierung des Inhaltsverzeichnisses und die PDF-Ausgabe sowie Poppler für die visuelle PDF-Prüfung.

```powershell
python -m pip install -r validierung/anforderungen.txt
python validierung/erzeuge_diagramme.py --werkzeug-herunterladen
python validierung/erzeuge_dokumente.py
powershell -NoProfile -ExecutionPolicy Bypass -File validierung/aktualisiere_word_felder.ps1
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
```

Die sechs Diagramme werden als leicht bearbeitbare PlantUML-Quellen unter [`diagramme/`](diagramme/) gepflegt und lokal in SVG und PNG umgewandelt. Das PNG wird anschließend als feste Inline-Abbildung in das DOCX übernommen. Die Dokumenterzeugung liest den OSCAL-Katalog und das Quellenregister. Änderungen an normativen Anforderungen werden zuerst im Katalog vorgenommen. Das PowerShell-Skript aktualisiert danach das echte Word-Inhaltsverzeichnis, speichert das DOCX und erzeugt unmittelbar daraus das PDF. Die verbindlichen Typografie-, Tabellen-, Diagramm-, Risikodarstellungs-, Silbentrennungs-, Inhaltsverzeichnis- und Seitenführungswerte stehen in [`dokumentation/LAYOUTREGELN.md`](dokumentation/LAYOUTREGELN.md). Nach jeder Erzeugung sind DOCX und PDF vollständig zu rendern und auf jeder Seite redaktionell sowie visuell zu prüfen.

## Projektstruktur

```text
katalog/                         Normativer OSCAL-JSON-Katalog
konzept/                         DOCX-Master und daraus erzeugtes PDF
diagramme/                       Bearbeitbare PlantUML-Quellen und Prüfsummenmanifest
quellen/                         Quellenregister
quellen/lokale-eingaben/         Ignorierte lokale Ausgangsdokumente
schemata/                        Offizielle und projektspezifische JSON-Schemata
validierung/                     Erzeugungs- und Prüfwerkzeuge sowie Negativtests
dokumentation/                   Architektur, Verfahren und Wartungshinweise
.github/                         Deutsche Kollaborations- und Actions-Konfiguration
```

## Qualität, Mitwirkung und Sicherheit

- Fachliche Änderungen müssen die Nachweiskette Kontrolle → Fundstelle → Quelle erhalten.
- Verschärfungen von Empfehlungen zu projektinternen Muss-Anforderungen benötigen eine dokumentierte Risikobegründung.
- Änderungen an Kontroll-IDs sind inkompatibel und bedürfen einer dokumentierten Migration.
- Sensible Schwachstellen werden nicht als gewöhnliches Issue veröffentlicht; siehe [`SECURITY.md`](SECURITY.md).
- Beiträge folgen [`CONTRIBUTING.md`](CONTRIBUTING.md).

Das Projekt behauptet weder die automatische Konformität eines konkreten Systems mit BSI-Vorgaben, ISO-Normen oder dem EU AI Act noch eine VS-Freigabe. ISO-Normentexte werden nicht kopiert. Eine vollständige Konformitätsbewertung setzt lizenzierte Normfassungen, organisationsspezifische Nachweise und unabhängige Prüfung voraus. Eine Akkreditierung betrifft die prüfende Konformitätsbewertungsstelle; dieses Projekt stellt kein Zertifikat aus.

## Lizenz- und Veröffentlichungsgrenze

Für das Gesamtwerk ist noch keine Lizenzentscheidung getroffen. Bis dahin besteht keine allgemeine Nutzungserlaubnis über gesetzliche Schranken hinaus. Quellenangaben und abgeleitete Aussagen ersetzen keine Lizenz der jeweiligen Herausgeber. Die notwendige Entscheidung ist in der Wartungscheckliste festgehalten.
