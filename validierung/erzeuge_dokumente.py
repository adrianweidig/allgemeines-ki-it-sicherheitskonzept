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

DOKUMENTTITEL = "Allgemeines KI-Informationssicherheitskonzept"
UMGEBUNGSUEBERSICHT_ABBILDUNG = MEDIEN_PFAD / "umgebungsuebersicht.png"
CLOUD_ABBILDUNG = MEDIEN_PFAD / "architektur-cloud.png"
BELEHRUNG_ZIEL = ZIEL.with_name("anlage-1-nutzerbelehrung.docx")
BELEHRUNG_TITEL = "Belehrung zur betrieblichen Nutzung von KI"
BELEHRUNG_FELDER = (
    ("name", "Name und Vorname", 24),
    ("organisationseinheit", "Organisationseinheit", 24),
    ("ort_datum", "Ort und Datum", 24),
    ("unterschrift", "Unterschrift", 56),
)

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
                absatz.paragraph_format.keep_with_next = ist_kopf
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
    setze_absatzformat(absatz, danach=0, zeilen=1.0, zusammenhalten=True)
    absatz.paragraph_format.keep_with_next = True
    run = absatz.add_run()
    bild = run.add_picture(str(pfad), width=Cm(breite_cm))
    if bild.height > Cm(20.5):
        bild.width = int(bild.width * Cm(20.5) / bild.height)
        bild.height = Cm(20.5)
    inline = bild._inline
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


def quellenverweis(absatz, quelle, fundstelle=None):
    element = OxmlElement("w:hyperlink")
    element.set(qn("w:anchor"), f"quelle_{quelle['_nummer']}")
    run = OxmlElement("w:r")
    eigenschaften = OxmlElement("w:rPr")
    stil = OxmlElement("w:rStyle")
    stil.set(qn("w:val"), "Hyperlink")
    eigenschaften.append(stil)
    run.append(eigenschaften)
    inhalt = OxmlElement("w:t")
    inhalt.text = f"[{quelle['_nummer']}]" + (f" {fundstelle}" if fundstelle else "")
    run.append(inhalt)
    element.append(run)
    absatz._p.append(element)


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
        "Heading 1": (16, BLAU, 16, 8, False),
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
        ("TOC 1", 10.5, 0.0, 1, 1),
        ("TOC 2", 10.0, 0.6, 0, 0),
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


def add_heading(doc, text, ebene):
    p = doc.add_heading(text, level=ebene)
    p.paragraph_format.keep_with_next = True
    return p


def inhaltsverzeichnis(doc):
    doc.add_paragraph("Inhaltsverzeichnis", style="Vorspannüberschrift")
    feldabsatz = doc.add_paragraph()
    feldabsatz.paragraph_format.space_after = Pt(0)
    füge_inhaltsverzeichnisfeld_hinzu(feldabsatz)


def richte_seiten_ein(doc, version, *, belehrung=False):
    abschnitt = doc.sections[0]
    abschnitt.page_width = Cm(21)
    abschnitt.page_height = Cm(29.7)
    abschnitt.top_margin = Cm(2.5)
    abschnitt.bottom_margin = Cm(2.5)
    abschnitt.left_margin = Cm(2.5)
    abschnitt.right_margin = Cm(2.5)
    abschnitt.header_distance = Cm(1.25)
    abschnitt.footer_distance = Cm(1.25)
    abschnitt.different_first_page_header_footer = False

    kopf = abschnitt.header
    p = kopf.paragraphs[0]
    p.style = doc.styles["Laufende Kopfzeile"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.SPACES)
    p.add_run("Nutzerbelehrung" if belehrung else DOKUMENTTITEL).bold = True
    p.add_run("\t")
    p.add_run("Anlage 1" if belehrung else f"Version {version}")
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(DUNKELGRAU)
    if not belehrung:
        status_p = p.insert_paragraph_before()
        status_p.style = doc.styles["Laufende Kopfzeile"]
        status_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        status_p.paragraph_format.space_after = Pt(2)
        status_p.paragraph_format.line_spacing = 1.0
        status_run = status_p.add_run(ÖFFENTLICH)
        status_run.bold = True
        status_run.font.name = "Calibri"
        status_run.font.size = Pt(9)
        status_run.font.color.rgb = RGBColor.from_string(DUNKELBLAU)
    setze_absatzrahmen(p, position="bottom", farbe=RAHMENGRAU, stärke=4, abstand=5)

    fuß = abschnitt.footer
    p = fuß.paragraphs[0]
    p.style = doc.styles["Laufende Fußzeile"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.SPACES)
    if not belehrung:
        p.add_run("ÖFFENTLICH")
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



def dokumentsteuerung(doc, version, kennzeichnung, katalog):
    doc.add_paragraph("Dokumentenlenkung", style="Vorspannüberschrift")
    t = doc.add_table(rows=1, cols=2)
    t.rows[0].cells[0].text = "Merkmal"
    t.rows[0].cells[1].text = "Festlegung"
    for a, b in (
        ("Dokumenttitel", DOKUMENTTITEL),
        ("Dokumentstatus", kennzeichnung),
        ("Version", version),
        ("Dokumentdatum", deutsches_datum(katalog['catalog']['metadata']['last-modified'][:10])),
        ("Geltungsbereich", "KI-spezifische Ergänzung des Informationssicherheitskonzepts"),
        ("Szenarien", "Air-Gap und Cloud-Inferenz"),
        ("Modellnutzung", "Inferenz ohne eigenes Training oder Feinabstimmung"),
    ):
        cells=t.add_row().cells
        cells[0].text, cells[1].text=a,b
    formatiere_tabelle(t,[2500,6422])


def vorwort(doc):
    doc.add_paragraph("Vorwort", style="Vorspannüberschrift")
    text_absatz(doc,"Dieses KI-Informationssicherheitskonzept ergänzt ein bestehendes Informationssicherheitskonzept um die Nutzung Künstlicher Intelligenz (KI). Es regelt die zulässigen KI-Funktionen, ihre Daten- und Berechtigungsgrenzen sowie die Verantwortlichkeiten für Auswahl, Prüfung, Änderung und Außerbetriebnahme.")
    text_absatz(doc,"Im Air-Gap-Szenario arbeitet die KI vollständig innerhalb einer vom Internet getrennten Umgebung. Im Cloud-Szenario werden ausschließlich freigegebene Eingaben und Kontextausschnitte an einen zugelassenen Modellanbieter übermittelt. Dokumentbestände, Rechteprüfung und Werkzeugausführung bleiben in beiden Szenarien unter betrieblicher Kontrolle.")
    füge_abbildung_hinzu(doc,UMGEBUNGSUEBERSICHT_ABBILDUNG,
        "Abbildung 1: Zwei getrennte Referenzszenarien mit gemeinsamen Nutzungsregeln.",
        "Air-Gap und Cloud sind getrennte Betriebsvarianten. Im Air-Gap-Szenario befinden sich Anwendungen, Daten und Modelle in der abgeschlossenen Umgebung. Das Cloud-Szenario übermittelt ausschließlich freigegebene Anfragen und ausgewählten Kontext an den zugelassenen Anbieter. Zwischen den beiden Varianten besteht kein automatischer Übergang.",breite_cm=15.8)
    text_absatz(doc,"Fach- und Datenverantwortliche bestimmen zugelassene Anwendungsfälle und Datenarten. Nutzende legen innerhalb dieses Rahmens den Arbeitsauftrag und die erforderlichen Inhalte fest, prüfen Ergebnisse vor der Verwendung und genehmigen Agentenaktionen innerhalb ihrer Befugnisse. Die Nutzerbelehrung ist als Anlage 1 beigefügt.")


