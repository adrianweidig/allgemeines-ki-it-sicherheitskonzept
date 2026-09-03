# Leitfaden zur organisationsspezifischen Übernahme

## Zweck

Dieser Leitfaden beschreibt die kontrollierte Überführung der öffentlichen, organisationsneutralen Referenz in ein konkretes KI-IT-Sicherheitskonzept. Die Hinweise stehen bewusst außerhalb des Sicherheitskonzepts. Das Konzept selbst beschreibt den vorgesehenen Sollzustand und enthält keine redaktionellen Arbeitsanweisungen.

## Schutzgrenze vor Beginn

Eine organisationsspezifische Bearbeitung findet nicht im öffentlichen Referenzrepository statt. Vor der ersten realen Angabe wird eine getrennte, angemessen geschützte Offline-Fassung angelegt. In dieser Fassung wird in `projektstatus.json` zuerst `organisationsspezifisch` auf `true` gesetzt. Die Dokumenterzeugung verwendet dann automatisch die Kennzeichnung:

> **NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH**

Die Kennzeichnung ist noch keine formale Einstufung. Schutzbedarf, Geheimhaltungsgrad, Freigabekreis und technische Verarbeitungsvoraussetzungen werden durch die befugten Stellen der jeweiligen Organisation festgelegt. Reale Domänen, Hostnamen, IP-Adressen, Konten, interne Schwachstellen, Netzpläne, Verantwortliche und Nachweise verbleiben vollständig in der geschützten Fassung.

## Kontrollierter Ablauf

1. Geltungsbereich, Systemverantwortung, Informationsverbünde und ausgeschlossene Anwendungsfälle festlegen.
2. Schutzbedarf und Informationsklassifikation für Eingaben, Ausgaben, RAG-Bestände, Embeddings, Indizes, Protokolle und Sicherungen bestimmen.
3. Reale Architektur, Vertrauenszonen, Schnittstellen und Datenflüsse in der geschützten Fassung erfassen und gegen die Architekturgrenzen des Katalogs prüfen.
4. Rechts-, Datenschutz-, Geheimschutz- und Beteiligungsprüfung je Anwendungsfall durchführen und Entscheidungen nachvollziehbar dokumentieren.
5. Jede OSCAL-Kontrolle auf Anwendbarkeit prüfen, konkrete Umsetzung und Verantwortlichkeit festlegen und erwartete Nachweise benennen.
6. Abweichungen, kompensierende Maßnahmen und akzeptierte Restrisiken mit Befristung, Eigentümer und Freigabe dokumentieren.
7. Technische Wirksamkeits-, Missbrauchs-, Negativ-, Wiederanlauf- und Regressionstests in der tatsächlichen Umgebung durchführen.
8. Konzept, Katalog, Nachweise und Testergebnisse unabhängig fachlich prüfen und durch die zuständigen Rollen freigeben lassen.
9. Änderungen, Modellwechsel, Vorfälle, Ausnahmen, Wiedervorlagen und Außerbetriebnahme in die bestehenden ISMS- und Betriebsprozesse aufnehmen.

## Anpassung nach Konzeptabschnitt

| Konzeptabschnitt | Organisationsspezifische Festlegung in der geschützten Fassung |
|---|---|
| Dokumentenlenkung | Eigentümer, Prüfende, Freigebende, Gültigkeit, Wiedervorlage und formale Einstufung |
| Zweck und Abgrenzung | Konkrete Dienste, Nutzergruppen, Anwendungsfälle, Datenarten und Ausschlüsse |
| Basis-Sicherheitskonzept | Verbindlicher Bezug zum Informationsverbund, Sicherheitskonzept und ISMS |
| Systemarchitektur | Reale Komponenten, Zonen, Schnittstellen, Protokolle und freigegebene Kommunikationsbeziehungen |
| Recht und Governance | Anwendbare Rechtsrollen, Beteiligungen, Zuständigkeiten und Entscheidungswege |
| Sicherheitsmaßnahmen | Umsetzung, Verantwortlichkeit, technische Parameter, Prüfmethode und Evidenz je Kontroll-ID |
| RAG und Uploads | Datenquellen, Klassifikation, ACL-Modell, Formate, Größen, Aufbewahrung und Löschkette |
| Agentische Anwendungen | Freigegebene Tools, Arbeitsbereiche, Bestätigungsregeln, Sandbox und Protokollierung |
| Betrieb | Freigabeschwellen, Überwachung, Vorfallbehandlung, Rückgriff und Wiederanlauf |

