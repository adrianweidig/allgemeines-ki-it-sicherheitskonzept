# Allgemeines KI-IT-Sicherheitskonzept

> [!CAUTION]
> **ÖFFENTLICH – organisationsneutrale Referenzvorlage.** Jede Anreicherung mit organisationsspezifischen Informationen beendet diesen Status. Anpassungen dürfen ausschließlich in einer getrennten, angemessen geschützten Offline-Fassung begonnen werden. Dort ist `organisationsspezifisch` in `projektstatus.json` vor der ersten Anpassung auf `true` zu setzen; die Dokumentkennzeichnung wechselt dadurch auf **NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH**. Eine formale Einstufung darf nur die zuständige Organisation durch befugte Stellen vornehmen.

![Abstrakte lokale KI-Referenzarchitektur](dokumentation/medien/architektur.svg)

Dieses Repository entwickelt eine audit- und zertifizierungsvorbereitende Referenz für den sicheren Betrieb vollständig lokaler KI-Infrastrukturen in einer klassischen Domäne. Es enthält keine Anwendung, Workbench, Plattform oder produktive KI-Komponente. Es setzt ein wirksames allgemeines IT-Sicherheitskonzept voraus und ergänzt dieses ausschließlich um KI-spezifische Risiken, Verschärfungen, Prüfziele und Nachweise.

## Kernergebnisse

- [`katalog/ki-it-sicherheitskatalog.oscal.json`](katalog/ki-it-sicherheitskatalog.oscal.json): normativer OSCAL-Katalog nach OSCAL 1.1.3.
- `konzept/ki-it-sicherheitskonzept.docx`: redaktionelles Masterdokument.
- `konzept/ki-it-sicherheitskonzept.pdf`: ausschließlich aus derselben DOCX-Fassung erzeugte Lesefassung.
- [`quellen/quellenregister.json`](quellen/quellenregister.json): nachvollziehbare öffentliche Fundstellen, Prüfsummen und konkrete Belegstellen.

Die erste gemeinsame fachliche Fassung trägt die Version `0.1.0`. Der OSCAL-Katalog ist für normative Anforderungen maßgeblich. Das Konzept erläutert Architektur, Anwendung und Zusammenwirken; es führt keine zusätzlichen, nur dort vorhandenen Muss-Anforderungen ein.

## Geltungsbereich

Die organisationsneutrale Standardumgebung umfasst verwaltete Clients, eine sichere Domäne mit lokalem Identitätsprovider, einen internen KI-Zugang über HTTPS und eine getrennte KI-Serverzone. Dort laufen Container auf Kubernetes, Docker oder Podman mit lokaler Chat-Oberfläche, lokalem Inferenzserver, lokaler RAG-Verarbeitung, Embedding- und Reranking-Diensten, Vektor- beziehungsweise Datenbank sowie lokaler Überwachung.

Vorausgesetzt werden bereits umgesetzte Basismaßnahmen wie MFA, rollenbasierte Rechte, interne PKI, Segmentierung, Patch- und Schwachstellenmanagement, Protokollierung, Backup und Notfallmanagement. Ein internes Container- oder Pod-Netz ist allein keine hinreichende Sicherheitsgrenze. Nur der kontrollierte KI-Zugang darf aus dem Clientnetz erreichbar sein; interne Verwaltungs-, Metrik-, Debug-, Cluster-, Inferenz- und Cache-Schnittstellen bleiben abgeschottet.

Fernzugriff erfolgt ausschließlich über ein organisationskontrolliertes VPN mit MFA. Git, Datenablagen, Verzeichnisse, Registrierungen, Modelle, RAG-Daten, Telemetrie und Sicherungen bleiben lokal.

## Verbindliche Architekturgrenzen

- `betriebsmodell` ist `vollständig-lokal`.
- `externe-inferenz` ist standardmäßig `false`.
- `modelltraining` und `feinabstimmung` müssen `false` bleiben.
- Vortraining, Fine-Tuning, LoRA, PEFT, RLHF, kontinuierliches Lernen und Änderungen produktiver Modellgewichte sind ausgeschlossen.
- Domänenwissen wird ausschließlich über lokales RAG oder kontrollierte, lokale On-Demand-Uploads bereitgestellt.
- Vortrainierte Basismodelle sind austauschbare, versionierte Artefakte; Fachwissen verbleibt außerhalb des Modells.

Embedding-Erzeugung, RAG-Indexierung, Systemanweisungen und temporärer Gesprächskontext sind kein Modelltraining, benötigen jedoch eigene Schutzmaßnahmen.

## Bedingte externe Inferenz

Externe Inferenz ist technisch möglich, aber nicht Teil der Standardarchitektur. Bei ihrer Aktivierung werden Prompts, Systemanweisungen, Gesprächskontexte, RAG-Ausschnitte, Uploadinhalte, Metadaten und angeforderte Ausgaben außerhalb der lokalen Infrastruktur verarbeitet. Transportverschlüsselung verhindert diese Verarbeitung durch den externen Betreiber nicht.