def kapitel_eins_bis_acht(doc, kennzeichnung, quellen_nach_id, katalog):
    add_heading(doc,"1 Geltungsbereich",1).paragraph_format.page_break_before=True
    text_absatz(doc,"Dieses Konzept regelt Modellverarbeitung, KI-gestützte Wissenssuche und agentische Projektarbeit. Allgemeine Infrastruktur, IT-Betrieb, Kontenverwaltung und Datenübernahme richten sich nach dem bestehenden Informationssicherheitskonzept. Die eingesetzten Programme stehen in der vorhandenen Softwareliste. Produktwahl, Hardwareumfang und Betriebsparameter sind austauschbar, solange Funktionen und Schutzgrenzen erhalten bleiben (KI-GEL-001, KI-GOV-001).")
    add_heading(doc,"2 Nutzungskonzept",1)
    text_absatz(doc,"Die KI unterstützt Programmierfragen, Code- und Testfallentwürfe, Dokumentauswertung und Zusammenfassungen. Die Wissenssuche verwendet Retrieval-Augmented Generation (RAG). Agentische Funktionen bearbeiten abgegrenzte Aufträge mit den bestehenden Nutzerrechten. Training und Feinabstimmung sind ausgeschlossen. Die Arbeit bleibt ohne KI durchführbar (KI-GOV-002, KI-TRN-001).")
    add_heading(doc,"3 Mitgeltende Vorgaben",1)
    p=text_absatz(doc,"Das Informationssicherheitskonzept und die für den jeweiligen Zweck geltenden Datenschutz-, Informationsschutz- und Freigaberegeln gelten auch für die KI-Nutzung. Dieses Dokument ergänzt ausschließlich die KI-spezifischen Aspekte. Allgemeine Anbieter- und Cloud-Betriebsregeln verbleiben in den bestehenden Verfahren (KI-GEL-001, KI-REC-001). ")
    quellenverweis(p,quellen_nach_id['Q-BSI-2002-001'],'S. 69–74, 154–156')
    add_heading(doc,"4 Verarbeitungs- und Zugriffsgrenzen",1)
    add_heading(doc,"4.1 Air-Gap-Szenario",2)
    text_absatz(doc,"Chat, Projektassistent, Modelle und Dokumentaufbereitung befinden sich in der abgeschlossenen Umgebung. Es besteht keine Netzwerkverbindung zum Internet oder zu externen KI-Diensten. Die Übernahme benötigter Dateien erfolgt nach dem bestehenden Verfahren. Das Konzept ergänzt dieses um Modellprüfung und KI-bezogene Dokumentaufbereitung (KI-ARC-002, KI-MOD-001).")
    füge_abbildung_hinzu(doc,ARCHITEKTUR_ABBILDUNG,
        "Abbildung 2: Air-Gap-Verarbeitung ohne Verbindung zu externen KI-Diensten.",
        "Dateien werden über das bestehende Übernahmeverfahren in die getrennte Umgebung eingebracht. Der gestrichelte Pfeil bezeichnet eine Dateiübernahme und keine Netzwerkverbindung. Chat und Projektassistent verwenden interne Modelle. Wissenssuche und Dokumentaufbereitung greifen nur auf berechtigte interne Daten zu.",breite_cm=15.8)
    add_heading(doc,"4.2 Cloud-Szenario",2)
    text_absatz(doc,"Chatanwendung und Projektassistent verwenden den betrieblich freigegebenen Modellzugang. Dokumentablage, Dokumentaufbereitung, Suchvektoren und Rechteprüfung bleiben intern. Der Zugang übermittelt nur ausgewählte Eingaben und berechtigte Kontextausschnitte an den zugelassenen Anbieter. Die Freigabe erfasst auch automatisch erzeugte Folgeanfragen und Werkzeugrückmeldungen (KI-ARC-002, KI-API-002, KI-EXT-001).")
    füge_abbildung_hinzu(doc,CLOUD_ABBILDUNG,
        "Abbildung 3: Cloud-Inferenz mit begrenzter Übermittlung und intern geprüften Datenrechten.",
        "Interne Anwendungen greifen über den freigegebenen KI-Zugang auf ein Anbietermodell zu. Nur ausgewählte Eingaben und berechtigte Kontextausschnitte verlassen den internen Bereich. Antworten werden intern geprüft. Der Anbieter hat keinen direkten Zugriff auf interne Dokumentbestände oder lokale Werkzeuge. Externe Dokumentaufbereitung und anbieterbetriebene Werkzeuge gehören nicht zu diesem Szenario.",breite_cm=15.8)
    text_absatz(doc,"Das Cloud-Szenario umfasst keine anbieterbetriebenen Werkzeuge, keine externe Dokumentaufbereitung und keine Verarbeitung von Verschlusssachen. Änderungen an diesem Umfang werden vor ihrer Nutzung nach KI-VAL-002 bewertet. Ein Wechsel zwischen Air-Gap und Cloud erfolgt nicht automatisch (KI-EXT-001, KI-EXT-002).")
    add_heading(doc,"4.3 Anmeldung und Administration",2)
    text_absatz(doc,"Die Chatanwendung nutzt die betriebliche Identitätsverwaltung. Der Projektassistent arbeitet in der regulären Nutzersitzung. Die Administration verwaltet Modelle, serverseitige Werkzeuge und Aufgabenprofile. Technische Dienstzugänge ersetzen keine Prüfung individueller Nutzerrechte (KI-API-001, KI-IAM-001).")
    add_heading(doc,"4.4 Agentenaktionen und interne Verarbeitung",2)
    text_absatz(doc,"Genehmigte Datei- und Befehlsaktionen des Projektassistenten laufen mit den bestehenden Nutzerrechten. Ein interner Ausführungsdienst der Chatanwendung ist ausschließlich für deren Verarbeitung erreichbar. Er stellt keinen eigenen serverseitigen Codeausführungszugang für Nutzende bereit (KI-AGT-001, KI-TOL-002).")
    add_heading(doc,"5 Modelle und Dokumentkontext",1)
    add_heading(doc,"5.1 Modellbereitstellung",2)
    text_absatz(doc,"Lokale Modelle werden auf Herkunft, Integrität und Ladeformat geprüft. Cloud-Modelle werden über den freigegebenen Zugang mit zulässigen Testdaten erprobt. Änderungen an Modellen, Aufgabenprofilen oder verfügbaren Funktionen unterliegen der Änderungsprüfung (KI-MOD-001, KI-MOD-002, KI-VAL-001).")
    füge_abbildung_hinzu(doc,ARTEFAKTIMPORT_ABBILDUNG,
        "Abbildung 4: Modellprüfung und Freigabe entsprechend dem Betriebsweg.",
        "Lokale Modellartefakte durchlaufen das vorhandene Übernahmeverfahren sowie Herkunfts- und Integritätsprüfung. Bei Cloud-Modellen werden der zugelassene Dienst und sein Funktionsumfang geprüft. Beide Wege führen über fachliche Erprobung und Prüfung der Zugriffsgrenzen zur Modellfreigabe. Nicht freigegebene Modelle bleiben gesperrt.",breite_cm=12.5)
    add_heading(doc,"5.2 Dokumentauswahl und Aufbereitung",2)
    text_absatz(doc,"Fach- und Datenverantwortliche legen je Anwendungsfall zulässige und ausgeschlossene Datenarten fest. Nutzende wählen daraus die für ihren Auftrag erforderlichen Dokumente innerhalb ihrer Befugnisse aus. Vor Aufnahme und danach regelmäßig werden Herkunft, Vertrauenswürdigkeit, fachliche Eignung, Aktualität, Vollständigkeit sowie Nutzungs- und Verarbeitungsrechte geprüft. Dokumente unbekannter oder nicht vertrauenswürdiger Herkunft werden nicht aufgenommen. Die interne Aufbereitung verwendet bei Bedarf Optical Character Recognition (OCR), führt Quellrechte fort und stellt nur berechtigte Ausschnitte bereit. Die zusätzliche Cloud-Freigabe gilt für alle übermittelten Inhalte, auch wenn sie automatisch aus Dateien oder Werkzeugantworten ergänzt werden (KI-RAG-001 bis KI-RAG-004, KI-EXT-001).")
    add_heading(doc,"6 Einstufung und Verwendung von Informationen",1)
    text_absatz(doc,"Die erstellende Person legt die Einstufung eigener Informationen im Rahmen ihrer Befugnisse fest. Vorgegebene Einstufungen verwendeter Quellen bleiben erhalten. Bei Ergebnissen wird auch der Schutzbedarf zusammengeführter Informationen berücksichtigt. Die Entscheidung über Verarbeitung und Weitergabe bleibt an Zweck, berechtigten Empfängerkreis und den zugelassenen Verarbeitungsumfang gebunden (KI-REC-001, KI-REC-002).")
    add_heading(doc,"7 Aufgaben und Nutzerbelehrung",1)
    text_absatz(doc,"Die KI-Verantwortlichen steuern die zugelassenen KI-Funktionen. Fach- und Datenverantwortliche legen Anwendungsfälle und Datenarten fest. Die Administration stellt die freigegebenen Funktionen bereit. Testverantwortliche planen Prüfungen, dokumentieren die tatsächlich ausgeführten Schritte und bewerten Ergebnisse gemeinsam mit den Fachverantwortlichen. Änderungsverantwortliche entscheiden über den erforderlichen Prüfumfang. Betriebsverantwortliche behandeln Störungen und Außerbetriebnahmen. Nutzende bestimmen innerhalb der Freigaben Inhalte, Auftrag und Aktionsumfang und prüfen Ergebnisse vor ihrer Verwendung. Die Informationssicherheitsverantwortlichen bewerten die KI-spezifischen Risiken im bestehenden Zuständigkeitsrahmen (KI-GOV-001 bis KI-GOV-003).")
    text_absatz(doc,"Die Belehrung erfolgt anhand der Anlage 1. Die Unterschrift bestätigt ausschließlich Teilnahme, Verständnis und persönliche Verpflichtung zur Einhaltung der Regeln. Sie ersetzt weder technische Prüfungen noch die fachliche Freigabe oder den Nachweis der betrieblichen Wirksamkeit. Die Belehrung umfasst Datenauswahl, Einstufung, Ergebnisprüfung und Agentenaktionen. Bei Cloud-Nutzung behandelt sie zusätzlich den zulässigen Umfang der Übermittlung an den Anbieter (KI-GOV-002).")
    add_heading(doc,"8 Risikoanalyse",1)
    add_heading(doc,"8.1 Bewertungsverfahren",2)
    register=next(p for g in katalog['catalog']['groups'] for c in g['controls'] if c['id']=='ki-gov-003' for p in c['parts'] if p['name']=='risk-register')
    p=text_absatz(doc,register['prose']+' ')
    quellenverweis(p,quellen_nach_id['Q-BSI-2003-001'],'S. 26–28, 33–35')
    füge_abbildung_hinzu(doc,RISIKOBEWERTUNG_ABBILDUNG,
        "Abbildung 5: Szenariobezogene Bewertung und Behandlung der KI-Risiken.",
        "Der Ablauf erfasst Zweck und Datenumfang, bewertet Häufigkeit und Schadenshöhe und berücksichtigt die wirksamen KI-Kontrollen. Air-Gap und Cloud werden getrennt bewertet. Nicht akzeptable Risiken führen zu zusätzlichen Grenzen oder zur Unterbrechung der betroffenen Funktion.",breite_cm=14.0)
    add_heading(doc,"8.2 Risikomatrix",2)
    füge_abbildung_hinzu(doc,RISIKOMATRIX_ABBILDUNG,
        "Abbildung 6: Gemeinsamer Bewertungsmaßstab für beide Szenarien.",
        "Vier mal vier Risikomatrix nach BSI-Standard 200-3. Häufigkeit und Schadenshöhe ergeben geringes, mittleres, hohes oder sehr hohes Risiko. Die einzelnen Ausgangs- und Restbewertungen für Air-Gap und Cloud stehen im anschließenden Risikoregister.",breite_cm=15.8)
    add_heading(doc,"8.3 Risikoregister",2)
    for risk in register['parts']:
        add_heading(doc,risk['title'],3)
        text_absatz(doc,risk['prose'])
        cloud=next(p for p in risk['parts'] if p['name']=='cloud-assessment')
        t=doc.add_table(rows=1,cols=3)
        for cell,title in zip(t.rows[0].cells,('Szenario','Ausgangsrisiko','Restrisiko')): cell.text=title
        for title,item in [('Air-Gap',risk),('Cloud',cloud)]:
            cells=t.add_row().cells
            cells[0].text=title
            for i,pre in enumerate(('initial','residual'),1):
                cells[i].text=' × '.join(prop(item,pre+'-'+n)[0] for n in ('likelihood','impact'))+' = '+prop(item,pre+'-risk')[0]
        formatiere_tabelle(t,[1500,3711,3711])
        text_absatz(doc,teil(risk,'treatment'))
        text_absatz(doc,teil(risk,'initial-reasoning'))
        text_absatz(doc,teil(risk,'residual-reasoning'))
        text_absatz(doc,'Cloud: '+cloud['prose'])
        doc.add_paragraph('Zugeordnete Maßnahmen: '+', '.join(l['href'][1:].upper() for l in risk['links'])+'.')


