# Verbindliche Layout- und Redaktionsregeln

## Zweck und Geltung

Diese Regeln gelten für das DOCX-Masterdokument und die daraus erzeugte PDF-Lesefassung. Sie verhindern schleichende Abweichungen bei Typografie, Abständen, Tabellen, Diagrammen, Silbentrennung, Kopf- und Fußzeilen sowie Listen. Fachliche Inhalte bleiben davon unberührt.

Das Gestaltungsprofil basiert auf `standard_business_brief` und verwendet die benannte Übersteuerung `A4-Behördenreferenz` für Papierformat, Satzspiegel und den 1,15-fachen Grundzeilenabstand des Langdokuments. Die Gestaltung ist neutral und sachlich. Sie verwendet keine Logos, Wappen oder Elemente, die eine amtliche Herausgeberschaft vortäuschen.

## Verbindliche Gestaltungswerte

| Bereich | Festlegung |
|---|---|
| Papier und Satzspiegel | A4 im Hochformat, 25 mm Rand auf allen Seiten, 160 mm nutzbare Breite |
| Grundschrift | Calibri, 11 pt, 1,15-facher Zeilenabstand, 6 pt Abstand nach dem Absatz |
| Fließtext | Blocksatz mit automatischer deutscher Silbentrennung; nicht für Listen, Tabellen, Quellen, Beschriftungen oder kurze Hinweise |
| Begriffsdefinitionen | Calibri 10,5 pt, linksbündig, 1,05-facher Zeilenabstand, 3 pt Abstand danach |
| Überschrift 1 | 16 pt, dunkelblau, 16 pt davor, 8 pt danach, Beginn auf neuer Seite |
| Überschrift 2 | 13 pt, blau, 12 pt davor, 6 pt danach |
| Überschrift 3 | 12 pt, dunkelblau, 8 pt davor, 4 pt danach |
| Inhaltsverzeichnis | Automatisches Word-Feld, Ebenen 1 und 2, rechtsbündige Seitenzahlen, Punkt-Füllzeichen, eigene Formatvorlagen `TOC 1` und `TOC 2` |
| Aufzählungen | Echte Word-Listen, 12,7 mm Texteinzug, 6,35 mm hängender Einzug, 5 pt Abstand danach |
| Tabellenbreite | 8.922 DXA bei 150 DXA Einzug innerhalb des 9.072-DXA-Satzspiegels |
| Tabellenzellen | Calibri 10,5 pt, 1,10-facher Zeilenabstand, mindestens 120 DXA oben und unten sowie 150 DXA links und rechts |
| Tabellenköpfe | Fett, dezente blaugraue Fläche, horizontal und vertikal zentriert, auf Folgeseiten wiederholt |
| Tabellenkörper | Vertikal zentriert, Textspalten linksbündig, kurze Kennungs- und Statusspalten gezielt zentriert |
| Fußnoten | Calibri 8,5 pt, 1,05-facher Zeilenabstand, 2 pt Abstand danach |
| Seitenführung | Schutzstatus kurz links, `Seite X von Y` rechts, getrennt durch einen Tabstopp und eine dezente obere Linie |
| Silbentrennung | Automatisch, Sprache `de-DE`, höchstens zwei aufeinanderfolgende Trennzeilen; Zielwert der Trennzone 360 DXA |
| Abbildungen | Inline im Textfluss, höchstens 160 mm breit, aussagekräftiger Alternativtext und direkt folgende linksbündige Beschriftung |

Die numerischen Werte werden im Dokumentgenerator gesetzt und in der Projektvalidierung gegen das erzeugte OOXML geprüft. Word-Vorgaben, automatische Tabellenbreiten und direkt gesetzte Einzelabweichungen sind nicht zulässig.

## Regelkatalog

### LAY-TYP-001 – Formatvorlagen statt Einzelformatierung

Fließtext, Überschriften, Listen, Tabelleninhalt, Tabellenköpfe, Beschriftungen, Kopfzeilen, Fußzeilen und Fußnoten verwenden festgelegte Formatvorlagen. Abstände werden am Absatz und nicht durch Leerzeilen erzeugt. Überschriften bleiben mit dem folgenden Absatz verbunden. Die Absatzkontrolle gegen einzelne Anfangs- und Schlusszeilen bleibt aktiv.

### LAY-TYP-002 – Ruhiger Absatzrhythmus

