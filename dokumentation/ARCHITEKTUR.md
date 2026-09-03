# Organisationsneutrale KI-Referenzarchitektur

## Zielbild

Das Zielbild beschreibt eine vollständig lokale KI-Infrastruktur in einer klassischen, sicher verwalteten Domäne. Es ist produktneutral: Open WebUI, Ollama, vLLM, llama.cpp, Cline und OpenCode dienen nur als Beispiele für typische Funktionsklassen.

Die editierbare Quelle liegt unter [`diagramme/architektur.puml`](../diagramme/architektur.puml). Alle weiteren PlantUML-Quellen und der lokale Erzeugungsweg sind in [`diagramme/README.md`](../diagramme/README.md) beschrieben.

![Lokale KI-Systemarchitektur mit Vertrauenszonen](medien/architektur.svg)

Die Clientzone erreicht ausschließlich den kontrollierten KI-Zugang. Rohschnittstellen der Inferenz, Verwaltungszugänge und interne Containerkommunikation bleiben außerhalb des normalen Anfragepfads. Identität, Richtliniendurchsetzung, Registrierungen und Prüfdaten bilden eigene Sicherheitsfunktionen.

## Vertrauenszonen

1. **Verwaltete Clientzone:** Benutzerinteraktion, lokale Entwicklungswerkzeuge und agentische Anwendungen mit minimalen Arbeitsbereichsrechten.
2. **Kontrollierter KI-Zugang:** einzige aus der Clientzone erreichbare KI-Schnittstelle; setzt Identität, Rollen, Richtlinien, Modellfreigabe, Raten- und Kontextgrenzen sowie Protokollierung durch.
3. **KI-Serverzone:** Inferenz, Chat, lokale Wissenssuche (RAG), Datenhaltung und Überwachung. Interne Schnittstellen werden nicht in das allgemeine Netz veröffentlicht.
4. **Importzone:** kontrollierter Transfer und Prüfung von Modellen, Containerabbildern, Paketen und Erweiterungen vor Übernahme in lokale Registrierungen.
5. **Betriebs- und Nachweiszone:** lokale, besonders geschützte Protokolle, Sicherheitsnachweise, Sicherungen und Wiederherstellungsdaten.

## Sicherheitsgrenzen

Container- oder Pod-Netze sind keine eigenständige Vertrauensentscheidung. Verkehrsbeziehungen folgen dem Prinzip `standardmäßig verweigern, ausdrücklich erlauben`. KI-Dienste erhalten keine unnötigen Privilegien, laufen möglichst ohne privilegierten Systemnutzer (`rootless`), nutzen schreibgeschützte Dateisystemanteile und beziehen Artefakte nur aus kontrollierten lokalen Quellen.

Der Inferenzserver besitzt keinen Internetzugang und keine direkt veröffentlichte Rohschnittstelle. Nutzer- und Dienstzugriffe sind einzeln zuordenbar und widerrufbar; gemeinsame statische API-Schlüssel sind kein Standardverfahren.

## Datenflüsse

- Clientanfragen passieren den kontrollierten KI-Zugang und werden erst danach an freigegebene Modelle oder lokale Werkzeuge vermittelt.
- Dokumente für die lokale Wissenssuche werden vor der Verarbeitung auf Dateityp, Größe und Schadsoftware geprüft und in isolierten Prozessen ausgewertet.
- Eine Berechtigungsprüfung erfolgt vor Indexaufnahme und erneut bei jeder Abfrage; das Sprachmodell entscheidet keine Zugriffsrechte.
- Bedarfsgesteuerte Dateiübernahmen bleiben sitzungsbezogen, sofern keine ausdrücklich genehmigte lokale Ablage besteht.
- Löschung erfasst Quelldatei, extrahierten Text, Index, Suchvektoren, Zwischenspeicher, Protokollbezug und den geregelten Ablauf in Sicherungsketten.

### Kontrollierter Artefaktimport

![Kontrollierter Import von KI-Artefakten](medien/artefaktimport.svg)

Externe Artefakte werden nicht direkt in die Produktionszone übertragen. Ein getrennter Prüfweg verbindet Herkunfts- und Versionsnachweis, Integritätsprüfung, Schwachstellen- und Lizenzanalyse, dokumentierte Freigabe, lokalen Test und kontrollierten Rückgriff.

### Risikobewertung

![Ablauf der Risikobewertung](medien/risikobewertung.svg)

Gefährdungen werden als konkrete Szenarien beschrieben. Eintrittshäufigkeit und Schadenshöhe bestimmen die Risikokategorie. Nach der Behandlung wird das Restrisiko erneut eingestuft und verantwortlich entschieden.

![Risikomatrix mit Ausgangs- und Restrisiken](medien/risikomatrix.svg)

Die qualitative Matrix verwendet die Kategorien des BSI-Standards 200-3. Text, Zellenposition und stabile Risikokennungen tragen die Aussage; Farbe unterstützt nur die Orientierung.

### Lokaler RAG-Datenfluss

![RAG-Datenfluss mit Berechtigungsprüfung und Löschkette](medien/rag-datenfluss.svg)

Aufnahme und Abfrage sind getrennte Kontrollpunkte. Schutzbedarf, Herkunft und Zugriffsregeln begleiten jede Ableitung. Nur Treffer, die bei der konkreten Anfrage erneut freigegeben wurden, gelangen zur lokalen Inferenz.

### Agentische Werkzeugnutzung

![Agentische Werkzeugnutzung mit Richtlinienprüfung](medien/agentische-werkzeugnutzung.svg)

Eine Modellausgabe ist lediglich ein Aktionsvorschlag. Richtlinienprüfung, Wirkungsklassifikation, konkrete menschliche Bestätigung und minimal berechtigte Ausführung verhindern, dass Modelltext unmittelbar Datei-, Befehls- oder Netzwerkaktionen auslöst.

## Nicht enthalten

Nicht Bestandteil sind externe SaaS-Dienste, Training, Feinabstimmung, kontinuierliches Lernen und produktive Änderungen von Modellgewichten. Externe Inferenz benötigt eine neue, organisationsspezifische Bewertung und ist in der Referenz deaktiviert.
