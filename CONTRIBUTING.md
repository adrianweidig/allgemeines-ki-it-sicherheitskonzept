# Mitwirkung

## Grundsatz

Beiträge verwenden ausschließlich öffentliche Informationen und berücksichtigen die getrennten Air-Gap- und Cloud-Szenarien. Fachliche Änderungen benennen betroffene Kontrollen, Szenarien und öffentliche Quellen.

## Fachliche Anforderungen

1. Normative Anforderungen zuerst im OSCAL-Katalog ändern.
2. Für jede fachliche Änderung eine offizielle öffentliche Fundstelle mit genauer Seite, Abschnitt, Artikel oder fixierter Revision ergänzen.
3. Quellenmetadaten und Zuordnungen im Quellenregister aktualisieren.
4. Empfehlungen nur mit ausdrücklicher KI-Risikobegründung zu einem projektinternen `MUSS` verschärfen.
5. Kontroll- und Quellen-IDs nicht ohne dokumentierte Migration ändern.
6. Keine proprietären ISO-Normentexte übernehmen; nur zulässige Kennungen, öffentliche Metadaten und kenntlich gemachte Zuordnungen verwenden.
7. Konzeptdokumente aus dem abgestimmten Katalog neu erzeugen und vollständig prüfen.

## Schutzgrenzen

Beiträge dürfen keine realen Organisationsnamen, Domänen, Hostnamen, IP-Adressen, Konten, internen Schwachstellen, Geheimnisse oder eingestuften Inhalte enthalten. `quellen/lokale-eingaben/` bleibt unversioniert. Training und Feinabstimmung sind außerhalb des Projektumfangs. Das Cloud-Szenario umfasst ausschließlich die freigegebene Modellverarbeitung nach KI-EXT-001.

## Lokale Prüfung

```powershell
python -m pip install -r validierung/anforderungen.txt
python validierung/validiere_projekt.py --streng --online
python -m unittest discover -s validierung/testfälle -p "test_*.py"
python validierung/erzeuge_dokumente.py
```

Nach der Erzeugung müssen DOCX und PDF technisch geöffnet, sämtliche PDF-Seiten gerendert und visuell geprüft werden. Abweichungen zwischen Katalog, DOCX und PDF sind vor Einreichung zu beheben.

## Pull Request

Der Pull Request erläutert Zweck, betroffene Kontroll-IDs, neue oder geänderte Quellen, Prüfergebnisse und mögliche Auswirkungen auf die Dokumentversion. Eine Änderung gilt erst nach erfolgreicher Automatisierung und fachlicher Prüfung als übernahmefähig.
