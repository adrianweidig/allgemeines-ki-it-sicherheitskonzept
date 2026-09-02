# Verbindliche Layout- und Redaktionsregeln

## Zweck und Geltung

Diese Regeln gelten für das DOCX-Masterdokument und die daraus erzeugte PDF-Lesefassung. Sie verhindern schleichende Abweichungen bei Typografie, Abständen, Tabellen, Silbentrennung, Kopf- und Fußzeilen sowie Listen. Fachliche Inhalte bleiben davon unberührt.

Das Gestaltungsprofil basiert auf `standard_business_brief` und verwendet die benannte Übersteuerung `A4-Behördenreferenz` für Papierformat, Satzspiegel und den 1,15-fachen Grundzeilenabstand des Langdokuments. Die Gestaltung ist neutral und sachlich. Sie verwendet keine Logos, Wappen oder Elemente, die eine amtliche Herausgeberschaft vortäuschen.

## Verbindliche Gestaltungswerte

| Bereich | Festlegung |
|---|---|
| Papier und Satzspiegel | A4 im Hochformat, 25 mm Rand auf allen Seiten, 160 mm nutzbare Breite |
| Grundschrift | Calibri, 11 pt, linksbündig, 1,15-facher Zeilenabstand, 6 pt Abstand nach dem Absatz |
| Überschrift 1 | 16 pt, dunkelblau, 16 pt davor, 8 pt danach, Beginn auf neuer Seite |
| Überschrift 2 | 13 pt, blau, 12 pt davor, 6 pt danach |
| Überschrift 3 | 12 pt, dunkelblau, 8 pt davor, 4 pt danach |
| Aufzählungen | Echte Word-Listen, 12,7 mm Texteinzug, 6,35 mm hängender Einzug, 5 pt Abstand danach |
| Tabellenbreite | 8.922 DXA bei 150 DXA Einzug innerhalb des 9.072-DXA-Satzspiegels |
| Tabellenzellen | Calibri 10,5 pt, 1,10-facher Zeilenabstand, mindestens 120 DXA oben und unten sowie 150 DXA links und rechts |
| Tabellenköpfe | Fett, dezente blaugraue Fläche, horizontal und vertikal zentriert, auf Folgeseiten wiederholt |
| Tabellenkörper | Vertikal zentriert, Textspalten linksbündig, kurze Kennungs- und Statusspalten gezielt zentriert |
| Fußnoten | Calibri 8,5 pt, 1,05-facher Zeilenabstand, 2 pt Abstand danach |
| Seitenführung | Schutzstatus kurz links, `Seite X von Y` rechts, getrennt durch einen Tabstopp und eine dezente obere Linie |
| Silbentrennung | Automatisch, Sprache `de-DE`, Trennzone 360 DXA, höchstens zwei aufeinanderfolgende Trennzeilen |

Die numerischen Werte werden im Dokumentgenerator gesetzt und in der Projektvalidierung gegen das erzeugte OOXML geprüft. Word-Vorgaben, automatische Tabellenbreiten und direkt gesetzte Einzelabweichungen sind nicht zulässig.

## Regelkatalog

### LAY-TYP-001 – Formatvorlagen statt Einzelformatierung

Fließtext, Überschriften, Listen, Tabelleninhalt, Tabellenköpfe, Beschriftungen, Kopfzeilen, Fußzeilen und Fußnoten verwenden festgelegte Formatvorlagen. Abstände werden am Absatz und nicht durch Leerzeilen erzeugt. Überschriften bleiben mit dem folgenden Absatz verbunden. Die Absatzkontrolle gegen einzelne Anfangs- und Schlusszeilen bleibt aktiv.

### LAY-TYP-002 – Ruhiger Absatzrhythmus

Fließtext verwendet durchgängig 1,15-fachen Zeilenabstand und 6 pt Abstand danach. Tabellen und Fußnoten besitzen eigene, konsistente Werte. Abweichungen benötigen einen benannten, wiederverwendbaren Stil und eine Begründung in dieser Datei.

