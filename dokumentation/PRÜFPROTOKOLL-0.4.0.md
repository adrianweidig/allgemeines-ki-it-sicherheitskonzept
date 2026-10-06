# Prüfprotokoll 0.4.0

**Prüfdatum:** 06.10.2026
**Dokumentstatus:** ÖFFENTLICH – organisationsneutrale Referenzvorlage
**Gegenstand:** OSCAL-Katalog, KI-Informationssicherheitskonzept und Anlage 1

## Ergebnis

Version 0.4.0 enthält weiterhin 34 Kontrollen in 22 Gruppen und neun Risiken mit jeweils eigener Air-Gap- und Cloud-Bewertung. Kontroll-, Quellen-, Risiko- und Abschnittskennungen wurden nicht neu nummeriert. Der OSCAL-Katalog bleibt die maßgebliche Quelle der verbindlichen Anforderungen.

Die Prüfung bestätigt die technische Konsistenz und Ableitung der öffentlichen Referenzartefakte. Sie ist keine Freigabe einer konkreten Betriebsumgebung und kein Nachweis ihrer betrieblichen Wirksamkeit.

## Begründete Verbesserungen

- KI-GOV-001 trennt Zweck, zugelassene Anwendungsfälle, Datenarten, Funktionsgrenzen und verantwortliche Rollen.
- KI-GOV-002 stellt klar, dass eine unterschriebene Belehrung nur Teilnahme, Verständnis und persönliche Verpflichtung bestätigt.
- KI-REC-001 und KI-RAG-001 ordnen die Festlegung zulässiger Datenarten sowie die Prüfung von Herkunft, Vertrauenswürdigkeit, Eignung, Aktualität, Vollständigkeit und Verarbeitungsrechten den zuständigen Fach- und Datenverantwortlichen zu.
- KI-RAG-003, KI-OPS-001 und KI-DEC-001 erfassen Aufbewahrung und Löschung über Quelldateien, extrahierte Texte, Textabschnitte, Suchvektoren, Indexeinträge, Gesprächskontexte, Protokolle, Zwischenspeicher und Sicherungen hinweg.
- KI-TOL-001 begrenzt Projektfreigaben nach Aktionsart, Arbeitsbereich, Datenarten, Ziel und Dauer. Modellantworten und Werkzeugausgaben dürfen Freigaben nicht ausweiten.
- KI-VAL-001 trennt geplante Prüfziele und Annahmekriterien von tatsächlich ausgeführten Prüfschritten und Ergebnissen. Nutzeraussagen werden nicht als technische Prüfung behandelt.
- KI-VAL-002 verlangt vor einer Änderung eine dokumentierte Auswirkungsentscheidung und bestimmt daraus den erneut auszuführenden Prüfumfang.

Die Präzisierungen stützen sich insbesondere auf den [BSI-Kriterienkatalog für KI-Modelle und -Systeme in der Bundesverwaltung](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Kriterienkatalog_KI-Modelle_Bundesverwaltung.pdf?__blob=publicationFile&v=3), die [DSK-Orientierungshilfe zu RAG](https://www.datenschutzkonferenz-online.de/media/oh/DSK_OH_RAG.pdf) und das [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence).

## Technische Prüfungen

- JSON-Syntax, Quellenregisterschema und offizielles OSCAL-Katalogschema 1.1.3.
- Eindeutigkeit und Stabilität der Kontroll-, Quellen-, Risiko- und Abschnittskennungen.
- Vollständige Ableitung der Kontrollfestlegungen und Anwendungshinweise in das DOCX-Masterdokument.
- Getrennte Air-Gap- und Cloud-Bewertung für R-01 bis R-09.
- Versions- und normalisierter Textabgleich zwischen OSCAL, DOCX und PDF.
- Prüfung beider DOCX-Dateien auf Kommentare, Kommentarverweise, nicht angenommene Änderungen, Bearbeitungsschutz, Paketsignaturen und Wasserzeichen.
- Prüfung beider PDF-Dateien auf Verschlüsselung, Berechtigungsbeschränkungen, Signaturen, unerwartete Formulare und unzulässige Anmerkungen.
- Negativtest des Word-Exports mit befülltem PDF-Ziel. DOCX und PDF blieben nach dem abgebrochenen Aufruf bytegleich.
- Technisches Öffnen beider DOCX- und PDF-Dateien sowie Prüfung der vier leeren Formularfelder einschließlich des digitalen Signaturfelds.
- Vollständiges Rendern und visuelle Prüfung aller 38 Konzeptseiten und der einseitigen Nutzerbelehrung.

Der allgemeine DOCX-Renderer konnte auf dem Prüfhost mangels LibreOffice nicht ausgeführt werden. Die PDFs wurden unmittelbar aus den zuvor gespeicherten Word-Masterdokumenten erzeugt und mit dem gebündelten Poppler seitenweise gerendert. Der maschinenlesbare DOCX/PDF-Inhaltsvergleich bleibt davon unberührt.

## Verbleibende Grenzen

- Die Referenz enthält keine organisationsspezifischen Angaben und ersetzt keine Prüfung einer konkreten technischen Umgebung.
- Die öffentlichen ISO-Metadaten ersetzen keine lizenzierten Normtexte und keine unabhängige Konformitätsbewertung.
- Temporäre HTTP-Antworten wie 403, 405 oder Zeitüberschreitungen werden als manuell zu prüfende Quellenwarnungen behandelt. Bestätigte 404- und 410-Antworten bleiben Fehler.
- Die GitHub-Artefaktspeicherquote ist keine Eigenschaft der erzeugten Dokumente. Ein fehlgeschlagener Upload darf nicht als bestandene Veröffentlichung ausgegeben werden.