Eine Aktivierung verändert Systemgrenze, Verantwortlichkeiten, Datenflüsse, Rechtslage, Bedrohungsmodell und Nachweispflichten. Zuvor müssen mindestens Datenschutz, Datenklassifikation, Verträge und Auftragsverarbeitung, Drittlandbezug, Anbieter- und Lieferkettenprüfung, Protokollierung, Löschung, Aufbewahrung, Verschlüsselung, Schlüsselverwaltung, Verfügbarkeit, Vorfallprozesse und Ausstiegsszenario neu bewertet und freigegeben werden. Fallbacks, automatische Provider-Erkennung und Cloud-Modelle dürfen externe Inferenz nicht unbeabsichtigt einschalten.

Die Kontrollgruppe `Bedingte externe Inferenz` bleibt deshalb sichtbar, ist im Standardstatus jedoch nicht anwendbar. Das Setzen von `externe-inferenz` auf `true` ohne eine organisationsspezifische, getrennte Fassung und ohne aktivierte Zusatzkontrollen schlägt in der Validierung fehl.

## Statusmechanismus

`projektstatus.json` ist das maschinenlesbare Gate. Im öffentlichen Referenzrepository ist ausschließlich folgende Kombination zulässig:

```json
{
  "dokumentstatus": "ÖFFENTLICH",
  "organisationsspezifisch": false,
  "betriebsmodell": "vollständig-lokal",
  "externe-inferenz": false,
  "modelltraining": false,
  "feinabstimmung": false
}
```

Eine automatische Erkennung beliebiger Organisationsdaten ist technisch nicht vollständig möglich. Die Validierung sucht ergänzend heuristisch nach IP-Adressen, Host- und Domänennamen, Organisationskennzeichen, Geheimhaltungsvermerken und typischen Zugangsdaten. Verantwortlich bleibt der kontrollierte Anpassungsprozess.

## Quellenprinzip

Jede normative Kontrolle besitzt mindestens eine öffentliche, nachvollziehbare Fundstelle oder ist ausdrücklich als organisationsneutrale Projektfestlegung gekennzeichnet. Lokale Dateien allein gelten nicht als Beleg. Das Quellenregister dokumentiert Herausgeber, Titel, Fassung, Datum, URL, Abruf- und Prüfdatum, Seitenzahl, Prüfsumme, Autoritätsstufe, Nachnutzungsstatus, konkrete Fundstellen, Wiedervorlage und abgeleitete Kontrollen.

Die drei lokal vorhandenen Ausgangsdokumente liegen ausschließlich unter `quellen/lokale-eingaben/`; dieses Verzeichnis wird von Git ausgeschlossen. Ihre offiziellen Fundstellen sind im Quellenregister verzeichnet. Die abweichende Binärfassung des BMVg-PDF wurde nicht ersetzt: Die lokal vorliegende und die am 02.09.2026 erneut geladene offizielle Fassung besitzen unterschiedliche PDF-Prüfsummen, aber dieselbe Seitenzahl und nach normalisierter Extraktion denselben Textinhalt. Beide Prüfergebnisse sind transparent registriert.

Die Zitierform lautet:

> Herausgeber: Titel, Fassung/Stand, Veröffentlichungsdatum, konkrete Seite oder Abschnitt, öffentliche URL, abgerufen am TT.MM.JJJJ.

Im Fließtext werden Quellenkennungen wie `[Q-BSI-001]` verwendet. Rechtsquellen enthalten zusätzlich Artikel beziehungsweise Paragraf und den geprüften konsolidierten Stand. GitHub-Quellen werden auf einen Commit oder Release fixiert.

## Nutzung und Validierung

Voraussetzungen sind Python 3.11 oder neuer, die in [`validierung/anforderungen.txt`](validierung/anforderungen.txt) fixierten Pakete, LibreOffice für die reproduzierbare PDF-Erzeugung sowie Poppler für die visuelle PDF-Prüfung.

```powershell
python -m pip install -r validierung/anforderungen.txt
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
python validierung/erzeuge_dokumente.py
```

Die Dokumenterzeugung liest den OSCAL-Katalog und das Quellenregister. Änderungen an normativen Anforderungen werden zuerst im Katalog vorgenommen. Die verbindlichen Typografie-, Tabellen-, Silbentrennungs- und Seitenführungswerte stehen in [`dokumentation/LAYOUTREGELN.md`](dokumentation/LAYOUTREGELN.md). Nach jeder Erzeugung sind DOCX und PDF zu öffnen, vollständig zu rendern und auf jeder Seite redaktionell sowie visuell zu prüfen.

## Projektstruktur

```text
katalog/                         Normativer OSCAL-JSON-Katalog
konzept/                         DOCX-Master und daraus erzeugtes PDF
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