def erzeuge_docx(ziel, *, belehrung=False):
    ziel=Path(ziel).resolve()
    katalog=lade_json(KATALOG_PFAD)
    register=lade_json(REGISTER_PFAD)
    status=lade_json(STATUS_PFAD)
    if status != {'dokumentstatus':'ÖFFENTLICH', 'organisationsspezifisch':False,
                  'betriebsmodell':'unternehmensintegriert', 'externe-inferenz':False,
                  'modelltraining':False, 'feinabstimmung':False}:
        raise SystemExit('Dokumenterzeugung abgebrochen: dieser Generator erzeugt nur die öffentliche Referenz ohne aktivierte Inferenz oder Training.')
    version=katalog['catalog']['metadata']['version']
    doc=Document()
    richte_stile_ein(doc)
    richte_seiten_ein(doc,version,belehrung=belehrung)
    doc.core_properties.title=BELEHRUNG_TITEL if belehrung else DOKUMENTTITEL
    doc.core_properties.author=''
    doc.core_properties.last_modified_by=''
    doc.core_properties.subject='Betriebliche KI-Nutzung' if belehrung else ÖFFENTLICH
    doc.core_properties.keywords='KI, Informationssicherheit, Air-Gap, Cloud'
    doc.core_properties.comments=''
    if belehrung:
        nutzerbelehrung(doc)
    else:
        for _ in range(4): doc.add_paragraph()
        p=doc.add_paragraph(style='Title')
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run('ALLGEMEINES\nKI-INFORMATIONSSICHERHEITSKONZEPT')
        p=doc.add_paragraph('Air-Gap und Cloud-Inferenz')
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.size=Pt(16)
        setze_absatzformat(p,danach=26)
        doc.add_paragraph(ÖFFENTLICH,style='Dokumentstatus')
        p=doc.add_paragraph('Version '+version)
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        doc.add_page_break()
        vorwort(doc)
        doc.add_page_break()
        dokumentsteuerung(doc,version,ÖFFENTLICH,katalog)
        doc.add_page_break()
        inhaltsverzeichnis(doc)
        for n,q in enumerate(register['quellen'],1): q['_nummer']=n
        kapitel_eins_bis_acht(doc,ÖFFENTLICH,{q['id']:q for q in register['quellen']},katalog)
        kapitel_neun(doc,katalog,{q['oscal_uuid']:q for q in register['quellen']})
        kapitel_zehn_bis_dreizehn(doc,katalog)
        kapitel_vierzehn(doc,register)
    ziel.parent.mkdir(parents=True,exist_ok=True)
    doc.save(ziel)
    print('DOCX erzeugt:',ziel)



