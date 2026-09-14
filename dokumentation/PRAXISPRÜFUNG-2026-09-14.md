# Kritische Praxisprüfung des KI-IT-Sicherheitskonzepts

Stand: 14.09.2026. Geprüft wurden die kommentierte PDF, das vorhandene DOCX/PDF-Paar, alle 38 OSCAL-Kontrollen und die zugehörigen Generatorpassagen. Die Seitenangaben beziehen sich auf die 64-seitige PDF der Version 0.1.0 mit fachlichem Stichtag 03.09.2026.

**Die folgenden Formulierungen sind Empfehlungen zur Entscheidung. Sie wurden nicht in das Konzept oder die Anforderungen des Katalogs übernommen.** Die Prüfung bewertet die praktische Erfüllbarkeit und Nachweisbarkeit der Festlegungen. Eine tatsächliche Unternehmensumgebung wurde noch nicht bewertet.

## PDF-Kommentar

Die eingereichte PDF enthält genau eine inhaltliche Annotation und deren leeres Anzeigefenster. Auf Seite 1 ist „Sicherheitskonzept für vollständig lokale KI-Infrastrukturen“ markiert. Der Kommentar lautet „Hier ist etwas kommentiert“.

Der Kommentar enthält weder eine gewünschte Änderung noch einen Ersatztext. Deshalb wurde daraus keine inhaltliche Änderung abgeleitet. Der gesamte extrahierte Seitentext ist auf allen 64 Seiten mit der Repository-PDF identisch. Weitere Änderungsanweisungen wurden nicht gefunden. Für die Bearbeitung dieser Markierung ist noch die beabsichtigte Änderung zu benennen, sofern es sich nicht um einen Testkommentar handelt.

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

## P01 Restrisiken sind keine zugesicherte Maßnahmenwirkung

**Fundstelle:** S. 13, Beschriftung der Abbildung 4: „Die KI-spezifischen Maßnahmen senken alle hohen und sehr hohen Ausgangsrisiken auf höchstens mittel.“ S. 14, Risikoregister, besonders R-08.

