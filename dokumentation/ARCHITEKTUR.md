# Organisationsneutrale KI-Referenzarchitektur

## Zielbild

Das Zielbild beschreibt eine vollständig lokale KI-Infrastruktur in einer klassischen, sicher verwalteten Domäne. Es ist produktneutral: Open WebUI, Ollama, vLLM, llama.cpp, Cline und OpenCode dienen nur als Beispiele für typische Funktionsklassen.

```text
Entfernter verwalteter Client
        │
        └── Organisations-VPN mit MFA
                    │
Verwaltete Clients im internen Netz
        ├── Browser
        ├── agentische Anwendungen
        └── lokaler Git- und Entwicklungszugriff
                    │
             ausschließlich HTTPS
                    │
        Interner KI-Zugang / API-Gateway
        ├── lokaler IdP und Autorisierung
        ├── Modell- und Tool-Freigaben
        ├── Protokollierung und Begrenzung
        └── TLS-Terminierung
                    │
          getrennte KI-Serverzone
                    │
      lokale Containerplattform
        ├── Chat-Oberfläche
        ├── Inferenzserver
        ├── RAG- und Dokumentenaufbereitung
        ├── Embedding- und Reranking-Dienste
        ├── lokale Vektor-/Datenbank
        └── technische Überwachung
                    │
       internes Container- beziehungsweise Pod-Netz
                    │
              kein Internet-Egress
```

## Vertrauenszonen

1. **Verwaltete Clientzone:** Benutzerinteraktion, lokale Entwicklungswerkzeuge und agentische Anwendungen mit minimalen Arbeitsbereichsrechten.
2. **Kontrollierter KI-Zugang:** einzige aus der Clientzone erreichbare KI-Schnittstelle; setzt Identität, Rollen, Richtlinien, Modellfreigabe, Raten- und Kontextgrenzen sowie Protokollierung durch.
3. **KI-Serverzone:** Inferenz, Chat, RAG, Datenhaltung und Überwachung. Interne Schnittstellen werden nicht in das allgemeine Netz veröffentlicht.
4. **Importzone:** kontrollierter Transfer und Prüfung von Modellen, Images, Paketen und Erweiterungen vor Übernahme in lokale Registrierungen.
5. **Betriebs- und Nachweiszone:** lokale, besonders geschützte Protokolle, Sicherheitsnachweise, Sicherungen und Wiederherstellungsdaten.

## Sicherheitsgrenzen

Container- oder Pod-Netze sind keine eigenständige Vertrauensentscheidung. Verkehrsbeziehungen folgen dem Prinzip `standardmäßig verweigern, ausdrücklich erlauben`. Workloads erhalten keine unnötigen Privilegien, laufen möglichst rootless, nutzen schreibgeschützte Dateisystemanteile und beziehen Artefakte nur aus kontrollierten lokalen Quellen.

Der Inferenzserver besitzt keinen Internetzugang und keine direkt veröffentlichte Rohschnittstelle. Nutzer- und Dienstzugriffe sind einzeln zuordenbar und widerrufbar; gemeinsame statische API-Schlüssel sind kein Standardverfahren.

## Datenflüsse

- Clientanfragen passieren den kontrollierten KI-Zugang und werden erst danach an freigegebene Modelle oder lokale Werkzeuge vermittelt.
- RAG-Dokumente werden vor Verarbeitung auf Dateityp, Größe und Schadsoftware geprüft und in isolierten Parserprozessen aufbereitet.
- Eine Berechtigungsprüfung erfolgt vor Indexaufnahme und erneut bei jeder Abfrage; das Sprachmodell entscheidet keine Zugriffsrechte.
- Uploads bleiben sitzungsbezogen, sofern keine ausdrücklich genehmigte lokale Ablage besteht.
- Löschung erfasst Quelldatei, extrahierten Text, Index, Embeddings, Cache, Protokollbezug und den geregelten Ablauf in Sicherungsketten.

## Nicht enthalten

Nicht Bestandteil sind externe SaaS-Dienste, Training, Feinabstimmung, kontinuierliches Lernen und produktive Änderungen von Modellgewichten. Externe Inferenz benötigt eine neue, organisationsspezifische Bewertung und ist in der Referenz deaktiviert.