## Diagramme und Datenflüsse

Die bearbeitbaren Diagrammquellen liegen unter `diagramme/` im PlantUML-Format. PlantUML-Dateien sind einfacher Text, können ohne Cloud-Dienst lokal gerendert und in der Versionsverwaltung zeilenweise geprüft werden. In einer geschützten Fassung werden ausschließlich die tatsächlichen Systemgrenzen und freigegebenen Beziehungen dargestellt. Produktnamen, interne Netzangaben und reale technische Bezeichner gehören nicht in das öffentliche Referenzrepository. Bedienung, Dateizuordnung und der geprüfte Erzeugungsweg sind in [`diagramme/README.md`](../diagramme/README.md) beschrieben.

Für jede Abbildung gelten folgende Schritte:

1. PlantUML-Quelle in der geschützten Fassung fachlich aktualisieren.
2. SVG für die Dokumentation und PNG mit 180 dpi für das DOCX über `validierung/erzeuge_diagramme.py` erzeugen.
3. Alternativtext und Bildunterschrift an die tatsächliche Aussage anpassen.
4. Jede dargestellte Verbindung gegen Firewall-, Gateway- oder Plattformregeln nachweisen.
5. Veraltete Pfade, ungewollten Egress und nicht dargestellte Verwaltungszugänge durch Negativtests ausschließen.

## Externe Inferenz

Externe Inferenz ist kein einfacher Produktwechsel. Ihre Aktivierung verändert Systemgrenze, Verantwortlichkeit, Datenflüsse, Rechtslage und Nachweispflichten. Vor einer Freigabe werden mindestens KI-EXT-001 und KI-EXT-002 vollständig bearbeitet. Zusätzlich sind Datenschutz, Datenklassifikation, Verträge, Auftragsverarbeitung, Drittlandbezug, Anbieter- und Lieferkette, Verschlüsselung, Schlüsselverwaltung, Protokollierung, Löschung, Verfügbarkeit, Vorfallbehandlung und Ausstiegsszenario neu zu bewerten.

Automatische Fallbacks, Provider-Erkennung und Cloudmodelle bleiben deaktiviert, solange diese Freigabe nicht nachweislich vorliegt.

## Training und Feinabstimmung

Das Konzept erteilt keine Freigabe für Training, Fine-Tuning, LoRA, PEFT, RLHF, kontinuierliches Lernen oder produktive Änderungen von Modellgewichten. Soll eine solche Nutzung später eingeführt werden, ist ein eigenständiges Sicherheits-, Datenschutz-, Datenqualitäts- und Freigabekonzept erforderlich. Das Aktivieren der entsprechenden Statuswerte wird von der Projektvalidierung absichtlich abgewiesen.

## Erzeugung und Prüfung

Normative Änderungen werden zuerst im OSCAL-Katalog vorgenommen. Anschließend werden DOCX und PDF ausschließlich über den Generator neu erzeugt und vollständig geprüft.

```powershell
python validierung/erzeuge_diagramme.py
python validierung/erzeuge_dokumente.py
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
```

Vor der Freigabe werden zusätzlich alle Seiten des DOCX und PDF visuell geprüft. Die fachliche Prüfung umfasst die tatsächliche Systemumgebung, Kontrollnachweise, Wirksamkeitstests, Restrisiken, Rechtslage und korrekte Einstufung. Automatisierte Prüfungen ersetzen diese Freigaben nicht.