Fließtext verwendet durchgängig 1,15-fachen Zeilenabstand und 6 pt Abstand danach. Tabellen und Fußnoten besitzen eigene, konsistente Werte. Abweichungen benötigen einen benannten, wiederverwendbaren Stil und eine Begründung in dieser Datei.

### LAY-TYP-003 – Selektiver Blocksatz

Zusammenhängende narrative Absätze und die Erläuterungstexte der Kontrollen verwenden die Formatvorlage `Fließtext` mit Blocksatz und automatischer deutscher Silbentrennung. Tabellenzellen, Listen, Quellenangaben, Bild- und Tabellenbeschriftungen, Überschriften, Kopf- und Fußzeilen sowie kurze Statushinweise bleiben linksbündig oder erhalten ihre ausdrücklich festgelegte Ausrichtung.

Blocksatz wird nicht in schmalen Spalten erzwungen. Die selektive Regel vermeidet große Wortabstände und berücksichtigt, dass durchgehend erzwungener Blocksatz die Lesbarkeit insbesondere für Menschen mit Dyslexie erschweren kann. Sichtprüfungen achten deshalb zusätzlich auf auffällige Weißräume, Trennhäufungen und einzelne überdehnte Zeilen.

### LAY-TYP-004 – Geschlossene Begriffsübersicht

Kurze Definitionen verwenden die eigene Formatvorlage `Begriffsdefinition` mit Calibri 10,5 pt, linksbündiger Ausrichtung, 1,05-fachem Zeilenabstand und 3 pt Absatzabstand. Die kompakte, aber gut lesbare Gestaltung verhindert überdehnte Wortabstände und eine fast leere Fortsetzungsseite. Kapitel 2.1 enthält genau die vor der ersten technischen Verwendung benötigten fünfzehn Begriffe.

### LAY-TOC-001 – Automatisches und ruhiges Inhaltsverzeichnis

Das Inhaltsverzeichnis ist ein echtes Word-Feld und übernimmt ausschließlich die Überschriftsebenen 1 und 2. Kapitelnummer, Titel und Seitenzahl bilden eine Zeile. Die Seitenzahlen stehen an einem gemeinsamen rechten Tabstopp; Punkt-Füllzeichen führen das Auge über die Zeile. Ebene 2 wird maßvoll eingerückt und typografisch gegenüber Ebene 1 zurückgenommen. Dokumentenlenkung und die Überschrift `Inhaltsverzeichnis` verwenden einen Vorspannstil und dürfen nicht als eigene Einträge erscheinen.

Vor jeder Veröffentlichung werden das Feld und seine Seitenzahlen in Word aktualisiert. Dabei werden die sprachunabhängigen integrierten Word-Stile `TOC 1` und `TOC 2` formatiert, auch wenn Word sie in der Benutzeroberfläche lokalisiert benennt. Das DOCX wird danach gespeichert und erst aus dieser gespeicherten Fassung wird das PDF erzeugt. Ein manuell geschriebenes Inhaltsverzeichnis, ein veralteter Feldinhalt oder ein Platzhalter ist unzulässig.

### LAY-LST-001 – Keine Strichpunkte als Listenabschluss

Listenpunkte werden als kurze vollständige Sätze mit Großbuchstaben und Punkt formuliert. Alternativ dürfen echte Satzfragmente nach einem einleitenden Satz ohne Schlusszeichen stehen. Ein Strichpunkt am Ende eines Listenpunkts ist unzulässig. Abläufe verwenden echte nummerierte Word-Listen und keine manuell eingetippten Ziffern oder Aufzählungszeichen.

Die Regel folgt der amtlichen redaktionellen Praxis, Listen konsistent zu behandeln und Strichpunkte am Zeilenende zu vermeiden. Die konkrete Projektausprägung verwendet vollständige Sätze mit Punkt.

### LAY-TAB-001 – Tabellen nur für vergleichbare Daten

Tabellen werden nur verwendet, wenn Zeilen und Spalten eine echte fachliche Beziehung bilden. Längere Erläuterungen bleiben Fließtext oder strukturierte Abschnitte. Layouttabellen sind nicht zulässig. Ein Absatz direkt nach einer Tabelle darf nicht lediglich Aufbau oder Inhalt der Tabelle wiederholen. Fachlich notwendige Folgeregeln erhalten eine eigene Zwischenüberschrift oder stehen vor der Tabelle.

