#!/usr/bin/env python3
"""Erzeugt das redaktionelle DOCX-Master aus OSCAL-Katalog und Quellenregister.

Das PDF wird anschließend ausschließlich aus diesem DOCX mit dem dokumentierten
Renderverfahren erzeugt. Der Katalog bleibt die normative Quelle.
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from lxml import etree


WURZEL = Path(__file__).resolve().parents[1]
KATALOG_PFAD = WURZEL / "katalog" / "ki-it-sicherheitskatalog.oscal.json"
REGISTER_PFAD = WURZEL / "quellen" / "quellenregister.json"
STATUS_PFAD = WURZEL / "projektstatus.json"
ZIEL = WURZEL / "konzept" / "ki-it-sicherheitskonzept.docx"

ÖFFENTLICH = "ÖFFENTLICH – organisationsneutrale Referenzvorlage"
NICHT_ÖFFENTLICH = "NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH"

# compact_reference_guide mit benannter A4-Behördenpapier-Übersteuerung:
# A4 210 × 297 mm, Ränder 25 mm, nutzbare Breite 160 mm (9.072 DXA).
SEITENBREITE_DXA = 11906
INHALTSBREITE_DXA = 9072
TABELLENBREITE_DXA = 8952
BLAU = "2E74B5"
DUNKELBLAU = "1F4D78"
HELLBLAU = "E8EEF5"
HELLGRAU = "F5F7FA"
DUNKELGRAU = "3F4A54"

FOOTNOTES: list[str] = []


def lade_json(pfad: Path):
    return json.loads(pfad.read_text(encoding="utf-8"))


def prop(objekt, name):
    return [p["value"] for p in objekt.get("props", []) if p.get("name") == name]


def teil(control, name):
    return next(p["prose"] for p in control["parts"] if p["name"] == name)


def setze_zellenbreite(zelle, breite):
    zelle.width = breite
    tc_pr = zelle._tc.get_or_add_tcPr()
    tc_w = tc_pr.first_child_found_in("w:tcW")
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(breite.twips)))
    tc_w.set(qn("w:type"), "dxa")


def setze_zellenränder(zelle, oben=80, unten=80, start=120, ende=120):
    tc = zelle._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, wert in (("top", oben), ("bottom", unten), ("start", start), ("end", ende)):
        element = tc_mar.find(qn(f"w:{name}"))
        if element is None:
            element = OxmlElement(f"w:{name}")
            tc_mar.append(element)
        element.set(qn("w:w"), str(wert))
        element.set(qn("w:type"), "dxa")


def schattiere(zelle, farbe):
    tc_pr = zelle._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), farbe)


def wiederhole_kopfzeile(zeile):
    tr_pr = zeile._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "1")
    tr_pr.append(tbl_header)


def verhindere_zeilentrennung(zeile):
    tr_pr = zeile._tr.get_or_add_trPr()
    tr_pr.append(OxmlElement("w:cantSplit"))


def formatiere_tabelle(tabelle, breiten, *, kopf=True, einzug=120):
    tabelle.alignment = WD_TABLE_ALIGNMENT.LEFT
    tabelle.autofit = False
    tbl_pr = tabelle._tbl.tblPr
    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(sum(breiten)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(einzug))
    tbl_ind.set(qn("w:type"), "dxa")
    for zeilenindex, zeile in enumerate(tabelle.rows):
        verhindere_zeilentrennung(zeile)
        if kopf and zeilenindex == 0:
            wiederhole_kopfzeile(zeile)
        for index, zelle in enumerate(zeile.cells):
            setze_zellenbreite(zelle, Pt(breiten[index] / 20))
            setze_zellenränder(zelle)
            zelle.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if kopf and zeilenindex == 0:
                schattiere(zelle, HELLBLAU)
                for absatz in zelle.paragraphs:
                    for run in absatz.runs:
                        run.bold = True


def setze_absatzformat(absatz, *, danach=6, davor=0, zeilen=1.25, zusammenhalten=False):
    fmt = absatz.paragraph_format
    fmt.space_after = Pt(danach)
    fmt.space_before = Pt(davor)
    fmt.line_spacing = zeilen
    fmt.widow_control = True
    if zusammenhalten:
        fmt.keep_with_next = True


def text_absatz(container, text, *, fett_prefix=None, stil=None, danach=6):
    absatz = container.add_paragraph(style=stil)
    setze_absatzformat(absatz, danach=danach)
    if fett_prefix and text.startswith(fett_prefix):
        absatz.add_run(fett_prefix).bold = True
        absatz.add_run(text[len(fett_prefix):])
    else:
        absatz.add_run(text)
    return absatz


def aufzählung(container, punkte):
    for punkt in punkte:
        absatz = container.add_paragraph()
        fmt = absatz.paragraph_format
        fmt.left_indent = Inches(0.375)
        fmt.first_line_indent = Inches(-0.188)
        fmt.space_after = Pt(4)
        fmt.line_spacing = 1.25
        absatz.add_run("•").bold = True
        absatz.add_run("  " + punkt)


def hyperlink(absatz, text, url):
    beziehung = absatz.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    element = OxmlElement("w:hyperlink")
    element.set(qn("r:id"), beziehung)
    run = OxmlElement("w:r")
    eigenschaften = OxmlElement("w:rPr")
    stil = OxmlElement("w:rStyle")
    stil.set(qn("w:val"), "Hyperlink")
    eigenschaften.append(stil)
    run.append(eigenschaften)
    inhalt = OxmlElement("w:t")
    inhalt.text = text
    run.append(inhalt)
    element.append(run)
    absatz._p.append(element)


def fußnotenmarke(absatz, text):
    FOOTNOTES.append(text)
    id_ = len(FOOTNOTES)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_style = OxmlElement("w:rStyle")
    r_style.set(qn("w:val"), "FootnoteReference")
    r_pr.append(r_style)
    run.append(r_pr)
    referenz = OxmlElement("w:footnoteReference")
    referenz.set(qn("w:id"), str(id_))
    run.append(referenz)
    absatz._p.append(run)


def vollzitat(quelle, fundstelle):
    datum = quelle["veröffentlichungsdatum"] or quelle["stand"]
    return (
        f"{quelle['herausgeber']}: {quelle['titel']}, {quelle['fassung']}, {datum}, "
        f"{fundstelle}, {quelle['öffentliche_url']}, abgerufen am 02.09.2026."
    )


def ergänze_fußnotenpaket(docx_pfad):
    ns_w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    ns_ct = "http://schemas.openxmlformats.org/package/2006/content-types"
    ns_rel = "http://schemas.openxmlformats.org/package/2006/relationships"
    with tempfile.TemporaryDirectory(prefix="ki-konzept-docx-") as temp:
        temp_pfad = Path(temp)
        with zipfile.ZipFile(docx_pfad, "r") as paket:
            paket.extractall(temp_pfad)

        content_types = temp_pfad / "[Content_Types].xml"
        wurzel = etree.parse(str(content_types)).getroot()
        vorhanden = wurzel.xpath("//*[local-name()='Override' and @PartName='/word/footnotes.xml']")
        if not vorhanden:
            override = etree.SubElement(wurzel, f"{{{ns_ct}}}Override")
            override.set("PartName", "/word/footnotes.xml")
            override.set("ContentType", "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml")
        etree.ElementTree(wurzel).write(str(content_types), xml_declaration=True, encoding="UTF-8", standalone="yes")

        rels_pfad = temp_pfad / "word" / "_rels" / "document.xml.rels"
        rels = etree.parse(str(rels_pfad)).getroot()
        typ = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
        if not rels.xpath(f"//*[local-name()='Relationship' and @Type='{typ}']"):
            rel = etree.SubElement(rels, f"{{{ns_rel}}}Relationship")
            rel.set("Id", "rIdFootnotes")
            rel.set("Type", typ)
            rel.set("Target", "footnotes.xml")
        etree.ElementTree(rels).write(str(rels_pfad), xml_declaration=True, encoding="UTF-8", standalone="yes")

        styles_pfad = temp_pfad / "word" / "styles.xml"
        styles = etree.parse(str(styles_pfad)).getroot()
        if not styles.xpath("//*[local-name()='style' and @w:styleId='FootnoteReference']", namespaces={"w": ns_w}):
            style = etree.SubElement(styles, f"{{{ns_w}}}style")
            style.set(f"{{{ns_w}}}type", "character")
            style.set(f"{{{ns_w}}}styleId", "FootnoteReference")
            etree.SubElement(style, f"{{{ns_w}}}name").set(f"{{{ns_w}}}val", "footnote reference")
            r_pr = etree.SubElement(style, f"{{{ns_w}}}rPr")
            etree.SubElement(r_pr, f"{{{ns_w}}}vertAlign").set(f"{{{ns_w}}}val", "superscript")
        if not styles.xpath("//*[local-name()='style' and @w:styleId='FootnoteText']", namespaces={"w": ns_w}):
            style = etree.SubElement(styles, f"{{{ns_w}}}style")
            style.set(f"{{{ns_w}}}type", "paragraph")
            style.set(f"{{{ns_w}}}styleId", "FootnoteText")
            etree.SubElement(style, f"{{{ns_w}}}name").set(f"{{{ns_w}}}val", "footnote text")
            etree.SubElement(style, f"{{{ns_w}}}basedOn").set(f"{{{ns_w}}}val", "Normal")
            p_pr = etree.SubElement(style, f"{{{ns_w}}}pPr")
            etree.SubElement(p_pr, f"{{{ns_w}}}spacing").set(f"{{{ns_w}}}after", "0")
            r_pr = etree.SubElement(style, f"{{{ns_w}}}rPr")
            etree.SubElement(r_pr, f"{{{ns_w}}}sz").set(f"{{{ns_w}}}val", "18")
        etree.ElementTree(styles).write(str(styles_pfad), xml_declaration=True, encoding="UTF-8", standalone="yes")

        footnotes = etree.Element(f"{{{ns_w}}}footnotes", nsmap={"w": ns_w})
        for id_, typname in ((-1, "separator"), (0, "continuationSeparator")):
            note = etree.SubElement(footnotes, f"{{{ns_w}}}footnote")
            note.set(f"{{{ns_w}}}id", str(id_))
            note.set(f"{{{ns_w}}}type", typname)
            p = etree.SubElement(note, f"{{{ns_w}}}p")
            r = etree.SubElement(p, f"{{{ns_w}}}r")
            etree.SubElement(r, f"{{{ns_w}}}{typname}")
        for id_, inhalt in enumerate(FOOTNOTES, start=1):
            note = etree.SubElement(footnotes, f"{{{ns_w}}}footnote")
            note.set(f"{{{ns_w}}}id", str(id_))
            p = etree.SubElement(note, f"{{{ns_w}}}p")
            p_pr = etree.SubElement(p, f"{{{ns_w}}}pPr")
            etree.SubElement(p_pr, f"{{{ns_w}}}pStyle").set(f"{{{ns_w}}}val", "FootnoteText")
            abstand = etree.SubElement(p_pr, f"{{{ns_w}}}spacing")
            abstand.set(f"{{{ns_w}}}before", "0")
            abstand.set(f"{{{ns_w}}}after", "0")
            abstand.set(f"{{{ns_w}}}line", "200")
            abstand.set(f"{{{ns_w}}}lineRule", "auto")
            ref_run = etree.SubElement(p, f"{{{ns_w}}}r")
            ref_pr = etree.SubElement(ref_run, f"{{{ns_w}}}rPr")
            etree.SubElement(ref_pr, f"{{{ns_w}}}rStyle").set(f"{{{ns_w}}}val", "FootnoteReference")
            etree.SubElement(ref_run, f"{{{ns_w}}}footnoteRef")
            text_run = etree.SubElement(p, f"{{{ns_w}}}r")
            text_pr = etree.SubElement(text_run, f"{{{ns_w}}}rPr")
            etree.SubElement(text_pr, f"{{{ns_w}}}sz").set(f"{{{ns_w}}}val", "16")
            etree.SubElement(text_pr, f"{{{ns_w}}}szCs").set(f"{{{ns_w}}}val", "16")
            text_element = etree.SubElement(text_run, f"{{{ns_w}}}t")
            text_element.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            text_element.text = " " + inhalt
        etree.ElementTree(footnotes).write(
            str(temp_pfad / "word" / "footnotes.xml"),
            xml_declaration=True, encoding="UTF-8", standalone="yes",
        )

        neu = docx_pfad.with_suffix(".docx.neu")
        with zipfile.ZipFile(neu, "w", compression=zipfile.ZIP_DEFLATED) as paket:
            for datei in sorted(temp_pfad.rglob("*")):
                if datei.is_file():
                    paket.write(datei, datei.relative_to(temp_pfad).as_posix())
        neu.replace(docx_pfad)


def richte_stile_ein(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor.from_string("202830")
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25
    normal.paragraph_format.widow_control = True
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    vorgaben = {
        "Heading 1": (16, BLAU, 18, 10, True),
        "Heading 2": (13, BLAU, 14, 7, False),
        "Heading 3": (12, DUNKELBLAU, 10, 5, False),
    }
    for name, (größe, farbe, davor, danach, seitenwechsel) in vorgaben.items():
        stil = doc.styles[name]
        stil.font.name = "Calibri"
        stil.font.size = Pt(größe)
        stil.font.bold = True
        stil.font.color.rgb = RGBColor.from_string(farbe)
        stil.paragraph_format.space_before = Pt(davor)
        stil.paragraph_format.space_after = Pt(danach)
        stil.paragraph_format.keep_with_next = True
        stil.paragraph_format.widow_control = True
        stil.paragraph_format.page_break_before = seitenwechsel

    if "Dokumentstatus" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Dokumentstatus", WD_STYLE_TYPE.PARAGRAPH)
        stil.base_style = normal
        stil.font.name = "Calibri"
        stil.font.size = Pt(10)
        stil.font.bold = True
        stil.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
        stil.paragraph_format.space_before = Pt(5)
        stil.paragraph_format.space_after = Pt(5)
        stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


def füge_seitenfeld_hinzu(absatz):
    absatz.add_run("Seite ")
    feld = OxmlElement("w:fldSimple")
    feld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    text = OxmlElement("w:t")
    text.text = "1"
    run.append(text)
    feld.append(run)
    absatz._p.append(feld)


def richte_seiten_ein(doc, version, kennzeichnung):
    abschnitt = doc.sections[0]
    abschnitt.page_width = Cm(21)
    abschnitt.page_height = Cm(29.7)
    abschnitt.top_margin = Cm(2.5)
    abschnitt.bottom_margin = Cm(2.5)
    abschnitt.left_margin = Cm(2.5)
    abschnitt.right_margin = Cm(2.5)
    abschnitt.header_distance = Cm(1.25)
    abschnitt.footer_distance = Cm(1.25)
    abschnitt.different_first_page_header_footer = True

    kopf = abschnitt.header
    p = kopf.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Allgemeines KI-IT-Sicherheitskonzept · Version {version}").bold = True
    p.add_run("\n" + kennzeichnung)
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)

    fuß = abschnitt.footer
    p = fuß.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"{kennzeichnung} · ")
    füge_seitenfeld_hinzu(p)
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)

    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings._element.append(update)


def add_heading(doc, text, ebene):
    p = doc.add_heading(text, level=ebene)
    p.paragraph_format.keep_with_next = True
    return p


def dokumentsteuerung(doc, version, kennzeichnung, katalog):
    add_heading(doc, "Dokumentenlenkung", 1)
    tabelle = doc.add_table(rows=1, cols=2)
    tabelle.style = "Table Grid"
    tabelle.rows[0].cells[0].text = "Merkmal"
    tabelle.rows[0].cells[1].text = "Festlegung"
    daten = [
        ("Dokumenttitel", "Allgemeines KI-IT-Sicherheitskonzept"),
        ("Dokumentstatus", kennzeichnung),
        ("Version", version),
        ("Fachlicher Stichtag", "02.09.2026"),
        ("Normative Quelle", "katalog/ki-it-sicherheitskatalog.oscal.json"),
        ("OSCAL-Fassung", katalog["catalog"]["metadata"]["oscal-version"]),
        ("Betriebsmodell", "vollständig lokal; externe Inferenz nicht anwendbar"),
        ("Modelländerung", "Training und Feinabstimmung ausgeschlossen"),
        ("Herausgeberschaft", "Organisationsneutrales Referenzprojekt; keine amtliche Herausgeberschaft"),
    ]
    for merkmal, festlegung in daten:
        zellen = tabelle.add_row().cells
        zellen[0].text = merkmal
        zellen[1].text = festlegung
    formatiere_tabelle(tabelle, [2200, 6752])
    text_absatz(doc, "Freigabehinweis: Diese Fassung enthält ausschließlich öffentliche, organisationsneutrale Informationen. Eine private Repository-Sichtbarkeit ist keine Freigabe für organisationsspezifische, vertrauliche oder eingestufte Inhalte.", danach=8)


def inhaltsverzeichnis(doc):
    add_heading(doc, "Inhaltsverzeichnis", 1)
    kapitel = [
        "1 Dokumentenlenkung und Status ÖFFENTLICH",
        "2 Zweck, Zielgruppe und Abgrenzung",
        "3 Voraussetzungen des allgemeinen IT-Sicherheitskonzepts",
        "4 Lokale KI-Referenzarchitektur",
        "5 Systemgrenzen, Vertrauenszonen und Datenflüsse",
        "6 Rechts-, Normen- und Anwendbarkeitsmatrix",
        "7 Governance, Rollen und Verantwortlichkeiten",
        "8 KI-Risiko- und Bedrohungsmodell",
        "9 Sicherheitsmaßnahmen entsprechend dem OSCAL-Katalog",
        "10 RAG-, Upload- und Datenkonzept",
        "11 Agentische Anwendungen und lokale Entwicklungsumgebungen",
        "12 Betrieb, Änderung, Modellwechsel, Vorfälle und Außerbetriebnahme",
        "13 Nachweis-, Prüf- und Mappingübersicht",
        "14 Verfahren zur organisationsspezifischen Übernahme",
        "15 Quellenverzeichnis, Glossar und Abkürzungen",
    ]
    for eintrag in kapitel:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(4)
        p.add_run(eintrag)


def kapitel_eins_bis_acht(doc, version, kennzeichnung):
    add_heading(doc, "1 Dokumentenlenkung und Status ÖFFENTLICH", 1)
    text_absatz(doc, f"Dieses Dokument trägt den Status {kennzeichnung}. Es ist eine organisationsneutrale Referenz und keine amtliche Veröffentlichung einer genannten Behörde. Version {version} bildet denselben Kontrollbestand wie der zugehörige OSCAL-Katalog ab.")
    text_absatz(doc, "Sobald reale Organisations-, Infrastruktur-, Schutzbedarfs-, Konto- oder Schwachstelleninformationen ergänzt werden, endet der öffentliche Status. Die Anpassung erfolgt nur in einer getrennten Offline-Fassung; Einstufung und Freigabe bleiben befugten Stellen der übernehmenden Organisation vorbehalten.")
    aufzählung(doc, [
        "Redaktionelles Master: DOCX; die PDF-Lesefassung wird ausschließlich daraus erzeugt.",
        "Normative Anforderungen: OSCAL-Katalog; dieses Dokument erläutert Anwendung und Zusammenwirken.",
        "Änderungslenkung: gemeinsame Versionierung von Katalog, DOCX und PDF sowie vollständige Quellen- und Prüfspur.",
        "Konformitätsgrenze: keine automatische ISO-, BSI-, EU-AI-Act-, VS- oder Systemkonformität und kein Zertifikat.",
    ])

    add_heading(doc, "2 Zweck, Zielgruppe und Abgrenzung", 1)
    text_absatz(doc, "Zweck ist eine prüfbare Referenz für Planung, Freigabe, Betrieb, Änderung und Außerbetriebnahme lokaler generativer KI-Dienste. Adressiert werden Leitung, Informationssicherheit, Datenschutz, Recht, Geheimschutz, Personalvertretung, Fachverantwortung, Architektur, Plattform-, Netz-, Identitäts-, RAG-, Modell-, Test- und Betriebsrollen.")
    text_absatz(doc, "Nicht Gegenstand sind eine produktive Plattform, Beschaffungsempfehlungen, Training, Feinabstimmung, kontinuierliches Lernen oder die pauschale Freigabe eines konkreten Anwendungsfalls. Domänenwissen wird über lokale RAG-Bestände oder kontrollierte lokale On-Demand-Uploads bereitgestellt.")

    add_heading(doc, "3 Voraussetzungen des allgemeinen IT-Sicherheitskonzepts", 1)
    text_absatz(doc, "Die Referenz setzt ein wirksames allgemeines IT-Sicherheitskonzept voraus. Die folgenden Fähigkeiten werden nicht vollständig erneut spezifiziert, sondern nur dort verschärft, wo KI-spezifische Daten-, Modell-, Prompt-, RAG- oder Toolrisiken dies verlangen:")
    aufzählung(doc, [
        "verwaltete Clients und Server, sichere Domäne, lokaler Identitätsprovider, Rollen und MFA;",
        "interne PKI, vertrauenswürdige Zertifikate, Segmentierung, Firewalls und abgesicherter Fernzugriff;",
        "Patch-, Schwachstellen-, Konfigurations- und sichere Softwareverteilung;",
        "lokale Protokollierung, Überwachung, Backup, Wiederherstellung, Notfallmanagement und Schadsoftwareschutz.",
    ])
    text_absatz(doc, "KI-GEL-001 verlangt für jede Übernahme den expliziten Bezug auf diese Basis. Fehlende Basismaßnahmen werden nicht durch den KI-Katalog geheilt und müssen im allgemeinen Sicherheitsprozess behandelt werden.")

    add_heading(doc, "4 Lokale KI-Referenzarchitektur", 1)
    text_absatz(doc, "Die Standardarchitektur ist vollständig lokal. Verwaltete Clients erreichen über HTTPS ausschließlich einen kontrollierten internen KI-Zugang. Dahinter liegt eine getrennte KI-Serverzone mit lokaler Containerplattform, Chat-Oberfläche, Inferenz, RAG, Embeddings, Reranking, Vektor- beziehungsweise Datenbank und technischer Überwachung. Fernzugriff erfolgt nur über ein organisationskontrolliertes VPN mit MFA.")
    arch = doc.add_table(rows=2, cols=3)
    arch.style = "Table Grid"
    titel = ["Clientzone  →", "Kontrollierter KI-Zugang  →", "KI-Serverzone"]
    inhalte = [
        "Browser · agentische Clients · lokales Git\nAusgehend ausschließlich HTTPS",
        "IdP · Rollen · TLS\nModell- und Toolfreigabe\nProtokollierung · Begrenzung",
        "Chat · Inferenz · RAG\nEmbeddings · Datenbank\nMonitoring · kein Egress",
    ]
    for i, wert in enumerate(titel):
        arch.rows[0].cells[i].text = wert
        schattiere(arch.rows[0].cells[i], HELLBLAU)
        for run in arch.rows[0].cells[i].paragraphs[0].runs:
            run.bold = True
        arch.rows[0].cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, wert in enumerate(inhalte):
        arch.rows[1].cells[i].text = wert
        arch.rows[1].cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    formatiere_tabelle(arch, [2700, 3000, 3252])
    p = doc.add_paragraph("Abbildung 1: Abstrakte lokale Referenzarchitektur; Produkte sind austauschbare Beispiele.")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.italic = True
        run.font.size = Pt(9)

    add_heading(doc, "5 Systemgrenzen, Vertrauenszonen und Datenflüsse", 1)
    zonen = [
        ("Verwaltete Clientzone", "Benutzerinteraktion, lokale Entwicklungswerkzeuge und begrenzte agentische Aktionen."),
        ("Kontrollierter KI-Zugang", "Einziger Clientpfad; Identität, Rollen, TLS, Modell-, Kontext-, Raten- und Toolregeln."),
        ("KI-Serverzone", "Interne Inferenz-, RAG-, Daten- und Überwachungsdienste ohne öffentliches oder allgemeines Clientnetz-Exposure."),
        ("Importweg", "Prüfung von Modellen, Images, Paketen und Erweiterungen vor Übernahme in lokale Registrierungen."),
        ("Betriebs- und Nachweisbereich", "Besonders geschützte Protokolle, SIEM-Daten, Freigaben, Sicherungen und Wiederherstellungsdaten."),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Vertrauenszone"
    t.rows[0].cells[1].text = "Aufgabe und Grenze"
    for a, b in zonen:
        z = t.add_row().cells
        z[0].text = a
        z[1].text = b
    formatiere_tabelle(t, [2400, 6552])
    text_absatz(doc, "Das interne Container- oder Pod-Netz gilt nicht als hinreichende Sicherheitsgrenze. Kommunikationsbeziehungen werden standardmäßig verweigert und ausdrücklich erlaubt. Inferenz-, Administrations-, Debug-, Metrik-, Cluster- und Cache-Ports bleiben vom normalen Netz getrennt.")
    text_absatz(doc, "Alle fachlichen Datenflüsse bleiben lokal: Identitäten, Git, Modelle, Dokumente, Embeddings, Indizes, Chats, Protokolle, Telemetrie und Sicherungen. Der Standardbetrieb besitzt keinen Internet-Egress. Artefaktimporte erfolgen über einen kontrollierten separaten Prozess.")

    add_heading(doc, "6 Rechts-, Normen- und Anwendbarkeitsmatrix", 1)
    matrix = [
        ("KI-Verordnung (EU) 2024/1689", "Anwendungsfallbezogen", "Rolle, Risikoklasse, Betreiberpflichten, KI-Kompetenz und Folgenabschätzung prüfen.", "Q-EU-001"),
        ("Datenschutzrecht", "Bei personenbezogenen Daten", "Rechtsgrundlage, Zweck, Minimierung, Rollen, Transparenz, Rechte, Löschung und Folgenabschätzung prüfen.", "Q-BFDI-001; Q-DSK-001 bis Q-DSK-003"),
        ("BSIG und adressatenbezogene BSI-Vorgaben", "Organisationsspezifisch", "Adressat, Verbindlichkeit, Basis-Sicherheitskonzept und Nachweispflichten feststellen.", "Q-BSIG-001; Q-BSI-001"),
        ("Geheimschutz", "Bei entsprechend geschützten Inhalten", "Verarbeitung nur nach befugter Einstufung, Systemzulässigkeit und ausdrücklicher Freigabe.", "Q-SUEG-001; Q-VSA-001"),
        ("ISO/IEC 27001 und 27002", "Orientierende Zuordnung", "Lizenzierte Normtexte und unabhängige Bewertung für eine Konformitätsaussage erforderlich.", "Q-ISO-27001; Q-ISO-27002"),
        ("ISO/IEC 42001, 23894, 42005, 5338, 5259, 25059", "Orientierende KI-Zuordnung", "Nur öffentliche Metadaten und Kennungen; keine Wiedergabe proprietärer Anforderungen.", "Q-ISO-42001; Q-ISO-23894; Q-ISO-42005; Q-ISO-5338; Q-ISO-5259; Q-ISO-25059"),
    ]
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for i, wert in enumerate(("Grundlage", "Anwendbarkeit", "Erforderliche organisationsspezifische Klärung", "Quellen")):
        t.rows[0].cells[i].text = wert
    for zeile in matrix:
        z = t.add_row().cells
        for i, wert in enumerate(zeile):
            z[i].text = wert
    formatiere_tabelle(t, [1900, 1450, 3950, 1652])
    text_absatz(doc, "Die Matrix ist ein Prüfungseinstieg und keine Rechtsberatung. Fachgesetze, Mitbestimmung und behördenspezifische Vorschriften sind je Organisation und Anwendungsfall zu ergänzen.")

    add_heading(doc, "7 Governance, Rollen und Verantwortlichkeiten", 1)
    rollen = [
        ("Leitung", "Risikobereitschaft, Ressourcen, wesentliche Restrisiken und Freigaberahmen."),
        ("KI-Verantwortliche", "Inventar, Anwendungsfälle, Modell- und Richtlinienfreigaben sowie koordinierter Lebenszyklus."),
        ("Informationssicherheit", "Bedrohungsmodell, Kontrollanforderungen, Prüfung, Vorfälle und Basis-ISMS-Verknüpfung."),
        ("Datenschutz, Recht, Geheimschutz, Personalvertretung", "Anwendbarkeitsprüfung, Beteiligung, Bedingungen und befugte Freigaben im jeweiligen Zuständigkeitsbereich."),
        ("Architektur, Netz, Plattform, Identität und Gateway", "Technische Zonen, Egress, Laufzeitbaseline, Identitäten, Zertifikate und Richtliniendurchsetzung."),
        ("Modell, RAG, Daten und Tools", "Provenienz, Integrität, ACLs, Löschung, Erweiterungsfreigabe und fachliche Datenverantwortung."),
        ("Test und Betrieb", "Reproduzierbare Evaluation, Regression, Monitoring, Protokollierung, Wiederanlauf und Außerbetriebnahme."),
        ("Nutzende", "Zweckgebundene Nutzung, Schutzregeln, Ergebnisprüfung und Meldung von Auffälligkeiten."),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Rolle"
    t.rows[0].cells[1].text = "Kernverantwortung"
    for rolle, aufgabe in rollen:
        z = t.add_row().cells
        z[0].text = rolle
        z[1].text = aufgabe
    formatiere_tabelle(t, [2400, 6552])
    text_absatz(doc, "Eine Person kann mehrere Rollen wahrnehmen, sofern Interessenkonflikte und notwendige unabhängige Prüfungen behandelt werden. Verantwortung darf nicht an das Sprachmodell oder eine automatisierte Agentenkette delegiert werden.")

    add_heading(doc, "8 KI-Risiko- und Bedrohungsmodell", 1)
    text_absatz(doc, "Das Bedrohungsmodell erweitert das allgemeine IT-Modell um probabilistische Ausgaben, untrusted Kontext, Modell- und Wissenslieferketten sowie agentische Wirkungsketten. Es betrachtet Eingabe, Modell, Systemanweisung, RAG, Tool, Client, Schnittstelle, Plattform, Protokoll und Importpfad.")
    bedrohungen = [
        ("Prompt Injection", "Direkte oder indirekte Anweisungen überschreiben beabsichtigte Regeln.", "Kontexttrennung, Tool-Policy, Bestätigung, Tests und Monitoring."),
        ("Poisoning und manipulierte Provenienz", "Modell- oder RAG-Artefakte verändern Verhalten und Quellenlage.", "Kontrollierter Import, Hash, Signatur, Herkunft, Freigabe und Rollback."),
        ("Datenabfluss und Rekonstruktion", "Prompts, Embeddings, Caches, Ausgaben oder Tools überschreiten Berechtigungen.", "ACL vor Aufnahme und Abfrage, Minimierung, Egress-Verbot und Ausgabeprüfung."),
        ("Unsichere Modellausgabe", "Fehlerhafte Inhalte oder Code erhalten reale Folgewirkung.", "Validierung, menschliche Freigabe, sichere Weiterverarbeitung und Kennzeichnung."),
        ("Übermäßige Agentenrechte", "Modellfehler führen zu Datei-, Befehls- oder Netzwerkaktionen.", "Getrennte Fähigkeiten, Least Privilege, konkrete Bestätigung und Auditspur."),
        ("Ressourcenerschöpfung", "Kontexte, Schleifen und Last verdrängen lokale Dienste.", "Quoten, Timeouts, Queueing, Ressourcenlimits und sichere Beendigung."),
        ("Drift und Regression", "Geänderte Kette verschlechtert Sicherheit oder Qualität.", "Versionierte Freigabe, Regression, Betriebsmetriken und getesteter Rollback."),
    ]
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for i, wert in enumerate(("Szenario", "Auswirkung", "Behandlungsschwerpunkt")):
        t.rows[0].cells[i].text = wert
    for zeile in bedrohungen:
        z = t.add_row().cells
        for i, wert in enumerate(zeile):
            z[i].text = wert
    formatiere_tabelle(t, [1900, 3300, 3752])
    text_absatz(doc, "Bewertungen werden vor Erstnutzung, mindestens jährlich und nach wesentlichen Änderungen wiederholt. Akzeptierte Restrisiken bleiben sichtbar, befristet und einer befugten Rolle zugeordnet.")


def kapitel_neun(doc, katalog, quellen_nach_uuid):
    add_heading(doc, "9 Sicherheitsmaßnahmen entsprechend dem OSCAL-Katalog", 1)
    text_absatz(doc, "Die folgenden Kontrollblöcke übernehmen die normative Anforderung unverändert aus dem OSCAL-Katalog und erläutern Begründung, Referenzumsetzung, Prüfziel und Nachweise. Quellen- und Mappingangaben sind nachvollziehbare Zuordnungen; sie stellen keine Zertifizierung oder behördliche Freigabe dar.")
    for gruppenindex, gruppe in enumerate(katalog["catalog"]["groups"], start=1):
        add_heading(doc, f"9.{gruppenindex} {gruppe['title']}", 2)
        for control in gruppe.get("controls", []):
            kennung = prop(control, "alt-identifier")[0]
            kontrollüberschrift = add_heading(doc, f"{kennung} – {control['title']}", 3)
            felder = [
                ("Normative Anforderung", teil(control, "statement")),
                ("Begründung", teil(control, "rationale")),
                ("Umsetzung in der Referenzarchitektur", teil(control, "guidance")),
                ("Prüfziel", teil(control, "assessment-objective")),
                ("Erwartete Nachweise", teil(control, "evidence")),
            ]
            for feldindex, (merkmal, inhalt) in enumerate(felder):
                p = doc.add_paragraph()
                setze_absatzformat(p, danach=7)
                label = p.add_run(merkmal + "\n")
                label.bold = True
                label.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
                p.add_run(inhalt)
                if feldindex == 0:
                    p_pr = p._p.get_or_add_pPr()
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:fill"), HELLGRAU)
                    p_pr.append(shd)
                    p.paragraph_format.keep_together = True

            metadaten = doc.add_table(rows=1, cols=2)
            metadaten.style = "Table Grid"
            metadaten.rows[0].cells[0].text = "Steuermerkmal"
            metadaten.rows[0].cells[1].text = "Ausprägung"
            daten = [
                ("Anwendbarkeit", ", ".join(prop(control, "anwendbarkeit"))),
                ("Lebenszyklus und Rollen", f"{', '.join(prop(control, 'lebenszyklus')).replace(';', '; ')}; {', '.join(prop(control, 'rolle')).replace(';', '; ')}"),
                ("Orientierende Zuordnung", f"BSI/IT-Grundschutz: {', '.join(prop(control, 'mapping-bsi-it-grundschutz'))}; ISO: {', '.join(prop(control, 'mapping-iso'))}"),
            ]
            for merkmal, inhalt in daten:
                z = metadaten.add_row().cells
                z[0].text = merkmal
                z[1].text = inhalt
            formatiere_tabelle(metadaten, [2200, 6752])

            quelle_p = doc.add_paragraph()
            setze_absatzformat(quelle_p, davor=6, danach=10)
            label = quelle_p.add_run("Quellen\n")
            label.bold = True
            label.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
            zitate = []
            kurzangaben = []
            for link in control["links"]:
                q = quellen_nach_uuid[link["href"][1:]]
                fundstelle = link["text"].split("] ", 1)[1]
                kurzangaben.append(link["text"])
                zitate.append(vollzitat(q, fundstelle))
            quelle_p.add_run("; ".join(kurzangaben))
            fußnotenmarke(quelle_p, " | ".join(zitate))
            p_pr = quelle_p._p.get_or_add_pPr()
            p_bdr = OxmlElement("w:pBdr")
            unten = OxmlElement("w:bottom")
            unten.set(qn("w:val"), "single")
            unten.set(qn("w:sz"), "8")
            unten.set(qn("w:space"), "6")
            unten.set(qn("w:color"), BLAU)
            p_bdr.append(unten)
            p_pr.append(p_bdr)


def kapitel_zehn_bis_vierzehn(doc, katalog):
    add_heading(doc, "10 RAG-, Upload- und Datenkonzept", 1)
    text_absatz(doc, "Domänenwissen verbleibt außerhalb der Modellgewichte. Lokale RAG-Bestände und lokale On-Demand-Uploads bilden die einzigen vorgesehenen Zuführungswege. KI-RAG-001 bis KI-RAG-004 fordern eine Quarantäne und isolierte Parser, Herkunfts- und Klassifikationsmetadaten, Berechtigungsprüfung vor Aufnahme und erneut bei jeder Abfrage, durchgängige ACL-Trennung sowie vollständige Aufbewahrungs- und Löschsteuerung.")
    aufzählung(doc, [
        "Embeddings, Chunks, Indizes, Caches und Reranking-Daten erhalten mindestens den Schutzbedarf der Quelldaten.",
        "Das Sprachmodell und Systemanweisungen treffen keine Zugriffsentscheidung.",
        "On-Demand-Uploads bleiben ohne ausdrückliche persistente Freigabe sitzungsbezogen.",
        "Ausgaben weisen verwendete Quellen und konkrete Fundstellen nachvollziehbar aus.",
        "Löschung umfasst Onlinekopien, Ableitungen, Caches und den geregelten Ablauf in Sicherungsketten.",
    ])
    text_absatz(doc, "KI-TRN-001 stellt klar, dass Indexierung und Embedding-Erzeugung keine Freigabe für Training, Feinabstimmung oder Änderungen von Modellgewichten sind.")

    add_heading(doc, "11 Agentische Anwendungen und lokale Entwicklungsumgebungen", 1)
    text_absatz(doc, "Agentische Clients wie Cline- oder OpenCode-artige Werkzeuge sind Produktbeispiele. Sie greifen ausschließlich über den lokalen HTTPS-Zugang auf freigegebene Modelle zu. Lokale Git-, Paket- und Entwicklungsdienste bleiben in der Organisationsumgebung.")
    aufzählung(doc, [
        "Arbeitsbereichs- und Dateirechte sind minimal und überschreiten weder Projekt noch genehmigten Zweck.",
        "Lesen, Schreiben, Befehlsausführung und Netzwerkzugriff sind getrennte Fähigkeiten.",
        "Kritische, destruktive, privilegierte oder externe Aktionen benötigen eine konkrete menschliche Bestätigung.",
        "Indirekte Prompt Injection aus Quellcode, Dokumenten, Webseiten und Tool-Ausgaben darf keine Rechte erweitern.",
        "Plug-ins, MCP-Server, Erweiterungen und Pakete stammen aus kontrollierten lokalen Quellen und sind versionsfixiert.",
        "Tool-Aufrufe werden identitätsbezogen, nachvollziehbar und datensparsam lokal protokolliert.",
    ])

    add_heading(doc, "12 Betrieb, Änderung, Modellwechsel, Vorfälle und Außerbetriebnahme", 1)
    text_absatz(doc, "Der Betrieb verbindet Freigabemanifest, lokale Protokollierung, SIEM-Auswertung, Qualitäts- und Sicherheitsmetriken, Driftbeobachtung, Kapazitätsgrenzen und den allgemeinen Vorfallprozess. Eine laufende Komponente allein belegt weder Berechtigung, Qualität, Datenlöschung noch Wiederherstellbarkeit.")
    text_absatz(doc, "Jede Änderung an Modell, Quantisierung, Laufzeit, Systemanweisung, RAG, Embedding, Reranker, Gateway, Tool oder Sicherheitsparameter löst eine risikobasierte Regression und Wiederfreigabe aus. Vorherige geprüfte Kombinationen bleiben kontrolliert rückrollbar. Wiederanlaufprüfungen erfolgen ohne Internetzugang und umfassen Hashes, Richtlinien, ACLs und Kernevaluation.")
    text_absatz(doc, "Bei Außerbetriebnahme werden Identitäten, Zertifikate, Geheimnisse, Endpunkte, Jobs, Modelle, Daten, Indizes und Caches behandelt. Erforderliche Auditnachweise bleiben entsprechend Aufbewahrung erhalten; unzulässige Restkopien und Erreichbarkeit müssen durch Nachtests ausgeschlossen werden.")

    add_heading(doc, "13 Nachweis-, Prüf- und Mappingübersicht", 1)
    text_absatz(doc, "Die Übersicht dient der Prüfplanung. Der vollständige Wortlaut, die Quellenlinks und sämtliche Eigenschaften verbleiben im OSCAL-Katalog.")
    t = doc.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    for i, wert in enumerate(("Kontrolle", "Titel", "Anwendbarkeit", "BSI/IT-Grundschutz", "ISO-Kennungen")):
        t.rows[0].cells[i].text = wert
    for gruppe in katalog["catalog"]["groups"]:
        for control in gruppe.get("controls", []):
            z = t.add_row().cells
            werte = (
                prop(control, "alt-identifier")[0], control["title"],
                ", ".join(prop(control, "anwendbarkeit")),
                ", ".join(prop(control, "mapping-bsi-it-grundschutz")),
                ", ".join(prop(control, "mapping-iso")),
            )
            for i, wert in enumerate(werte):
                z[i].text = wert
    formatiere_tabelle(t, [1050, 2850, 1300, 1650, 2102])

    add_heading(doc, "14 Verfahren zur organisationsspezifischen Übernahme", 1)
    text_absatz(doc, "Eine Übernahme beginnt niemals durch direkte Ergänzung dieses Referenzrepositorys. Vor der ersten Organisationsangabe wird eine getrennte, angemessen geschützte Offline-Fassung erstellt. Der Statusmechanismus setzt Deckblatt, Kopfzeilen und Metadaten auf die Kennzeichnung, dass eine Einstufung durch die Organisation erforderlich ist.")
    schritte = [
        "Geltungsbereich, Verantwortliche, Schutz- und Informationsklassifikation durch befugte Stellen festlegen.",
        "Reale Architektur ausschließlich in der geschützten Fassung erfassen und Vertrauenszonen sowie Datenflüsse verifizieren.",
        "Rechts-, Datenschutz-, Geheimschutz- und Beteiligungsprüfung je Anwendungsfall durchführen.",
        "Kontrollanwendbarkeit, Basisabhängigkeiten, konkrete Umsetzung, Nachweise und Restrisiken bestimmen.",
        "Technische Negativ- und Wirksamkeitstests in der tatsächlichen Umgebung durchführen.",
        "Unabhängige Fachprüfung, Risikofreigabe und gegebenenfalls formale Einstufung dokumentieren.",
        "Änderungs-, Vorfall-, Wiederanlauf-, Modellwechsel- und Außerbetriebnahmeverfahren betreiben.",
    ]
    for nummer, schritt in enumerate(schritte, start=1):
        text_absatz(doc, f"{nummer}. {schritt}", danach=4)
    text_absatz(doc, "Externe Inferenz ist ein eigener Systemgrenzenwechsel. Sie darf nicht als einfache Konfigurationsvariante übernommen werden, sondern erfordert die vollständige Neubewertung nach KI-EXT-001 und KI-EXT-002.")


def kapitel_fünfzehn(doc, register):
    add_heading(doc, "15 Quellenverzeichnis, Glossar und Abkürzungen", 1)
    add_heading(doc, "15.1 Quellenverzeichnis", 2)
    text_absatz(doc, "Maßgeblich ist das maschinenlesbare Quellenregister. Die folgenden Angaben verwenden den Prüfstand 02.09.2026. Bei HTML-Dokumentation ohne ausgewiesenes Veröffentlichungsdatum wird ausdrücklich der Abrufstand genannt.")
    for quelle in register["quellen"]:
        datum = quelle["veröffentlichungsdatum"] or quelle["stand"]
        fundstellen = "; ".join(f["fundstelle"] for f in quelle["verwendete_fundstellen"])
        p = doc.add_paragraph()
        setze_absatzformat(p, danach=7)
        p.add_run(f"[{quelle['id']}] ").bold = True
        p.add_run(f"{quelle['herausgeber']}: {quelle['titel']}, {quelle['fassung']}, {datum}, {fundstellen}, ")
        hyperlink(p, "öffentliche Fundstelle", quelle["öffentliche_url"])
        p.add_run(f", abgerufen am 02.09.2026. Autoritätsstufe: {quelle['autoritätsstufe']}. Wiedervorlage: {quelle['wiedervorlage_am']}.")
    add_heading(doc, "15.2 Glossar", 2)
    glossar = [
        ("Agentische Anwendung", "Client oder Dienst, der Modellausgaben in Datei-, Tool-, Befehls- oder Netzwerkaktionen überführen kann."),
        ("Embedding", "Numerische Repräsentation eines Inhalts für Ähnlichkeitssuche; kann Schutzbedarf und Personenbezug der Quelle bewahren."),
        ("Feinabstimmung", "Veränderung vortrainierter Modellgewichte für Aufgaben oder Datenbestände; innerhalb dieses Konzepts ausgeschlossen."),
        ("Inferenz", "Ausführung eines vortrainierten Modells zur Erzeugung einer Ausgabe ohne beabsichtigte Änderung der Modellgewichte."),
        ("On-Demand-Upload", "Temporär und lokal bereitgestelltes Dokument für einen begrenzten Nutzungskontext."),
        ("Prompt Injection", "Eingabe oder eingebettete Anweisung, die beabsichtigte Regeln, Kontextgrenzen oder Toolentscheidungen beeinflussen soll."),
        ("RAG", "Retrieval Augmented Generation; lokale Suche liefert freigegebene Textausschnitte als Kontext für die Inferenz."),
        ("Untrusted", "Nicht als Steueranweisung vertrauenswürdig; der Inhalt kann fehlerhaft oder absichtlich manipuliert sein."),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Begriff"
    t.rows[0].cells[1].text = "Bedeutung in dieser Referenz"
    for begriff, bedeutung in glossar:
        z = t.add_row().cells
        z[0].text = begriff
        z[1].text = bedeutung
    formatiere_tabelle(t, [2200, 6752])

    add_heading(doc, "15.3 Abkürzungen", 2)
    abkürzungen = [
        ("ACL", "Access Control List"), ("API", "Application Programming Interface"),
        ("BfDI", "Die Bundesbeauftragte für den Datenschutz und die Informationsfreiheit"),
        ("BMI", "Bundesministerium des Innern"), ("BMVg", "Bundesministerium der Verteidigung"),
        ("BSI", "Bundesamt für Sicherheit in der Informationstechnik"),
        ("DSK", "Konferenz der unabhängigen Datenschutzaufsichtsbehörden des Bundes und der Länder"),
        ("IdP", "Identity Provider"), ("ISMS", "Informationssicherheitsmanagementsystem"),
        ("KI", "Künstliche Intelligenz"), ("MFA", "Mehrfaktorauthentisierung"),
        ("MCP", "Model Context Protocol"), ("OSCAL", "Open Security Controls Assessment Language"),
        ("RAG", "Retrieval Augmented Generation"), ("SIEM", "Security Information and Event Management"),
        ("TLS", "Transport Layer Security"), ("VPN", "Virtual Private Network"),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Abkürzung"
    t.rows[0].cells[1].text = "Langform"
    for kurz, lang in abkürzungen:
        z = t.add_row().cells
        z[0].text = kurz
        z[1].text = lang
    formatiere_tabelle(t, [1800, 7152])


def erzeuge_docx(ziel):
    FOOTNOTES.clear()
    katalog = lade_json(KATALOG_PFAD)
    register = lade_json(REGISTER_PFAD)
    status = lade_json(STATUS_PFAD)
    version = katalog["catalog"]["metadata"]["version"]
    kennzeichnung = NICHT_ÖFFENTLICH if status["organisationsspezifisch"] else ÖFFENTLICH
    if status["modelltraining"] or status["feinabstimmung"]:
        raise SystemExit("Dokumenterzeugung abgebrochen: Training und Feinabstimmung sind unzulässig.")
    if status["organisationsspezifisch"] is False and status["dokumentstatus"] != "ÖFFENTLICH":
        raise SystemExit("Dokumenterzeugung abgebrochen: inkonsistenter öffentlicher Projektstatus.")

    doc = Document()
    richte_stile_ein(doc)
    richte_seiten_ein(doc, version, kennzeichnung)
    eigenschaften = doc.core_properties
    eigenschaften.title = "Allgemeines KI-IT-Sicherheitskonzept"
    eigenschaften.subject = kennzeichnung
    eigenschaften.keywords = "KI, Informationssicherheit, OSCAL, RAG, lokale Inferenz"
    eigenschaften.author = ""
    eigenschaften.last_modified_by = ""
    eigenschaften.comments = "Organisationsneutrale Referenzvorlage"

    # editorial_cover: zurückhaltendes, zentriertes Deckblatt ohne Logos oder Amtsanmutung.
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ALLGEMEINES\nKI-IT-SICHERHEITSKONZEPT")
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(24)
    run.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
    setze_absatzformat(p, danach=20)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Audit- und zertifizierungsvorbereitende Referenz für vollständig lokale KI-Infrastrukturen")
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    setze_absatzformat(p, danach=26)
    status_p = doc.add_paragraph(style="Dokumentstatus")
    status_p.add_run(kennzeichnung)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Version {version} · Fachlicher Stichtag 02.09.2026")
    setze_absatzformat(p, danach=18)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Keine amtliche Veröffentlichung · keine Systemfreigabe · kein Zertifikat")
    run.italic = True
    run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    doc.add_page_break()

    dokumentsteuerung(doc, version, kennzeichnung, katalog)
    doc.add_page_break()
    inhaltsverzeichnis(doc)
    kapitel_eins_bis_acht(doc, version, kennzeichnung)
    quellen_nach_uuid = {q["oscal_uuid"]: q for q in register["quellen"]}
    kapitel_neun(doc, katalog, quellen_nach_uuid)
    kapitel_zehn_bis_vierzehn(doc, katalog)
    kapitel_fünfzehn(doc, register)

    ziel.parent.mkdir(parents=True, exist_ok=True)
    doc.save(ziel)
    ergänze_fußnotenpaket(ziel)
    print(f"DOCX erzeugt: {ziel}")
    print(f"Version {version}; {sum(len(g.get('controls', [])) for g in katalog['catalog']['groups'])} Kontrollen; {len(FOOTNOTES)} Quellenfußnoten")


def main():
    befehle = argparse.ArgumentParser(description=__doc__)
    befehle.add_argument("--ziel", type=Path, default=ZIEL, help="Zielpfad des DOCX-Masterdokuments.")
    argumente = befehle.parse_args()
    ziel = argumente.ziel if argumente.ziel.is_absolute() else WURZEL / argumente.ziel
    erzeuge_docx(ziel)


if __name__ == "__main__":
    main()
