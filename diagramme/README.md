# Bearbeitbare Diagramme

Die vier Fachdiagramme werden als textbasierte PlantUML-Dateien gepflegt. PlantUML ist für diese Vorlage zweckmäßig, weil die Quellen mit einem Texteditor bearbeitet, versionsgenau verglichen und ohne Cloud-Dienst lokal in SVG und PNG umgewandelt werden können. Das PNG wird als feste Inline-Abbildung in das DOCX übernommen; das PDF entsteht anschließend ausschließlich aus dem DOCX.

## Dateien und Verwendung

| PlantUML-Quelle | Inhalt | Verwendung im Konzept |
|---|---|---|
| `architektur.puml` | Zonen, Zugang und Vertrauensgrenzen | Abbildung 1 |
| `artefaktimport.puml` | Prüfung, Freigabe und Rückgriff auf eine freigegebene Vorversion | Abbildung 2 |
| `rag-datenfluss.puml` | Aufnahme, ACL-Prüfung, Inferenz und Löschung | Abbildung 3 |
| `agentische-werkzeugnutzung.puml` | Richtlinienprüfung, Bestätigung und Auditspur | Abbildung 4 |

Die abgeleiteten Dateien liegen unter `dokumentation/medien/`. SVG dient der Darstellung in Markdown. PNG ist die mit 180 dpi erzeugte Word-Eingabe. `diagramm-manifest.json` bindet jede Quelle und beide Ableitungen über SHA-256 aneinander.

## Lokal erzeugen

Voraussetzungen sind Java 17 oder neuer sowie eine geprüfte PlantUML-JAR. Der Hilfsbefehl lädt bei Bedarf die im Skript festgelegte PlantUML-Fassung von der offiziellen GitHub-Veröffentlichung, prüft deren SHA-256 und legt sie ausschließlich im ignorierten Verzeichnis `.arbeitsdaten/werkzeuge/` ab.

```powershell
python validierung/erzeuge_diagramme.py --werkzeug-herunterladen
python validierung/erzeuge_dokumente.py
```

Ist eine geprüfte JAR bereits vorhanden, kann sie ohne Download verwendet werden:

```powershell
python validierung/erzeuge_diagramme.py --plantuml-jar C:\Werkzeuge\plantuml.jar
```

Nach jeder Änderung werden die Diagramme vor DOCX und PDF erzeugt. Die strenge Projektvalidierung erkennt nicht aktualisierte Quellen, SVG- oder PNG-Dateien anhand des Manifests.

## Organisationsspezifisch anpassen

Die Anpassung erfolgt nur in der getrennten, angemessen geschützten Offline-Fassung. Dort werden Zonen, Rollen, Kommunikationsbeziehungen und Entscheidungen in den `.puml`-Dateien auf die tatsächliche Architektur abgebildet. Reale Domänen, Hostnamen, IP-Adressen, Konten oder interne Schutzbedarfe dürfen nicht in dieses öffentliche Referenzrepository zurückfließen.

Die Knotennamen hinter `as` bleiben möglichst stabil. Sichtbare Bezeichnungen können direkt zwischen den Anführungszeichen geändert werden. Neue Beziehungen werden erst ergänzt, wenn sie fachlich bewertet und durch eine OSCAL-Kontrolle gedeckt sind. Farbe bleibt ergänzend; Form, Text und Pfeilbeschriftung tragen die eigentliche Aussage.

Weiterführend gelten der [`Leitfaden zur organisationsspezifischen Übernahme`](../dokumentation/ÜBERNAHMELEITFADEN.md) und die verbindlichen [`Layoutregeln`](../dokumentation/LAYOUTREGELN.md).
