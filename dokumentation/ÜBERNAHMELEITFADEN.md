# Leitfaden zur organisationsspezifischen Übernahme

## Zweck

Dieser Leitfaden beschreibt die kontrollierte Überführung der öffentlichen, organisationsneutralen Referenz in ein konkretes KI-IT-Sicherheitskonzept. Die Hinweise stehen bewusst außerhalb des Sicherheitskonzepts. Das Konzept selbst beschreibt den vorgesehenen Sollzustand und enthält keine redaktionellen Arbeitsanweisungen.

## Schutzgrenze vor Beginn

Eine organisationsspezifische Bearbeitung findet nicht im öffentlichen Referenzrepository statt. Vor der ersten realen Angabe wird eine getrennte, angemessen geschützte geschützte Fassung angelegt. In dieser Fassung wird in `projektstatus.json` zuerst `organisationsspezifisch` auf `true` gesetzt. Die Dokumenterzeugung verwendet dann automatisch die Kennzeichnung:

> **NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH**

Die Kennzeichnung ist noch keine formale Einstufung. Schutzbedarf, Geheimhaltungsgrad, Freigabekreis und technische Verarbeitungsvoraussetzungen werden durch die befugten Stellen der jeweiligen Organisation festgelegt. Reale Domänen, Hostnamen, IP-Adressen, Konten, interne Schwachstellen, Netzpläne, Verantwortliche und Nachweise verbleiben vollständig in der geschützten Fassung.

## Kontrollierter Ablauf

1. Geltungsbereich, Systemverantwortung, Informationsverbünde und ausgeschlossene Anwendungsfälle festlegen.
2. Schutzbedarf und Informationsklassifikation für Eingaben, Ausgaben, RAG-Bestände, Suchvektoren, Indizes, Protokolle und Sicherungen bestimmen.
3. Reale Architektur, Vertrauenszonen, Schnittstellen und Datenflüsse in der geschützten Fassung erfassen und gegen die Architekturgrenzen des Katalogs prüfen.
4. Rechts-, Datenschutz-, Geheimschutz- und Beteiligungsprüfung je Anwendungsfall durchführen und Entscheidungen nachvollziehbar dokumentieren.
5. Jede OSCAL-Kontrolle auf Anwendbarkeit prüfen, konkrete Umsetzung und Verantwortlichkeit festlegen und erwartete Nachweise benennen.
6. Die neun bewerteten Szenarien und ihre Umsetzungsannahmen mit der tatsächlichen Umgebung abgleichen. Bei Übereinstimmung können Bewertung und Maßnahmen übernommen und Verantwortliche sowie Fundstellen ergänzt werden. Abweichungen werden bewertet; mittlere Restrisiken benötigen keinen pauschalen Zusatzplan. Hohe Ausnahmen sind ausdrücklich zu genehmigen und zu befristen.
7. Technische Wirksamkeits-, Missbrauchs-, Negativ-, Wiederanlauf- und Wiederholungsprüfungen in der tatsächlichen Umgebung durchführen.
8. Konzept, Katalog, Nachweise und Testergebnisse unabhängig fachlich prüfen und durch die zuständigen Rollen freigeben lassen.
9. Änderungen, Modellwechsel, Vorfälle, Ausnahmen, Wiedervorlagen und Außerbetriebnahme in die bestehenden ISMS- und Betriebsprozesse aufnehmen.

## Anpassung nach Konzeptabschnitt

| Konzeptabschnitt | Organisationsspezifische Festlegung in der geschützten Fassung |
|---|---|
| Dokumentenlenkung | Eigentümer, Prüfende, Freigebende, Gültigkeit, Wiedervorlage und formale Einstufung |
| Zweck und Abgrenzung | Konkrete Dienste, Nutzergruppen, Anwendungsfälle, Datenarten und Ausschlüsse |
| Basis-Sicherheitskonzept | Verbindlicher Bezug zum Informationsverbund, Sicherheitskonzept und ISMS |
| Systemarchitektur | Reale Komponenten, Zonen, Schnittstellen, Protokolle und freigegebene Kommunikationsbeziehungen |
| Recht und Steuerung | Anwendbare Rechtsrollen, Beteiligungen, Zuständigkeiten und Entscheidungswege |
| Sicherheitsmaßnahmen | Umsetzung, Verantwortlichkeit, technische Parameter, Prüfmethode und Nachweise je Kontroll-ID |
| Lokale Wissenssuche und Dateiübernahmen | Datenquellen, Klassifikation, Zugriffsmodell, Formate, Größen, Aufbewahrung und Löschkette |
| Agentische Anwendungen | Freigegebene Werkzeuge, Arbeitsbereiche, Bestätigungsregeln, abgeschottete Ausführungsumgebung und Protokollierung |
| Betrieb | Freigabeschwellen, Überwachung, Vorfallbehandlung, Rückkehr zur freigegebenen Vorversion und Wiederanlauf |

