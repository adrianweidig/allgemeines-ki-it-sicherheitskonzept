#!/usr/bin/env python3
"""Erzeugt das redaktionelle DOCX-Master aus OSCAL-Katalog und Quellenregister.

Das PDF wird anschließend ausschließlich aus diesem DOCX mit dem dokumentierten
Renderverfahren erzeugt. Der Katalog bleibt die normative Quelle.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from lxml import etree


WURZEL = Path(__file__).resolve().parents[1]
KATALOG_PFAD = WURZEL / "katalog" / "ki-it-sicherheitskatalog.oscal.json"
REGISTER_PFAD = WURZEL / "quellen" / "quellenregister.json"
STATUS_PFAD = WURZEL / "projektstatus.json"
ZIEL = WURZEL / "konzept" / "ki-it-sicherheitskonzept.docx"
MEDIEN_PFAD = WURZEL / "dokumentation" / "medien"
ARCHITEKTUR_ABBILDUNG = MEDIEN_PFAD / "architektur.png"
ARTEFAKTIMPORT_ABBILDUNG = MEDIEN_PFAD / "artefaktimport.png"
RISIKOBEWERTUNG_ABBILDUNG = MEDIEN_PFAD / "risikobewertung.png"
RISIKOMATRIX_ABBILDUNG = MEDIEN_PFAD / "risikomatrix.png"
RAG_ABBILDUNG = MEDIEN_PFAD / "rag-datenfluss.png"
AGENTEN_ABBILDUNG = MEDIEN_PFAD / "agentische-werkzeugnutzung.png"

ÖFFENTLICH = "ÖFFENTLICH – organisationsneutrale Referenzvorlage"
NICHT_ÖFFENTLICH = "NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH"

# standard_business_brief mit benannter A4-Behördenpapier-Übersteuerung:
# A4 210 × 297 mm, Ränder 25 mm, nutzbare Breite 160 mm (9.072 DXA).
SEITENBREITE_DXA = 11906
INHALTSBREITE_DXA = 9072
TABELLENEINZUG_DXA = 150
TABELLENBREITE_DXA = INHALTSBREITE_DXA - TABELLENEINZUG_DXA
BLAU = "2E74B5"
DUNKELBLAU = "1F4D78"
HELLBLAU = "E8EEF5"
HELLGRAU = "F5F7FA"
DUNKELGRAU = "3F4A54"
MITTELGRAU = "77838F"
RAHMENGRAU = "AAB4BF"
INNENRAHMEN = "D5DBE1"

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


def setze_zellenränder(zelle, oben=120, unten=120, start=150, ende=150):
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


def setze_tabellenrahmen(tabelle):
    tbl_pr = tabelle._tbl.tblPr
    rahmen = tbl_pr.find(qn("w:tblBorders"))
    if rahmen is None:
        rahmen = OxmlElement("w:tblBorders")
        tbl_pr.append(rahmen)
    for name, farbe, stärke in (
        ("top", RAHMENGRAU, 6),
        ("left", RAHMENGRAU, 6),
        ("bottom", RAHMENGRAU, 6),
        ("right", RAHMENGRAU, 6),
        ("insideH", INNENRAHMEN, 4),
        ("insideV", INNENRAHMEN, 4),
    ):
        element = rahmen.find(qn(f"w:{name}"))
        if element is None:
            element = OxmlElement(f"w:{name}")
            rahmen.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), str(stärke))
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), farbe)


def formatiere_tabelle(
    tabelle,
    breiten,
    *,
    kopf=True,
    einzug=TABELLENEINZUG_DXA,
    zentrierte_spalten=frozenset(),
):
    if len(breiten) != len(tabelle.columns):
        raise ValueError("Für jede Tabellenspalte muss genau eine Breite festgelegt sein.")
    if sum(breiten) != TABELLENBREITE_DXA:
        raise ValueError(
            f"Tabellenbreiten müssen zusammen {TABELLENBREITE_DXA} DXA ergeben, "
            f"erhalten: {sum(breiten)} DXA."
        )
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

    tbl_grid = tabelle._tbl.tblGrid
    for spalte in list(tbl_grid):
        tbl_grid.remove(spalte)
    for breite in breiten:
        spalte = OxmlElement("w:gridCol")
        spalte.set(qn("w:w"), str(breite))
        tbl_grid.append(spalte)

    setze_tabellenrahmen(tabelle)
    for zeilenindex, zeile in enumerate(tabelle.rows):
        verhindere_zeilentrennung(zeile)
        if kopf and zeilenindex == 0:
            wiederhole_kopfzeile(zeile)
        for index, zelle in enumerate(zeile.cells):
            setze_zellenbreite(zelle, Pt(breiten[index] / 20))
            setze_zellenränder(zelle)
            zelle.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            ist_kopf = kopf and zeilenindex == 0
            if ist_kopf:
                schattiere(zelle, HELLBLAU)
            for absatz in zelle.paragraphs:
                absatz.style = "Tabellenkopf" if ist_kopf else "Tabellentext"
                absatz.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if ist_kopf or index in zentrierte_spalten
                    else WD_ALIGN_PARAGRAPH.LEFT
                )


def normalisiere_listenpunkt(text):
    punkt = text.strip()
    if punkt.endswith((";", ",")):
        punkt = punkt[:-1].rstrip()
    if not re.search(r"[.!?]$", punkt):
        punkt += "."
    return punkt


def setze_absatzformat(absatz, *, danach=6, davor=0, zeilen=1.15, zusammenhalten=False):
    fmt = absatz.paragraph_format
    fmt.space_after = Pt(danach)
    fmt.space_before = Pt(davor)
    fmt.line_spacing = zeilen
    fmt.widow_control = True
    if zusammenhalten:
        fmt.keep_with_next = True


def unterdrücke_silbentrennung(absatz):
    p_pr = absatz._p.get_or_add_pPr()
    sperre = p_pr.find(qn("w:suppressAutoHyphens"))
    if sperre is None:
        sperre = OxmlElement("w:suppressAutoHyphens")
        p_pr.append(sperre)
    sperre.set(qn("w:val"), "true")


def text_absatz(container, text, *, fett_prefix=None, stil=None, danach=6, davor=0):
    absatz = container.add_paragraph(style=stil or "Fließtext")
    setze_absatzformat(absatz, danach=danach, davor=davor)
    if fett_prefix and text.startswith(fett_prefix):
        absatz.add_run(fett_prefix).bold = True
        absatz.add_run(text[len(fett_prefix):])
    else:
        absatz.add_run(text)
    return absatz


def begriffsdefinition(container, begriff, bedeutung):
    """Setzt eine kurze Definition kompakt und ohne überdehnten Blocksatz."""
    absatz = container.add_paragraph(style="Begriffsdefinition")
    absatz.add_run(f"{begriff}:").bold = True
    absatz.add_run(f" {bedeutung}")
    return absatz


def füge_abbildung_hinzu(doc, pfad, beschriftung, alternativtext, *, breite_cm=16.0):
    """Fügt eine ausschließlich inline platzierte, barrierearme Abbildung ein."""
    if not pfad.is_file():
        raise FileNotFoundError(f"Abbildung fehlt: {pfad}")
    absatz = doc.add_paragraph()
    absatz.alignment = WD_ALIGN_PARAGRAPH.CENTER
    setze_absatzformat(absatz, danach=0, zusammenhalten=True)
    run = absatz.add_run()
    inline = run.add_picture(str(pfad), width=Cm(breite_cm))._inline
    inline.docPr.set("title", beschriftung.split(":", 1)[0])
    inline.docPr.set("descr", alternativtext)
    beschriftungsabsatz = doc.add_paragraph(beschriftung, style="Abbildungsbeschriftung")
    beschriftungsabsatz.paragraph_format.keep_together = True
    return beschriftungsabsatz


def aufzählung(container, punkte):
    for punkt in punkte:
        absatz = container.add_paragraph(style="List Bullet")
        fmt = absatz.paragraph_format
        fmt.left_indent = Inches(0.5)
        fmt.first_line_indent = Inches(-0.25)
        fmt.space_after = Pt(5)
        fmt.line_spacing = 1.15
        fmt.widow_control = True
        absatz.add_run(normalisiere_listenpunkt(punkt))


def nummerierte_liste(container, punkte):
    for punkt in punkte:
        absatz = container.add_paragraph(style="List Number")
        fmt = absatz.paragraph_format
        fmt.left_indent = Inches(0.5)
        fmt.first_line_indent = Inches(-0.25)
        fmt.space_after = Pt(5)
        fmt.line_spacing = 1.15
        fmt.widow_control = True
        absatz.add_run(normalisiere_listenpunkt(punkt))


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
    return (
        f"{quelle['herausgeber']}: {quelle['titel']}, {quelle['fassung']}, {quellendatum(quelle)}, "
        f"{fundstelle}, {quelle['öffentliche_url']}, abgerufen am {deutsches_datum(quelle['abrufdatum'])}."
    )


def deutsches_datum(wert):
    """Formatiert ein ISO-Datum für die deutschsprachige Dokumentfassung."""
    try:
        return date.fromisoformat(wert).strftime("%d.%m.%Y")
    except (TypeError, ValueError):
        return str(wert)


def quellendatum(quelle):
    """Gibt Stand und, soweit abweichend, das Veröffentlichungsdatum aus."""
    stand = str(quelle["stand"])
    if re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", stand):
        angabe = f"Stand {stand}"
    elif stand.casefold().startswith(("stand ", "pdf-stand", "abrufstand", "gültigkeitsbeginn", "commit ")):
        angabe = stand
    else:
        angabe = f"Stand {stand}"

    veröffentlicht = quelle.get("veröffentlichungsdatum")
    if not veröffentlicht:
        return angabe
    veröffentlicht_de = deutsches_datum(veröffentlicht)
    if veröffentlicht_de in stand:
        return angabe
    try:
        datum = date.fromisoformat(veröffentlicht)
        monate = (
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember",
        )
        if datum.day == 1 and f"{monate[datum.month - 1]} {datum.year}".casefold() in stand.casefold():
            return angabe
    except (TypeError, ValueError):
        pass
    return f"{angabe}, veröffentlicht am {veröffentlicht_de}"


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
            abstand = etree.SubElement(p_pr, f"{{{ns_w}}}spacing")
            abstand.set(f"{{{ns_w}}}after", "40")
            abstand.set(f"{{{ns_w}}}line", "252")
            abstand.set(f"{{{ns_w}}}lineRule", "auto")
            r_pr = etree.SubElement(style, f"{{{ns_w}}}rPr")
            etree.SubElement(r_pr, f"{{{ns_w}}}rFonts").set(f"{{{ns_w}}}ascii", "Calibri")
            etree.SubElement(r_pr, f"{{{ns_w}}}sz").set(f"{{{ns_w}}}val", "17")
            etree.SubElement(r_pr, f"{{{ns_w}}}lang").set(f"{{{ns_w}}}val", "de-DE")
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
            etree.SubElement(p_pr, f"{{{ns_w}}}suppressAutoHyphens").set(f"{{{ns_w}}}val", "true")
            abstand = etree.SubElement(p_pr, f"{{{ns_w}}}spacing")
            abstand.set(f"{{{ns_w}}}before", "0")
            abstand.set(f"{{{ns_w}}}after", "40")
            abstand.set(f"{{{ns_w}}}line", "252")
            abstand.set(f"{{{ns_w}}}lineRule", "auto")
            ref_run = etree.SubElement(p, f"{{{ns_w}}}r")
            ref_pr = etree.SubElement(ref_run, f"{{{ns_w}}}rPr")
            etree.SubElement(ref_pr, f"{{{ns_w}}}rStyle").set(f"{{{ns_w}}}val", "FootnoteReference")
            etree.SubElement(ref_run, f"{{{ns_w}}}footnoteRef")
            text_run = etree.SubElement(p, f"{{{ns_w}}}r")
            text_pr = etree.SubElement(text_run, f"{{{ns_w}}}rPr")
            text_schrift = etree.SubElement(text_pr, f"{{{ns_w}}}rFonts")
            text_schrift.set(f"{{{ns_w}}}ascii", "Calibri")
            text_schrift.set(f"{{{ns_w}}}hAnsi", "Calibri")
            etree.SubElement(text_pr, f"{{{ns_w}}}sz").set(f"{{{ns_w}}}val", "17")
            etree.SubElement(text_pr, f"{{{ns_w}}}szCs").set(f"{{{ns_w}}}val", "17")
            etree.SubElement(text_pr, f"{{{ns_w}}}lang").set(f"{{{ns_w}}}val", "de-DE")
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
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.widow_control = True
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    sprache = normal._element.rPr.find(qn("w:lang"))
    if sprache is None:
        sprache = OxmlElement("w:lang")
        normal._element.rPr.append(sprache)
    sprache.set(qn("w:val"), "de-DE")
    sprache.set(qn("w:eastAsia"), "de-DE")

    if "Fließtext" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Fließtext", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Fließtext"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(11)
    stil.font.color.rgb = RGBColor.from_string("202830")
    stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    stil.paragraph_format.space_before = Pt(0)
    stil.paragraph_format.space_after = Pt(6)
    stil.paragraph_format.line_spacing = 1.15
    stil.paragraph_format.widow_control = True
    stil._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    stil._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    stil._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    if "Begriffsdefinition" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Begriffsdefinition", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Begriffsdefinition"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(10.5)
    stil.font.color.rgb = RGBColor.from_string("202830")
    stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    stil.paragraph_format.space_before = Pt(0)
    stil.paragraph_format.space_after = Pt(3)
    stil.paragraph_format.line_spacing = 1.05
    stil.paragraph_format.widow_control = True
    stil._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    stil._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    stil._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    vorgaben = {
        "Heading 1": (16, BLAU, 16, 8, True),
        "Heading 2": (13, BLAU, 12, 6, False),
        "Heading 3": (12, DUNKELBLAU, 8, 4, False),
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
        stil._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
        stil._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
        stil._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
        sprache = stil._element.rPr.find(qn("w:lang"))
        if sprache is None:
            sprache = OxmlElement("w:lang")
            stil._element.rPr.append(sprache)
        sprache.set(qn("w:val"), "de-DE")

    for name in ("List Bullet", "List Number"):
        stil = doc.styles[name]
        stil.base_style = normal
        stil.font.name = "Calibri"
        stil.font.size = Pt(11)
        stil.paragraph_format.left_indent = Inches(0.5)
        stil.paragraph_format.first_line_indent = Inches(-0.25)
        stil.paragraph_format.space_after = Pt(5)
        stil.paragraph_format.line_spacing = 1.15

    for name, fett in (("Tabellentext", False), ("Tabellenkopf", True)):
        if name not in [s.name for s in doc.styles]:
            stil = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        else:
            stil = doc.styles[name]
        stil.base_style = normal
        stil.font.name = "Calibri"
        stil.font.size = Pt(10.5)
        stil.font.bold = fett
        stil.font.color.rgb = RGBColor.from_string(DUNKELBLAU if fett else "202830")
        stil.paragraph_format.space_before = Pt(0)
        stil.paragraph_format.space_after = Pt(0)
        stil.paragraph_format.line_spacing = 1.10
        stil.paragraph_format.widow_control = True

    if "Tabellenbeschriftung" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Tabellenbeschriftung", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Tabellenbeschriftung"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(9)
    stil.font.italic = True
    stil.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    stil.paragraph_format.space_before = Pt(5)
    stil.paragraph_format.space_after = Pt(9)
    stil.paragraph_format.line_spacing = 1.05

    if "Abbildungsbeschriftung" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Abbildungsbeschriftung", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Abbildungsbeschriftung"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(9)
    stil.font.italic = True
    stil.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    stil.paragraph_format.space_before = Pt(4)
    stil.paragraph_format.space_after = Pt(9)
    stil.paragraph_format.line_spacing = 1.05
    stil.paragraph_format.widow_control = True

    if "Kontrollfeldbezeichnung" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Kontrollfeldbezeichnung", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Kontrollfeldbezeichnung"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(11)
    stil.font.bold = True
    stil.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
    stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    stil.paragraph_format.space_before = Pt(4)
    stil.paragraph_format.space_after = Pt(1)
    stil.paragraph_format.line_spacing = 1.0
    stil.paragraph_format.keep_with_next = True
    stil.paragraph_format.widow_control = True

    for name, größe in (("Laufende Kopfzeile", 8), ("Laufende Fußzeile", 8)):
        if name not in [s.name for s in doc.styles]:
            stil = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        else:
            stil = doc.styles[name]
        stil.base_style = normal
        stil.font.name = "Calibri"
        stil.font.size = Pt(größe)
        stil.font.color.rgb = RGBColor.from_string(MITTELGRAU)
        stil.paragraph_format.space_before = Pt(0)
        stil.paragraph_format.space_after = Pt(0)
        stil.paragraph_format.line_spacing = 1.0

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

    if "Vorspannüberschrift" not in [s.name for s in doc.styles]:
        stil = doc.styles.add_style("Vorspannüberschrift", WD_STYLE_TYPE.PARAGRAPH)
    else:
        stil = doc.styles["Vorspannüberschrift"]
    stil.base_style = normal
    stil.font.name = "Calibri"
    stil.font.size = Pt(16)
    stil.font.bold = True
    stil.font.color.rgb = RGBColor.from_string(BLAU)
    stil.paragraph_format.space_before = Pt(0)
    stil.paragraph_format.space_after = Pt(10)
    stil.paragraph_format.keep_with_next = True
    stil.paragraph_format.widow_control = True

    for name, größe, einzug, davor, danach in (
        ("TOC 1", 10.5, 0.0, 2, 3),
        ("TOC 2", 10.0, 0.6, 0, 2),
    ):
        if name not in [s.name for s in doc.styles]:
            stil = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        else:
            stil = doc.styles[name]
        stil.base_style = normal
        stil.font.name = "Calibri"
        stil.font.size = Pt(größe)
        stil.font.bold = name == "TOC 1"
        stil.font.color.rgb = RGBColor.from_string(DUNKELBLAU if name == "TOC 1" else "202830")
        stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        stil.paragraph_format.left_indent = Cm(einzug)
        stil.paragraph_format.first_line_indent = Cm(0)
        stil.paragraph_format.space_before = Pt(davor)
        stil.paragraph_format.space_after = Pt(danach)
        stil.paragraph_format.line_spacing = 1.0
        stil.paragraph_format.widow_control = True
        stil.paragraph_format.tab_stops.clear_all()
        stil.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)


def füge_feld_hinzu(absatz, anweisung, ersatz):
    feld = OxmlElement("w:fldSimple")
    feld.set(qn("w:instr"), anweisung)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    schrift = OxmlElement("w:rFonts")
    schrift.set(qn("w:ascii"), "Calibri")
    schrift.set(qn("w:hAnsi"), "Calibri")
    r_pr.append(schrift)
    größe = OxmlElement("w:sz")
    größe.set(qn("w:val"), "16")
    r_pr.append(größe)
    farbe = OxmlElement("w:color")
    farbe.set(qn("w:val"), MITTELGRAU)
    r_pr.append(farbe)
    run.append(r_pr)
    text = OxmlElement("w:t")
    text.text = ersatz
    run.append(text)
    feld.append(run)
    absatz._p.append(feld)


def füge_inhaltsverzeichnisfeld_hinzu(absatz):
    """Fügt ein aktualisierbares Word-Inhaltsverzeichnis für Ebenen 1 und 2 ein."""
    def feldlauf(element):
        lauf = OxmlElement("w:r")
        lauf.append(element)
        absatz._p.append(lauf)

    beginn = OxmlElement("w:fldChar")
    beginn.set(qn("w:fldCharType"), "begin")
    beginn.set(qn("w:dirty"), "true")
    feldlauf(beginn)

    anweisung = OxmlElement("w:instrText")
    anweisung.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    anweisung.text = ' TOC \\o "1-2" \\h \\z \\u '
    feldlauf(anweisung)

    trennung = OxmlElement("w:fldChar")
    trennung.set(qn("w:fldCharType"), "separate")
    feldlauf(trennung)
    absatz.add_run("Inhaltsverzeichnis wird beim Erzeugen der Lesefassung aktualisiert.")

    ende = OxmlElement("w:fldChar")
    ende.set(qn("w:fldCharType"), "end")
    feldlauf(ende)


def setze_absatzrahmen(absatz, *, position, farbe, stärke=4, abstand=6):
    p_pr = absatz._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    linie = OxmlElement(f"w:{position}")
    linie.set(qn("w:val"), "single")
    linie.set(qn("w:sz"), str(stärke))
    linie.set(qn("w:space"), str(abstand))
    linie.set(qn("w:color"), farbe)
    p_bdr.append(linie)


def schattiere_absatz(absatz, farbe):
    p_pr = absatz._p.get_or_add_pPr()
    shd = p_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        p_pr.append(shd)
    shd.set(qn("w:fill"), farbe)


def richte_silbentrennung_ein(doc):
    einstellungen = doc.settings._element
    werte = {
        "autoHyphenation": "true",
        "consecutiveHyphenLimit": "2",
        "hyphenationZone": "360",
    }
    for name, wert in werte.items():
        element = einstellungen.find(qn(f"w:{name}"))
        if element is None:
            element = OxmlElement(f"w:{name}")
            einstellungen.append(element)
        element.set(qn("w:val"), wert)


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
    p.style = doc.styles["Laufende Kopfzeile"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.SPACES)
    p.add_run("Allgemeines KI-IT-Sicherheitskonzept").bold = True
    p.add_run("\t")
    p.add_run(f"Version {version}")
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    status_p = kopf.add_paragraph()
    status_p.style = doc.styles["Laufende Kopfzeile"]
    status_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    status_p.paragraph_format.space_after = Pt(2)
    status_p.paragraph_format.line_spacing = 1.0
    status_run = status_p.add_run(kennzeichnung)
    status_run.font.name = "Calibri"
    status_run.font.size = Pt(7.5)
    status_run.font.color.rgb = RGBColor.from_string(MITTELGRAU)
    setze_absatzrahmen(status_p, position="bottom", farbe=RAHMENGRAU, stärke=4, abstand=5)

    fuß = abschnitt.footer
    p = fuß.paragraphs[0]
    p.style = doc.styles["Laufende Fußzeile"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.SPACES)
    status_kurz = "NICHT ÖFFENTLICH" if kennzeichnung.startswith("NICHT ÖFFENTLICH") else "ÖFFENTLICH"
    p.add_run(status_kurz)
    p.add_run("\tSeite ")
    füge_feld_hinzu(p, "PAGE", "1")
    p.add_run(" von ")
    füge_feld_hinzu(p, "NUMPAGES", "1")
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(MITTELGRAU)
    setze_absatzrahmen(p, position="top", farbe=RAHMENGRAU, stärke=4, abstand=5)

    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings._element.append(update)
    richte_silbentrennung_ein(doc)


def add_heading(doc, text, ebene):
    p = doc.add_heading(text, level=ebene)
    p.paragraph_format.keep_with_next = True
    return p


def dokumentsteuerung(doc, version, kennzeichnung, katalog, stichtag):
    doc.add_paragraph("Dokumentenlenkung", style="Vorspannüberschrift")
    tabelle = doc.add_table(rows=1, cols=2)
    tabelle.style = "Table Grid"
    tabelle.rows[0].cells[0].text = "Merkmal"
    tabelle.rows[0].cells[1].text = "Festlegung"
    daten = [
        ("Dokumenttitel", "Allgemeines KI-IT-Sicherheitskonzept"),
        ("Dokumentstatus", kennzeichnung),
        ("Version", version),
        ("Fachlicher Stichtag", deutsches_datum(stichtag)),
        ("Normative Anforderungen", "KI-IT-Sicherheitskatalog nach Open Security Controls Assessment Language (OSCAL) 1.1.3"),
        ("OSCAL-Fassung", katalog["catalog"]["metadata"]["oscal-version"]),
        ("Betriebsmodell", "Vollständig lokal; externe Inferenz nicht anwendbar"),
        ("Modelländerung", "Training und Feinabstimmung ausgeschlossen"),
    ]
    for merkmal, festlegung in daten:
        zellen = tabelle.add_row().cells
        zellen[0].text = merkmal
        zellen[1].text = festlegung
    formatiere_tabelle(tabelle, [2500, 6422])


def inhaltsverzeichnis(doc):
    doc.add_paragraph("Inhaltsverzeichnis", style="Vorspannüberschrift")
    feldabsatz = doc.add_paragraph()
    feldabsatz.paragraph_format.space_after = Pt(0)
    füge_inhaltsverzeichnisfeld_hinzu(feldabsatz)


def kapitel_eins_bis_acht(doc, kennzeichnung, quellen_nach_id):
    add_heading(doc, "1 Dokumentenstatus und Geltungsbereich", 1)
    text_absatz(doc, f"Das Konzept trägt den Status {kennzeichnung}. Es gilt für die organisationsneutrale Standardarchitektur einer vollständig lokalen generativen KI-Umgebung mit verwalteten Clients, kontrolliertem KI-Zugang und getrennter KI-Serverzone.")
    text_absatz(doc, "Der Status ÖFFENTLICH gilt nur für die organisationsneutrale Fassung. Sobald reale Organisations-, Infrastruktur-, Schutzbedarfs-, Konto- oder Schwachstelleninformationen aufgenommen werden, ist die Fassung getrennt zu führen, angemessen zu schützen und durch die zuständigen Stellen einzustufen und freizugeben.")

    add_heading(doc, "2 Zweck, Zielgruppe und Abgrenzung", 1)
    text_absatz(doc, "Dieses Sicherheitskonzept regelt Planung, Freigabe, Betrieb, Änderung und Außerbetriebnahme lokaler generativer KI-Dienste. Es richtet sich an Leitung, Informationssicherheit, Datenschutz, Recht, Geheimschutz, Personalvertretung und Fachverantwortung sowie an Rollen für Architektur, Plattform, Netzwerk, Identität, lokale Wissenssuche, Modelle, Tests und Betrieb.")
    text_absatz(doc, "Nicht Gegenstand sind eine produktive Plattform, Beschaffungsempfehlungen, Training, Feinabstimmung, kontinuierliches Lernen oder die pauschale Freigabe eines konkreten Anwendungsfalls. Fachwissen wird ausschließlich aus lokalen Wissensbeständen oder aus kontrollierten, zeitlich begrenzten Dateiübernahmen bereitgestellt.")

    add_heading(doc, "2.1 Zentrale Begriffe", 2)
    begriffe = [
        ("Lokale Inferenz", "Ausführung eines vortrainierten Modells innerhalb der eigenen Infrastruktur, ohne beabsichtigte Änderung der Modellgewichte."),
        ("Lokale Wissenssuche (RAG)", "Suche nach freigegebenen Textausschnitten, die der lokalen Inferenz als zusätzlicher Kontext übergeben werden."),
        ("Suchvektor (Embedding)", "Numerische Darstellung eines Inhalts für die Ähnlichkeitssuche. Der Schutzbedarf der Quelldaten kann darin erhalten bleiben."),
        ("Bedarfsgesteuerte Dateiübernahme", "Zeitlich begrenzte Übergabe einer Datei an die lokale KI-Umgebung. Ohne ausdrückliche Freigabe bleibt die Verarbeitung auf die Sitzung begrenzt."),
        ("Programmierschnittstelle (API)", "Technischer Zugang, über den ein Client festgelegte Funktionen eines Dienstes aufruft."),
        ("Identitätsdienst (IdP)", "Lokaler Dienst, der Personen und technische Konten verlässlich identifiziert und deren Anmeldung unterstützt."),
        ("Transportverschlüsselung (TLS)", "Verschlüsselung einer Netzwerkverbindung zum Schutz vor Mitlesen und Veränderung während der Übertragung."),
        ("Zentrale Sicherheitsauswertung (SIEM)", "Lokale Sammlung und Auswertung sicherheitsrelevanter Protokollereignisse."),
        ("Model Context Protocol (MCP)", "Technisches Protokoll zur Anbindung zusätzlicher Werkzeuge oder Datenquellen an eine agentische Anwendung."),
        ("Agentische Anwendung", "Client oder Dienst, der einen Modellvorschlag in einen Datei-, Werkzeug-, Befehls- oder Netzwerkzugriff überführen kann."),
        ("Eingeschleuste Anweisung (Prompt Injection)", "Anweisung in einer Eingabe, einem Dokument oder einer Werkzeugausgabe, die festgelegte Regeln oder Berechtigungsgrenzen umgehen soll."),
        ("Herkunftsnachweis", "Nachvollziehbare Kette von der veröffentlichten Quelle eines Modells, Pakets oder Dokuments bis zum tatsächlich verwendeten Artefakt."),
        ("Ausgehende Verbindung", "Netzwerkverbindung aus der KI-Umgebung zu einem Ziel außerhalb der freigegebenen lokalen Systemgrenze."),
        ("Zugriffsregel (ACL)", "Technische Liste, die festlegt, welche Identität auf welche Daten oder Funktionen zugreifen darf."),
        ("Restrisiko", "Risiko, das nach Umsetzung und Prüfung der vorgesehenen Sicherheitsmaßnahmen verbleibt."),
    ]
    for begriff, bedeutung in begriffe:
        begriffsdefinition(doc, begriff, bedeutung)

    add_heading(doc, "3 Voraussetzungen des allgemeinen IT-Sicherheitskonzepts", 1)
    grundlage = text_absatz(doc, "Der sichere KI-Betrieb setzt ein wirksames allgemeines IT-Sicherheitskonzept und einen festgelegten Informationsverbund voraus. Die KI-spezifischen Maßnahmen ergänzen diesen Sicherheitsprozess dort, wo Modelle, Wissensbestände, Eingaben oder automatisierte Werkzeugzugriffe zusätzliche Risiken erzeugen:")
    fußnotenmarke(
        grundlage,
        vollzitat(quellen_nach_id["Q-BSI-2002-001"], "S. 11, S. 69–74 und S. 154–156"),
    )
    aufzählung(doc, [
        "Verwaltete Clients und Server, sichere Domäne, lokaler Identitätsdienst, Rollen und Mehrfaktorauthentisierung (MFA).",
        "Interne Zertifikatsinfrastruktur (PKI), vertrauenswürdige Zertifikate, Segmentierung, Firewalls und abgesicherter Fernzugriff.",
        "Patch-, Schwachstellen-, Konfigurations- und sichere Softwareverteilung.",
        "Lokale Protokollierung, Überwachung, Datensicherung, Wiederherstellung, Notfallmanagement und Schadsoftwareschutz.",
    ])
    text_absatz(doc, "Fehlende Basismaßnahmen sperren die Freigabe der abhängigen KI-Funktion. Sie werden im allgemeinen Sicherheitsprozess behandelt und nicht durch KI-spezifische Einzelmaßnahmen ersetzt.")

    add_heading(doc, "4 Lokale KI-Systemarchitektur", 1)
    text_absatz(doc, "Die Systemarchitektur ist vollständig lokal. Verwaltete Clients erreichen über HTTPS ausschließlich den kontrollierten internen KI-Zugang. Dahinter liegt eine getrennte KI-Serverzone mit Containerplattform, Chat-Oberfläche, lokaler Inferenz, lokaler Wissenssuche, Suchvektoren, Treffer-Neusortierung, Datenhaltung und technischer Überwachung. Fernzugriff erfolgt nur über ein organisationskontrolliertes virtuelles privates Netz (VPN) mit Mehrfaktorauthentisierung.")
    text_absatz(doc, "Der kontrollierte KI-Zugang ist der einzige zulässige Anfragepfad aus der Clientzone. Identitätsdienst, Verwaltungszugang, lokale Registrierungen und Prüfprotokolle sind vom normalen Anfragepfad getrennt. Die Inferenz besitzt keine ausgehende Internetverbindung (Abbildung 1).")
    füge_abbildung_hinzu(
        doc,
        ARCHITEKTUR_ABBILDUNG,
        "Abbildung 1: Nur der kontrollierte KI-Zugang verbindet die Clientzone mit der abgeschotteten KI-Serverzone.",
        "Ein entfernter oder interner verwalteter Client erreicht über VPN und HTTPS nur den kontrollierten KI-Zugang. Dieser vermittelt identitäts- und rollenbasiert zur getrennten KI-Serverzone mit Chat, Inferenz, lokaler Wissenssuche, Datenhaltung und Überwachung. Verwaltung, Prüfprotokolle und Registrierungen sind getrennt; die Inferenz besitzt keine ausgehende Internetverbindung.",
        breite_cm=13.5,
    )

    add_heading(doc, "5 Systemgrenzen, Vertrauenszonen und Datenflüsse", 1)
    text_absatz(doc, "Jede Vertrauenszone besitzt eine klar abgegrenzte Aufgabe. Übergänge zwischen den Zonen werden authentisiert, protokolliert und auf die ausdrücklich freigegebenen Kommunikationsbeziehungen begrenzt.")
    zonen = [
        ("Verwaltete Clientzone", "Benutzerinteraktion, lokale Entwicklungswerkzeuge und begrenzte agentische Aktionen."),
        ("Kontrollierter KI-Zugang", "Einziger Clientpfad; Identität, Rollen, Transportverschlüsselung sowie Modell-, Kontext-, Raten- und Werkzeugregeln."),
        ("KI-Serverzone", "Interne Inferenz-, Wissens-, Daten- und Überwachungsdienste ohne Erreichbarkeit aus öffentlichen oder allgemeinen Clientnetzen."),
        ("Importweg", "Prüfung von Modellen, Containerabbildern, Paketen und Erweiterungen vor der Übernahme in lokale Registrierungen."),
        ("Betriebs- und Nachweisbereich", "Besonders geschützte Protokolle, Sicherheitsauswertungen, Freigaben, Sicherungen und Wiederherstellungsdaten."),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Vertrauenszone"
    t.rows[0].cells[1].text = "Aufgabe und Grenze"
    for a, b in zonen:
        z = t.add_row().cells
        z[0].text = a
        z[1].text = b
    formatiere_tabelle(t, [2500, 6422])
    add_heading(doc, "5.1 Kommunikations- und Importregeln", 2)
    text_absatz(doc, "Ein internes Container- oder Pod-Netz ist keine ausreichende Sicherheitsgrenze. Kommunikationsbeziehungen werden standardmäßig verweigert und einzeln erlaubt. Inferenz-, Administrations-, Diagnose-, Metrik-, Cluster- und Zwischenspeicher-Schnittstellen bleiben vom normalen Netz getrennt.")
    text_absatz(doc, "Identitäten, Git, Modelle, Dokumente, Suchvektoren, Indizes, Chats, Protokolle, Telemetrie und Sicherungen verbleiben lokal. Externe Artefakte gelangen ausschließlich über eine getrennte Prüfzone, kontrollierte Übertragung, lokale Registrierung und Freigabe in die Produktionsumgebung (Abbildung 2).")
    füge_abbildung_hinzu(
        doc,
        ARTEFAKTIMPORT_ABBILDUNG,
        "Abbildung 2: Nur geprüfte und freigegebene Artefakte erreichen die abgeschottete Produktionsumgebung.",
        "Ein versionsfixiertes Artefakt aus einer offiziellen externen Quelle wird in einer getrennten Zone auf Herkunft, kryptografische Prüfsumme, Signatur, Schwachstellen, Lizenz und Schadsoftware geprüft. Nur freigegebene Artefakte gelangen kontrolliert in lokale Registrierungen, eine Testumgebung und nach einer Wiederholungsprüfung in die Produktion. Ablehnungen und Rückgriffe werden dokumentiert.",
        breite_cm=14.0,
    )

    add_heading(doc, "6 Rechts-, Normen- und Anwendbarkeitsmatrix", 1)
    text_absatz(doc, "Vor der Freigabe eines Anwendungsfalls bestimmen die zuständigen Funktionen die anwendbaren Rechtsgrundlagen, Beteiligungsrechte, behördlichen Vorgaben und Freigabebedingungen. Die Ergebnisse werden als technische oder organisatorische Bedingungen umgesetzt.")
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
    for i, wert in enumerate(("Grundlage", "Anwendbarkeit", "Prüf- und Festlegungsbedarf", "Quellen")):
        t.rows[0].cells[i].text = wert
    for zeile in matrix:
        z = t.add_row().cells
        for i, wert in enumerate(zeile):
            z[i].text = wert
    formatiere_tabelle(t, [1850, 1550, 3872, 1650], zentrierte_spalten={1, 3})

    add_heading(doc, "7 Steuerung, Rollen und Verantwortlichkeiten", 1)
    text_absatz(doc, "Entscheidungs-, Umsetzungs- und Prüffunktionen werden so getrennt, dass Freigaben und wesentliche Restrisiken nachvollziehbar verantwortet werden. Eine Person darf mehrere Rollen wahrnehmen, sofern Interessenkonflikte behandelt und notwendige unabhängige Prüfungen erhalten bleiben.")
    rollen = [
        ("Leitung", "Risikobereitschaft, Ressourcen, wesentliche Restrisiken und Freigaberahmen."),
        ("KI-Verantwortliche", "Inventar, Anwendungsfälle, Modell- und Richtlinienfreigaben sowie koordinierter Lebenszyklus."),
        ("Informationssicherheit", "Bedrohungsmodell, Kontrollanforderungen, Prüfung, Vorfälle und Basis-ISMS-Verknüpfung."),
        ("Datenschutz, Recht, Geheimschutz, Personalvertretung", "Anwendbarkeitsprüfung, Beteiligung, Bedingungen und befugte Freigaben im jeweiligen Zuständigkeitsbereich."),
        ("Architektur, Netz, Plattform, Identität und KI-Zugang", "Technische Zonen, ausgehender Netzwerkverkehr, freigegebener Laufzeitstand, Identitäten, Zertifikate und Richtliniendurchsetzung."),
        ("Modell, Wissenssuche, Daten und Werkzeuge", "Herkunftsnachweis, Integrität, Zugriffsregeln, Löschung, Erweiterungsfreigabe und fachliche Datenverantwortung."),
        ("Test und Betrieb", "Reproduzierbare Bewertung, Wiederholungsprüfung, Überwachung, Protokollierung, Wiederanlauf und Außerbetriebnahme."),
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
    formatiere_tabelle(t, [2600, 6322])

    add_heading(doc, "8 KI-Risiko- und Bedrohungsmodell", 1)
    add_heading(doc, "8.1 Bewertungsverfahren", 2)
    methodik = text_absatz(doc, "Jedes Risiko wird als nachvollziehbares Szenario aus Ursache, betroffenem Wert und möglicher Auswirkung beschrieben. Danach werden Eintrittshäufigkeit und Schadenshöhe unter Berücksichtigung bereits wirksamer Maßnahmen eingeschätzt. Die Risikokategorie bestimmt die Behandlung. Nach Umsetzung und Prüfung zusätzlicher Maßnahmen wird das Restrisiko erneut eingestuft und einer verantwortlichen Entscheidung zugeführt.")
    fußnotenmarke(
        methodik,
        vollzitat(quellen_nach_id["Q-BSI-2003-001"], "S. 5–7, S. 26–28 und S. 33–35"),
    )
    text_absatz(doc, "Die Bewertung erfasst Eingaben, Modelle, Systemanweisungen, lokale Wissenssuche, Werkzeuge, Clients, Schnittstellen, Plattform, Protokolle und Importwege. Änderungen oder abgelaufene Prüffristen führen zurück in die vollständige Bewertung (Abbildung 3).")
    füge_abbildung_hinzu(
        doc,
        RISIKOBEWERTUNG_ABBILDUNG,
        "Abbildung 3: Risiken werden szenariobezogen behandelt und bis zur Freigabe erneut bewertet.",
        "Der Ablauf beginnt mit Geltungsbereich und Schutzzielen. Darauf folgen Gefährdungsübersicht, Einschätzung von Eintrittshäufigkeit und Schadenshöhe sowie die Einstufung anhand der Risikomatrix. Nicht akzeptable Risiken durchlaufen zusätzliche Maßnahmen und eine erneute Bewertung. Akzeptable Restrisiken werden verantwortlich freigegeben, im Risikoregister dokumentiert und bei Änderungen erneut betrachtet.",
        breite_cm=13.0,
    )

    add_heading(doc, "8.2 Bewertungsmaßstab und Freigabegrenzen", 2)
    text_absatz(doc, "Die Eintrittshäufigkeit wird als selten, mittel, häufig oder sehr häufig eingestuft. Die Schadenshöhe wird als vernachlässigbar, begrenzt, beträchtlich oder existenzbedrohend bewertet. Die Kombination ergibt die Risikokategorie gering, mittel, hoch oder sehr hoch. Jede Matrixzelle nennt die Kategorie als Text; die Farbe dient nur der schnellen Orientierung.")
    füge_abbildung_hinzu(
        doc,
        RISIKOMATRIX_ABBILDUNG,
        "Abbildung 4: Die KI-spezifischen Maßnahmen senken alle hohen und sehr hohen Ausgangsrisiken auf höchstens mittel.",
        "Vier mal vier Risikomatrix nach BSI-Standard 200-3. Die Spalten bilden die Eintrittshäufigkeit von selten bis sehr häufig ab, die Zeilen die Schadenshöhe von vernachlässigbar bis existenzbedrohend. Die Zellen nennen die Risikokategorie gering, mittel, hoch oder sehr hoch und verorten die Ausgangsrisiken mit A sowie die verbleibenden Risiken mit R.",
        breite_cm=15.8,
    )
    aufzählung(doc, [
        "Geringe Risiken dürfen durch die zuständige Rolle akzeptiert und überwacht werden.",
        "Mittlere Risiken dürfen nur befristet, mit benannter Verantwortung, Maßnahmenplan und Prüftermin akzeptiert werden.",
        "Hohe und sehr hohe Risiken sperren die Erstfreigabe oder den Weiterbetrieb, bis zusätzliche Maßnahmen nachweislich wirken.",
        "Jede Akzeptanz nennt Begründung, Entscheidung, Gültigkeitsfrist und erneuten Bewertungsanlass.",
    ])

    add_heading(doc, "8.3 Risikoregister der Standardarchitektur", 2)
    text_absatz(doc, "Die Risikobewertung wird vor der Erstnutzung, mindestens jährlich sowie nach wesentlichen Änderungen, Sicherheitsvorfällen oder neuen Erkenntnissen wiederholt. Die folgende Bewertung gilt für die in diesem Konzept festgelegte Standardarchitektur und die vollständige Umsetzung der genannten Kontrollen.")
    risiken = [
        ("R-01", "Eine eingeschleuste Anweisung löst eine nicht erlaubte Werkzeugaktion aus.", "häufig × beträchtlich = hoch\n→ selten × beträchtlich = mittel", "Kontexttrennung, Werkzeugrichtlinie, konkrete Bestätigung und Negativtests; KI-PMT-001, KI-TOL-001, KI-THR-001."),
        ("R-02", "Ein manipuliertes Modell, Containerabbild oder Paket wird übernommen.", "mittel × beträchtlich = mittel\n→ selten × beträchtlich = mittel", "Getrennte Importprüfung, Herkunftsnachweis, Signatur, Prüfsumme und Freigabe; KI-MOD-001, KI-TOL-002, KI-VAL-002."),
        ("R-03", "Die lokale Wissenssuche gibt Inhalte ohne ausreichende Berechtigung aus.", "häufig × beträchtlich = hoch\n→ selten × beträchtlich = mittel", "Zugriffsprüfung bei Aufnahme und Abfrage, getrennte Indizes und Löschtests; KI-RAG-002, KI-RAG-003."),
        ("R-04", "Eine direkte Inferenzschnittstelle umgeht Identitäts- und Zugriffsregeln.", "mittel × beträchtlich = mittel\n→ selten × beträchtlich = mittel", "Nur der kontrollierte KI-Zugang ist erreichbar; Rohschnittstellen bleiben abgeschottet; KI-API-001, KI-ARC-001."),
        ("R-05", "Protokolle speichern mehr schutzbedürftige Inhalte als erforderlich.", "häufig × begrenzt = mittel\n→ selten × begrenzt = gering", "Trennung von Sicherheitsmetadaten und Inhaltsdaten, Minimierung, Zugriff und Löschung; KI-OPS-001."),
        ("R-06", "Lange Kontexte oder Agentenschleifen erschöpfen lokale Rechenressourcen.", "häufig × beträchtlich = hoch\n→ mittel × begrenzt = gering", "Quoten, Zeitgrenzen, Warteschlangen, Prioritäten und sichere Beendigung; KI-THR-002."),
        ("R-07", "Eine unzutreffende oder unsichere Ausgabe beeinflusst Entscheidungen oder Quellcode.", "sehr häufig × beträchtlich = sehr hoch\n→ selten × beträchtlich = mittel", "Fachliche Prüfung, sichere Weiterverarbeitung, menschliche Freigabe und Wirksamkeitstests; KI-OUT-001, KI-VAL-001."),
        ("R-08", "Eine Ausweichverbindung überträgt Eingaben unbeabsichtigt an einen externen Dienst.", "mittel × existenzbedrohend = hoch\n→ selten × begrenzt = gering", "Deaktivierte externe Anbieter, gesperrter ausgehender Verkehr und negative Verbindungstests; KI-EXT-002, KI-ARC-002."),
        ("R-09", "Ein Modell- oder Versionswechsel verschlechtert Sicherheit oder Ergebnisqualität.", "häufig × beträchtlich = hoch\n→ selten × beträchtlich = mittel", "Gebundene Freigabestände, Wiederholungsprüfungen und getestete Rückkehr zur Vorversion; KI-MOD-002, KI-VAL-002."),
    ]
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for i, wert in enumerate(("ID", "Risikoszenario", "Ausgangsrisiko → Restrisiko", "Behandlung und Kontrollen")):
        t.rows[0].cells[i].text = wert
    for zeile in risiken:
        z = t.add_row().cells
        for i, wert in enumerate(zeile):
            z[i].text = wert
    formatiere_tabelle(t, [700, 2500, 2100, 3622], zentrierte_spalten={0, 2})


def kapitel_neun(doc, katalog, quellen_nach_uuid):
    add_heading(doc, "9 KI-spezifische Sicherheitsmaßnahmen", 1)
    text_absatz(doc, "Eine KI-Funktion darf nur freigegeben oder weiterbetrieben werden, wenn alle anwendbaren Anforderungen umgesetzt, geprüft und durch aktuelle Nachweise belegt sind. Abweichungen benötigen eine dokumentierte Behandlung und eine befristete, befugte Restrisikoentscheidung.")
    for gruppenindex, gruppe in enumerate(katalog["catalog"]["groups"], start=1):
        add_heading(doc, f"9.{gruppenindex} {gruppe['title']}", 2)
        for control in gruppe.get("controls", []):
            kennung = prop(control, "alt-identifier")[0]
            kontrollüberschrift = add_heading(doc, f"{kennung} – {control['title']}", 3)
            felder = [
                ("Normative Anforderung", teil(control, "statement")),
                ("Begründung", teil(control, "rationale")),
                ("Umsetzung im Geltungsbereich", teil(control, "guidance")),
                ("Prüfziel", teil(control, "assessment-objective")),
                ("Erwartete Nachweise", teil(control, "evidence")),
            ]
            for feldindex, (merkmal, inhalt) in enumerate(felder):
                label_p = doc.add_paragraph(merkmal, style="Kontrollfeldbezeichnung")
                p = doc.add_paragraph(style="Fließtext")
                setze_absatzformat(p, danach=7)
                p.add_run(inhalt)
                if feldindex == 0:
                    label_p.paragraph_format.space_before = Pt(0)
                    label_p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.space_after = Pt(8)
                    schattiere_absatz(label_p, HELLGRAU)
                    schattiere_absatz(p, HELLGRAU)
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
            formatiere_tabelle(metadaten, [2500, 6422])

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
            unterdrücke_silbentrennung(quelle_p)
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


def kapitel_zehn_bis_dreizehn(doc, katalog):
    add_heading(doc, "10 Lokale Wissenssuche, Dateiübernahmen und Daten", 1)
    text_absatz(doc, "Fachwissen verbleibt außerhalb der Modellgewichte. Die lokale Wissenssuche und zeitlich begrenzte lokale Dateiübernahmen sind die einzigen vorgesehenen Zuführungswege. Dateien durchlaufen Quarantäne, Schadsoftware- und Typprüfung sowie eine isolierte Auswertung. Herkunft, Eigentümer, Schutzbedarf und Zugriffsregeln bleiben an allen abgeleiteten Daten erhalten.")
    text_absatz(doc, "Aufnahme und Abfrage sind getrennte Wege. Vor der Aufnahme und erneut bei jeder Abfrage wird die Berechtigung anhand der aktuellen Identität geprüft. Nur freigegebene Treffer gelangen in den Kontext der lokalen Inferenz; eine Löschung erfasst Quelle, Ableitungen, Index, Zwischenspeicher und Sicherungskette (Abbildung 5).")
    füge_abbildung_hinzu(
        doc,
        RAG_ABBILDUNG,
        "Abbildung 5: Aufnahme, berechtigte Abfrage und vollständige Löschung bleiben technisch getrennt.",
        "Freigegebene Dokumente oder lokale Dateiübernahmen durchlaufen Quarantäne, isolierte Aufbereitung, Herkunfts- und Zugriffsmetadaten, Aufteilung in Textabschnitte und lokale Erzeugung von Suchvektoren. Bei einer identifizierten Anfrage werden die Zugriffsrechte erneut geprüft. Nur freigegebene und neu sortierte Treffer gelangen zur lokalen Inferenz. Die Löschung erfasst Quelle, Ableitungen, Index, Zwischenspeicher und Sicherungskette.",
        breite_cm=15.0,
    )
    aufzählung(doc, [
        "Suchvektoren, Textabschnitte, Indizes, Zwischenspeicher und Daten zur Neusortierung erhalten mindestens den Schutzbedarf der Quelldaten.",
        "Das Sprachmodell und Systemanweisungen treffen keine Zugriffsentscheidung.",
        "Bedarfsgesteuerte Dateiübernahmen bleiben ohne ausdrückliche Genehmigung einer dauerhaften Ablage sitzungsbezogen.",
        "Ausgaben weisen verwendete Quellen und konkrete Fundstellen nachvollziehbar aus.",
        "Löschung umfasst Onlinekopien, Ableitungen, Zwischenspeicher und den geregelten Ablauf in Sicherungsketten.",
    ])
    text_absatz(doc, "Indexierung und die Erzeugung von Suchvektoren ändern keine Modellgewichte. Training, Feinabstimmung und jede lernende Rückkopplung aus Chats, Dateiübernahmen oder Wissensbeständen bleiben technisch und organisatorisch ausgeschlossen.")

    add_heading(doc, "11 Agentische Anwendungen und lokale Entwicklungsumgebungen", 1)
    text_absatz(doc, "Agentische Clients wie Cline- oder OpenCode-artige Werkzeuge sind Produktbeispiele. Sie greifen ausschließlich über den lokalen HTTPS-Zugang auf freigegebene Modelle zu. Lokale Git-, Paket- und Entwicklungsdienste bleiben in der Organisationsumgebung.")
    text_absatz(doc, "Eine Modellausgabe löst keine unmittelbare Werkzeugaktion aus. Werkzeugrichtlinie, Prüfung der möglichen Wirkung, konkrete menschliche Bestätigung und eine minimal berechtigte Ausführungsumgebung bilden voneinander unabhängige Schranken (Abbildung 6).")
    füge_abbildung_hinzu(
        doc,
        AGENTEN_ABBILDUNG,
        "Abbildung 6: Eine Werkzeugaktion benötigt Richtlinienprüfung, begrenzte Rechte und bei erhöhter Wirkung eine konkrete Bestätigung.",
        "Eine identifizierte Person nutzt einen lokal begrenzten agentischen Client über den lokalen KI-Zugang. Der Vorschlag einer Werkzeugaktion wird gegen die Werkzeugrichtlinie geprüft. Schreib-, Befehls-, Netzwerk- oder destruktive Aktionen benötigen eine konkrete menschliche Bestätigung und laufen nur in einer minimal berechtigten Ausführungsumgebung. Blockierte und ausgeführte Aktionen gelangen in das lokale Prüfprotokoll.",
        breite_cm=15.5,
    )
    aufzählung(doc, [
        "Arbeitsbereichs- und Dateirechte sind minimal und überschreiten weder Projekt noch genehmigten Zweck.",
        "Lesen, Schreiben, Befehlsausführung und Netzwerkzugriff sind getrennte Fähigkeiten.",
        "Kritische, destruktive, privilegierte oder externe Aktionen benötigen eine konkrete menschliche Bestätigung.",
        "Eingeschleuste Anweisungen aus Quellcode, Dokumenten, Webseiten und Werkzeugausgaben dürfen keine Rechte erweitern.",
        "Plug-ins, MCP-Server, Erweiterungen und Pakete stammen aus kontrollierten lokalen Quellen und sind versionsfixiert.",
        "Werkzeugaufrufe werden identitätsbezogen, nachvollziehbar und datensparsam lokal protokolliert.",
    ])

    add_heading(doc, "12 Betrieb, Änderung, Modellwechsel, Vorfälle und Außerbetriebnahme", 1)
    text_absatz(doc, "Der Betrieb verbindet den freigegebenen Systemstand, lokale Protokollierung, zentrale Sicherheitsauswertung (SIEM), Qualitäts- und Sicherheitskennzahlen, Beobachtung schleichender Verhaltensänderungen, Kapazitätsgrenzen und den allgemeinen Vorfallprozess. Der reine technische Betrieb belegt weder korrekte Berechtigungen noch Ergebnisqualität, Datenlöschung oder Wiederherstellbarkeit.")
    text_absatz(doc, "Jede Änderung an Modell, Modellkomprimierung, Laufzeit, Systemanweisung, lokaler Wissenssuche, Suchvektoren, Treffer-Neusortierung, kontrolliertem KI-Zugang, Werkzeugen oder Sicherheitsparametern löst eine risikobasierte Wiederholungsprüfung und Wiederfreigabe aus. Vorherige geprüfte Kombinationen bleiben für eine kontrollierte Rückkehr verfügbar. Wiederanlaufprüfungen erfolgen ohne Internetzugang und umfassen Prüfsummen, Richtlinien, Zugriffsregeln und Kernbewertungen.")
    text_absatz(doc, "Bei Außerbetriebnahme werden Identitäten, Zertifikate, Geheimnisse, Endpunkte, automatisierte Aufgaben, Modelle, Daten, Indizes und Zwischenspeicher behandelt. Erforderliche Prüfnachweise bleiben entsprechend der Aufbewahrungsfrist erhalten; unzulässige Restkopien und Erreichbarkeit müssen durch Nachtests ausgeschlossen werden.")

    add_heading(doc, "13 Nachweis-, Prüf- und Zuordnungsübersicht", 1)
    text_absatz(doc, "Für jede anwendbare Kontrolle werden Umsetzung, verantwortliche Rolle, Prüfergebnis, Nachweisfundstelle, Abweichung und Restrisiko nachvollziehbar geführt. Die Zuordnungen unterstützen die gemeinsame Prüfung mit dem allgemeinen Informationssicherheitsmanagement.")
    t = doc.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    for i, wert in enumerate(("ID", "Titel", "Anwendbarkeit", "BSI/IT-Grundschutz", "ISO-Kennungen")):
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
    formatiere_tabelle(t, [1100, 2650, 1350, 1700, 2122], zentrierte_spalten={0, 2})


def kapitel_vierzehn(doc, register):
    add_heading(doc, "14 Quellenverzeichnis und Abkürzungen", 1)
    add_heading(doc, "14.1 Quellenverzeichnis", 2)
    for quelle in register["quellen"]:
        fundstellen = "; ".join(f["fundstelle"] for f in quelle["verwendete_fundstellen"])
        p = doc.add_paragraph()
        setze_absatzformat(p, danach=7)
        p.add_run(f"[{quelle['id']}] ").bold = True
        p.add_run(f"{quelle['herausgeber']}: {quelle['titel']}, {quelle['fassung']}, {quellendatum(quelle)}, {fundstellen}, ")
        hyperlink(p, quelle["öffentliche_url"], quelle["öffentliche_url"])
        p.add_run(f", abgerufen am {deutsches_datum(quelle['abrufdatum'])}.")
        unterdrücke_silbentrennung(p)
    add_heading(doc, "14.2 Abkürzungen", 2)
    abkürzungen = [
        ("ACL", "Zugriffssteuerungsliste (Access Control List)"),
        ("API", "Programmierschnittstelle (Application Programming Interface)"),
        ("BfDI", "Die Bundesbeauftragte für den Datenschutz und die Informationsfreiheit"),
        ("BMI", "Bundesministerium des Innern"), ("BMVg", "Bundesministerium der Verteidigung"),
        ("BSI", "Bundesamt für Sicherheit in der Informationstechnik"),
        ("DSK", "Konferenz der unabhängigen Datenschutzaufsichtsbehörden des Bundes und der Länder"),
        ("IdP", "Identitätsanbieter (Identity Provider)"), ("ISMS", "Informationssicherheitsmanagementsystem"),
        ("KI", "Künstliche Intelligenz"), ("MFA", "Mehrfaktorauthentisierung"),
        ("MCP", "Model Context Protocol"), ("OSCAL", "Open Security Controls Assessment Language"),
        ("RAG", "Abrufgestützte Generierung (Retrieval Augmented Generation)"),
        ("SIEM", "Zentrale Sammlung und Auswertung von Sicherheitsereignissen (Security Information and Event Management)"),
        ("TLS", "Transportverschlüsselung (Transport Layer Security)"),
        ("VPN", "Virtuelles privates Netz (Virtual Private Network)"),
    ]
    hälfte = (len(abkürzungen) + 1) // 2
    linke_spalte = abkürzungen[:hälfte]
    rechte_spalte = abkürzungen[hälfte:]
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Abkürzung"
    t.rows[0].cells[1].text = "Langform"
    t.rows[0].cells[2].text = "Abkürzung"
    t.rows[0].cells[3].text = "Langform"
    for index, (kurz, lang) in enumerate(linke_spalte):
        z = t.add_row().cells
        z[0].text = kurz
        z[1].text = lang
        if index < len(rechte_spalte):
            z[2].text = rechte_spalte[index][0]
            z[3].text = rechte_spalte[index][1]
    formatiere_tabelle(t, [1000, 3461, 1000, 3461], zentrierte_spalten={0, 2})


def erzeuge_docx(ziel):
    FOOTNOTES.clear()
    katalog = lade_json(KATALOG_PFAD)
    register = lade_json(REGISTER_PFAD)
    status = lade_json(STATUS_PFAD)
    version = katalog["catalog"]["metadata"]["version"]
    stichtag = register["stichtag"]
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
    eigenschaften.comments = "Öffentliche organisationsneutrale Konzeptfassung"

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
    run = p.add_run("Sicherheitskonzept für vollständig lokale KI-Infrastrukturen")
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    setze_absatzformat(p, danach=26)
    status_p = doc.add_paragraph(style="Dokumentstatus")
    status_p.add_run(kennzeichnung)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Version {version} · Fachlicher Stichtag {deutsches_datum(stichtag)}")
    setze_absatzformat(p, danach=18)
    doc.add_page_break()

    dokumentsteuerung(doc, version, kennzeichnung, katalog, stichtag)
    doc.add_page_break()
    inhaltsverzeichnis(doc)
    quellen_nach_uuid = {q["oscal_uuid"]: q for q in register["quellen"]}
    quellen_nach_id = {q["id"]: q for q in register["quellen"]}
    kapitel_eins_bis_acht(doc, kennzeichnung, quellen_nach_id)
    kapitel_neun(doc, katalog, quellen_nach_uuid)
    kapitel_zehn_bis_dreizehn(doc, katalog)
    kapitel_vierzehn(doc, register)

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
