# Bearbeitbare Diagramme

Acht lokal erzeugte PlantUML-Diagramme erläutern die Referenzszenarien. PNG-Dateien mit 180 dpi stehen inline im DOCX, SVG-Dateien dienen der Markdown-Darstellung. Das PDF wird ausschließlich aus dem gespeicherten DOCX erzeugt.

| Quelle | Aussage | Abbildung |
|---|---|---|
| `umgebungsuebersicht.puml` | Zwei Szenarien mit gemeinsamen Regeln | 1 |
| `architektur.puml` | Air-Gap ohne externe Netzwerkverbindung | 2 |
| `architektur-cloud.puml` | Cloud-Inferenz mit intern begrenztem Kontext | 3 |
| `artefaktimport.puml` | Modellprüfung für beide Betriebswege | 4 |
| `risikobewertung.puml` | Bewertung und Behandlung von KI-Risiken | 5 |
| `risikomatrix.puml` | Gemeinsamer Bewertungsmaßstab | 6 |
| `rag-datenfluss.puml` | Dokumentauswahl, Quellrechte und Ableitungen | 7 |
| `agentische-werkzeugnutzung.puml` | Einzelgenehmigung und begrenzte Projektfreigabe | 8 |

Die Ableitungen liegen unter `dokumentation/medien/`. `diagramm-manifest.json` verbindet Quellen, SVG und PNG über SHA-256. Quelltexte verwenden UTF-8 ohne BOM, LF-Zeilenenden und eine abschließende neue Zeile.

```powershell
python validierung/erzeuge_diagramme.py --werkzeug-herunterladen
python validierung/erzeuge_dokumente.py
powershell -NoProfile -ExecutionPolicy Bypass -File validierung/aktualisiere_word_felder.ps1
```

Ein vorhandenes geprüftes PlantUML-JAR wird ohne Download verwendet. Die Matrix wird aus dem gemeinsamen Bewertungsmaßstab erzeugt. Die Einzelwerte beider Szenarien stehen im Katalog und in Kapitel 8.3. Andere Diagrammquellen werden direkt redigiert.

Jede Abbildung wird auf Leserichtung, lesbare Beschriftung und Übereinstimmung mit den Kontrollen geprüft. Farbe unterstützt die Aussage, ersetzt aber keine Beschriftung. Dateiübernahme und Netzwerkverkehr sind erkennbar verschieden dargestellt. Der Generator ergänzt einen vollständigen Alternativtext und eine unmittelbare Beschriftung.