### LAY-LST-001 – Keine Strichpunkte als Listenabschluss

Listenpunkte werden als kurze vollständige Sätze mit Großbuchstaben und Punkt formuliert. Alternativ dürfen echte Satzfragmente nach einem einleitenden Satz ohne Schlusszeichen stehen. Ein Strichpunkt am Ende eines Listenpunkts ist unzulässig. Abläufe verwenden echte nummerierte Word-Listen und keine manuell eingetippten Ziffern oder Aufzählungszeichen.

Die Regel folgt der amtlichen redaktionellen Praxis, Listen konsistent zu behandeln und Strichpunkte am Zeilenende zu vermeiden. Die konkrete Projektausprägung verwendet vollständige Sätze mit Punkt.

### LAY-TAB-001 – Tabellen nur für vergleichbare Daten

Tabellen werden nur verwendet, wenn Zeilen und Spalten eine echte fachliche Beziehung bilden. Längere Erläuterungen bleiben Fließtext oder strukturierte Abschnitte. Layouttabellen sind nicht zulässig.

### LAY-TAB-002 – Feste und nachweisbare Geometrie

Jede Tabelle verwendet feste DXA-Werte. Tabellenbreite, Einzug, Spaltenraster und jede Zellenbreite müssen rechnerisch übereinstimmen. Automatische Größenanpassung, Prozentbreiten und feste Zeilenhöhen sind unzulässig. Zeilen dürfen bei ausreichendem Platz nicht auseinandergerissen werden.

### LAY-TAB-003 – Lesbare Zellen

Zellränder, Zeilenabstand und Spaltenbreiten werden vor einer Schriftverkleinerung angepasst. Tabellenköpfe sind semantisch als Kopfzeilen markiert und werden bei automatischen Seitenumbrüchen wiederholt. Narrative Spalten sind linksbündig. Kurze Kennungen, Statusangaben und vergleichbare Werte dürfen zentriert werden. Die vertikale Ausrichtung ist einheitlich zentriert.

### LAY-SIL-001 – Deutsche Silbentrennung

Das Dokument aktiviert automatische Silbentrennung und weist `de-DE` als Korrektursprache aus. Höchstens zwei aufeinanderfolgende Zeilen dürfen mit einer Trennung enden. Eigennamen, Kennungen und technisch gebundene Ausdrücke werden bei auffälliger Trennung im Seitenbild geprüft und bei Bedarf mit einem geschützten Bindestrich, einer engeren lokalen Formulierung oder einer absatzbezogenen Trennausnahme stabilisiert. Quellen- und URL-Absätze unterdrücken die automatische Trennung, weil sie regelmäßig mehrere Sprachräume und technisch gebundene Zeichenfolgen enthalten.

### LAY-SEI-001 – Unaufdringliche Seitenzahlen

Die Seitenzahl steht nicht in einer langen zentrierten Textzeile. Ab Seite 2 führt die Fußzeile links nur den kurzen Schutzstatus und rechts `Seite X von Y`. Beide Zahlen sind echte Word-Felder. Deckblatt und Dokumentenlenkung enthalten weiterhin die vollständige Schutzkennzeichnung.

### LAY-QA-001 – Strukturprüfung

Die Projektvalidierung prüft mindestens die Seitengröße, Ränder, Grundschrift, Absatzabstand, Silbentrennung, Dokumentsprache, echte Listen, Listeninterpunktion, Tabellenbreite, Spaltenraster, Zellränder, wiederholte Kopfzeilen, fehlende feste Zeilenhöhen sowie PAGE- und NUMPAGES-Felder.

### LAY-QA-002 – Vollständige Sichtprüfung

Nach jeder layoutwirksamen Änderung werden DOCX und PDF neu erzeugt. Jede PDF-Seite wird bei 100 Prozent geprüft. Die Prüfung umfasst abgeschnittene oder überlagerte Inhalte, falsche Trennungen, unruhige Umbrüche, zu dichte Tabellen, unpassende Ausrichtungen, verwaiste Überschriften, Fußnoten, Kopf- und Fußzeilen sowie die fortlaufende Seitenführung. Eine reine Text- oder XML-Prüfung ersetzt diesen Schritt nicht.