**Kritik:** Die Formulierung behauptet eine bereits feststehende Wirkung, obwohl weder konkrete Unternehmensdaten noch Wirksamkeitsmessungen vorliegen. Bei R-08 sinkt sogar die Schadenshöhe eines Datenabflusses von „existenzbedrohend“ auf „begrenzt“. Eine blockierte Verbindung kann die Eintrittshäufigkeit senken; weshalb ein dennoch eintretender Abfluss weniger schädlich wäre, begründen die genannten Maßnahmen nicht. Das NIST-Profil betont die Abhängigkeit von Nutzungskontext und empirischer Grundlage sowie Grenzen der Risikoschätzung. Die Folgerung für dieses Konzept ist eine eigene fachliche Bewertung. [NIST AI 600-1, Abschnitt 2, S. 2–3](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

**Empfohlene Ersatzformulierung:**

> Nach Umsetzung und Prüfung der Maßnahmen werden Eintrittshäufigkeit und Schadenshöhe für jedes Szenario erneut bewertet. Eine Freigabe setzt ein nach den festgelegten Kriterien akzeptables und nachvollziehbar begründetes Restrisiko voraus. Eine niedrigere Schadenshöhe wird nur angesetzt, wenn konkrete Maßnahmen die mögliche Schadenswirkung nachweisbar begrenzen.

**Erforderlicher Nachweis:** Annahmen, Messungen oder geeignete Erfahrungswerte je Szenario; gesonderte Begründung jeder geänderten Schadenshöhe. Die Zielwerte dürfen bis dahin nur als Planungsannahmen gelten. Bei Annahme der Empfehlung müssen Register, Matrix und Beschriftung gemeinsam angepasst werden.

## P02 Eine hohe Risikoeinstufung benötigt eine differenzierte Betriebsentscheidung

**Fundstelle:** S. 13 und 19, KI-GOV-003: „Hohe und sehr hohe Risiken MÜSSEN eine Erstfreigabe oder den Weiterbetrieb bis zur wirksamen Behandlung sperren.“

**Kritik:** Die Regel ist als bewusst gewählte Risikotoleranz zulässig und erfüllbar, kann im laufenden Betrieb aber ohne weitere Eingrenzung unverhältnismäßige Abschaltungen auslösen. Sie unterscheidet weder betroffene Funktionen noch akute Gefahren von längerfristigem Handlungsbedarf. Die zugrunde liegende BSI-Methodik kennt mehrere Behandlungsoptionen einschließlich verantworteter Risikoakzeptanz; daraus folgt keine pauschale Erlaubnis, verbindliche Anforderungen außer Kraft zu setzen. [BSI-Standard 200-3, Kapitel 6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/BSI_Standards/standard_200_3.pdf?__blob=publicationFile&v=2)

**Empfohlene Ersatzformulierung:**

> Hohe und sehr hohe Risiken werden unverzüglich an die zuständige Entscheidungsstelle eskaliert. Nicht akzeptable Risiken sperren die betroffenen Funktionen. Ein befristeter eingeschränkter Weiterbetrieb darf nur innerhalb der festgelegten Risikotoleranz, mit dokumentierter Entscheidung, wirksamen kompensierenden Maßnahmen, Überwachung und verbindlichem Endtermin zugelassen werden. Zwingende Freigabevoraussetzungen und akute Gefahren dürfen dadurch nicht umgangen werden.

**Erforderlicher Nachweis:** Entscheidungsbefugnisse, nicht ausnahmefähige Grenzen, betroffene Funktionen, Fristen und Abschaltkriterien. Die Organisation kann die bisherige strengere Grenze ausdrücklich beibehalten.

## P03 Alle real möglichen Angriffswege lassen sich nicht vollständig testen

**Fundstelle:** S. 42, KI-THR-001, Prüfziel: „jeder real mögliche Daten- und Aktionspfad modelliert, mit Szenarien getestet“. Verwandte sehr absolute Prüfziele stehen in KI-API-002 und KI-PMT-001.

**Kritik:** Schnittstellen, Datenklassen und Berechtigungsgrenzen lassen sich inventarisieren. Alle möglichen Inhalte, Modellreaktionen und mehrstufigen Werkzeugkombinationen lassen sich bei einem offenen generativen System dagegen nicht erschöpfend prüfen. Ein erfolgreicher Testsatz belegt seine geprüften Fälle. Er ist kein Beweis, dass kein weiterer Angriff existiert. NIST beschreibt ausdrücklich Grenzen bei Umfang und Bewertung teilweise unbekannter KI-Risiken. [NIST AI 600-1, Abschnitt 2, S. 3](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

**Empfohlene Ersatzformulierung:**

> Das Bedrohungsmodell erfasst alle inventarisierten Schnittstellen, Vertrauensgrenzen und freigegebenen Aktionsklassen. Sicherheitskritische Grenzen werden mit risikobasierten positiven und negativen Tests geprüft. Testabdeckung, nicht geprüfte Kombinationen und verbleibende Unsicherheiten werden dokumentiert. Berechtigungen und Werkzeuggrenzen werden unabhängig vom Modell technisch durchgesetzt.

**Erforderlicher Nachweis:** Abdeckungsmatrix mit Daten- und Aktionsklassen, Testsatz, Ergebnissen und benannten Grenzen. Die eigentliche Anforderung, unberechtigte Zugriffe technisch zu verhindern, bleibt bestehen.

## P04 Nicht jede RAG-Aktualisierung benötigt eine vollständige Wiederfreigabe

**Fundstelle:** S. 12: „Änderungen oder abgelaufene Prüffristen führen zurück in die vollständige Bewertung.“ S. 45, KI-VAL-002: Änderungen unter anderem an RAG-Daten müssen Wiederholungsprüfung und Wiederfreigabe auslösen; für jede Änderung wird eine erfolgreiche Rückkehr zur vorherigen Kombination verlangt.

**Kritik:** Der Katalog nennt zwar bereits risikobasierte Tests, unterscheidet aber nicht zwischen Modellwechsel, Rechteänderung, Korrektur eines Dokuments und täglichem Wissensimport. Eine formale Gesamtfreigabe und praktisch ausgeführte Rückkehr für jede Datenaktualisierung würden den regulären Betrieb erheblich belasten. Eine Rückkehr darf außerdem keine gelöschten Inhalte oder entzogenen Rechte erneut aktivieren.

**Empfohlene Ersatzformulierung:**

> Änderungen werden vor ihrer Umsetzung nach Auswirkung auf Sicherheit, Berechtigungen und Ergebnisqualität eingestuft. Standardänderungen innerhalb eines genehmigten Änderungsprofils dürfen nach festgelegten automatisierten Prüfungen übernommen werden. Wesentliche Änderungen erfordern gezielte Wiederholungsprüfungen und eine ausdrückliche Wiederfreigabe. Die Wiederherstellbarkeit wird regelmäßig und nach relevanten Änderungen erprobt; Löschungen und Berechtigungswiderrufe bleiben dabei wirksam.

**Erforderlicher Nachweis:** Änderungsmatrix, Kriterien für Standardänderungen, betroffene Tests, Entscheidung und regelmäßig erprobtes Wiederherstellungsverfahren. Keine Ausnahme für Änderungen der System- oder Berechtigungsgrenze allein wegen ihres geringen Umfangs.

## P05 Sofortige Nichtzugreifbarkeit und abgeschlossene Löschung sind verschiedene Ziele

**Fundstelle:** S. 34, KI-RAG-004: „nachweislich vollständigen Löschlauf“ und Nichtzugreifbarkeit von Datei, Auszügen, Suchvektoren und Zwischenspeichern nach Sitzungsende. Ergänzend S. 33, KI-RAG-003.

**Kritik:** Sitzungsende ist bei Verbindungsabbruch, abgestürzten Diensten und asynchroner Verarbeitung ohne Definition unklar. Die sofortige Sperre einer Sitzung ist technisch anders nachzuweisen als das Entfernen aller gespeicherten Ableitungen. Die vorhandene Sicherungsregel ist bereits realistisch: KI-RAG-003 sieht Löschmarkierungen und geregeltes Auslaufen aus Sicherungen vor. Sie verlangt keine sofortige Veränderung jeder Sicherungskopie.

**Empfohlene Ersatzformulierung:**

> Sitzungsbezogene Inhalte werden bei Beendigung oder Ablauf der Sitzung für weitere Anfragen gesperrt. Quelldateien und Ableitungen werden innerhalb der im Löschkonzept festgelegten Fristen gelöscht; fehlgeschlagene Löschaufträge werden erkannt und nachbearbeitet. Temporäre Inhalte werden grundsätzlich nicht in dauerhafte Wissensbestände oder reguläre Sicherungen übernommen. Erforderliche Ausnahmen werden ausdrücklich geregelt. Bei Wiederherstellungen werden gültige Löschmarkierungen vor Freigabe der Daten erneut angewandt.

**Erforderlicher Nachweis:** Eindeutiger Sitzungsablauf, getrennte Sperr- und Löschfristen, Tests bei Absturz und Wiederherstellung, Umgang mit Sicherungen und minimalen Prüfprotokollen. Die Fristen werden anhand des tatsächlichen Schutzbedarfs festgelegt.

## P06 Der Fließtext verlangt mehr Bestätigungen als die normative Kontrolle

**Fundstelle:** S. 40, KI-TOL-001, fordert konkrete Bestätigung für kritische, destruktive, privilegierte oder externe Aktionen; die Umsetzung verbietet Sammelfreigaben. S. 54, Kapitel 11, nennt eine konkrete menschliche Bestätigung allgemein als Schranke jeder Werkzeugaktion. Der Alternativtext erfasst zudem alle Schreib-, Befehls- und Netzwerkaktionen.

**Kritik:** Diese unterschiedlichen Grenzen führen zu verschiedenen Implementierungen. Eine Bestätigung jedes unkritischen Dateilesens, Tests oder reversiblen Bearbeitungsschritts erschwert den Nutzen von Agenten und fördert routinemäßiges Bestätigen ohne Prüfung. Die normative Kontrolle enthält bereits eine sinnvolle Differenzierung nach Wirkung; Fließtext und Diagramm sollten ihr entsprechen.

**Empfohlene Ersatzformulierung:**

> Jede Werkzeugaktion unterliegt einer technisch erzwungenen Richtlinie und minimalen Rechten. Für risikoarme Aktionen können vorab genehmigte Aktionsprofile innerhalb eines benannten Arbeitsbereichs gelten. Kritische, destruktive, privilegierte oder externe Aktionen erfordern eine konkrete Bestätigung mit Ziel und Wirkung. Eine Profilfreigabe darf diese Bestätigung nicht ersetzen oder Rechte erweitern.

**Erforderlicher Nachweis:** Aktionsklassen, wirksame Profile, konkrete Bestätigungsgrenzen und Negativtests. Bei Annahme müssen Katalog, Kapitel 11, PlantUML-Quelle und Alternativtext zusammengeführt werden.

## P07 Trainingsfähige Bibliotheken sind nicht mit freigegebenem Training gleichzusetzen

**Fundstelle:** S. 30, KI-TRN-001, Umsetzung: „Trainingssoftware, Schreibpfade auf Modellgewichte und lernende Rückkopplungen werden nicht bereitgestellt.“ Das Prüfziel erfasst auch Pakete, die keine Gewichtsänderung erlauben sollen.

**Kritik:** Das Verbot tatsächlichen Trainings ist umsetzbar. Ein pauschales Verbot jeder Bibliothek mit Trainingsfunktionen kann dagegen gängige Inferenzumgebungen ausschließen. Entscheidend sind erreichbare Funktionen, Aufträge, Datenflüsse und effektive Schreibrechte. Aus dem Vorhandensein einer Funktion allein folgt noch keine erlaubte Ausführung.

**Empfohlene Ersatzformulierung:**

> Training, Feinabstimmung und lernende Rückkopplungen sind im Geltungsbereich untersagt. Produktive Modellartefakte werden im Inferenzbetrieb schreibgeschützt bereitgestellt. Trainingsaufträge und Schnittstellen zur Gewichtsänderung werden weder freigegeben noch durch Dienstrechte ermöglicht. Unvermeidbare Bibliotheksfunktionen werden in der Komponentenprüfung erfasst und dürfen keinen freigegebenen Ausführungspfad erhalten.

**Erforderlicher Nachweis:** Effektive Dateirechte, erreichbare Schnittstellen, Auftragsinventar, Integritätskontrolle und negative Ausführungstests. Das Trainingsverbot selbst wird nicht gelockert.

## P08 Wiederholbare Bewertung bedeutet nicht stets wortgleiche Antworten

**Fundstelle:** S. 44, KI-VAL-001: dokumentierte und wiederholbare Ergebnisse; eine Stichprobe muss mit derselben Konfiguration reproduzierbar sein.

**Kritik:** Ohne Abnahmedefinition kann dies als Zusage identischer Modellantworten verstanden werden. Zufallsparameter, Parallelisierung und numerische Ausführung beeinflussen Ergebnisse. Die PyTorch-Dokumentation beschreibt Grenzen vollständiger Reproduzierbarkeit und die zusätzlichen Voraussetzungen deterministischer Ausführung. [PyTorch, Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)

**Empfohlene Ersatzformulierung:**

> Testverfahren, Modellstand, Laufzeit, Hardware, Parameter und Testdaten werden versioniert. Sicherheitsentscheidungen werden deterministisch geprüft, soweit sie durch klassische Zugriffskontrollen getroffen werden. Für variable Modellantworten werden Wiederholungszahl, Messgrößen und zulässige Schwankungsbereiche vorab festgelegt. Die Freigabe setzt die Einhaltung der definierten Abnahmekriterien voraus.

**Erforderlicher Nachweis:** Wiederholte Messungen mit vorab festgelegten Schwellen. Ein gesetzter Zufallsstartwert allein genügt nicht als Nachweis identischer Ausführung.

## P09 Vollständig lokaler Betrieb ist eine Architekturentscheidung

**Fundstelle:** S. 7–9 und 23, KI-ARC-002: unter anderem lokale Identitäten, Git, Registrierungen, Protokolle, Telemetrie und Sicherungen; keine ausgehende Internetverbindung der KI-Komponenten im Standardbetrieb.

**Kritik:** Das ist technisch erreichbar. Es kann jedoch für ein Unternehmen mit zentralen Cloud-Identitäten, externer Codeverwaltung oder ausgelagerter Sicherheitsüberwachung erhebliche zusätzliche Infrastruktur verlangen. Die Anforderung ist kein allgemeiner Beweis, dass nur vollständig lokale Architekturen sicher betrieben werden können. Sie ist die bewusst gewählte Grenze dieser Referenz und sollte nicht stillschweigend aufgeweicht werden.

**Empfohlene Ersatzformulierung zur Präzisierung der lokalen Variante:**

> Die festgelegte Systemgrenze umfasst die KI-Dienste und ihre im Datenflussmodell bezeichneten Abhängigkeiten. Inferenz und KI-Inhaltsdaten werden ausschließlich innerhalb dieser lokalen Grenze verarbeitet. Abhängigkeiten zu Identität, Codeverwaltung, Überwachung und Sicherung werden je Dienst benannt und auf die freigegebenen Datenflüsse begrenzt. Direkte Internetverbindungen der KI-Komponenten bleiben gesperrt; Aktualisierungen erfolgen über den kontrollierten Importweg.

**Erforderliche Entscheidung:** Welche bestehenden Unternehmensdienste liegen innerhalb der lokalen Grenze? Falls externe Dienste erforderlich sind, muss die Unternehmensfassung als gesonderte Architekturvariante bewertet werden. Eine externe Identitäts- oder Protokollierungsabhängigkeit wird nicht allein durch die Kontrollen zur externen Inferenz abgedeckt.

## P10 Die aktuelle Berechtigung benötigt eine messbare Widerrufsfrist

**Fundstelle:** S. 32, KI-RAG-002: Prüfung „bei jeder Abfrage“ anhand einer maßgeblichen lokalen Quelle; Änderungen und Widerrufe werden „zeitnah“ übernommen.

**Kritik:** „Zeitnah“ lässt bei Verzeichnisreplikation, Sitzungen und Zwischenspeichern keine eindeutige Abnahme zu. Eine Prüfung je Abfrage kann mit einem lokalen Berechtigungsstand erfolgen; der zulässige Verzug zu dessen maßgeblicher Quelle muss feststehen. Die Zugriffstrennung selbst ist erreichbar und darf nicht durch ein allgemeines Bemühen ersetzt werden.

**Empfohlene Ersatzformulierung:**

> Jede Abfrage wird serverseitig gegen einen gültigen Berechtigungsstand geprüft. Für Berechtigungsänderungen, Sitzungen und Zwischenspeicher werden maximale Gültigkeits- und Übernahmefristen entsprechend dem Schutzbedarf festgelegt und überwacht. Bei überschrittener Gültigkeit wird der betroffene Zugriff verweigert. Für kritische Widerrufe besteht ein unmittelbar wirksamer Sperrweg.

**Erforderlicher Nachweis:** Gemessene Übernahmezeiten einschließlich Verzeichnisstörung, laufender Sitzung, Trefferzwischenspeicher und direktem Objektzugriff. Keine pauschale Frist ohne Bezug zur tatsächlichen Architektur festlegen.

## P11 Eine externe Variante wird freigegeben und jede Anfrage dagegen geprüft

**Fundstelle:** S. 50, KI-EXT-001: „vor jeder Datenübertragung eine neue organisationsspezifische Bewertung und Freigabe“.

**Kritik:** Wörtlich gelesen wären Verträge, Anbieterprüfung und Datenschutzbewertung für jede einzelne Anfrage neu durchzuführen. Gemeint sein dürfte eine gültige Variantenfreigabe vor der ersten Übertragung, kombiniert mit technischer Prüfung jeder Anfrage. Im Standardmodell ist diese Kontrolle nicht anwendbar und externe Inferenz bleibt deaktiviert.

**Empfohlene Ersatzformulierung:**

> Vor der ersten Datenübertragung wird die externe Betriebsvariante organisationsspezifisch bewertet und freigegeben. Die Freigabe benennt Anbieter, Endpunkte, Modelle, Datenkategorien, Zwecke und Gültigkeit. Jede Anfrage wird gegen diese Freigabe geprüft. Wesentliche Änderungen oder ihr Ablauf erfordern eine erneute Bewertung; außerhalb einer gültigen Freigabe findet keine Übertragung statt.

**Erforderlicher Nachweis:** Gültige Variantenentscheidung, technische Anfrageprüfung und eindeutig definierte Änderungsanlässe. Rechts- und Vertragsprüfung werden dadurch nicht entbehrlich.

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
