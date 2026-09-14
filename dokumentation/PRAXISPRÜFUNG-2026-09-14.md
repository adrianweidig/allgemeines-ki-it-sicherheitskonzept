# Kritische Praxisprüfung des KI-IT-Sicherheitskonzepts

Stand: 14.09.2026. Geprüft wurden die kommentierte PDF, das vorhandene DOCX/PDF-Paar, alle 38 OSCAL-Kontrollen und die zugehörigen Generatorpassagen. Die Seitenangaben beziehen sich auf die 64-seitige PDF der Version 0.1.0 mit fachlichem Stichtag 03.09.2026.

**Die folgenden Formulierungen sind Empfehlungen zur Entscheidung. Sie wurden nicht in das Konzept oder die Anforderungen des Katalogs übernommen.** Die Prüfung bewertet die praktische Erfüllbarkeit und Nachweisbarkeit der Festlegungen. Eine tatsächliche Unternehmensumgebung wurde noch nicht bewertet.

## PDF-Kommentar

Die eingereichte PDF enthält genau eine inhaltliche Annotation und deren leeres Anzeigefenster. Auf Seite 1 ist „Sicherheitskonzept für vollständig lokale KI-Infrastrukturen“ markiert. Der Kommentar lautet „Hier ist etwas kommentiert“.

Der Kommentar wurde durch den Auftraggeber als Testkommentar bestätigt; eine Änderung ist nicht gewünscht. Deshalb wurde daraus keine inhaltliche Änderung abgeleitet. Der gesamte extrahierte Seitentext ist auf allen 64 Seiten mit der Repository-PDF identisch. Weitere Änderungsanweisungen wurden nicht gefunden. Die Kommentarbearbeitung ist damit abgeschlossen.

## Gesamtbewertung

Das Konzept beschreibt einen anspruchsvollen, grundsätzlich umsetzbaren lokalen KI-Betrieb. Rechteprüfung außerhalb des Sprachmodells, getrennte Vertrauenszonen, kontrollierte Modellimporte, Datenminimierung und verantwortete Freigaben sind tragfähige Anforderungen.

Die größten Probleme liegen in vorweggenommenen Wirksamkeitsaussagen, nicht begrenzten Vollständigkeitsnachweisen und Freigabeprozessen, deren Wortlaut auch kleine Routinevorgänge erfassen kann. Die folgenden zwölf Punkte sollten vor einer verbindlichen Unternehmensfassung entschieden werden.

| Priorität | Empfehlung | Wichtigste Fundstelle |
|---|---|---|
| Hoch | P01 Restrisiken erst nach Wirksamkeitsprüfung einstufen | S. 13–14, Kapitel 8.2–8.3 |
| Hoch | P02 Betriebsunterbrechung und Risikoakzeptanz differenzieren | S. 13 und 19, KI-GOV-003 |
| Hoch | P03 Vollständigkeitsnachweis auf überprüfbare Abdeckung begrenzen | S. 42, KI-THR-001 |
| Hoch | P04 Änderungen nach Wirkung prüfen und freigeben | S. 12 und 45, KI-VAL-002 |
| Hoch | P05 Sitzungssperre und physische Löschung auseinanderhalten | S. 33–34, KI-RAG-003/004 |
| Hoch | P06 Menschliche Bestätigung konsistent nach Wirkung verlangen | S. 40 und 54, KI-TOL-001, Kapitel 11 |
| Mittel | P07 Trainingsverbot über Ausführbarkeit und Rechte durchsetzen | S. 30, KI-TRN-001 |
| Mittel | P08 Wiederholbarkeit von identischen Modellantworten abgrenzen | S. 44, KI-VAL-001 |
| Entscheidung über Architektur | P09 Umfang der lokalen Betriebsgrenze festlegen | S. 7–9 und 23, KI-ARC-002 |
| Mittel | P10 Fristen für Berechtigungswiderrufe bestimmen | S. 32, KI-RAG-002 |
| Mittel, nur externe Variante | P11 Variantenfreigabe von der Prüfung jeder Anfrage trennen | S. 50, KI-EXT-001 |
| Hoch | P12 Anwendbarkeit und MUSS-Verschärfungen einzeln begründen | Gesamtkatalog, 38 Kontrollen |

<a id="p01"></a>

## P01 Restrisiken sind keine zugesicherte Maßnahmenwirkung

**Fundstelle:** S. 13, Beschriftung der Abbildung 4: „Die KI-spezifischen Maßnahmen senken alle hohen und sehr hohen Ausgangsrisiken auf höchstens mittel.“ S. 14, Risikoregister, besonders R-08.