def kapitel_neun(doc, katalog, quellen_nach_uuid):
    add_heading(doc, "9 Sicherheitsmaßnahmen", 1)
    text_absatz(doc, "Die folgenden Kontrollen beschreiben die KI-Sicherheitsmaßnahmen der beiden Referenzszenarien. Die Aufgaben sind in Kapitel 7 zugeordnet. Die Risikobewertung folgt KI-GOV-003.")
    for gruppenindex, gruppe in enumerate(katalog["catalog"]["groups"], start=1):
        add_heading(doc, f"9.{gruppenindex} {gruppe['title']}", 2)
        for control in gruppe.get("controls", []):
            kennung = prop(control, "alt-identifier")[0]
            kontrollüberschrift = add_heading(doc, f"{kennung} – {control['title']}", 3)
            doc.add_paragraph("Geltung: " + prop(control, "anwendbarkeit")[0], style="Kontrollfeldbezeichnung")
            felder = [
                ("Festlegung", teil(control, "statement")),
                ("Betrieb und Anwendung", teil(control, "guidance")),
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

            quelle_p = doc.add_paragraph()
            setze_absatzformat(quelle_p, davor=3, danach=8)
            quelle_p.add_run("Quellen: ")
            for index, link in enumerate(control["links"]):
                if index:
                    quelle_p.add_run(" · ")
                q = quellen_nach_uuid[link["href"][1:]]
                fundstelle = link["text"].split("] ", 1)[1]
                # Präzise Seiten-/Abschnittsangaben, längere Webtitel nur im Verzeichnis.
                kurz = fundstelle if re.match(r"^(S\.|§|Art\.|Abschnitt |Kapitel )", fundstelle) and len(fundstelle) <= 100 else None
                quellenverweis(quelle_p, q, kurz)
            unterdrücke_silbentrennung(quelle_p)


def kapitel_zehn_bis_dreizehn(doc, katalog):
    add_heading(doc, "10 Wissenssuche", 1)
    text_absatz(doc, "Nutzende stellen Dokumente bewusst über die freigegebene Dokumentenablage bereit. Die Wissenssuche verarbeitet ausschließlich fachlich freigegebene, hinreichend aktuelle und rechtlich nutzbare Inhalte. Verantwortliche Stelle, Prüfentscheidung und nächster Prüftermin bleiben nachvollziehbar. Die Aufnahme und Verarbeitung folgen KI-RAG-001 (Abbildung 7).")
    text_absatz(doc, "Der Aufbereitungsdienst extrahiert die Dokumentinhalte, das Embedding-Modell erzeugt Suchvektoren und der Suchdienst liefert Textstellen als Kontext an das Hauptmodell. KI-RAG-001 regelt die Aufnahme. KI-RAG-002 und KI-RAG-003 führen die Quellrechte durch Textabschnitte, Suchtreffer und Antworten fort. Aufbewahrung, Sperrung und Löschung erfassen Quelldatei, extrahierten Text, Textabschnitte, Suchvektoren, Indexeinträge, Zwischenspeicher, Gesprächskontext und Sicherungen.")
    füge_abbildung_hinzu(
        doc,
        RAG_ABBILDUNG,
        "Abbildung 7: Die freigegebene Wissenssuche verarbeitet bewusst abgelegte Dokumente unter durchgängigen Quellrechten.",
        "Der Ablauf gilt für freigegebene Suchfunktionen. Auf bewusste Dokumentablage folgen Zweck- und Rechteprüfung, isolierte Aufbereitung und Erzeugung von Suchvektoren. Jede Abfrage prüft aktuelle Rechte und gibt nur berechtigte Textabschnitte an das Hauptmodell. Antworten weisen ihre Quellen aus. Zugriffssperren und Löschung erfassen Ableitungen und Sicherungen. Persönliche Chats und Agentenarbeit werden nicht automatisch aufgenommen.",
        breite_cm=12.0,
    )

    add_heading(doc, "11 Agentische Anwendungen", 1)
    text_absatz(doc, "Der Projektassistent verwendet den für das Szenario freigegebenen Modellzugang. Freigegebene Datei- und Befehlsaktionen laufen in der regulären Nutzersitzung mit den Rechten des angemeldeten Benutzers. In der Ausgangskonfiguration benötigt jede Aktion eine Einzelgenehmigung, auch das Lesen. Projektfreigaben werden auf Aktionsart, Arbeitsbereich oder Pfad, zulässige Datenarten, Ziel und Geltungsdauer begrenzt. Die Nutzerbelehrung nach Anlage 1 behandelt die Prüfung von Auftrag, Freigabeumfang und erwarteter Wirkung (KI-AGT-001, Abbildung 8).")
    text_absatz(doc, "Nutzende und Teams gestalten ihre lokale Projektarbeit mit Projektregeln und Arbeitsabläufen. Diese erweitern weder Nutzerrechte noch Befugnisse zur Änderung von Serverfunktionen. Modellantworten und Werkzeugausgaben dürfen keine Freigabe erteilen, ausweiten oder verlängern. Den Rahmen für Aktionsfreigaben legt KI-TOL-001 fest. Kritische, privilegierte, externe oder nicht beherrschbar rückgängig zu machende Aktionen erfordern weiterhin die konkrete befugte Entscheidung. Die verbindliche Übernahme von Ergebnissen folgt Kapitel 3.")
    text_absatz(doc, "Quellcode, Dokumente und Werkzeugausgaben können eingeschleuste Anweisungen enthalten. KI-PMT-001 behandelt deren Einfluss auf Agentenaktionen. Die Beschränkung auf freigegebene Modellziele wird nach KI-AGT-002 geprüft, einschließlich veränderter Projektkonfigurationen und Fehlerpfade.")
    füge_abbildung_hinzu(
        doc,
        AGENTEN_ABBILDUNG,
        "Abbildung 8: Agentenaktionen beginnen mit Einzelgenehmigungen. Projektfreigaben bleiben an Rechte und Wirkung gebunden.",
        "Der Projektassistent prüft vorgeschlagene Aktionen gegen Auftrag und Nutzerrechte. Standardmäßig wird auch Lesen einzeln genehmigt. Eine bewusste Projektfreigabe kann passende Routineaktionen abdecken. Kritische, privilegierte oder nicht beherrschbar rückgängig zu machende Wirkungen benötigen weiterhin eine konkrete Genehmigung. Unzulässige oder nicht genehmigte Aktionen werden blockiert. Freigegebene Aktionen laufen in der regulären Nutzersitzung mit den Rechten des angemeldeten Benutzers. Verbindliche Übernahme und Freigabe erfolgen im menschlichen Prozess.",
        breite_cm=12.0,
    )

    add_heading(doc, "12 Pflege der KI-Funktionen", 1)
    add_heading(doc, "12.1 Modell- und Funktionsänderungen", 2)
    text_absatz(doc, "Vor einer Erprobung werden Prüfziel, Prüfumfang, Testdaten, Annahmen und Annahmekriterien festgelegt. Testverantwortliche dokumentieren getrennt davon die tatsächlich ausgeführten Prüfschritte, Ergebnisse, Abweichungen und Freigabeentscheidung. Bewertungen oder Selbstauskünfte von Nutzenden werden als solche gekennzeichnet und nicht als ausgeführte technische Prüfung behandelt (KI-VAL-001).")
    text_absatz(doc, "Vor der Bereitstellung einer Änderung wird ihre Auswirkung bewertet. Diese Entscheidung legt fest, welche bestehenden Prüfungen erneut auszuführen sind. Modellwechsel werden mit den betroffenen Aufgabenprofilen, Werkzeugfunktionen und Dokumentbeständen erprobt; bei Cloud-Modellen werden auch vom Anbieter geändertes Verhalten und veränderte Funktionen berücksichtigt. Lokale Modellaliase bleiben dem geprüften Stand zugeordnet. Änderungen an der Dokumentaufbereitung oder am Embedding-Modell berücksichtigen die Konsistenz vorhandener Suchindizes (KI-MOD-002, KI-VAL-001, KI-VAL-002).")
    text_absatz(doc, "Die Fortschreibung des Konzepts richtet sich nach Änderungen an Zweck, Datenverwendung, KI-Berechtigungsgrenzen und Risikobewertung. Ein Austausch von Programmen oder Betriebsmitteln bei unveränderten Konzeptfestlegungen wird in der vorhandenen Softwareliste und den betroffenen Konfigurationen gepflegt (KI-GOV-001, KI-VAL-002).")
    add_heading(doc, "12.2 Protokolle und Auffälligkeiten", 2)
    text_absatz(doc, "Die KI-Protokollierung vermeidet die Übernahme nicht erforderlicher Gesprächs- und Dokumentinhalte. Für jede Protokollart sind Zweck, zugriffsberechtigte Rollen, Aufbewahrungsdauer und Löschzeitpunkt festgelegt. Bei einer Auffälligkeit werden der Modellstand, der betroffene Kontext und die tatsächlichen Werkzeugaktionen betrachtet. Der allgemeine Betrieb und die Vorfallbearbeitung folgen dem bestehenden Informationssicherheitskonzept (KI-OPS-001, KI-OPS-002).")
    add_heading(doc, "12.3 Wiederaufnahme und Außerbetriebnahme", 2)
    text_absatz(doc, "Nach einer Wiederherstellung werden zusammengehörige Modellstände, Aufgabenprofile und Suchindizes auf Konsistenz geprüft. Aktuelle Rechte und Löschstände gelten auch für wiederhergestellte KI-Ableitungen. Bei der Außerbetriebnahme werden Zugänge aufgehoben und alle gespeicherten oder abgeleiteten KI-Daten erfasst. Quelldateien, extrahierte Texte, Textabschnitte, Suchvektoren, Indexeinträge, Gesprächskontexte, Protokolle, Zwischenspeicher und Sicherungen werden nach dem bestehenden Aufbewahrungs- und Löschverfahren behandelt; der Abschluss wird nachvollziehbar bestätigt (KI-OPS-003, KI-DEC-001).")

    add_heading(doc, "13 BSI- und ISO-Zuordnung", 1)
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for i, wert in enumerate(("ID", "Titel", "BSI/IT-Grundschutz", "ISO-Kennungen")):
        t.rows[0].cells[i].text = wert
    for gruppe in katalog["catalog"]["groups"]:
        for control in gruppe.get("controls", []):
            z = t.add_row().cells
            werte = (
                prop(control, "alt-identifier")[0], control["title"],
                ", ".join(prop(control, "mapping-bsi-it-grundschutz")),
                ", ".join(prop(control, "mapping-iso")),
            )
            for i, wert in enumerate(werte):
                z[i].text = wert
    formatiere_tabelle(t, [1250, 3050, 2000, 2622], zentrierte_spalten={0})


def kapitel_vierzehn(doc, register):
    add_heading(doc, "14 Verzeichnisse", 1)
    add_heading(doc, "14.1 Quellenverzeichnis", 2)
    for quelle in register["quellen"]:
        p = doc.add_paragraph()
        setze_absatzformat(p, danach=7)
        p.paragraph_format.keep_together = True
        anker = OxmlElement("w:bookmarkStart")
        anker.set(qn("w:id"), str(quelle["_nummer"]))
        anker.set(qn("w:name"), f"quelle_{quelle['_nummer']}")
        p._p.append(anker)
        p.add_run(f"[{quelle['_nummer']}] ").bold = True
        ende = OxmlElement("w:bookmarkEnd")
        ende.set(qn("w:id"), str(quelle["_nummer"]))
        p._p.append(ende)
        p.add_run(f"{quelle['herausgeber']}: {quelle['titel']}. ")
        if quelle['fassung'] != 'Dokumentation zum Abrufstand':
            p.add_run(f"{quelle['fassung']}. ")
        if not quelle['stand'].casefold().startswith('abrufstand'):
            p.add_run(f"{quellendatum(quelle)}. ")
        hyperlink(p, "Öffentliche Fundstelle", quelle["öffentliche_url"])
        p.add_run(f". Abgerufen am {deutsches_datum(quelle['abrufdatum'])}.")
        unterdrücke_silbentrennung(p)
    add_heading(doc, "14.2 Glossar und Abkürzungen", 2)
    begriffe = [
        ('Agentische Anwendung', 'KI-Anwendung, die im erteilten Auftrag Werkzeuge verwendet. Nutzerrechte und Freigaben begrenzen ihre Aktionen.'),
        ('Air-Gap', 'Betriebsumgebung ohne Netzwerkverbindung zum Internet oder zu externen KI-Diensten. Dateiübernahmen erfolgen über ein geregeltes Verfahren.'),
        ('Anbietertraining', 'Verwendung von Kundeninhalten zur Änderung oder Verbesserung eines Anbietermodells. Im Cloud-Szenario dieses Konzepts ausgeschlossen.'),
        ('API', 'Application Programming Interface. Programmierschnittstelle, über die Anwendungen festgelegte Funktionen eines Dienstes aufrufen.'),
        ('Artefakt', 'Bereitgestellter Modell- oder Softwarebestand einschließlich der für seine Verwendung erforderlichen Bestandteile.'),
        ('Aufgabenprofil', 'Vorbereitete Systemvorgaben und Funktionen einer KI-Anwendung. Es verändert weder Modellgewichte noch Berechtigungen.'),
        ('BfDI', 'Die Bundesbeauftragte für den Datenschutz und die Informationsfreiheit.'),
        ('BMI / BMVg', 'Bundesministerium des Innern / Bundesministerium der Verteidigung.'),
        ('BSI', 'Bundesamt für Sicherheit in der Informationstechnik.'),
        ('Cloud-Inferenz', 'Verarbeitung einer Anfrage beim freigegebenen Anbieter innerhalb des zugelassenen Verarbeitungsumfangs.'),
        ('DSK', 'Konferenz der unabhängigen Datenschutzaufsichtsbehörden des Bundes und der Länder.'),
        ('Embedding / Suchvektor', 'Numerische Darstellung eines Inhalts, mit der inhaltlich ähnliche Textstellen gefunden werden. Sie verändert die Modellgewichte nicht.'),
        ('Endpunkt / Route', 'Festgelegter Zugang zu einer Dienstfunktion. Freigaben bestimmen, wer diese Funktion aufrufen darf.'),
        ('Fine-Tuning / LoRA / RLHF', 'Verfahren zur Anpassung eines Modells. Fine-Tuning bezeichnet die Feinabstimmung, Low-Rank Adaptation eine parameterarme Anpassung und Reinforcement Learning from Human Feedback die Anpassung mit menschlicher Rückmeldung. Alle sind hier ausgeschlossen.'),
        ('Inferenz', 'Verarbeitung einer Anfrage mit einem vorhandenen Modell. Die Modellgewichte werden dabei verwendet und nicht verändert.'),
        ('ISO / IEC', 'Internationale Organisation für Normung / Internationale Elektrotechnische Kommission. Kennungen bezeichnen die herangezogenen Normen.'),
        ('KI', 'Künstliche Intelligenz. Hier: Modelle zur Verarbeitung und Erstellung von Text, Quellcode und Dokumentinhalten.'),
        ('Kontext', 'Informationen für die Bearbeitung einer Anfrage, etwa die Eingabe, vorherige Gesprächsbeiträge und passende Dokumentstellen.'),
        ('MCP', 'Model Context Protocol. Schnittstellenprotokoll zur Anbindung von Werkzeugen und Datenquellen an KI-Anwendungen.'),
        ('Modellalias', 'Stabile Kennung für ein freigegebenes Modell. Die Modellzuordnung kann nach Prüfung geändert werden.'),
        ('Modellgewichte', 'Beim Training bestimmte Parameter eines Modells. Die hier beschriebene Nutzung verändert diese Parameter nicht.'),
        ('OCR', 'Optical Character Recognition. Optische Zeichenerkennung zur Gewinnung von Text aus Bildern oder gescannten Dokumenten.'),
        ('OSCAL', 'Open Security Controls Assessment Language. Offenes NIST-Format für strukturierte Sicherheitsanforderungen und ihre Quellen.'),
        ('Prompt Injection', 'Anweisung innerhalb bereitgestellter Inhalte, die vom eigentlichen Arbeitsauftrag abweicht. Inhalte erteilen keine zusätzlichen Rechte oder Freigaben.'),
        ('RAG', 'Retrieval-Augmented Generation. Ergänzung einer Anfrage um passende Textstellen aus freigegebenen Dokumenten ohne Modelltraining.'),
        ('Restrisiko', 'Risiko, das nach Berücksichtigung der umgesetzten Schutzmaßnahmen verbleibt.'),
        ('Schleuse', 'Verfahren zur kontrollierten Übernahme von Dateien zwischen getrennten Sicherheitsbereichen. Der Ablauf richtet sich nach den bestehenden Bestimmungen.'),
        ('Suchindex', 'Strukturierter Bestand zur Suche in Dokumenten. Er enthält Verweise und gegebenenfalls Suchvektoren unter den Rechten der Quellen.'),
        ('Systemvorgaben', 'Voreingestellte Anweisungen für die Bearbeitung einer Aufgabe durch das Modell. Technische Berechtigungen werden unabhängig davon geprüft.'),
        ('Training', 'Ermittlung oder Änderung von Modellgewichten anhand von Daten. Training ist in der Umgebung ausgeschlossen.'),
        ('Werkzeugaufruf', 'Aufruf einer freigegebenen Funktion innerhalb des Auftrags und der Nutzerrechte, etwa zum Lesen einer Datei.'),
    ]
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Begriff oder Abkürzung"
    t.rows[0].cells[1].text = "Bedeutung im Konzept"
    for begriff, bedeutung in begriffe:
        z = t.add_row().cells
        z[0].text = begriff
        z[1].text = bedeutung
    formatiere_tabelle(t, [2500, 6422])
    for row in t.rows[1:]:
        for absatz in row.cells[1].paragraphs:
            absatz.style = doc.styles["Begriffsdefinition"]


def nutzerbelehrung(doc):
    """Anlage 1 fasst die bestehenden Nutzungsregeln aus KI-GOV-002 zusammen."""
    doc.styles["Normal"].font.size = Pt(10.5)
    doc.styles["Fließtext"].font.size = Pt(10.5)
    titel = doc.styles["Title"]
    titel.font.name = "Calibri"
    titel.font.size = Pt(19)
    titel.font.bold = True
    titel.font.color.rgb = RGBColor(0, 0, 0)
    titel.paragraph_format.space_after = Pt(8)
    p = doc.add_paragraph(BELEHRUNG_TITEL, style="Title")
    for eigenschaften in (titel._element.get_or_add_pPr(), p._p.get_or_add_pPr()):
        rahmen = eigenschaften.find(qn("w:pBdr"))
        if rahmen is not None:
            eigenschaften.remove(rahmen)
    for name in ("Heading 2", "Heading 3"):
        doc.styles[name].font.color.rgb = RGBColor(0, 0, 0)
        doc.styles[name].font.size = Pt(11)
        doc.styles[name].paragraph_format.space_before = Pt(6)
        doc.styles[name].paragraph_format.space_after = Pt(3)

    abschnitte = (
        ("Geltende Bestimmungen",
         "Für die betriebliche Nutzung künstlicher Intelligenz (KI) gelten die jeweils gültigen betrieblichen Bestimmungen "
         "zu Informationssicherheit, Datenschutz und Geheimschutz sowie das Informationssicherheitskonzept und das "
         "zugehörige KI-Informationssicherheitskonzept. Diese Belehrung ergänzt die geltenden Unterweisungen zu Informationsschutz und Datenschutz."),
        ("Nutzungsumfang",
         "Nutzen Sie die freigegebene generative KI über die Chat-Oberfläche oder agentische KI für die Projektarbeit "
         "im Rahmen Ihres betrieblichen Auftrags. Modelle und serverseitige Werkzeuge werden ausschließlich durch die Administration "
         "bereitgestellt. Für die Datenübernahme gelten die bestehenden Verfahren. Die Arbeit bleibt auch ohne KI durchführbar."),
        ("Informationen auswählen und freigeben",
         "Verwenden Sie nur Datenarten, die für den freigegebenen Anwendungsfall und das gewählte Szenario zugelassen sind. Legen Sie die Einstufung eigener Informationen im Rahmen Ihrer Befugnisse fest und entscheiden Sie entsprechend "
         "über Verarbeitung und Weitergabe. Vorgegebene Einstufungen verwendeter Quellen bleiben erhalten. Beachten Sie "
         "den zugelassenen Verarbeitungsumfang der Umgebung. Bei Cloud-Nutzung gilt dies auch für automatisch ergänzten Kontext und Werkzeugrückmeldungen. Private Konten und nicht freigegebene Dienste sind ausgeschlossen. Wählen Sie nur erforderliche Inhalte und berechtigte Empfänger. "
         "Prüfen Sie bei Dokumenten Herkunft, Vertrauenswürdigkeit und Aktualität. Dokumente unbekannter oder nicht vertrauenswürdiger Herkunft werden nicht in die Wissenssuche aufgenommen. Zugangsdaten werden nicht in KI-Eingaben oder den bereitgestellten Kontext aufgenommen."),
        ("Ergebnisse und Agentenaktionen prüfen",
         "Prüfen Sie KI-Ergebnisse und Quellen vor der fachlichen Verwendung. Generierten Code prüfen und testen Sie im "
         "bestehenden Entwicklungsverfahren. Agentische Aktionen laufen in Ihrer regulären Nutzersitzung mit Ihren bestehenden "
         "Rechten. Genehmigen Sie Aktionen zunächst einzeln. Begrenzen Sie Projektfreigaben auf Aktionsart, Arbeitsbereich, betroffene Daten, Ziel, Geltungsdauer "
         "und erwartete Wirkung. Modellantworten und Werkzeugausgaben dürfen Freigaben nicht erweitern. Freigaben sind widerrufbar. Kritische, privilegierte, externe oder nicht beherrschbar rückgängig zu machende Aktionen "
         "benötigen eine konkrete befugte Entscheidung. KI-Ausgaben erweitern keine Befugnisse."),
        ("Auffälligkeiten behandeln",
         "Unterbrechen Sie unzulässige oder unerwartete Aktionen und nutzen Sie die betrieblichen Meldewege. "
         "Die betroffene Nutzung wird erst nach Klärung fortgesetzt."),
    )
    for überschrift, text in abschnitte:
        add_heading(doc, überschrift, 3)
        text_absatz(doc, text)

    add_heading(doc, "Bestätigung", 2)
    bestätigung = text_absatz(doc, "Ich wurde über die betriebliche KI-Nutzung und die damit verbundenen Pflichten belehrt. "
                "Ich habe die Inhalte verstanden, konnte Rückfragen klären und verpflichte mich, diese Regeln bei der "
                "betrieblichen KI-Nutzung einzuhalten. Meine Unterschrift bestätigt ausschließlich Teilnahme, Verständnis "
                "und persönliche Verpflichtung. Sie ersetzt keine technische Prüfung oder fachliche Freigabe.")
    bestätigung.paragraph_format.keep_with_next = True
    # Wiederverwendbare Formularstile halten Beschriftung und Eingabefläche zusammen.
    for name in ("Formularbezeichnung", "Formulareingabe"):
        stil = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        stil.base_style = doc.styles["Normal"]
        stil.font.size = Pt(10)
        stil.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        stil.paragraph_format.space_before = Pt(0)
        stil.paragraph_format.space_after = Pt(0 if name == "Formularbezeichnung" else 6)
        stil.paragraph_format.line_spacing = 1.0
        stil.paragraph_format.keep_with_next = name == "Formularbezeichnung"
    doc.styles["Formularbezeichnung"].font.bold = True
    formular = doc.add_table(rows=2, cols=2)
    formatiere_tabelle(formular, [TABELLENBREITE_DXA // 2] * 2, kopf=False, einzug=0)
    formular._tbl.tblPr.remove(formular._tbl.tblPr.find(qn("w:tblBorders")))
    for index, (_, beschriftung, höhe) in enumerate(BELEHRUNG_FELDER):
        zelle = formular.cell(index // 2, index % 2)
        zelle.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        setze_zellenränder(zelle, oben=0, unten=0, start=0, ende=200)
        p = zelle.paragraphs[0]
        p.style = "Formularbezeichnung"
        p.paragraph_format.keep_with_next = True
        p.add_run(beschriftung)
        unterdrücke_silbentrennung(p)
        p = zelle.add_paragraph("\u00a0", style="Formulareingabe")
        p.paragraph_format.line_spacing = Pt(höhe + 4)
        p.paragraph_format.keep_with_next = index < 2
        setze_absatzrahmen(p, position="bottom", farbe=RAHMENGRAU, stärke=4, abstand=0)
    for p in doc.paragraphs:
        if p.style.name == "Fließtext":
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(4)


def ergänze_belehrungsformular(pdf_pfad):
    """Ergänzt echte AcroForm-Felder im unveränderten PDF-Export der Anlage."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject,
                              DictionaryObject, FloatObject, NameObject,
                              NumberObject, TextStringObject)

    pdf_pfad = Path(pdf_pfad).resolve()
    if not pdf_pfad.is_relative_to(WURZEL):
        raise ValueError("Das Formular muss im Projektverzeichnis bleiben.")
    reader = PdfReader(pdf_pfad)
    if reader.metadata.title != BELEHRUNG_TITEL or reader.get_fields():
        raise ValueError("Erwartet wird ein unbefüllter Word-Export der Nutzerbelehrung ohne Formularfelder.")
    writer = PdfWriter(clone_from=reader)
    felder = ArrayObject()
    schrift = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"), NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
    }))
    ressourcen = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/Helv"): schrift})})
    writer.root_object[NameObject("/AcroForm")] = writer._add_object(DictionaryObject({
        NameObject("/Fields"): felder, NameObject("/SigFlags"): NumberObject(3),
        NameObject("/NeedAppearances"): BooleanObject(False), NameObject("/DR"): ressourcen,
        NameObject("/DA"): TextStringObject("/Helv 11 Tf 0 g"),
    }))
    zeilen = []
    for seite in writer.pages:
        fragmente = {}
        def sammle(text, cm, tm, font, size):
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            if text and y > 70:
                fragmente.setdefault((round(y, 1), x > 280), []).append((x, text))
        seite.extract_text(visitor_text=sammle)
        for (y, _), teile in fragmente.items():
            teile.sort(key=lambda t: t[0])
            zeilen.append((" ".join("".join(t for _, t in teile).split()), seite, teile[0][0], y))
    for feldname, beschriftung, höhe in BELEHRUNG_FELDER:
        treffer = [(seite, x, y) for text, seite, x, y in zeilen if text == beschriftung]
        if len(treffer) != 1:
            raise ValueError(f"Formularbeschriftung nicht eindeutig gefunden: {beschriftung}")
        seite, x, y = treffer[0]
        breite = (TABELLENBREITE_DXA / 2 - 200) / 20
        unten = y - höhe - 7
        if seite.rotation or not (65 <= x <= 305 and unten > 70 and x + breite < float(seite.mediabox.right) - 65):
            raise ValueError(f"Formularfläche liegt außerhalb des Satzspiegels: {beschriftung}")
        ap = DecodedStreamObject()
        ap.set_data(f"q 1 g 0 0 {breite:.2f} {höhe} re f "
                    f"0.65 G 0.5 w 0 0.5 m {breite:.2f} 0.5 l S Q".encode("ascii"))
        ap.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Form"),
                   NameObject("/BBox"): ArrayObject([FloatObject(v) for v in (0, 0, breite, höhe)])})
        feld = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Sig" if feldname == "unterschrift" else "/Tx"),
            NameObject("/T"): TextStringObject(feldname), NameObject("/TU"): TextStringObject(beschriftung),
            NameObject("/Rect"): ArrayObject([FloatObject(v) for v in (x, unten, x + breite, unten + höhe)]),
            NameObject("/F"): NumberObject(4), NameObject("/Ff"): NumberObject(2),
            NameObject("/P"): seite.indirect_reference,
            NameObject("/AP"): DictionaryObject({NameObject("/N"): writer._add_object(ap)}),
        })
        if feldname == "unterschrift":
            feld[NameObject("/Lock")] = writer._add_object(DictionaryObject({
                NameObject("/Type"): NameObject("/SigFieldLock"), NameObject("/Action"): NameObject("/All"),
            }))
        else:
            feld[NameObject("/DA")] = TextStringObject("/Helv 11 Tf 0 g")
            feld[NameObject("/V")] = TextStringObject("")
        referenz = writer._add_object(feld)
        felder.append(referenz)
        if "/Annots" not in seite:
            seite[NameObject("/Annots")] = ArrayObject()
        seite["/Annots"].append(referenz)
        seite[NameObject("/Tabs")] = NameObject("/R")
    with tempfile.NamedTemporaryFile(dir=pdf_pfad.parent, suffix=".tmp", delete=False) as tmp:
        tmp_pfad = Path(tmp.name)
    try:
        writer.write(tmp_pfad)
        kontrolle = PdfReader(tmp_pfad).get_fields()
        if set(kontrolle) != {n for n, _, _ in BELEHRUNG_FELDER} or kontrolle["unterschrift"]["/FT"] != "/Sig":
            raise ValueError("Die Formularprüfung nach dem Speichern ist fehlgeschlagen.")
        tmp_pfad.replace(pdf_pfad)
    finally:
        tmp_pfad.unlink(missing_ok=True)
        writer.close()
    print(f"Digital unterschreibbares PDF erzeugt: {pdf_pfad}")


def prüfe_pdf_zielschutz(pdf_pfad):
    """Verhindert das Überschreiben befüllter, signierter oder geschützter PDFs."""
    from pypdf import PdfReader

    pdf_pfad = Path(pdf_pfad).resolve()
    if not pdf_pfad.is_relative_to(WURZEL):
        raise ValueError("Das PDF-Ziel muss im Projektverzeichnis bleiben.")
    if not pdf_pfad.exists():
        return
    reader = PdfReader(pdf_pfad)
    if reader.is_encrypted:
        raise ValueError("Das vorhandene PDF-Ziel ist verschlüsselt oder kennwortgeschützt und wird nicht überschrieben.")
    if "/Perms" in reader.trailer["/Root"].get_object():
        raise ValueError("Das vorhandene PDF-Ziel enthält Signatur- oder Berechtigungsbeschränkungen und wird nicht überschrieben.")
    for name, feld in (reader.get_fields() or {}).items():
        wert = feld.get("/V")
        if wert not in (None, "", "/Off"):
            raise ValueError(f"Das vorhandene PDF-Ziel enthält ein befülltes oder signiertes Formularfeld ({name}) und wird nicht überschrieben.")


def main():
    befehle = argparse.ArgumentParser(description=__doc__)
    modus = befehle.add_mutually_exclusive_group()
    modus.add_argument("--belehrung", action="store_true", help="Anlage 1 als DOCX erzeugen.")
    modus.add_argument("--belehrung-formular", type=Path, metavar="PDF", help="Word-Export der Anlage um ausfüllbare Felder und Signaturfeld ergänzen.")
    modus.add_argument("--pruefe-pdf-zielschutz", type=Path, metavar="PDF", help="Vorhandenes PDF-Ziel auf Befüllung, Signatur und Schutz prüfen.")
    befehle.add_argument("--ziel", type=Path, help="Zielpfad des DOCX-Masterdokuments.")
    argumente = befehle.parse_args()
    if argumente.belehrung_formular:
        ergänze_belehrungsformular(argumente.belehrung_formular)
        return
    if argumente.pruefe_pdf_zielschutz:
        prüfe_pdf_zielschutz(argumente.pruefe_pdf_zielschutz)
        return
    ziel = argumente.ziel or (BELEHRUNG_ZIEL if argumente.belehrung else ZIEL)
    ziel = ziel if ziel.is_absolute() else WURZEL / ziel
    erzeuge_docx(ziel, belehrung=argumente.belehrung)

if __name__ == '__main__':
    main()