### LAY-TAB-002 – Feste und nachweisbare Geometrie

Jede Tabelle verwendet feste DXA-Werte. Tabellenbreite, Einzug, Spaltenraster und jede Zellenbreite müssen rechnerisch übereinstimmen. Automatische Größenanpassung, Prozentbreiten und feste Zeilenhöhen sind unzulässig. Zeilen dürfen bei ausreichendem Platz nicht auseinandergerissen werden.

### LAY-TAB-003 – Lesbare Zellen

Zellränder, Zeilenabstand und Spaltenbreiten werden vor einer Schriftverkleinerung angepasst. Tabellenköpfe sind semantisch als Kopfzeilen markiert und werden bei automatischen Seitenumbrüchen wiederholt. Narrative Spalten sind linksbündig. Kurze Kennungen, Statusangaben und vergleichbare Werte dürfen zentriert werden. Die vertikale Ausrichtung ist einheitlich zentriert.

### LAY-TAB-004 – Keine schwach gefüllten Fortsetzungsseiten

Kurze Verzeichnisse und Tabellen am Dokumentende werden so angeordnet, dass keine Fortsetzungsseite mit nur wenigen Restzeilen entsteht. Das Abkürzungsverzeichnis verwendet deshalb zwei Begriffspaare je Tabellenzeile. Beide Langformspalten behalten ausreichende Breite und die allgemeinen Zellränder. Die Validierung prüft diese Vier-Spalten-Struktur und begrenzt ihre Zeilenzahl.

### LAY-ABB-001 – Diagramm statt Layouttabelle

Vertrauenszonen, Kommunikationsbeziehungen, Prozessfolgen und Entscheidungswege werden als Diagramm dargestellt, wenn eine Tabelle nur der räumlichen Anordnung dienen würde. Tabellen bleiben echten Vergleichs- und Matrixdaten vorbehalten. Pfeile oder künstliche Spalten in Tabellen dürfen keine Architektur oder Prozesskette nachbilden.

### LAY-ABB-002 – Reproduzierbare und barrierearme Abbildungen

Jede Diagrammquelle wird als versionierbare PlantUML-Datei unter `diagramme/` gepflegt. Daraus werden lokal ein SVG für Markdown und ein PNG mit 180 dpi für das DOCX erzeugt. Die im Diagrammmanifest registrierten SHA-256-Prüfsummen verbinden Quelle und beide Ableitungen. Abbildungen stehen ausschließlich inline im Textfluss, werden im vorhergehenden Text erläutert und erhalten unmittelbar danach eine nummerierte Beschriftung. Das DOCX enthält für jede Abbildung einen vollständigen Alternativtext.

Farbe ist nie der einzige Bedeutungsträger. Beschriftungen und Formen müssen die Aussage auch in Graustufen erkennen lassen. Überbreite oder gedrehte Diagramme sind unzulässig. Schrift, Linien und Entscheidungspfade müssen bei 100 Prozent in der PDF-Lesefassung ohne Vergrößerung erkennbar sein. Inline-Diagramme werden proportional auf höchstens 20,5 cm Höhe begrenzt und mit ihrer unmittelbar folgenden Beschriftung zusammengehalten; Tabellenköpfe bleiben beim ersten Datenabschnitt.

Die Word-Abbildung wird nicht mit Zeichenformen nachgebaut. Der Generator übernimmt ausschließlich die aus PlantUML erzeugte PNG-Datei als feste Inline-Abbildung. Damit bleiben Layout und Aussage zwischen Bearbeitungsquelle, DOCX und PDF reproduzierbar. Eine Bildschirmaufnahme ist nur zulässig, wenn sie dieselbe geprüfte PlantUML-Darstellung ohne Browserrahmen, Skalierungsartefakte oder zusätzliche Inhalte wiedergibt.

### LAY-ABB-003 – Inhaltliche Begrenzung

Diagramme zeigen nur Beziehungen, die im Konzept erläutert und durch OSCAL-Kontrollen gedeckt sind. Sie enthalten keine realen Organisationsbezeichnungen, Hostnamen, IP-Adressen, Konten oder Zugangsdaten. Produktlogos und amtliche Gestaltungselemente werden nicht verwendet.

### LAY-ABB-004 – Nachvollziehbare Risikodarstellung