**Kritik:** Die Formulierung behauptet eine bereits feststehende Wirkung, obwohl weder konkrete Unternehmensdaten noch Wirksamkeitsmessungen vorliegen. Bei R-08 sinkt sogar die Schadenshöhe eines Datenabflusses von „existenzbedrohend“ auf „begrenzt“. Eine blockierte Verbindung kann die Eintrittshäufigkeit senken; weshalb ein dennoch eintretender Abfluss weniger schädlich wäre, begründen die genannten Maßnahmen nicht. Das NIST-Profil betont die Abhängigkeit von Nutzungskontext und empirischer Grundlage sowie Grenzen der Risikoschätzung. Die Folgerung für dieses Konzept ist eine eigene fachliche Bewertung. [NIST AI 600-1, Abschnitt 2, S. 2–3](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

**Empfohlene Ersatzformulierung:**

> Nach Umsetzung und Prüfung der Maßnahmen werden Eintrittshäufigkeit und Schadenshöhe für jedes Szenario erneut bewertet. Eine Freigabe setzt ein nach den festgelegten Kriterien akzeptables und nachvollziehbar begründetes Restrisiko voraus. Eine niedrigere Schadenshöhe wird nur angesetzt, wenn konkrete Maßnahmen die mögliche Schadenswirkung nachweisbar begrenzen.

**Erforderlicher Nachweis:** Annahmen, Messungen oder geeignete Erfahrungswerte je Szenario; gesonderte Begründung jeder geänderten Schadenshöhe. Die Zielwerte dürfen bis dahin nur als Planungsannahmen gelten. Bei Annahme der Empfehlung müssen Register, Matrix und Beschriftung gemeinsam angepasst werden.

<a id="p02"></a>

## P02 Eine hohe Risikoeinstufung benötigt eine differenzierte Betriebsentscheidung

**Fundstelle:** S. 13 und 19, KI-GOV-003: „Hohe und sehr hohe Risiken MÜSSEN eine Erstfreigabe oder den Weiterbetrieb bis zur wirksamen Behandlung sperren.“

**Kritik:** Die Regel ist als bewusst gewählte Risikotoleranz zulässig und erfüllbar, kann im laufenden Betrieb aber ohne weitere Eingrenzung unverhältnismäßige Abschaltungen auslösen. Sie unterscheidet weder betroffene Funktionen noch akute Gefahren von längerfristigem Handlungsbedarf. Die zugrunde liegende BSI-Methodik kennt mehrere Behandlungsoptionen einschließlich verantworteter Risikoakzeptanz; daraus folgt keine pauschale Erlaubnis, verbindliche Anforderungen außer Kraft zu setzen. [BSI-Standard 200-3, Kapitel 6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/BSI_Standards/standard_200_3.pdf?__blob=publicationFile&v=2)

**Empfohlene Ersatzformulierung:**

> Hohe und sehr hohe Risiken werden unverzüglich an die zuständige Entscheidungsstelle eskaliert. Nicht akzeptable Risiken sperren die betroffenen Funktionen. Ein befristeter eingeschränkter Weiterbetrieb darf nur innerhalb der festgelegten Risikotoleranz, mit dokumentierter Entscheidung, wirksamen kompensierenden Maßnahmen, Überwachung und verbindlichem Endtermin zugelassen werden. Zwingende Freigabevoraussetzungen und akute Gefahren dürfen dadurch nicht umgangen werden.

**Erforderlicher Nachweis:** Entscheidungsbefugnisse, nicht ausnahmefähige Grenzen, betroffene Funktionen, Fristen und Abschaltkriterien. Die Organisation kann die bisherige strengere Grenze ausdrücklich beibehalten.

<a id="p03"></a>

## P03 Alle real möglichen Angriffswege lassen sich nicht vollständig testen

**Fundstelle:** S. 42, KI-THR-001, Prüfziel: „jeder real mögliche Daten- und Aktionspfad modelliert, mit Szenarien getestet“. Verwandte sehr absolute Prüfziele stehen in KI-API-002 und KI-PMT-001.

**Kritik:** Schnittstellen, Datenklassen und Berechtigungsgrenzen lassen sich inventarisieren. Alle möglichen Inhalte, Modellreaktionen und mehrstufigen Werkzeugkombinationen lassen sich bei einem offenen generativen System dagegen nicht erschöpfend prüfen. Ein erfolgreicher Testsatz belegt seine geprüften Fälle. Er ist kein Beweis, dass kein weiterer Angriff existiert. NIST beschreibt ausdrücklich Grenzen bei Umfang und Bewertung teilweise unbekannter KI-Risiken. [NIST AI 600-1, Abschnitt 2, S. 3](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

**Empfohlene Ersatzformulierung:**

> Das Bedrohungsmodell erfasst alle inventarisierten Schnittstellen, Vertrauensgrenzen und freigegebenen Aktionsklassen. Sicherheitskritische Grenzen werden mit risikobasierten positiven und negativen Tests geprüft. Testabdeckung, nicht geprüfte Kombinationen und verbleibende Unsicherheiten werden dokumentiert. Berechtigungen und Werkzeuggrenzen werden unabhängig vom Modell technisch durchgesetzt.

**Erforderlicher Nachweis:** Abdeckungsmatrix mit Daten- und Aktionsklassen, Testsatz, Ergebnissen und benannten Grenzen. Die eigentliche Anforderung, unberechtigte Zugriffe technisch zu verhindern, bleibt bestehen.

<a id="p04"></a>

## P04 Nicht jede RAG-Aktualisierung benötigt eine vollständige Wiederfreigabe

**Fundstelle:** S. 12: „Änderungen oder abgelaufene Prüffristen führen zurück in die vollständige Bewertung.“ S. 45, KI-VAL-002: Änderungen unter anderem an RAG-Daten müssen Wiederholungsprüfung und Wiederfreigabe auslösen; für jede Änderung wird eine erfolgreiche Rückkehr zur vorherigen Kombination verlangt.

**Kritik:** Der Katalog nennt zwar bereits risikobasierte Tests, unterscheidet aber nicht zwischen Modellwechsel, Rechteänderung, Korrektur eines Dokuments und täglichem Wissensimport. Eine formale Gesamtfreigabe und praktisch ausgeführte Rückkehr für jede Datenaktualisierung würden den regulären Betrieb erheblich belasten. Eine Rückkehr darf außerdem keine gelöschten Inhalte oder entzogenen Rechte erneut aktivieren.

**Empfohlene Ersatzformulierung:**

> Änderungen werden vor ihrer Umsetzung nach Auswirkung auf Sicherheit, Berechtigungen und Ergebnisqualität eingestuft. Standardänderungen innerhalb eines genehmigten Änderungsprofils dürfen nach festgelegten automatisierten Prüfungen übernommen werden. Wesentliche Änderungen erfordern gezielte Wiederholungsprüfungen und eine ausdrückliche Wiederfreigabe. Die Wiederherstellbarkeit wird regelmäßig und nach relevanten Änderungen erprobt; Löschungen und Berechtigungswiderrufe bleiben dabei wirksam.

**Erforderlicher Nachweis:** Änderungsmatrix, Kriterien für Standardänderungen, betroffene Tests, Entscheidung und regelmäßig erprobtes Wiederherstellungsverfahren. Keine Ausnahme für Änderungen der System- oder Berechtigungsgrenze allein wegen ihres geringen Umfangs.

<a id="p05"></a>

## P05 Sofortige Nichtzugreifbarkeit und abgeschlossene Löschung sind verschiedene Ziele

**Fundstelle:** S. 34, KI-RAG-004: „nachweislich vollständigen Löschlauf“ und Nichtzugreifbarkeit von Datei, Auszügen, Suchvektoren und Zwischenspeichern nach Sitzungsende. Ergänzend S. 33, KI-RAG-003.

**Kritik:** Sitzungsende ist bei Verbindungsabbruch, abgestürzten Diensten und asynchroner Verarbeitung ohne Definition unklar. Die sofortige Sperre einer Sitzung ist technisch anders nachzuweisen als das Entfernen aller gespeicherten Ableitungen. Die vorhandene Sicherungsregel ist bereits realistisch: KI-RAG-003 sieht Löschmarkierungen und geregeltes Auslaufen aus Sicherungen vor. Sie verlangt keine sofortige Veränderung jeder Sicherungskopie.

**Empfohlene Ersatzformulierung:**

> Sitzungsbezogene Inhalte werden bei Beendigung oder Ablauf der Sitzung für weitere Anfragen gesperrt. Quelldateien und Ableitungen werden innerhalb der im Löschkonzept festgelegten Fristen gelöscht; fehlgeschlagene Löschaufträge werden erkannt und nachbearbeitet. Temporäre Inhalte werden grundsätzlich nicht in dauerhafte Wissensbestände oder reguläre Sicherungen übernommen. Erforderliche Ausnahmen werden ausdrücklich geregelt. Bei Wiederherstellungen werden gültige Löschmarkierungen vor Freigabe der Daten erneut angewandt.

**Erforderlicher Nachweis:** Eindeutiger Sitzungsablauf, getrennte Sperr- und Löschfristen, Tests bei Absturz und Wiederherstellung, Umgang mit Sicherungen und minimalen Prüfprotokollen. Die Fristen werden anhand des tatsächlichen Schutzbedarfs festgelegt.

<a id="p06"></a>

## P06 Der Fließtext verlangt mehr Bestätigungen als die normative Kontrolle

**Fundstelle:** S. 40, KI-TOL-001, fordert konkrete Bestätigung für kritische, destruktive, privilegierte oder externe Aktionen; die Umsetzung verbietet Sammelfreigaben. S. 54, Kapitel 11, nennt eine konkrete menschliche Bestätigung allgemein als Schranke jeder Werkzeugaktion. Der Alternativtext erfasst zudem alle Schreib-, Befehls- und Netzwerkaktionen.

**Kritik:** Diese unterschiedlichen Grenzen führen zu verschiedenen Implementierungen. Eine Bestätigung jedes unkritischen Dateilesens, Tests oder reversiblen Bearbeitungsschritts erschwert den Nutzen von Agenten und fördert routinemäßiges Bestätigen ohne Prüfung. Die normative Kontrolle enthält bereits eine sinnvolle Differenzierung nach Wirkung; Fließtext und Diagramm sollten ihr entsprechen.

**Empfohlene Ersatzformulierung:**

> Jede Werkzeugaktion unterliegt einer technisch erzwungenen Richtlinie und minimalen Rechten. Für risikoarme Aktionen können vorab genehmigte Aktionsprofile innerhalb eines benannten Arbeitsbereichs gelten. Kritische, destruktive, privilegierte oder externe Aktionen erfordern eine konkrete Bestätigung mit Ziel und Wirkung. Eine Profilfreigabe darf diese Bestätigung nicht ersetzen oder Rechte erweitern.

**Erforderlicher Nachweis:** Aktionsklassen, wirksame Profile, konkrete Bestätigungsgrenzen und Negativtests. Bei Annahme müssen Katalog, Kapitel 11, PlantUML-Quelle und Alternativtext zusammengeführt werden.

<a id="p07"></a>

## P07 Trainingsfähige Bibliotheken sind nicht mit freigegebenem Training gleichzusetzen

**Fundstelle:** S. 30, KI-TRN-001, Umsetzung: „Trainingssoftware, Schreibpfade auf Modellgewichte und lernende Rückkopplungen werden nicht bereitgestellt.“ Das Prüfziel erfasst auch Pakete, die keine Gewichtsänderung erlauben sollen.

**Kritik:** Das Verbot tatsächlichen Trainings ist umsetzbar. Ein pauschales Verbot jeder Bibliothek mit Trainingsfunktionen kann dagegen gängige Inferenzumgebungen ausschließen. Entscheidend sind erreichbare Funktionen, Aufträge, Datenflüsse und effektive Schreibrechte. Aus dem Vorhandensein einer Funktion allein folgt noch keine erlaubte Ausführung.

**Empfohlene Ersatzformulierung:**

> Training, Feinabstimmung und lernende Rückkopplungen sind im Geltungsbereich untersagt. Produktive Modellartefakte werden im Inferenzbetrieb schreibgeschützt bereitgestellt. Trainingsaufträge und Schnittstellen zur Gewichtsänderung werden weder freigegeben noch durch Dienstrechte ermöglicht. Unvermeidbare Bibliotheksfunktionen werden in der Komponentenprüfung erfasst und dürfen keinen freigegebenen Ausführungspfad erhalten.

**Erforderlicher Nachweis:** Effektive Dateirechte, erreichbare Schnittstellen, Auftragsinventar, Integritätskontrolle und negative Ausführungstests. Das Trainingsverbot selbst wird nicht gelockert.

<a id="p08"></a>

## P08 Wiederholbare Bewertung bedeutet nicht stets wortgleiche Antworten

**Fundstelle:** S. 44, KI-VAL-001: dokumentierte und wiederholbare Ergebnisse; eine Stichprobe muss mit derselben Konfiguration reproduzierbar sein.

**Kritik:** Ohne Abnahmedefinition kann dies als Zusage identischer Modellantworten verstanden werden. Zufallsparameter, Parallelisierung und numerische Ausführung beeinflussen Ergebnisse. Die PyTorch-Dokumentation beschreibt Grenzen vollständiger Reproduzierbarkeit und die zusätzlichen Voraussetzungen deterministischer Ausführung. [PyTorch, Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)

**Empfohlene Ersatzformulierung:**

> Testverfahren, Modellstand, Laufzeit, Hardware, Parameter und Testdaten werden versioniert. Sicherheitsentscheidungen werden deterministisch geprüft, soweit sie durch klassische Zugriffskontrollen getroffen werden. Für variable Modellantworten werden Wiederholungszahl, Messgrößen und zulässige Schwankungsbereiche vorab festgelegt. Die Freigabe setzt die Einhaltung der definierten Abnahmekriterien voraus.

**Erforderlicher Nachweis:** Wiederholte Messungen mit vorab festgelegten Schwellen. Ein gesetzter Zufallsstartwert allein genügt nicht als Nachweis identischer Ausführung.

<a id="p09"></a>

## P09 Vollständig lokaler Betrieb ist eine Architekturentscheidung

**Fundstelle:** S. 7–9 und 23, KI-ARC-002: unter anderem lokale Identitäten, Git, Registrierungen, Protokolle, Telemetrie und Sicherungen; keine ausgehende Internetverbindung der KI-Komponenten im Standardbetrieb.

**Kritik:** Das ist technisch erreichbar. Es kann jedoch für ein Unternehmen mit zentralen Cloud-Identitäten, externer Codeverwaltung oder ausgelagerter Sicherheitsüberwachung erhebliche zusätzliche Infrastruktur verlangen. Die Anforderung ist kein allgemeiner Beweis, dass nur vollständig lokale Architekturen sicher betrieben werden können. Sie ist die bewusst gewählte Grenze dieser Referenz und sollte nicht stillschweigend aufgeweicht werden.

**Empfohlene Ersatzformulierung zur Präzisierung der lokalen Variante:**

> Die festgelegte Systemgrenze umfasst die KI-Dienste und ihre im Datenflussmodell bezeichneten Abhängigkeiten. Inferenz und KI-Inhaltsdaten werden ausschließlich innerhalb dieser lokalen Grenze verarbeitet. Abhängigkeiten zu Identität, Codeverwaltung, Überwachung und Sicherung werden je Dienst benannt und auf die freigegebenen Datenflüsse begrenzt. Direkte Internetverbindungen der KI-Komponenten bleiben gesperrt; Aktualisierungen erfolgen über den kontrollierten Importweg.

**Erforderliche Entscheidung:** Welche bestehenden Unternehmensdienste liegen innerhalb der lokalen Grenze? Falls externe Dienste erforderlich sind, muss die Unternehmensfassung als gesonderte Architekturvariante bewertet werden. Eine externe Identitäts- oder Protokollierungsabhängigkeit wird nicht allein durch die Kontrollen zur externen Inferenz abgedeckt.

<a id="p10"></a>

## P10 Die aktuelle Berechtigung benötigt eine messbare Widerrufsfrist

**Fundstelle:** S. 32, KI-RAG-002: Prüfung „bei jeder Abfrage“ anhand einer maßgeblichen lokalen Quelle; Änderungen und Widerrufe werden „zeitnah“ übernommen.

**Kritik:** „Zeitnah“ lässt bei Verzeichnisreplikation, Sitzungen und Zwischenspeichern keine eindeutige Abnahme zu. Eine Prüfung je Abfrage kann mit einem lokalen Berechtigungsstand erfolgen; der zulässige Verzug zu dessen maßgeblicher Quelle muss feststehen. Die Zugriffstrennung selbst ist erreichbar und darf nicht durch ein allgemeines Bemühen ersetzt werden.

**Empfohlene Ersatzformulierung:**

> Jede Abfrage wird serverseitig gegen einen gültigen Berechtigungsstand geprüft. Für Berechtigungsänderungen, Sitzungen und Zwischenspeicher werden maximale Gültigkeits- und Übernahmefristen entsprechend dem Schutzbedarf festgelegt und überwacht. Bei überschrittener Gültigkeit wird der betroffene Zugriff verweigert. Für kritische Widerrufe besteht ein unmittelbar wirksamer Sperrweg.

**Erforderlicher Nachweis:** Gemessene Übernahmezeiten einschließlich Verzeichnisstörung, laufender Sitzung, Trefferzwischenspeicher und direktem Objektzugriff. Keine pauschale Frist ohne Bezug zur tatsächlichen Architektur festlegen.

<a id="p11"></a>

## P11 Eine externe Variante wird freigegeben und jede Anfrage dagegen geprüft

**Fundstelle:** S. 50, KI-EXT-001: „vor jeder Datenübertragung eine neue organisationsspezifische Bewertung und Freigabe“.

**Kritik:** Wörtlich gelesen wären Verträge, Anbieterprüfung und Datenschutzbewertung für jede einzelne Anfrage neu durchzuführen. Gemeint sein dürfte eine gültige Variantenfreigabe vor der ersten Übertragung, kombiniert mit technischer Prüfung jeder Anfrage. Im Standardmodell ist diese Kontrolle nicht anwendbar und externe Inferenz bleibt deaktiviert.

**Empfohlene Ersatzformulierung:**

> Vor der ersten Datenübertragung wird die externe Betriebsvariante organisationsspezifisch bewertet und freigegeben. Die Freigabe benennt Anbieter, Endpunkte, Modelle, Datenkategorien, Zwecke und Gültigkeit. Jede Anfrage wird gegen diese Freigabe geprüft. Wesentliche Änderungen oder ihr Ablauf erfordern eine erneute Bewertung; außerhalb einer gültigen Freigabe findet keine Übertragung statt.

**Erforderlicher Nachweis:** Gültige Variantenentscheidung, technische Anfrageprüfung und eindeutig definierte Änderungsanlässe. Rechts- und Vertragsprüfung werden dadurch nicht entbehrlich.

<a id="p12"></a>

## P12 Einzelfallbezogene Anwendbarkeit und konkrete Verschärfungsbegründungen fehlen

**Fundstelle:** Gesamtkatalog: 38 Kontrollen mit Modalität MUSS, davon 36 mit Anwendbarkeit `standard` und zwei mit `bedingt-externe-inferenz`. Bei 33 Kontrollen ist die Verschärfungsbegründung wortgleich.

**Kritik:** Der allgemeine Satz, eine Verschärfung begrenze ein KI-spezifisches Risiko, begründet nicht, weshalb gerade diese Maßnahme in jedem Einsatz zwingend sein soll. RAG- und Agentenkontrollen sind für einen Dienst ohne Wissenssuche beziehungsweise Werkzeuge teilweise nicht anwendbar. Eine dokumentierte Nichtanwendbarkeit ist eine andere Entscheidung als eine Ausnahme von einer erforderlichen Schutzmaßnahme. Auch die unterschiedlichen Quellengeltungsbereiche müssen sichtbar bleiben: Der referenzierte BSI-Kriterienkatalog richtet sich an die Integration generativer Modelle in der Bundesverwaltung. [BSI-Kriterienkatalog, Kapitel 1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Kriterienkatalog_KI-Modelle_Bundesverwaltung.pdf?__blob=publicationFile&v=3)

**Empfohlene Festlegung für die Überarbeitung:**

> Die Anwendbarkeit jeder Kontrolle wird aus dem freigegebenen Anwendungsfall, den vorhandenen Funktionen und dem Schutzbedarf abgeleitet. Zusätzliche projektinterne MUSS-Festlegungen benennen das konkrete Risikoszenario, die unzureichende Wirkung vorhandener Basismaßnahmen und die erforderliche zusätzliche Wirkung. Nichtanwendbarkeit und abweichende Umsetzung werden getrennt begründet und entschieden.

**Erforderlicher Nachweis:** Einzelfallbezogene Begründungen sowie Einsatzprofile für beispielsweise reine Chatnutzung, RAG und Agenten. Bestehende Nachweise aus dem allgemeinen Sicherheitsprozess dürfen referenziert werden. Eine pauschale Herabstufung aller MUSS-Anforderungen zu SOLLTE ist nicht empfohlen.

## Anforderungen, die bereits praktikabel differenziert sind

- KI-CON-002 verlangt einen Betrieb ohne privilegierten Systemnutzer „nach Möglichkeit“ und schreibgeschützte Bereiche, soweit die Funktion dies zulässt. Technisch begründete Ausnahmen sind bereits vorgesehen.
- KI-MOD-001 verlangt die Dokumentation einer **verfügbaren** Signatur. Eine nicht existierende Herstellersignatur muss nicht erfunden oder beschafft werden; Herkunft, Integrität und Importentscheidung bleiben nachzuweisen.
- KI-RAG-003 behandelt das Auslaufen aus Sicherungen bereits ausdrücklich. Eine sofortige physische Löschung aus allen Sicherungsständen steht dort nicht.
- Kapitel 7 erlaubt die Zusammenlegung von Rollen unter Behandlung von Interessenkonflikten. Es verlangt nicht für jede Rolle eine zusätzliche Person.
- Serverseitige Autorisierung, minimale Rechte, kontrollierte Importwege und das Verbot nicht freigegebener externer Übertragung sollten beibehalten werden.

## Nächste Entscheidungen für die Unternehmensfassung

Benötigt werden zunächst der konkrete Einsatzzweck, vorhandene Betriebsdienste, Datenklassen, Nutzergruppen und das zulässige Maß an Agentenwirkung. Daraus folgen Geltungsbereich, Rollen, Wiederherstellungsziele, Widerrufs- und Löschfristen sowie akzeptable Restrisiken. Diese Angaben gehören ausschließlich in die getrennte geschützte Fassung.

Nach Auswahl der Empfehlungen werden normative Änderungen zuerst im OSCAL-Katalog vorgenommen. Betroffene Erläuterungen und Diagramme folgen anschließend. Kontroll-IDs bleiben stabil; Änderungen werden dokumentiert, DOCX und PDF neu erzeugt und erneut geprüft.

## Prüfbasis und Grenzen

Die Zählung der Annotationen, der Seitenvergleich, die Kontrollzahlen und die Gleichheit der 33 Verschärfungsbegründungen wurden maschinell geprüft. Die Bewertung der Formulierungen und die Ersatztexte sind fachliche Empfehlungen aus dieser Prüfung.

NIST und die PyTorch-Dokumentation wurden am 14.09.2026 online eingesehen. Die direkten BSI-PDF-Abrufe im Recherchewerkzeug waren durch HTTP 403 eingeschränkt; einschlägige Abschnitte waren über die Suchindexauszüge der offiziellen BSI-Quellen einsehbar. Daraus wird keine vollständige aktuelle BSI-Quellenprüfung oder Konformitätsbestätigung abgeleitet. Die Empfehlungen verändern keine gesetzliche Pflicht.

Die 22 vorhandenen Negativtests bestanden. Die strenge Projektvalidierung mit Onlineprüfung und `--ohne-lokale-eingaben` meldete keine Fehler und elf Abrufwarnungen: acht ISO-Quellen, die BMI-Fundstelle samt gesondertem PDF-Abgleich und die NIST-OSCAL-Fundstelle. Die Option war erforderlich, weil die registrierten, von Git ausgeschlossenen Eingangsdateien in diesem Checkout fehlen. Der erfolgreiche Prüflauf ersetzt die noch erforderlichen manuellen Prüfungen dieser nicht erreichbaren Quellen nicht.

<a id="entscheidungen"></a>

## Festgehaltene Vorgaben aus der Abstimmung

Die folgenden Vorgaben konkretisieren den Auftrag zur Überarbeitung. Die fachlichen Vorgaben sind noch nicht in die Anforderungstexte des OSCAL-Katalogs, den Generator oder die Konzeptdokumente übernommen. A09 zur Auffindbarkeit ist bereits in Arbeitsregeln, Index und Katalogkennungen umgesetzt. Der [Inhaltsindex](INHALTSINDEX.md) verknüpft Entscheidungen, Risiken und Kontrollen. Die Abstimmung läuft im Frage-Antwort-Verfahren weiter. Unternehmensbezogene Betriebsangaben gehören ausschließlich in die getrennte private Fassung.

<a id="a01"></a>

### A01 Vollständig bewertetes, praktisch betreibbares Referenzkonzept

Die allgemeine Fassung soll für den beschriebenen Geltungsbereich bereits konkrete Ausgangs- und Restrisikobewertungen enthalten. Die Einstufungen werden aus dem vorgesehenen Einsatz und den tatsächlich umsetzbaren Maßnahmen hergeleitet. Das Restrisiko wird unter der ausdrücklich beschriebenen Annahme der Umsetzung dieser Maßnahmen bewertet; die jeweiligen Auswirkungen auf Eintrittshäufigkeit und Schadenshöhe werden begründet. Eine erfolgte Wirksamkeitsprüfung in einem bestimmten Unternehmen wird dadurch nicht behauptet.

Die Maßnahmen müssen einen funktionsfähigen Betrieb ermöglichen. Überzogene Vollständigkeitsnachweise und unverhältnismäßige Freigabeprozesse werden durch prüfbare, praktikable Festlegungen ersetzt. Für Unternehmen, deren Umgebung und Nutzung dem beschriebenen Geltungsbereich entsprechen, soll eine Übernahme mit wenigen Stammdaten- und Zuständigkeitsanpassungen möglich sein.

<a id="a02"></a>

### A02 Selbstständige Projektarbeit und einfache Wiederherstellung

Analyse, Lesen, Erzeugen, Codebearbeitung und Tests sollen innerhalb freigegebener Rechte und Arbeitsbereiche selbstständig möglich sein. Auch Änderungen, Löschungen und Übertragungen in freigegebene Projektablagen dürfen ohne Einzelgenehmigung erfolgen, wenn der Nutzer die betroffenen Daten und Zustände schnell, einfach und zuverlässig wiederherstellen kann. Sicherheitsrelevante Folgewirkungen sind einzubeziehen. Eine bestimmte Versionierungs- oder Sicherungstechnik wird nicht vorgeschrieben. Ohne diese Absicherung benötigen Löschungen und sonstige destruktive Tätigkeiten eine konkrete Genehmigung. Besondere Grenzen für kritische und privilegierte Eingriffe bleiben zu beachten.

<a id="a03"></a>

### A03 Bestehende Dokumenten- und Sicherheitsprozesse anwenden

Dokumente unterliegen dem regulären Qualitäts-, Freigabe- und Konfigurationsmanagement des Unternehmens. Ihre Nutzung durch KI begründet allein keine zusätzliche Dokumentenfreigabe. Die Zulässigkeit der KI-Nutzung wird für geeignete Arbeitsbereiche, Ablagen oder Datenbestände im bestehenden Regelwerk festgelegt. In einem entsprechend freigegebenen Bereich dürfen dessen Inhalte für die zugelassenen Zwecke im Rahmen der jeweiligen Nutzerrechte mit KI verarbeitet werden. Bestehende Nutzungsbeschränkungen bleiben wirksam; technische Lesbarkeit allein begründet keine allgemeine KI-Nutzungsfreigabe.

Die genehmigte Nutzung eines Bereichs kann auch dessen festgelegte Aufnahme in einen Wissensbestand abdecken. Dadurch entstehen keine weitergehenden Zugriffsrechte für andere Nutzer oder Zwecke. Ob ein Inhalt dauerhaft gespeichert werden darf, folgt aus der vorgesehenen Nutzung und den geltenden Ablageregeln. Eine besondere Genehmigung jedes einzelnen Dokuments ist dafür nicht erforderlich.

Allgemeine Sicherheitsmaßnahmen werden durch ausdrücklichen Bezug auf das maßgebliche IT-Sicherheitskonzept und die zugehörigen betrieblichen Richtlinien angewandt. Je Thema beschreibt das KI-Konzept zusätzlich, auf welche KI-Komponenten, Daten und Vorgänge die Basismaßnahmen anzuwenden sind und welche KI-spezifischen Ergänzungen erforderlich sind. Vorhandene Zuständigkeiten, Freigaben und Nachweise werden weiterverwendet. Ein Verweis ersetzt keine tatsächlich fehlende Basismaßnahme.

<a id="a04"></a>

### A04 Integration in das Unternehmensnetz und Übernahme der Anmeldung

Die KI-Umgebung wird in die bestehende Unternehmensinfrastruktur integriert. Bereits zugelassene Identitäts-, Netzwerk-, Ablage-, Versionsverwaltungs- und Betriebsdienste werden im Rahmen der geltenden IT-Sicherheitsvorgaben weiterverwendet. Dies gilt auch für extern betriebene Dienste, soweit deren Freigabe die vorgesehene KI-Nutzung und die damit verbundenen Datenflüsse abdeckt. Eine vollständig lokale Ausführung sämtlicher Basisdienste wird nicht vorausgesetzt.

Der KI-Zugang nutzt die bestehende Unternehmensanmeldung und die zugehörigen Nutzer- und Gruppenberechtigungen. Eine bereits erfolgte Anmeldung wird über die vorhandenen vertrauenswürdigen Anmeldemechanismen weiterverwendet, sodass keine erneute Anmeldung allein aufgrund der KI-Nutzung erforderlich ist. Zusätzliche Anmelde- oder Freigabeschritte richten sich nach den bestehenden Unternehmensrichtlinien. Der Zugriff bleibt einer berechtigten Person oder einem zugelassenen Dienst zugeordnet; Sperrungen und Rechteänderungen werden auch für die KI-Nutzung wirksam.

Lokale KI-Verarbeitung wird bevorzugt. Externe KI-Dienste können als gesonderte Betriebsvariante für freigegebene Zwecke und Daten genutzt werden. Für deren Anbindung gelten die bestehenden Vorgaben zu externen Dienstleistungen, Datenübertragung und Zugangsdaten. API-Schlüssel werden nach den betrieblichen Regeln für Dienstzugänge und Geheimnisse verwaltet. Bei gemeinsam genutzten Dienstzugängen bleibt die Nutzung den berechtigten Nutzern zuordenbar.

Fachliche Präzisierung: Die vorhandene Anmeldung soll ohne erneute Passworteingabe genutzt werden; der KI-Zugang muss den vertrauenswürdigen Anmeldekontext und die dazugehörige Berechtigung jedoch tatsächlich übernehmen können. Die reine Erreichbarkeit aus einem Unternehmensnetz stellt diesen Nachweis nicht her. Die Unterscheidung ist mit dem beschriebenen Einmalanmeldeverfahren und dem fehlenden automatischen Vertrauen allein aufgrund der Netzposition vereinbar. [Microsoft: Single Sign-on](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/what-is-single-sign-on), [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)

<a id="a05"></a>

### A05 Internetnutzung, ausdrückliche KI-Freigabe und Ausweichziele

Für Internetnutzung und externe Kommunikation gelten die Vorgaben des allgemeinen IT-Sicherheitskonzepts und der zugehörigen betrieblichen Richtlinien. Sie sind auch auf die KI-Umgebung anzuwenden. Eine allgemeine Freigabe des Internetzugangs beinhaltet keine Freigabe zur Nutzung externer KI-Dienste. Diese benötigen zusätzlich eine ausdrückliche Nutzungsfreigabe für den vorgesehenen Einsatz und die zulässigen Daten.

Als Ausweichziele können weitere freigegebene Modelle oder KI-Umgebungen vorgesehen werden. Diese können lokal oder extern betrieben sein. Die Freigabe muss die vorgesehene Nutzung als Ausweichziel einschließen. Automatische Wechsel dürfen ausschließlich innerhalb dieses freigegebenen Rahmens erfolgen; eine erneute Einzelgenehmigung jedes abgedeckten Wechsels ist nicht erforderlich. Ein Wechsel in eine nicht freigegebene KI-Umgebung bleibt auch bei Störung oder Überlastung unzulässig.

Ausweichziele sind eine optionale Betriebsfunktion. Ein automatischer Wechsel zu Cloud-KI wird weder vorausgesetzt noch pauschal aus einem vorhandenen Internetzugang abgeleitet. Die Risikobewertung darf einem nicht vorgesehenen oder nicht wirksamen Ausweichbetrieb keine risikomindernde Wirkung zuschreiben.

<a id="a06"></a>

### A06 Persönliche Speicherung und freiwillige Unternehmenswissensbildung

Persönliche Chatverläufe, Dateiübernahmen und Arbeitsergebnisse dürfen im zulässigen persönlichen Arbeitsbereich, beispielsweise auf dem verwalteten Arbeitsplatzrechner, nach den bestehenden Aufbewahrungs- und Löschregeln gespeichert werden. Allein wegen der KI-Nutzung ist hierfür keine zusätzliche Einzelfreigabe erforderlich. Die Speicherung eines Verlaufs bewirkt keine automatische Übernahme in einen Unternehmenswissensbestand.

Die Nutzung bereits freigegebener Wissensquellen zur Beantwortung einer Anfrage und das Hinzufügen neuer Wissensbeiträge sind getrennte Funktionen. Gewöhnliche Chatbot-Dialoge speisen Fragen, Antworten und beigefügte Inhalte standardmäßig nicht in Unternehmenswissensbestände zurück. Anbieter und Bedienoberfläche bestimmen diese Einordnung nicht; maßgeblich sind die freigegebene Funktion und ihre tatsächlichen Datenflüsse. Die Datenverwendung eines externen Anbieters ist zusätzlich in dessen Nutzungsfreigabe zu berücksichtigen; es wird keine allgemeine Zusage über ein bestimmtes Produkt oder dessen Speicherung getroffen.

Eine Unternehmenswissensbildung aus Agentenprojekten kann optional vorgesehen werden. Sie bleibt standardmäßig deaktiviert. Bei der erstmaligen Nutzung der KI und zu Beginn jedes Agentenprojekts wird eine ausdrückliche Entscheidung des Nutzers eingeholt. Die Information und Entscheidung für das erste Projekt können bei der Initialisierung zusammen erfolgen. Eine Zustimmung für ein früheres Projekt gilt nicht automatisch für spätere Projekte; ohne ausdrückliche Zustimmung findet keine Wissensübernahme statt. Eine Ablehnung lässt die übrige freigegebene KI-Nutzung unberührt.

Vor der Zustimmung werden vorgesehene Inhalte, Zweck, Zielbestand und berechtigter Nutzerkreis verständlich benannt. Während einer aktiven Wissensübernahme müssen deren Status und Umfang jederzeit erkennbar sein. Verdeckte Aktivierung oder stillschweigende Erweiterung sind unzulässig. Weitere Übernahmen müssen vom Nutzer beendet werden können. Fehlen die erforderlichen Zustimmungs-, Anzeige- oder Zugriffsschutzfunktionen, bleibt diese optionale Funktion deaktiviert; der übrige KI-Betrieb benötigt sie nicht.

Die Nutzerzustimmung erweitert keine Zugriffsrechte und ersetzt keine betriebliche oder datenschutzrechtliche Zulässigkeit. Vor einer Übernahme müssen zulässige Verwendung, Schutzbedarf und Zugriffsregeln für den Zielbestand bestimmbar sein. Bei Zusammenführung mehrerer Quellen dürfen abgeleitete Inhalte keinem Empfängerkreis zugänglich werden, der für die darin enthaltenen Informationen nicht berechtigt ist. Eine Zusammenfassung durch ein Sprachmodell ist für sich kein Nachweis, dass vertrauliche oder personenbezogene Informationen entfernt wurden. Bei unklarer Zulässigkeit oder nicht zuverlässig durchsetzbaren Rechten unterbleibt die automatische Übernahme.

Diese Grenzen gelten ebenso für abgeleitete Wissensbeiträge, Auszüge, Suchindizes und spätere Antworten. Ein unternehmensweit betriebener Speicher bedeutet keine unternehmensweite Leseberechtigung. Die Berechtigungsprüfung erfolgt unabhängig vom Sprachmodell und muss die unzulässige Offenlegung etwa persönlicher Korrespondenz, Gehaltsangaben oder Kundendaten auch bei aktiver Projektzustimmung verhindern. Ergänzend zu den bestehenden Berechtigungstests sind die deaktivierte Grundeinstellung, die fehlende Zustimmung, die Ablehnung, der Projektwechsel und die Trennung persönlicher Dialoge vom gemeinsamen Wissensbestand nachzuweisen.

Die Bereichsfreigabe aus A03 ist keine pauschale Zustimmung zur automatischen Zweitverwendung persönlicher Chat- und Agenteninteraktionen. Die bewusste Ablage oder Veröffentlichung freigegebener Fachdokumente erfolgt weiterhin über die normalen Dokumentenprozesse; ihre anschließende Nutzung richtet sich nach der freigegebenen Ablage und den bestehenden Rechten.

Mit Unternehmenswissensbildung ist hier die kontrollierte Aufnahme von Informationen für spätere Wissensabfragen gemeint. Training, Feinabstimmung und selbsttätige Änderungen von Modellgewichten bleiben ausgeschlossen. Fachliche Einordnung: Die RAG-Methode ergänzt Anfragen um Informationen aus getrennten Datenbeständen und verändert dadurch keine Modellgewichte. Zugriffstrennung ist im Wissenssystem mit klassischen Rollen- und Rechteverfahren durchzusetzen. [DSK-Orientierungshilfe RAG, Abschnitte 2.1 und 3.3](https://www.datenschutzkonferenz-online.de/media/oh/DSK_OH_RAG.pdf)

<a id="a07"></a>

### A07 Beenden der Wissensübernahme und Umgang mit bestehenden Beiträgen

Beim Deaktivieren der Wissensübernahme werden weitere Beiträge aus dem betroffenen Projekt nicht mehr in den Unternehmenswissensbestand übernommen. Bereits übernommene Beiträge werden nach den bestehenden Nutzungs-, Aufbewahrungs- und Löschregeln behandelt; das Deaktivieren allein löst weder eine pauschale Löschung noch eine pauschale Ausblendung rechtmäßig weiter nutzbarer Beiträge aus. Diese Wirkung wird dem Nutzer vor der Zustimmung und beim Deaktivieren verständlich erklärt.

Entfällt die Zulässigkeit der weiteren Nutzung oder eine Zugriffsberechtigung, muss die betroffene Nutzung unabhängig von dieser Einstellung unterbunden werden. Eine erforderliche Aufbewahrung begründet keine weitere Berechtigung zur KI-Verarbeitung. Erforderliche Berichtigungen und Löschungen erfolgen nach den geltenden Unternehmensprozessen und umfassen auch die betroffenen Ableitungen und Suchindizes.

<a id="a08"></a>

### A08 Begründete Akzeptanz mittlerer Restrisiken

Mittlere Restrisiken dürfen innerhalb der geltenden Risikotoleranz von der zuständigen Stelle begründet akzeptiert und regelmäßig überprüft werden. Sind die erforderlichen Maßnahmen umgesetzt und keine weiteren Maßnahmen beschlossen, wird kein zusätzlicher Maßnahmenplan allein wegen der Risikokategorie „mittel“ verlangt. Eine Befristung richtet sich nach der konkreten Entscheidung und den bestehenden Unternehmensregeln. Verantwortung, Begründung und erneute Bewertungsanlässe bleiben dokumentiert; veränderte Voraussetzungen oder erkannte Schutzmängel erfordern eine erneute Entscheidung.

<a id="a09"></a>

### A09 Dauerhafte Auffindbarkeit für Menschen und KI-Agenten

Entscheidungen, Risiken, Kontrollen und Quellen werden über stabile Kennungen und einen kompakten, vom Projekteinstieg erreichbaren Index miteinander verknüpft. Der Index benennt die maßgebliche Datei, den Abschnitt oder eine strukturierte Kennung sowie den Entscheidungs- und Umsetzungsstand. Er vervielfältigt keine normativen Anforderungstexte. Im OSCAL-Katalog erhalten auch die einzelnen Kontrollabschnitte dauerhafte Kennungen.

Die Pflege dieser Verweise ist Bestandteil jeder einschlägigen Änderung. Umbenennungen und Verschiebungen dürfen keine unbemerkten veralteten Verweise hinterlassen. Beschlossene Vorgaben, offene Empfehlungen und tatsächlich umgesetzte Inhalte bleiben unterscheidbar. Der Zugriff über einen Index erweitert keine Berechtigungen; organisationsbezogene Informationen und ihre Indizes verbleiben in der dafür vorgesehenen geschützten Fassung. Die Regel wird auch in den übergeordneten Workspace-Arbeitsregeln festgehalten.

<a id="a10"></a>

### A10 Hohe Restrisiken und begrenzter Ausnahmebetrieb

Hohe und sehr hohe Restrisiken werden an die zuständige Entscheidungsstelle eskaliert. Die betroffenen Funktionen bleiben gesperrt, sofern kein ausdrücklich genehmigter, befristeter Betrieb innerhalb der geltenden Unternehmensvorgaben mit zusätzlichen wirksamen Schutzmaßnahmen möglich ist. Die Entscheidung benennt Umfang, Verantwortung, Endtermin, Überwachung und klare Abbruchkriterien. Akute Gefahren, unzulässige Datenverarbeitung und fehlende Berechtigungen erlauben keine solche Ausnahme. Nicht betroffene Funktionen dürfen im Rahmen ihrer Freigabe weiterbetrieben werden. Die verbindliche Weiterarbeit ohne KI nach A11 darf durch eine Ausnahmeentscheidung ebenfalls nicht aufgehoben werden.

<a id="a11"></a>

### A11 Jede betriebliche Tätigkeit bleibt ohne KI ausführbar

Die KI unterstützt die Arbeit, darf jedoch keine unverzichtbare Voraussetzung für eine betriebliche Tätigkeit oder einen bestehenden Prozess werden. Sämtliche Tätigkeiten müssen auch bei einem länger andauernden KI-Ausfall ohne absehbaren Wiederherstellungszeitpunkt weiter ausführbar bleiben. Dies gilt ausdrücklich auch für bisher mit KI unterstützte Abläufe. Erforderliche Unterlagen, Arbeitsergebnisse, Zugangswege und Anwendungen bleiben unabhängig von der KI erreichbar und nutzbar. Die notwendigen Kenntnisse und Arbeitsverfahren werden erhalten. Geringere Geschwindigkeit oder geringerer Komfort und eine verminderte Ergebnisqualität sind im Rahmen der regulären Qualitätsanforderungen möglich; die grundsätzliche Arbeitsfähigkeit bleibt erhalten.

Die KI-Anbindung wird so begrenzt, dass ihre Überlastung, Störung oder Abschaltung den übrigen Unternehmensbetrieb nicht blockiert. Vorhandene Maßnahmen zur Ressourcenbegrenzung und zum Schutz der übrigen IT werden dafür angewandt. Die Weiterarbeit ohne KI ist eine verbindliche Voraussetzung des zugelassenen Einsatzes; eine allgemeine oder befristete Risikoakzeptanz ersetzt sie nicht. Vorhandene Prozessbeschreibungen und angemessene Funktionsprüfungen belegen, dass die betroffenen Tätigkeiten und benötigten Informationen ohne KI verfügbar bleiben. Ein gesondertes Verfahren für jede einzelne Arbeitsaktion ist nicht erforderlich.

Die Wiederherstellung der KI erfolgt über die regulären IT-Betriebs-, Instandsetzungs- und Änderungsverfahren. Konfigurationen, geeignete Sicherungen und Zuständigkeiten ermöglichen die spätere Wiederinbetriebnahme. Ein zusätzliches KI-Notfallkonzept, eine besondere Notfallorganisation oder eine pauschale KI-spezifische Wiederanlaufzeit werden nicht verlangt. Die bestehenden betrieblichen Regeln bleiben maßgeblich; eine Wiederaufnahme der normalen Tätigkeiten darf nicht von der Reparatur der KI abhängen.

Als betriebliche Wiederherstellungswege kommen beispielsweise das Ersetzen fehlerhafter Zugangsdaten für einen bereits freigegebenen externen KI-Dienst oder das Zuschalten eines gleich konfigurierten lokalen Ersatzsystems in Betracht. Ein bereitgehaltenes Ersatzsystem ist eine mögliche Umsetzung und keine allgemeine Pflicht zur doppelten Hardwareausstattung. Bei Ersatz und Wiederinbetriebnahme bleiben die freigegebenen Zwecke, Daten, Zugriffsrechte und Schutzmaßnahmen wirksam. Ein anderer API-Schlüssel behebt nur entsprechende Zugangsprobleme; er ersetzt keinen ausgefallenen Anbieter. Ein Wechsel zu einer anderen KI-Umgebung richtet sich weiterhin nach A05 und ist für die Weiterarbeit ohne KI nicht erforderlich.

Für R-06 wird das verbleibende Verfügbarkeitsrisiko bei Umsetzung dieser Bedingungen als gering bewertet. Die Schadenshöhe wird konservativ als begrenzt geführt, weil zusätzlicher Arbeitsaufwand und verminderte Geschwindigkeit oder Qualität verbleiben können. Diese Bewertung setzt keine rasche Reparatur, keinen zweiten Anbieter und keinen automatisch verfügbaren Ersatzserver voraus. Andere Risiken wie Datenoffenlegung oder bereits verursachte Fehlentscheidungen werden dadurch nicht herabgestuft.

Die fachliche Übernahme betrifft insbesondere KI-GOV-002 (zugelassene Nutzung und Kenntnisse), KI-THR-002 (Ressourcen und Auswirkungen auf andere Dienste) sowie KI-OPS-003 (reguläre Wiederherstellung). Kapitel 3, 8 und 13 und die zugehörigen Prüfziele sind gemeinsam anzupassen. Die bisher pauschal verlangte Wiederherstellung ohne Internetzugang in KI-OPS-003 wird dabei an die nach A04/A05 freigegebene Betriebsvariante angepasst; zugelassene Unternehmens- und Cloud-Dienste dürfen genutzt werden.

<a id="basisprozesse"></a>

### Prüfung der Überschneidungen für alle 38 Kontrollen

Geprüft wurden die Anforderungen und Umsetzungstexte aller Kontrollen sowie Kapitel 3 des Generators. Ein konkretes betriebliches IT-Sicherheitskonzept liegt dieser Prüfung nicht zugrunde; die Tabelle ordnet die Referenzkontrollen den zu referenzierenden Basisprozessen zu. Die tatsächlichen Dokumenttitel und Fundstellen werden bei der Unternehmensübernahme zugeordnet und nicht erfunden.

| Kontrollen | Bezug zum allgemeinen Sicherheitsprozess | Im KI-Konzept verbleibende Konkretisierung |
|---|---|---|
| KI-GEL-001 | Geltungsbereich, Sicherheitskonzept und zugehörige Richtlinien | Verbindliche Zuordnung der Basismaßnahmen und ihrer KI-spezifischen Ergänzungen; vorhandene Regel ist je Thema umzusetzen. |
| KI-GEL-002, KI-GOV-001, KI-GOV-003, KI-ASS-001 | Dokumentenlenkung, Inventar, Verantwortlichkeiten, Risikomanagement und Nachweisführung | KI-Dienste, Modelle und Wissensbestände in bestehende Register aufnehmen; KI-Szenarien und zusätzliche Nachweise ergänzen. Keine getrennten Register allein wegen KI verlangen. |
| KI-GOV-002, KI-REC-001, KI-REC-002 | Nutzungsrichtlinien, Qualifikation, Datenschutz, Informationsklassifikation und besondere Schutzvorgaben | Zugelassene KI-Nutzungen und Bereiche festlegen; zusätzliche Auswirkungen des KI-Einsatzes prüfen und vermitteln. Vorhandene Freigaben gelten innerhalb ihres abgedeckten Umfangs. |
| KI-ARC-001, KI-ARC-002, KI-CON-001, KI-CON-002 | Netz-, Plattform-, Container- und Kommunikationssicherheit | Die freigegebenen Dienste und Datenflüsse der KI-Architektur zuordnen; Inferenz- und Verwaltungsschnittstellen begrenzen. Vorhandene Unternehmensdienste gemäß A04 einbinden; lokale Inferenz erfordert keine ausschließlich lokalen Basisdienste. |
| KI-API-001, KI-API-002, KI-IAM-001, KI-AGT-001, KI-AGT-002 | Identitäten, Rollen, Berechtigungen, Geheimnisverwaltung und erlaubte Dienstzugriffe | Nutzerrechte an KI-Zugang und Werkzeugen wirksam fortführen; zusätzliche Modell-, Kontext- und Aktionsgrenzen festlegen. Keine zusätzlichen Rechte allein durch KI-Verarbeitung. |
| KI-MOD-001, KI-MOD-002, KI-TOL-002, KI-VAL-001, KI-VAL-002 | Beschaffung, Softwareverteilung, Konfigurationsmanagement, Änderungen, Tests und Freigaben | Modellartefakte und Werkzeuge in vorhandene Verfahren einbeziehen; passende Prüfungen der Ergebnisqualität, Sicherheit und Kompatibilität ergänzen. Normale Dokumentenänderungen lösen keine zusätzliche KI-Einzelfreigabe aus. |
| KI-RAG-001, KI-RAG-002, KI-RAG-003, KI-RAG-004 | Dokumentenqualität, Ablagefreigabe, Schadsoftwareschutz, Nutzerrechte, Aufbewahrung und Löschung | Bereichsfreigabe gemäß A03 nutzen; persönliche Speicherung und optionale Wissensübernahme gemäß A06 trennen. Sichere Dateiaufbereitung sowie Rechte und Löschung auch für Suchindizes, Auszüge und Zwischenspeicher gewährleisten. Verwendbare bestehende Dateiprüfungen nicht ohne Anlass doppeln. |
| KI-PMT-001, KI-OUT-001, KI-TOL-001 | Sichere Verarbeitung, Ergebnisprüfung, Änderungsrechte und Freigaben nach Auswirkung | Dokumentinhalt darf keine Rechte erweitern. Ausgaben entsprechend ihrer vorgesehenen Wirkung prüfen; selbstständige Projektarbeit und abgesicherte Wiederherstellung gemäß A02 ermöglichen. |
| KI-THR-001, KI-THR-002 | Bedrohungsbewertung, Kapazitätsplanung und Verfügbarkeit | KI-Angriffswege, Modellunsicherheit, lange Anfragen und Agentenschleifen in bestehende Bewertungen aufnehmen; überprüfbare Abdeckung und angemessene Betriebsgrenzen festlegen. |
| KI-OPS-001, KI-OPS-002, KI-OPS-003, KI-DEC-001 | Protokollierung, Überwachung, Vorfallbehandlung, Sicherung, Wiederanlauf und Außerbetriebnahme | KI-Ereignisse und Dienstzusammenhänge ergänzen; Modelle, Berechtigungen, Indizes und Konfiguration konsistent behandeln. Bestehende Meldewege und Wiederanlaufverfahren verwenden. |
| KI-TRN-001 | Genehmigter Softwareeinsatz und Schutz vor unzulässigen Änderungen | Das spezifische Verbot von Training und Gewichtsänderungen bleibt ausdrücklich im KI-Konzept; Durchsetzung über erlaubte Funktionen und Rechte statt eines pauschalen Verbots vielseitiger Bibliotheken. |
| KI-EXT-001, KI-EXT-002 | Fremdleistungen, externe Datenübertragung, Anbieterprüfung und Datenschutz | Lokale Verarbeitung bevorzugen; externe KI gemäß A04 und A05 ausdrücklich zur Nutzung freigeben. Internetregeln aus dem Basis-Sicherheitskonzept anwenden. Keine erneute vollständige Vertragsprüfung für jede einzelne Anfrage; optionale Ausweichziele müssen vom freigegebenen Nutzungsrahmen erfasst sein. |

Besonders zu überarbeiten sind die pauschale Wiederfreigabe in KI-VAL-002 sowie die Auslegung der dauerhaften Übernahme in KI-RAG-004 als Einzelfreigabe. Der technische Schutz bei Dateiaufbereitung in KI-RAG-001 und die durchgängigen Nutzerrechte in KI-RAG-002 bleiben als Anforderungen erhalten; ihre Umsetzung wird mit den vorhandenen Basismaßnahmen abgestimmt.

Ein wiederverwendbarer Formulierungsansatz lautet: „Für diesen Regelungsbereich gelten die Maßnahmen des maßgeblichen IT-Sicherheitskonzepts und der zugehörigen betrieblichen Richtlinien. Sie sind auf die hier beschriebenen KI-Dienste, Datenbestände und Vorgänge anzuwenden. Die nachfolgenden Festlegungen ergänzen diese Maßnahmen um die KI-spezifischen Anforderungen.“ Die jeweiligen Dienste, Daten und Ergänzungen werden im betreffenden Abschnitt konkret benannt.

<a id="risikobewertungen"></a>

## Vorbereitete Risikobewertungen für die weitere Abstimmung

Die nachfolgenden Einstufungen sind fachliche Vorschläge auf Grundlage der Beschlüsse A01 bis A11; R-06 berücksichtigt die verbindliche Weiterarbeit ohne KI aus A11. Sie ersetzen noch nicht das Risikoregister in Kapitel 8. Bewertet wird jeweils das schädliche Ereignis: beispielsweise die tatsächlich unberechtigte Offenlegung, nicht bereits eine persönliche Speicherung, ein Angriffsversuch oder eine fehlerhafte Modellantwort ohne weitere Auswirkung.

Das Ausgangsrisiko berücksichtigt die regulären Schutzmaßnahmen des Unternehmens, jedoch noch nicht die zusätzliche KI-spezifische Behandlung. Das Restrisiko setzt die beschriebenen, umsetzbaren Maßnahmen und ihre wirksame Anwendung voraus. Die Häufigkeiten sind qualitative Einschätzungen für eine regelmäßig genutzte Unternehmensumgebung, keine gemessenen Ereignisraten. Insbesondere setzt „selten“ bei Zugriffs- und Aktionsverletzungen voraus, dass die Grenze außerhalb des Sprachmodells durchgesetzt und mit geeigneten Tests geprüft wird. Eine Anweisung an das Modell allein rechtfertigt diese Herabstufung nicht.

Die bestehende Matrix wird für diese Gegenüberstellung beibehalten. Eine geringere Eintrittshäufigkeit kann innerhalb derselben Risikokategorie liegen. „Selten × beträchtlich“ und „mittel × beträchtlich“ ergeben beide „mittel“; die Maßnahmenwirkung wird deshalb zusätzlich erläutert. Auch „selten × existenzbedrohend“ ergibt in dieser Matrix „mittel“. Eine solche Einstufung darf eine besonders schwerwiegende Schadensmöglichkeit bei der Akzeptanzentscheidung nicht verdecken.

| ID und konkretisiertes Schadensereignis | Ausgangsrisiko | Vorgeschlagenes Restrisiko | Umsetzbare Behandlung und verbleibende Grenze |
|---|---|---|---|
| <a id="r-01"></a>R-01: Eingeschleuste Inhalte führen zu einer unzulässigen Werkzeugaktion mit erheblicher Auswirkung. | häufig × beträchtlich = hoch | selten × beträchtlich = mittel | Rechte und erlaubte Aktionen außerhalb des Modells begrenzen; selbstständige Arbeit einschließlich leicht rückgängig zu machender Änderungen nach A02 zulassen. Nicht ausreichend abgesicherte destruktive Tätigkeiten erfordern Genehmigung. Wiederherstellung begrenzt reversible Projektfehler, macht aber eine Offenlegung oder andere nicht rückholbare Folgewirkungen nicht ungeschehen. |
| <a id="r-02"></a>R-02: Manipulierte Modelle, Pakete oder Erweiterungen werden übernommen und beeinträchtigen die Umgebung. | mittel × beträchtlich = mittel | selten × beträchtlich = mittel | Bestehende Beschaffungs-, Herkunfts-, Integritäts- und Freigabeprüfungen auf KI-Artefakte anwenden; Signaturen prüfen, soweit verfügbar. Herkunft und Prüfsumme belegen nicht allein die Unbedenklichkeit des Inhalts. Eine kompromittierte vertrauenswürdige Quelle bleibt möglich; die Schadenshöhe wird nicht pauschal herabgesetzt. |
| <a id="r-03"></a>R-03: Wissensabfragen oder übernommene Projektbeiträge offenbaren geschützte Informationen an Unberechtigte. | häufig × beträchtlich = hoch | selten × beträchtlich = mittel | Nutzerrechte bei Aufnahme und Abruf fortführen; persönliche Verläufe und Unternehmenswissen nach A06/A07 trennen. Projektzustimmung, sichtbarer Status und technisch durchgesetzte Empfängerrechte müssen gemeinsam vorliegen. Unklare Beiträge werden nicht automatisch übernommen. Fehlzuordnungen, Rechtefehler oder unbekannte Schwachstellen bleiben ein Restrisiko; ein dennoch erfolgter Abfluss kann weiterhin beträchtlich schaden. |
| <a id="r-04"></a>R-04: Ein Zugriff auf die KI umgeht die vorgesehene Identitäts- oder Berechtigungsprüfung. | mittel × beträchtlich = mittel | selten × beträchtlich = mittel | Unternehmensanmeldung und zugehörige Rechte wirksam übernehmen; auch direkte Schnittstellen müssen denselben Schutz gewährleisten oder für unberechtigte Zugriffe gesperrt sein. Netzzugehörigkeit ersetzt keine Berechtigung. Fehlkonfigurationen oder kompromittierte Zugänge bleiben möglich. |
| <a id="r-05"></a>R-05: Betriebsprotokolle speichern unnötig geschützte Inhalte und machen sie zusätzlich zugänglich. | häufig × beträchtlich = hoch | selten × beträchtlich = mittel | Im Regelfall erforderliche Betriebs- und Sicherheitsmetadaten protokollieren; Inhaltsaufzeichnungen begrenzen, zweckgebunden schützen und nach den geltenden Fristen löschen. Zulässige persönliche Verlaufsspeicherung ist davon getrennt. Wegen möglicher Personal-, Kunden- oder Geschäftsangaben wird ohne belegte Inhaltsbegrenzung keine pauschal geringe Schadenshöhe angenommen. |
| <a id="r-06"></a>R-06: Aufwendige Anfragen oder Agentenschleifen überlasten die KI und beeinträchtigen die unterstützte Arbeit oder gemeinsame IT-Ressourcen. | häufig × beträchtlich = hoch | mittel × begrenzt = gering | Ressourcen- und Laufzeitgrenzen sowie kontrolliertes Beenden begrenzen Überlastung und schützen die übrige IT. Nach A11 bleibt jede Tätigkeit auch bei längerem KI-Ausfall ohne KI ausführbar; notwendige Informationen und Anwendungen bleiben erreichbar. Die verbleibenden Folgen beschränken sich auf begrenzten Mehraufwand und Einbußen innerhalb der zulässigen Qualitätsanforderungen. Die KI wird im normalen IT-Betrieb repariert. Eine schnelle Wiederherstellung, ein Ersatzsystem oder ein Anbieterwechsel sind keine Voraussetzung dieser Schadensbegrenzung. |
| <a id="r-07"></a>R-07: Fehlerhafte Ausgaben werden ohne ausreichende Qualitätssicherung wirksam eingesetzt und verursachen Fehlentscheidungen oder unsichere Software. | häufig × beträchtlich = hoch | mittel × beträchtlich = mittel | Normale fachliche Prüfung, Softwaretests und Freigaben nach der Auswirkung anwenden; keine Einzelbestätigung für jede gewöhnliche KI-Antwort oder reversible Codeänderung verlangen. Auch geprüfte Ergebnisse können Fehler enthalten. Die bisherige starke Absenkung auf „selten“ wird ohne zusätzliche Begründung nicht übernommen. Häufige Modellfehler sind nicht mit ebenso häufigen beträchtlichen Schäden gleichzusetzen. |
| <a id="r-08"></a>R-08: Eine KI-Verbindung oder ein Ausweichziel übermittelt geschützte Inhalte außerhalb der zugelassenen Nutzung. | mittel × existenzbedrohend = hoch | selten × existenzbedrohend = mittel | Nur ausdrücklich freigegebene KI-Ziele für die zugelassenen Zwecke und Daten verwenden; auch automatische Wechsel daran binden. Bestehende Internet- und Übertragungsregeln anwenden und unzulässige Verbindungen technisch unterbinden. Für den bereits angesetzten schweren Schadensfall bleibt die Schadenshöhe erhalten. Eine niedrigere Einstufung benötigt eine begründete Begrenzung der betroffenen Daten und Auswirkungen. |
| <a id="r-09"></a>R-09: Eine Änderung beeinträchtigt Sicherheit oder Ergebnisqualität im wirksamen Betrieb. | häufig × beträchtlich = hoch | mittel × beträchtlich = mittel | Bestehendes Änderungsmanagement verwenden: Routineänderungen nach genehmigtem Verfahren, wesentliche Änderungen mit passenden Wiederholungsprüfungen und Freigabe. Wiederherstellung muss entzogene Rechte und erforderliche Löschungen berücksichtigen. Tests und Rückkehrmöglichkeiten erfassen nicht jeden Fehler und machen bereits eingetretene Folgen nicht rückgängig; „selten“ wird daher nicht pauschal angesetzt. |

R-03, R-05 und R-08 behalten jeweils die Schadenshöhe der betrachteten Informationen. Bei besonders schutzbedürftigen Informationen kann auch außerhalb von R-08 eine höhere Schadenshöhe erforderlich sein; die Referenzeinstufung darf die bestehende Schutzbedarfsfeststellung nicht überschreiben. R-08 führt den bereits enthaltenen existenzbedrohenden Schadensfall fort, ohne ihn als allgemeinen Normalfall jeder externen KI-Nutzung darzustellen. Die Tabelle bewertet weder eine ordnungsgemäß freigegebene externe Verarbeitung noch eine zulässige persönliche Speicherung als Sicherheitsvorfall.

Bei R-06 beschreibt das hohe Ausgangsrisiko eine Einbindung vor der KI-spezifischen Behandlung, bei der ungebremste KI-Ressourcennutzung oder fehlende Arbeitsmöglichkeiten ohne KI beträchtliche Auswirkungen haben können. Eine solche Abhängigkeit ist nach A11 kein zugelassener Betriebszustand. Ressourcenbegrenzungen mindern die Häufigkeit wirksamer Überlastungen; die erhaltene Arbeitsfähigkeit ohne KI begrenzt deren Schaden. Die Weiterarbeitsmöglichkeit allein verhindert keinen KI-Ausfall. Die Häufigkeitsannahme „mittel“ bezieht sich auf das betrachtete Überlastungsszenario und wird nicht pauschal auf alle Hardware-, Anbieter- oder Zugangsprobleme übertragen.

Die Akzeptanzregeln sind mit A08 und A10 beschlossen: Mittlere Restrisiken werden im regulären Prozess behandelt; für hohe und sehr hohe Restrisiken gelten Eskalation, Sperrung betroffener Funktionen und die eng begrenzte Ausnahmeentscheidung. A11 zur Weiterarbeit ohne KI bleibt dabei eine nicht ausnahmefähige Voraussetzung. Die fachliche Übernahme in Katalog und Konzept steht noch aus.

Diese Akzeptanzempfehlung ist eine eigene fachliche Festlegung. Das öffentliche BSI-Beispiel RECPLAST zeigt in Abschnitt 7.6 sowohl zusätzliche Maßnahmen als auch begründete Akzeptanz bei mittleren Risiken. Daraus wird keine allgemeine Genehmigung eines konkreten Unternehmensrisikos abgeleitet. Die relevante Passage war am 14.09.2026 im Suchindex der offiziellen Quelle einsehbar; der direkte Abruf des BSI-Standards 200-3 blieb mit HTTP 403 gesperrt. [BSI: RECPLAST, Abschnitt 7.6, S. 52](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Webkurs/Recplast_Onlinekurs2018.pdf?__blob=publicationFile&v=7)