## Diagramme und Datenflüsse

Die bearbeitbaren Diagrammquellen liegen unter `diagramme/` im PlantUML-Format. PlantUML-Dateien sind einfacher Text, können ohne Cloud-Dienst lokal gerendert und in der Versionsverwaltung zeilenweise geprüft werden. In einer geschützten Fassung werden ausschließlich die tatsächlichen Systemgrenzen und freigegebenen Beziehungen dargestellt. Produktnamen, interne Netzangaben und reale technische Bezeichner gehören nicht in das öffentliche Referenzrepository. Bedienung, Dateizuordnung und der geprüfte Erzeugungsweg sind in [`diagramme/README.md`](../diagramme/README.md) beschrieben.

Für jede Abbildung gelten folgende Schritte:

1. PlantUML-Quelle in der geschützten Fassung fachlich aktualisieren.
2. SVG für die Dokumentation und PNG mit 180 dpi für das DOCX über `validierung/erzeuge_diagramme.py` erzeugen.
3. Alternativtext und Bildunterschrift an die tatsächliche Aussage anpassen.
4. Jede dargestellte Verbindung gegen Firewall-, KI-Zugangs- oder Plattformregeln nachweisen.
5. Veraltete Pfade, ungewollten ausgehenden Netzwerkverkehr und nicht dargestellte Verwaltungszugänge durch Negativtests ausschließen.

## Externe Inferenz

Externe Inferenz ist kein einfacher Produktwechsel. Ihre Aktivierung verändert Systemgrenze, Verantwortlichkeit, Datenflüsse, Rechtslage und Nachweispflichten. Vor einer Freigabe werden mindestens KI-EXT-001 und KI-EXT-002 vollständig bearbeitet. Zusätzlich sind Datenschutz, Datenklassifikation, Verträge, Auftragsverarbeitung, Drittlandbezug, Anbieter- und Lieferkette, Verschlüsselung, Schlüsselverwaltung, Protokollierung, Löschung, Verfügbarkeit, Vorfallbehandlung und Ausstiegsszenario neu zu bewerten.

Automatische Wechsel bleiben auf bereits freigegebene Ausweichprofile begrenzt. Allgemeine Internet- oder Identitätsdienstfreigaben ersetzen die zusätzliche KI-Freigabe nicht. Eine Profilfreigabe kann gleichartige Anfragen abdecken. Ersatzmodelle sind optional; jede Tätigkeit bleibt ohne KI möglich.

## Training und Feinabstimmung

Das Konzept erteilt keine Freigabe für Training, Fine-Tuning, LoRA, PEFT, RLHF, kontinuierliches Lernen oder produktive Änderungen von Modellgewichten. Soll eine solche Nutzung später eingeführt werden, ist ein eigenständiges Sicherheits-, Datenschutz-, Datenqualitäts- und Freigabekonzept erforderlich. Das Aktivieren der entsprechenden Statuswerte wird von der Projektvalidierung absichtlich abgewiesen.

## Praktische Übernahme

Bei Übereinstimmung mit den beschriebenen Annahmen ist keine Neuerfindung des Konzepts nötig: Namen, Zuständigkeiten, bestehende IT-Prozesse und Nachweisfundstellen werden zugeordnet. Die tatsächliche Umsetzung und befugte Risikoentscheidung bleiben nachzuweisen; bloßes Umbenennen ist kein Wirksamkeitsbeleg. Agenten erhalten übliche Projektfunktionen im genehmigten Umfang. Löschungen ohne einfache Nutzerwiederherstellung benötigen immer konkrete Genehmigung. Persönliche Wissensbeiträge bleiben standardmäßig aus und benötigen eine informierte Entscheidung je Agentenprojekt.

## Erzeugung und Prüfung

Normative Änderungen werden zuerst im OSCAL-Katalog vorgenommen. Anschließend werden DOCX und PDF ausschließlich über den Generator neu erzeugt und vollständig geprüft.

```powershell
python validierung/erzeuge_diagramme.py
python validierung/erzeuge_dokumente.py
powershell -NoProfile -ExecutionPolicy Bypass -File validierung/aktualisiere_word_felder.ps1
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
```

Vor der Freigabe werden zusätzlich alle Seiten des DOCX und PDF visuell geprüft. Die fachliche Prüfung umfasst die tatsächliche Systemumgebung, Kontrollnachweise, Wirksamkeitstests, Restrisiken, Rechtslage und korrekte Einstufung. Automatisierte Prüfungen ersetzen diese Freigaben nicht.