Risiken werden nach BSI-Standard 200-3 als Szenarien beschrieben und über Eintrittshäufigkeit und Schadenshöhe qualitativ eingestuft. Eine Prozessgrafik zeigt Gefährdungsübersicht, Risikoeinschätzung, Risikobewertung, Behandlung und erneute Bewertung des Restrisikos. Eine Risikomatrix zeigt die Kategorien `gering`, `mittel`, `hoch` und `sehr hoch`. Ausgangs- und Restrisiken erhalten stabile Risikokennungen und werden zusätzlich zur Farbe direkt in den Matrixzellen bezeichnet.

Die Risikomatrix darf nicht dekorativ oder rein numerisch sein. Jede Position muss auf ein Risikoszenario im Register zurückführbar sein. Hohe und sehr hohe Risiken werden als Freigabesperre erkennbar behandelt. Farbflächen bleiben auch in Graustufen durch Text, Kennung und Zellenposition verständlich.

### LAY-RED-001 – Sicherheitskonzept statt Redaktionsanleitung

Das Sicherheitskonzept beschreibt Geltungsbereich, Sollzustand, Risiken, Maßnahmen, Zuständigkeiten, Prüfungen und Nachweise. Erläuterungen zur Dokumenterzeugung, zum Aufbau der Vorlage, zur Anpassung des Repositorys oder zur Funktion des Quellenregisters gehören in README, Layoutregeln oder Übernahmeleitfaden. Pauschale Haftungs- und Beratungsausschlüsse sowie Sätze wie `Die Matrix ist ein Prüfungseinstieg` sind im Fachkonzept unzulässig.

### LAY-RED-002 – Verständliche Fachsprache

Bekannte deutsche Begriffe haben Vorrang vor unnötigem englischem oder fachsprachlichem Jargon. Beispielsweise werden `Herkunftsnachweis` statt `Provenienz`, `gezielte Manipulation von Modellen oder Wissensquellen` statt `Poisoning`, `Wiederholungsprüfung` statt `Regression`, `Rückkehr zur freigegebenen Vorversion` statt `Rollback`, `Nachweis` statt `Evidenz` und `Überprüfung` statt `Review` verwendet. `Bedarfsgesteuerte Dateiübernahme` ersetzt `On-Demand-Upload`; `automatische Ausweichverbindung` ersetzt `Fallback`. Unvermeidbare Abkürzungen und Fachbegriffe werden vor ihrer ersten inhaltlichen Verwendung knapp und eindeutig erklärt.

### LAY-RED-003 – Inhalt vor Dokumentmechanik

Einleitende Absätze benennen die fachliche Festlegung oder Entscheidung. Sie erklären nicht, dass eine folgende Tabelle eine Übersicht sei, eine Abbildung etwas zeige oder der vollständige Wortlaut an anderer Stelle stehe. Querverweise auf Tabellen und Abbildungen werden in eine inhaltliche Aussage eingebettet. Quellenangaben bleiben davon unberührt.

### LAY-SIL-001 – Deutsche Silbentrennung

Das Dokument aktiviert automatische Silbentrennung und weist `de-DE` als Korrektursprache aus. Höchstens zwei aufeinanderfolgende Zeilen dürfen mit einer Trennung enden; für die Trennzone gilt 360 DXA als Zielwert. Microsoft Word darf diesen Wert beim Speichern in eine gleichwertige Anwendungseinstellung normalisieren. Eigennamen, Kennungen und technisch gebundene Ausdrücke werden bei auffälliger Trennung im Seitenbild geprüft und bei Bedarf mit einem geschützten Bindestrich, einer engeren lokalen Formulierung oder einer absatzbezogenen Trennausnahme stabilisiert. Quellen- und URL-Absätze unterdrücken die automatische Trennung, weil sie regelmäßig mehrere Sprachräume und technisch gebundene Zeichenfolgen enthalten.

### LAY-SEI-001 – Unaufdringliche Seitenzahlen

Die Seitenzahl steht nicht in einer langen zentrierten Textzeile. Ab Seite 2 führt die Fußzeile links nur den kurzen Schutzstatus und rechts `Seite X von Y`. Beide Zahlen sind echte Word-Felder. Deckblatt und Dokumentenlenkung enthalten weiterhin die vollständige Schutzkennzeichnung.

### LAY-QA-001 – Strukturprüfung