## Herleitung aus öffentlichen Best Practices

Die folgenden Quellen wurden am 02.09.2026 geprüft:

- Microsoft: [Ändern des Zeilen- und Absatzabstands in Word](https://support.microsoft.com/de-de/word/change-the-line-spacing-in-word). Microsoft empfiehlt die zentrale Steuerung über Absatz- und Formatvorlageneinstellungen. Daraus werden die festen Stilwerte und das Verbot manueller Leerzeilen abgeleitet.
- Microsoft: [Steuern der Silbentrennung](https://support.microsoft.com/de-DE/Word/control-hyphenation). Die Quelle beschreibt automatische Silbentrennung, Trennzone, Begrenzung aufeinanderfolgender Trennungen und geschützte Bindestriche.
- Microsoft: [Ändern der Größe einer Tabelle, Spalte oder Zeile](https://support.microsoft.com/de-DE/Word/resize-a-table-column-or-row). Die Quelle weist auf bewusste Spaltenbreiten und einstellbare Zellränder hin.
- Microsoft: [Tabellenkopf auf nachfolgenden Seiten wiederholen](https://support.microsoft.com/de-DE/Word/repeat-table-header-on-subsequent-pages). Daraus folgt die verpflichtende Wiederholungskennzeichnung der ersten Tabellenzeile.
- Microsoft: [Hinzufügen von Seitenzahlen zu einer Kopf- oder Fußzeile in Word](https://support.microsoft.com/de-DE/Word/add-page-numbers-to-a-header-or-footer-in-word). Die Quelle beschreibt frei wählbare Ausrichtung sowie die Darstellung `Seite X von Y`.
- Überwachungsstelle des Bundes für Barrierefreiheit von Informationstechnik: [Hinweise zur Gestaltung von Tabellen](https://handreichungen.bfit-bund.de/bf-dokumente-lernkontext/1.4/tabellen.html). Die Handreichung fordert geeignete semantische Tabellenstrukturen und eine logische Lesereihenfolge.
- W3C Web Accessibility Initiative: [Tables Tutorial](https://www.w3.org/WAI/tutorials/tables/). Die Quelle unterscheidet Datentabellen von Layoutzwecken und betont korrekt ausgezeichnete Kopf- und Datenzellen.
- W3C Web Accessibility Initiative: [Designing for Web Accessibility](https://www.w3.org/WAI/tips/designing/). Die Quelle empfiehlt, Überschriften, Weißraum und Nähe zur erkennbaren Gruppierung einzusetzen sowie Textgröße und Zeilenlänge auf Lesbarkeit auszurichten.
- Office for National Statistics: [Bullet points and numbered lists](https://service-manual.ons.gov.uk/content/formatting-and-punctuation/lists). Der amtliche Stilhinweis verlangt eine konsistente Listenform und sieht keine Strichpunkte am Ende einzelner Listenpunkte vor.

[WCAG 2.2, Erfolgskriterium 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing) nennt größere benutzerseitige Textabstände als Robustheitsprüfung. Diese Werte sind keine Vorgabe für die Standarddarstellung. Das Projekt prüft deshalb, dass zusätzliche Abstände keine Inhalte abschneiden oder Tabellen überlagern, ohne die dort genannten Maximalwerte als Grundlayout auszugeben.

## Änderungsverfahren

Eine Änderung an einem Gestaltungswert erfordert gleichzeitig:

1. eine nachvollziehbare Änderung dieser Regeln
2. die entsprechende Generatoränderung
3. eine angepasste maschinenlesbare Prüfung
4. einen passenden positiven oder negativen Test
5. eine vollständige Neuerzeugung und Sichtprüfung aller Seiten

Eine Dokumentdatei darf nicht manuell so verändert werden, dass sie vom Generator abweicht.
