# Bearbeitbare Diagramme

Die sechs Fachdiagramme werden als textbasierte PlantUML-Dateien gepflegt. PlantUML ist für diese Vorlage zweckmäßig, weil die Quellen mit einem Texteditor bearbeitet, versionsgenau verglichen und ohne Cloud-Dienst lokal in SVG und PNG umgewandelt werden können. Das unmittelbar gerenderte PNG wird als feste Inline-Abbildung in das DOCX übernommen; ein Bildschirmfoto mit Browserrahmen oder Skalierungsartefakten ist nicht erforderlich. Das PDF entsteht anschließend ausschließlich aus dem gespeicherten DOCX.

## Dateien und Verwendung

| PlantUML-Quelle | Inhalt | Verwendung im Konzept |
|---|---|---|
| `architektur.puml` | Zonen, Zugang und Vertrauensgrenzen | Abbildung 1 |
| `artefaktimport.puml` | Prüfung, Freigabe und Rückgriff auf eine freigegebene Vorversion | Abbildung 2 |
| `risikobewertung.puml` | Ablauf von Szenario, Bewertung, Behandlung und Restrisiko | Abbildung 3 |
| `risikomatrix.puml` | Eintrittshäufigkeit, Schadenshöhe sowie Ausgangs- und Restrisiken | Abbildung 4 |
| `rag-datenfluss.puml` | Aufnahme, Zugriffsprüfung, Inferenz und Löschung | Abbildung 5 |
| `agentische-werkzeugnutzung.puml` | Richtlinienprüfung, Bestätigung und Prüfprotokoll | Abbildung 6 |

## Fachlicher Darstellungsauftrag

| Abbildung | Aussageauftrag | Datenform und Kodierung | Barrierefreiheit und Qualitätsprüfung |
|---|---|---|---|
| 1 | Erlaubter Zugang und gesperrte Internetverbindung | Zonen und gerichtete Kommunikationsbeziehungen | Zonen sind benannt; Sperre trägt Text und gestrichelte rote Verbindung |
| 2 | Nur geprüfte Artefakte erreichen die Produktion | Entscheidungs- und Freigabeprozess | Ja-/Nein-Pfade sind beschriftet; Rückkehrpfad bleibt ohne Farbe verständlich |
| 3 | Kein Risiko wird ohne Behandlung oder Entscheidung freigegeben | Prozess mit Rückschleife | Schritte sind nummeriert; Entscheidungspfade tragen Text |
| 4 | Maßnahmen senken hohe Ausgangsrisiken auf höchstens mittel | Qualitative Vier-mal-vier-Matrix | Jede Zelle nennt Kategorie und Risikokennungen; Farbe ist nur ergänzend |
| 5 | Wissensaufnahme, berechtigte Abfrage und Löschung sind getrennt | Datenfluss mit Zugriffsentscheidung | Ablehnung und Löschpfad sind beschriftet; Alternativtext nennt alle Stationen |
| 6 | Erhöhte Werkzeugwirkung benötigt konkrete Bestätigung | Entscheidungs- und Wirkungskette | Lesen, erhöhte Wirkung, Freigabe und Abweisung sind als Textpfade erkennbar |

Vor der Übernahme in das DOCX durchläuft jede Abbildung einen lokalen Fachpass: Stimmen Aussage und Leserichtung, sind alle Kennungen auf Text im Konzept zurückführbar, bleiben Beschriftungen bei 100 Prozent lesbar und ist Farbe nicht der einzige Bedeutungsträger? Erst danach werden PNG, SVG und Manifest gemeinsam übernommen.

Die abgeleiteten Dateien liegen unter `dokumentation/medien/`. SVG dient der Darstellung in Markdown. PNG ist die mit 180 dpi erzeugte Word-Eingabe. `diagramm-manifest.json` bindet jede Quelle und beide Ableitungen über SHA-256 aneinander.

## Lokal erzeugen

Voraussetzungen sind Java 17 oder neuer sowie eine geprüfte PlantUML-JAR. Der Hilfsbefehl lädt bei Bedarf die im Skript festgelegte PlantUML-Fassung von der offiziellen GitHub-Veröffentlichung, prüft deren SHA-256 und legt sie ausschließlich im ignorierten Verzeichnis `.arbeitsdaten/werkzeuge/` ab.

```powershell
python validierung/erzeuge_diagramme.py --werkzeug-herunterladen
python validierung/erzeuge_dokumente.py
powershell -NoProfile -ExecutionPolicy Bypass -File validierung/aktualisiere_word_felder.ps1
```

Ist eine geprüfte JAR bereits vorhanden, kann sie ohne Download verwendet werden:

```powershell
python validierung/erzeuge_diagramme.py --plantuml-jar E:\Werkzeuge\plantuml.jar
```

Die Risikomatrix wird beim Erzeugen aus `ki-gov-003-risk-register` und dem festgelegten Bewertungsmaßstab in `erzeuge_diagramme.py` abgeleitet; ihre `.puml`-Datei wird nicht unabhängig redigiert. Alle anderen Diagrammquellen werden direkt gepflegt. Nach jeder Änderung werden die Diagramme vor DOCX und PDF erzeugt. Die strenge Projektvalidierung erkennt nicht aktualisierte Quellen, SVG- oder PNG-Dateien anhand des Manifests.

## Organisationsspezifisch anpassen

Die Anpassung erfolgt nur in der getrennten, angemessen geschützten geschützte Fassung. Dort werden Zonen, Rollen, Kommunikationsbeziehungen und Entscheidungen in den `.puml`-Dateien auf die tatsächliche Architektur abgebildet. Reale Domänen, Hostnamen, IP-Adressen, Konten oder interne Schutzbedarfe dürfen nicht in dieses öffentliche Referenzrepository zurückfließen.

Die Knotennamen hinter `as` bleiben möglichst stabil. Sichtbare Bezeichnungen können direkt zwischen den Anführungszeichen geändert werden. Neue Beziehungen werden erst ergänzt, wenn sie fachlich bewertet und durch eine OSCAL-Kontrolle gedeckt sind. Farbe bleibt ergänzend; Form, Text und Pfeilbeschriftung tragen die eigentliche Aussage.

Weiterführend gelten der [`Leitfaden zur organisationsspezifischen Übernahme`](../dokumentation/ÜBERNAHMELEITFADEN.md) und die verbindlichen [`Layoutregeln`](../dokumentation/LAYOUTREGELN.md).