Die Projektvalidierung prüft mindestens die Seitengröße, Ränder, Grundschrift, selektiven Blocksatz, den kompakten Definitionsstil, Absatzabstand, Silbentrennung, Dokumentsprache, echte Listen, Listeninterpunktion, Tabellenbreite, Spaltenraster, Zellränder, wiederholte Kopfzeilen, fehlende feste Zeilenhöhen, eine kompakte Abkürzungstabelle, Inline-Abbildungen, Alternativtexte, Bildbeschriftungen, das aktualisierte Inhaltsverzeichnis sowie PAGE- und NUMPAGES-Felder. Zusätzlich werden verbotene Redaktionspassagen, vermeidbarer Fachjargon und der vollständige Risikobestand geprüft.

### LAY-QA-002 – Vollständige Sichtprüfung

Nach jeder layoutwirksamen Änderung werden DOCX und PDF neu erzeugt. Jede PDF-Seite wird bei 100 Prozent geprüft. Die Prüfung umfasst abgeschnittene oder überlagerte Inhalte, falsche Trennungen, unruhige Umbrüche, zu dichte Tabellen, unpassende Ausrichtungen, verwaiste Überschriften, Fußnoten, Kopf- und Fußzeilen sowie die fortlaufende Seitenführung. Eine reine Text- oder XML-Prüfung ersetzt diesen Schritt nicht.

## Herleitung aus öffentlichen Best Practices

Die folgenden Quellen wurden am 02. und 03.09.2026 geprüft:

- Microsoft: [Ändern des Zeilen- und Absatzabstands in Word](https://support.microsoft.com/de-de/word/change-the-line-spacing-in-word). Microsoft empfiehlt die zentrale Steuerung über Absatz- und Formatvorlageneinstellungen. Daraus werden die festen Stilwerte und das Verbot manueller Leerzeilen abgeleitet.
- Microsoft: [Ausrichten oder Setzen von Text im Blocksatz in Word](https://support.microsoft.com/en-us/word/align-or-justify-text-in-word). Die Quelle beschreibt Blocksatz als gleichmäßige Ausrichtung an beiden Rändern. Das Projekt wendet ihn nur auf zusammenhängenden Fließtext an.
- Microsoft: [Word mit einer Bildschirmsprachausgabe verwenden](https://support.microsoft.com/en-us/accessibility/word/use-a-screen-reader-to-align-text-and-paragraphs-in-word). Der Barrierefreiheitshinweis nennt mögliche Schwierigkeiten von Blocksatz für Menschen mit Dyslexie. Daraus folgt die selektive statt flächendeckende Anwendung.
- Microsoft: [Steuern der Silbentrennung](https://support.microsoft.com/de-DE/Word/control-hyphenation). Die Quelle beschreibt automatische Silbentrennung, Trennzone, Begrenzung aufeinanderfolgender Trennungen und geschützte Bindestriche.
- Microsoft: [Ändern der Größe einer Tabelle, Spalte oder Zeile](https://support.microsoft.com/de-DE/Word/resize-a-table-column-or-row). Die Quelle weist auf bewusste Spaltenbreiten und einstellbare Zellränder hin.
- Microsoft: [Tabellenkopf auf nachfolgenden Seiten wiederholen](https://support.microsoft.com/de-DE/Word/repeat-table-header-on-subsequent-pages). Daraus folgt die verpflichtende Wiederholungskennzeichnung der ersten Tabellenzeile.
- Microsoft: [Hinzufügen von Seitenzahlen zu einer Kopf- oder Fußzeile in Word](https://support.microsoft.com/de-DE/Word/add-page-numbers-to-a-header-or-footer-in-word). Die Quelle beschreibt frei wählbare Ausrichtung sowie die Darstellung `Seite X von Y`.
- Microsoft: [Formatieren oder Anpassen eines Inhaltsverzeichnisses in Word](https://support.microsoft.com/de-DE/Word/format-or-customize-a-table-of-contents-in-word). Die Quelle beschreibt angezeigte und rechtsbündig ausgerichtete Seitenzahlen, Füllzeichen, Überschriftsebenen und eigene Formatvorlagen für die Verzeichnisebenen.
- Überwachungsstelle des Bundes für Barrierefreiheit von Informationstechnik: [Hinweise zur Gestaltung von Tabellen](https://handreichungen.bfit-bund.de/bf-dokumente-lernkontext/1.4/tabellen.html). Die Handreichung fordert geeignete semantische Tabellenstrukturen und eine logische Lesereihenfolge.
- W3C Web Accessibility Initiative: [Tables Tutorial](https://www.w3.org/WAI/tutorials/tables/). Die Quelle unterscheidet Datentabellen von Layoutzwecken und betont korrekt ausgezeichnete Kopf- und Datenzellen.
- W3C Web Accessibility Initiative: [Images Tutorial](https://www.w3.org/WAI/tutorials/images/). Die Quelle fordert, Zweck und Komplexität einer Abbildung bei der textlichen Alternative zu berücksichtigen. Daraus folgen Alternativtext, Beschriftung und erläuternder Kontext für jedes Diagramm.
- PlantUML: [Command-line usage](https://plantuml.com/command-line), abgerufen und inhaltlich geprüft am 03.09.2026. Die offizielle Dokumentation beschreibt die lokale Erzeugung von PNG und anderen Ausgabeformaten aus einer Textquelle.
- PlantUML: [Release v1.2026.6](https://github.com/plantuml/plantuml/releases/tag/v1.2026.6), veröffentlicht am 08.06.2026, abgerufen und inhaltlich geprüft am 03.09.2026. Diese Fassung und die veröffentlichte SHA-256-Prüfsumme sind im Erzeugungsskript festgelegt.
- W3C Web Accessibility Initiative: [Designing for Web Accessibility](https://www.w3.org/WAI/tips/designing/). Die Quelle empfiehlt, Überschriften, Weißraum und Nähe zur erkennbaren Gruppierung einzusetzen sowie Textgröße und Zeilenlänge auf Lesbarkeit auszurichten.
- Office for National Statistics: [Bullet points and numbered lists](https://service-manual.ons.gov.uk/content/formatting-and-punctuation/lists). Der amtliche Stilhinweis verlangt eine konsistente Listenform und sieht keine Strichpunkte am Ende einzelner Listenpunkte vor.
- Bundesamt für Sicherheit in der Informationstechnik: [BSI-Standard 200-2: IT-Grundschutz-Methodik](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/BSI_Standards/standard_200_2.pdf?__blob=publicationFile&v=2), Version 1.0, Oktober 2017, abgerufen am 03.09.2026. Die Seiten 69 bis 74 und 154 bis 156 begründen die Verbindung von Strukturanalyse, Schutzbedarf, Sicherheitsprüfung, Risikoanalyse und Sicherheitskonzept.
- Bundesamt für Sicherheit in der Informationstechnik: [BSI-Standard 200-3: Risikomanagement](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/BSI_Standards/standard_200_3.pdf?__blob=publicationFile&v=2), Version 1.0, Oktober 2017, abgerufen am 03.09.2026. Die Seiten 5 bis 7, 26 bis 28 und 33 bis 35 begründen den Risikoablauf, die qualitative Matrix, Behandlungsoptionen und das erneut bewertete Restrisiko.
- DigitalService des Bundes: [Jeder Satz muss sitzen – wie Verwaltungsservices verständlich werden](https://digitalservice.bund.de/blog/jeder-satz-muss-sitzen-wie-verwaltungsservices-verstaendlich-werden), veröffentlicht am 26.02.2026, abgerufen am 03.09.2026. Daraus folgen kurze logisch aufgebaute Sätze, aktive Verben sowie das Vermeiden oder direkte Erklären von Fachbegriffen.

[WCAG 2.2, Erfolgskriterium 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing) nennt größere benutzerseitige Textabstände als Robustheitsprüfung. Diese Werte sind keine Vorgabe für die Standarddarstellung. Das Projekt prüft deshalb, dass zusätzliche Abstände keine Inhalte abschneiden oder Tabellen überlagern, ohne die dort genannten Maximalwerte als Grundlayout auszugeben.

## Änderungsverfahren

Eine Änderung an einem Gestaltungswert erfordert gleichzeitig:

1. eine nachvollziehbare Änderung dieser Regeln
2. die entsprechende Generatoränderung
3. eine angepasste maschinenlesbare Prüfung
4. einen passenden positiven oder negativen Test
5. eine vollständige Neuerzeugung und Sichtprüfung aller Seiten

Eine Dokumentdatei darf nicht manuell so verändert werden, dass sie vom Generator abweicht.
