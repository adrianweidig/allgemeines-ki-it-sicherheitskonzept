#!/usr/bin/env python3
"""Validiert Status, Quellen, OSCAL-Katalog, Dokumente und Veröffentlichungsgrenzen."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import time
import unicodedata
import urllib.error
import urllib.request
import uuid
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree

import regex
from docx import Document
from jsonschema import Draft7Validator, Draft202012Validator, FormatChecker, ValidationError, validators
from pypdf import PdfReader, __version__ as PYPDF_VERSION


WURZEL = Path(__file__).resolve().parents[1]
STATUS_PFAD = WURZEL / "projektstatus.json"
REGISTER_PFAD = WURZEL / "quellen" / "quellenregister.json"
REGISTER_SCHEMA_PFAD = WURZEL / "schemata" / "quellenregister.schema.json"
KATALOG_PFAD = WURZEL / "katalog" / "ki-it-sicherheitskatalog.oscal.json"
OSCAL_SCHEMA_PFAD = WURZEL / "schemata" / "oscal-1.1.3" / "oscal_catalog_schema.json"
DOCX_PFAD = WURZEL / "konzept" / "ki-it-sicherheitskonzept.docx"
PDF_PFAD = WURZEL / "konzept" / "ki-it-sicherheitskonzept.pdf"

ÖFFENTLICH = "ÖFFENTLICH – organisationsneutrale Referenzvorlage"
NICHT_ÖFFENTLICH = "NICHT ÖFFENTLICH – EINSTUFUNG DURCH DIE ORGANISATION ERFORDERLICH"
PFLICHTTEILE = {"statement", "rationale", "guidance", "assessment-objective", "evidence", "source"}


def lade_json(pfad: Path) -> dict[str, Any]:
    with pfad.open(encoding="utf-8") as datei:
        return json.load(datei)


def eigenschaft(quelle: dict[str, Any], name: str) -> list[str]:
    return [p["value"] for p in quelle.get("props", []) if p.get("name") == name]


def katalogkontrollen(katalog: dict[str, Any]) -> Iterable[dict[str, Any]]:
    def aus_gruppe(gruppe: dict[str, Any]) -> Iterable[dict[str, Any]]:
        yield from gruppe.get("controls", [])
        for untergruppe in gruppe.get("groups", []):
            yield from aus_gruppe(untergruppe)

    for gruppe in katalog["catalog"].get("groups", []):
        yield from aus_gruppe(gruppe)
    yield from katalog["catalog"].get("controls", [])


def oscal_validator(schema: dict[str, Any]):
    """OSCAL nutzt ECMA-262-Unicodeklassen, die Python-re nicht versteht."""

    def prüfe_muster(validator, muster, instanz, teilschema):
        if validator.is_type(instanz, "string") and regex.search(muster, instanz) is None:
            yield ValidationError(f"{instanz!r} entspricht nicht {muster!r}")

    validator_klasse = validators.extend(Draft7Validator, {"pattern": prüfe_muster})
    return validator_klasse(schema, format_checker=FormatChecker())


def prüfe_schemata(
    katalog: dict[str, Any], register: dict[str, Any]
) -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    warnungen: list[str] = []
    register_schema = lade_json(REGISTER_SCHEMA_PFAD)
    for problem in sorted(
        Draft202012Validator(register_schema, format_checker=FormatChecker()).iter_errors(register),
        key=lambda eintrag: list(eintrag.path),
    ):
        ort = "/".join(str(teil) for teil in problem.path) or "Wurzel"
        fehler.append(f"Quellenregister-Schema {ort}: {problem.message}")
    oscal_schema = lade_json(OSCAL_SCHEMA_PFAD)
    for problem in sorted(oscal_validator(oscal_schema).iter_errors(katalog), key=lambda eintrag: list(eintrag.path)):
        ort = "/".join(str(teil) for teil in problem.path) or "Wurzel"
        fehler.append(f"OSCAL-1.1.3-Schema {ort}: {problem.message}")
    schema_hash = hashlib.sha256(OSCAL_SCHEMA_PFAD.read_bytes()).hexdigest()
    if schema_hash != "5e120afbd14c480a9498ab6388857ef32b3b880e458525e966ff7c7f59333d90":
        fehler.append("Das eingebundene offizielle OSCAL-1.1.3-Katalogschema besitzt eine unerwartete Prüfsumme.")
    return fehler, warnungen


def wirksame_kennzeichnung(status: dict[str, Any]) -> str:
    return NICHT_ÖFFENTLICH if status.get("organisationsspezifisch") else ÖFFENTLICH


def prüfe_projektstatus(
    status: dict[str, Any], katalog: dict[str, Any] | None = None, *, repository_modus: bool = True
) -> list[str]:
    fehler: list[str] = []
    erwartet = {
        "dokumentstatus",
        "organisationsspezifisch",
        "betriebsmodell",
        "externe-inferenz",
        "modelltraining",
        "feinabstimmung",
    }
    if set(status) != erwartet:
        fehler.append("projektstatus.json muss exakt die sechs festgelegten Steuerfelder enthalten.")
    if status.get("betriebsmodell") != "vollständig-lokal":
        fehler.append("Das Betriebsmodell muss vollständig-lokal bleiben.")
    if status.get("modelltraining") is not False:
        fehler.append("Modelltraining ist innerhalb dieses Projekts unzulässig.")
    if status.get("feinabstimmung") is not False:
        fehler.append("Feinabstimmung ist innerhalb dieses Projekts unzulässig.")
    if status.get("organisationsspezifisch") is False and status.get("dokumentstatus") != "ÖFFENTLICH":
        fehler.append("Eine organisationsneutrale Fassung muss den Dokumentstatus ÖFFENTLICH tragen.")
    if repository_modus and status.get("organisationsspezifisch") is not False:
        fehler.append("Das öffentliche Referenzrepository darf keine organisationsspezifische Fassung enthalten.")
    if repository_modus and status.get("dokumentstatus") != "ÖFFENTLICH":
        fehler.append("Das öffentliche Referenzrepository erlaubt ausschließlich den Dokumentstatus ÖFFENTLICH.")
    if repository_modus and status.get("externe-inferenz") is not False:
        fehler.append("Externe Inferenz ist im öffentlichen Standardmodell deaktiviert.")
    if status.get("externe-inferenz") and katalog:
        externe = [c for c in katalogkontrollen(katalog) if c["id"].startswith("ki-ext-")]
        if not externe or any("nicht-anwendbar" in eigenschaft(c, "standardstatus") for c in externe):
            fehler.append("Externe Inferenz ist aktiviert, während zugehörige Kontrollen noch nicht anwendbar geschaltet sind.")
    return fehler


def prüfe_quellenregister(
    register: dict[str, Any], katalog: dict[str, Any], *, lokale_dateien_erforderlich: bool = True
) -> list[str]:
    fehler: list[str] = []
    quellen = register.get("quellen", [])
    ids = [q.get("id") for q in quellen]
    uuids = [q.get("oscal_uuid") for q in quellen]
    if len(ids) != len(set(ids)):
        fehler.append("Das Quellenregister enthält doppelte Quellen-IDs.")
    if len(uuids) != len(set(uuids)):
        fehler.append("Das Quellenregister enthält doppelte OSCAL-UUIDs.")
    heute = date.today()
    for q in quellen:
        qid = q.get("id", "unbekannt")
        url = q.get("öffentliche_url", "")
        if not isinstance(url, str) or not url.startswith("https://"):
            fehler.append(f"{qid}: öffentliche HTTPS-Fundstelle fehlt.")
        if not q.get("stand") or not (q.get("veröffentlichungsdatum") or "Abrufstand" in q.get("stand", "")):
            fehler.append(f"{qid}: Veröffentlichungsdatum oder ausdrücklich dokumentierter Abrufstand fehlt.")
        if not q.get("abrufdatum") or not q.get("letzte_inhaltsprüfung"):
            fehler.append(f"{qid}: Abruf- oder Inhaltsprüfdatum fehlt.")
        if not q.get("verwendete_fundstellen"):
            fehler.append(f"{qid}: konkrete Fundstelle fehlt.")
        if q.get("lokale_fassung") and not url:
            fehler.append(f"{qid}: lokale Fassung besitzt keine öffentliche Internetfundstelle.")
        if q.get("lokale_fassung"):
            lokal = WURZEL / q["lokale_fassung"]["pfad"]
            if not lokal.is_file() and lokale_dateien_erforderlich:
                fehler.append(f"{qid}: registrierte lokale Fassung fehlt.")
            elif lokal.is_file():
                digest = hashlib.sha256(lokal.read_bytes()).hexdigest()
                if digest != q["lokale_fassung"]["sha256"]:
                    fehler.append(f"{qid}: SHA-256 der lokalen Fassung weicht ab.")
                if lokal.stat().st_size != q["lokale_fassung"]["dateigröße_bytes"]:
                    fehler.append(f"{qid}: Dateigröße der lokalen Fassung weicht ab.")
        try:
            wiedervorlage = date.fromisoformat(q["wiedervorlage_am"])
            if wiedervorlage < heute:
                fehler.append(f"{qid}: Wiedervorlage ist seit {wiedervorlage.isoformat()} überfällig.")
        except (KeyError, TypeError, ValueError):
            fehler.append(f"{qid}: Wiedervorlage ist ungültig.")

    ressourcen = katalog["catalog"].get("back-matter", {}).get("resources", [])
    ressourcen_nach_uuid = {r["uuid"]: r for r in ressourcen}
    controls = list(katalogkontrollen(katalog))
    tatsächliche_ableitung = {q["id"]: set() for q in quellen}
    quelle_nach_uuid = {q["oscal_uuid"]: q for q in quellen}
    for c in controls:
        for link in c.get("links", []):
            if not str(link.get("href", "")).startswith("#"):
                fehler.append(f"{c['id']}: Quellenlink ist kein interner Back-Matter-Verweis.")
                continue
            quelle = quelle_nach_uuid.get(link["href"][1:])
            if quelle is None:
                fehler.append(f"{c['id']}: Quellenlink kann nicht zum Quellenregister aufgelöst werden.")
            else:
                tatsächliche_ableitung[quelle["id"]].add(c["id"])
    for q in quellen:
        if q["oscal_uuid"] not in ressourcen_nach_uuid:
            fehler.append(f"{q['id']}: Back-Matter-Ressource fehlt.")
        if set(q.get("abgeleitete_kontrollen", [])) != tatsächliche_ableitung[q["id"]]:
            fehler.append(f"{q['id']}: Rückverweise auf abgeleitete Kontrollen sind nicht synchron.")
    return fehler


def prüfe_katalog(katalog: dict[str, Any]) -> list[str]:
    fehler: list[str] = []
    controls = list(katalogkontrollen(katalog))
    ids = [c.get("id") for c in controls]
    if len(ids) != len(set(ids)):
        fehler.append("Der Katalog enthält doppelte Kontroll-IDs.")
    if len(controls) < 30:
        fehler.append("Der fachliche Katalog ist für den festgelegten Erstentwurf unvollständig.")
    sichtbare: list[str] = []
    for c in controls:
        cid = c.get("id", "unbekannt")
        if not re.fullmatch(r"ki-[a-z]{3}-[0-9]{3}", cid):
            fehler.append(f"{cid}: maschinenlesbare ID entspricht nicht dem festgelegten Muster.")
        alt = eigenschaft(c, "alt-identifier")
        if alt != [cid.upper()]:
            fehler.append(f"{cid}: sichtbare Kennung fehlt oder ist unstabil.")
        sichtbare.extend(alt)
        teile = {p.get("name"): p.get("prose", "") for p in c.get("parts", [])}
        fehlend = PFLICHTTEILE - set(teile)
        if fehlend:
            fehler.append(f"{cid}: Pflichtteile fehlen: {', '.join(sorted(fehlend))}.")
        for name in PFLICHTTEILE & set(teile):
            if len(teile[name].strip()) < 20:
                fehler.append(f"{cid}: Teil {name} ist nicht aussagekräftig.")
        if not c.get("links"):
            fehler.append(f"{cid}: öffentliche Quellenverknüpfung fehlt.")
        if eigenschaft(c, "modalitaet") != ["MUSS"]:
            fehler.append(f"{cid}: normative Modalität MUSS fehlt.")
        if not eigenschaft(c, "verschaerfungsbegruendung"):
            fehler.append(f"{cid}: begründete projektinterne Verschärfung fehlt.")
        for pflichtprop in ("lebenszyklus", "rolle", "anwendbarkeit", "schutzbedarf", "quellenmodalitaet"):
            if not eigenschaft(c, pflichtprop):
                fehler.append(f"{cid}: kontrollierte Eigenschaft {pflichtprop} fehlt.")
        if not eigenschaft(c, "mapping-bsi-it-grundschutz") or not eigenschaft(c, "mapping-iso"):
            fehler.append(f"{cid}: orientierende BSI- oder ISO-Zuordnung fehlt.")
    if len(sichtbare) != len(set(sichtbare)):
        fehler.append("Der Katalog enthält doppelte sichtbare Kennungen.")

    nach_id = {c["id"]: c for c in controls}
    training = nach_id.get("ki-trn-001", {})
    trainingstext = " ".join(p.get("prose", "") for p in training.get("parts", []))
    if not all(begriff in trainingstext for begriff in ("Fine-Tuning", "LoRA", "RLHF", "Modellgewichte")):
        fehler.append("Das Trainings- und Feinabstimmungsverbot ist unvollständig.")
    rag_acl = " ".join(p.get("prose", "") for p in nach_id.get("ki-rag-002", {}).get("parts", []))
    rag_löschung = " ".join(p.get("prose", "") for p in nach_id.get("ki-rag-003", {}).get("parts", []))
    if "Berechtig" not in rag_acl or "Sprachmodell" not in rag_acl:
        fehler.append("Die RAG-Kontrolle enthält keine durchgängige Berechtigungsgrenze.")
    if "Löschung" not in rag_löschung or "Embeddings" not in rag_löschung or "Cache" not in rag_löschung:
        fehler.append("Die RAG-Kontrolle enthält keine vollständige Löschanforderung.")
    tooltext = " ".join(p.get("prose", "") for p in nach_id.get("ki-tol-001", {}).get("parts", []))
    if not all(begriff in tooltext for begriff in ("Lesen", "Schreiben", "Befehlsausführung", "Netzwerkzugriff")):
        fehler.append("Die Agentenkontrolle trennt Tool- und Befehlsfähigkeiten nicht vollständig.")
    externe = [c for c in controls if c["id"].startswith("ki-ext-")]
    if len(externe) < 2 or any(eigenschaft(c, "anwendbarkeit") != ["bedingt-externe-inferenz"] for c in externe):
        fehler.append("Die bedingte Kontrollgruppe für externe Inferenz ist unvollständig oder falsch gekennzeichnet.")
    if any(eigenschaft(c, "standardstatus") != ["nicht-anwendbar"] for c in externe):
        fehler.append("Externe Inferenz muss im Standardzustand nicht anwendbar bleiben.")
    metadata = katalog["catalog"]["metadata"]
    if metadata.get("oscal-version") != "1.1.3":
        fehler.append("Der Katalog muss OSCAL 1.1.3 ausweisen.")
    if eigenschaft(metadata, "modelltraining") != ["ausgeschlossen"] or eigenschaft(metadata, "feinabstimmung") != ["ausgeschlossen"]:
        fehler.append("Metadaten weisen Trainings- oder Feinabstimmungsausschluss nicht aus.")
    return fehler


def _docx_text(pfad: Path) -> str:
    dokument = Document(pfad)
    teile: list[str] = []
    for abschnitt in dokument.sections:
        teile.extend(p.text for p in abschnitt.header.paragraphs)
        teile.extend(p.text for p in abschnitt.footer.paragraphs)
    teile.extend(p.text for p in dokument.paragraphs)
    for tabelle in dokument.tables:
        for zeile in tabelle.rows:
            teile.extend(zelle.text for zelle in zeile.cells)
    with zipfile.ZipFile(pfad) as paket:
        if "word/footnotes.xml" in paket.namelist():
            wurzel = ElementTree.fromstring(paket.read("word/footnotes.xml"))
            namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            teile.extend(knoten.text or "" for knoten in wurzel.iter(namespace + "t"))
    return "\n".join(teile)


def _pdf_text(pfad: Path) -> tuple[str, int]:
    leser = PdfReader(pfad)
    return "\n".join(seite.extract_text() or "" for seite in leser.pages), len(leser.pages)


def normalisiere_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)
    text = re.sub(r"\bSeite\s+\d+\b", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip().casefold()


def prüfe_versionsgleichheit(katalog_version: str, docx_text: str, pdf_text: str) -> list[str]:
    fehler = []
    marker = f"Version {katalog_version}"
    if marker not in docx_text:
        fehler.append("Die DOCX-Fassung weist nicht dieselbe Version wie der Katalog aus.")
    if marker not in pdf_text:
        fehler.append("Die PDF-Fassung weist nicht dieselbe Version wie der Katalog aus.")
    return fehler


def prüfe_dokumente(katalog: dict[str, Any], status: dict[str, Any]) -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    warnungen: list[str] = []
    for pfad in (DOCX_PFAD, PDF_PFAD):
        if not pfad.is_file() or pfad.stat().st_size < 1000:
            fehler.append(f"Dokument fehlt oder ist technisch leer: {pfad.relative_to(WURZEL)}")
    if fehler:
        return fehler, warnungen
    if not zipfile.is_zipfile(DOCX_PFAD):
        fehler.append("Das DOCX ist kein gültiges OOXML-ZIP-Paket.")
        return fehler, warnungen
    try:
        docx_text = _docx_text(DOCX_PFAD)
    except Exception as exc:
        fehler.append(f"DOCX kann nicht technisch geöffnet werden: {exc}")
        return fehler, warnungen
    try:
        pdf_text, seiten = _pdf_text(PDF_PFAD)
    except Exception as exc:
        fehler.append(f"PDF kann nicht technisch geöffnet werden: {exc}")
        return fehler, warnungen
    if seiten < 10:
        fehler.append("Die PDF-Fassung ist für den festgelegten Fachinhalt unerwartet kurz.")
    version = katalog["catalog"]["metadata"]["version"]
    fehler.extend(prüfe_versionsgleichheit(version, docx_text, pdf_text))
    kennzeichnung = wirksame_kennzeichnung(status)
    if kennzeichnung not in docx_text or kennzeichnung not in pdf_text:
        fehler.append("Schutzkennzeichnung ist in DOCX und PDF nicht konsistent wirksam.")
    for c in katalogkontrollen(katalog):
        kennung = c["id"].upper()
        if kennung not in docx_text:
            fehler.append(f"DOCX enthält die Kontroll-ID {kennung} nicht.")
        if kennung not in pdf_text:
            fehler.append(f"PDF enthält die Kontroll-ID {kennung} nicht.")
    norm_docx = normalisiere_text(docx_text)
    norm_pdf = normalisiere_text(pdf_text)
    docx_token = re.findall(r"\b[\wäöüß-]+\b", norm_docx)
    pdf_token = re.findall(r"\b[\wäöüß-]+\b", norm_pdf)
    docx_häufigkeit = Counter(docx_token)
    pdf_häufigkeit = Counter(pdf_token)
    gemeinsame_token = sum((docx_häufigkeit & pdf_häufigkeit).values())
    tokenabdeckung = gemeinsame_token / max(1, len(docx_token))
    docx_wörter = {wort for wort in docx_häufigkeit if len(wort) >= 5}
    pdf_wörter = {wort for wort in pdf_häufigkeit if len(wort) >= 5}
    wortabdeckung = len(docx_wörter & pdf_wörter) / max(1, len(docx_wörter))
    # Fußnoten stehen im OOXML technisch gesammelt am Dokumentende, im PDF aber
    # auf der jeweiligen Seite. Ein globaler Sequenzvergleich wäre deshalb
    # fachlich ungeeignet und bei langen Dokumenten quadratisch langsam.
    if tokenabdeckung < 0.98 or wortabdeckung < 0.97:
        fehler.append(
            "Normalisierter DOCX/PDF-Text weicht zu stark ab "
            f"(Tokenabdeckung {tokenabdeckung:.3f}, Wortabdeckung {wortabdeckung:.3f})."
        )
    return fehler, warnungen


def _menschenlesbare_jsontexte(objekt: Any, pfad: tuple[Any, ...] = ()) -> Iterable[str]:
    if isinstance(objekt, dict):
        for schlüssel, wert in objekt.items():
            if schlüssel in {"öffentliche_url", "href", "$schema", "$id", "pfad", "sha256", "offizielle_sha256_am_prüftag", "normalisierter_text_sha256_beider_fassungen"}:
                continue
            if schlüssel == "value" and "props" in pfad:
                continue
            yield from _menschenlesbare_jsontexte(wert, pfad + (schlüssel,))
    elif isinstance(objekt, list):
        for index, wert in enumerate(objekt):
            yield from _menschenlesbare_jsontexte(wert, pfad + (index,))
    elif isinstance(objekt, str):
        yield objekt


def prüfe_inhaltsgrenzen(katalog: dict[str, Any], register: dict[str, Any]) -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    warnungen: list[str] = []
    texte: list[tuple[str, str]] = []
    for pfad in [
        WURZEL / "README.md",
        WURZEL / "AGENTS.md",
        WURZEL / "SECURITY.md",
        WURZEL / "SUPPORT.md",
        WURZEL / "CONTRIBUTING.md",
        WURZEL / "CODE_OF_CONDUCT.md",
        WURZEL / "CHANGELOG.md",
        *sorted((WURZEL / "dokumentation").rglob("*.md")),
    ]:
        if pfad.is_file():
            texte.append((str(pfad.relative_to(WURZEL)), pfad.read_text(encoding="utf-8")))
    texte.append(("OSCAL-Katalog", "\n".join(_menschenlesbare_jsontexte(katalog))))
    texte.append(("Quellenregister", "\n".join(_menschenlesbare_jsontexte(register))))
    unerwünscht = [r"\bfuer\b", r"\boeffentlich\b", r"\bueberpruefen\b"]
    platzhalter = [r"\bTODO\b", r"\bTBD\b", r"change-me", r"your-name", r"your-repo", r"example\.com", r"lorem ipsum", r"coming soon", r"\bplaceholder\b"]
    positive_konformität = [r"garantiert(?:e|er|es)? Konformität", r"vollständig ISO-konform", r"automatisch BSI-konform", r"dieses Projekt ist zertifiziert"]
    geheimnisse = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", r"\bsk-[A-Za-z0-9]{24,}\b"]
    for name, text in texte:
        verbotener_status = "OF" + "FEN"
        if re.search(rf"\b{verbotener_status}\b", text):
            fehler.append(f"{name}: unzulässige Dokumentstatus-Bezeichnung gefunden.")
        for muster in unerwünscht:
            if re.search(muster, text, re.IGNORECASE):
                fehler.append(f"{name}: unerwünschte deutsche Ersatzschreibweise zu Muster {muster}.")
        for muster in platzhalter:
            if re.search(muster, text, re.IGNORECASE):
                fehler.append(f"{name}: verbotener Platzhalter zu Muster {muster}.")
        for muster in positive_konformität:
            if re.search(muster, text, re.IGNORECASE):
                fehler.append(f"{name}: unzulässige Konformitätsbehauptung.")
        for muster in geheimnisse:
            if re.search(muster, text):
                fehler.append(f"{name}: mögliches Geheimnis gefunden.")
        bereinigt = re.sub(r"https://\S+", "", text)
        if re.search(r"(?<!\d)(?:10|127|169\.254|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}(?!\d)", bereinigt):
            fehler.append(f"{name}: mögliche reale interne IP-Adresse gefunden.")
        if re.search(r"\b[a-z0-9-]+\.(?:local|intern|intra|corp)\b", bereinigt, re.IGNORECASE):
            fehler.append(f"{name}: möglicher organisationsspezifischer Host- oder Domänenname gefunden.")
    return fehler, warnungen


def prüfe_veröffentlichungsliste(pfade: Iterable[str]) -> list[str]:
    fehler = []
    normiert = [p.replace("\\", "/") for p in pfade]
    if any(p.startswith("quellen/lokale-eingaben/") for p in normiert):
        fehler.append("Eine lokale Eingangsdatei ist im Git- oder Veröffentlichungsbestand enthalten.")
    if any(p.startswith(".arbeitsdaten/") for p in normiert):
        fehler.append("Temporäre Arbeitsdaten sind im Git- oder Veröffentlichungsbestand enthalten.")
    return fehler


def _git(*argumente: str, binär: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *argumente], cwd=WURZEL, check=False,
        capture_output=True, text=not binär, encoding=None if binär else "utf-8",
    )


def prüfe_git() -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    warnungen: list[str] = []
    if not (WURZEL / ".git").is_dir():
        warnungen.append("Git-Prüfung übersprungen: Repository ist noch nicht initialisiert.")
        return fehler, warnungen
    lokale_pdfs = sorted((WURZEL / "quellen" / "lokale-eingaben").glob("*.pdf"))
    for pfad in lokale_pdfs:
        relativ = str(pfad.relative_to(WURZEL)).replace("\\", "/")
        ergebnis = _git("check-ignore", "-q", "--", relativ)
        if ergebnis.returncode != 0:
            fehler.append(f"Lokale Eingabe wird nicht von Git ignoriert: {relativ}")
    gelistet = _git("ls-files", "-z", binär=True)
    if gelistet.returncode != 0:
        fehler.append("git ls-files konnte nicht ausgeführt werden.")
    else:
        pfade = [p.decode("utf-8") for p in gelistet.stdout.split(b"\0") if p]
        fehler.extend(prüfe_veröffentlichungsliste(pfade))
    kopf = _git("rev-parse", "--verify", "HEAD")
    if kopf.returncode == 0:
        archiv = _git("archive", "--format=tar", "HEAD", binär=True)
        if archiv.returncode != 0:
            fehler.append("git archive konnte nicht erzeugt werden.")
        else:
            with tarfile.open(fileobj=io.BytesIO(archiv.stdout), mode="r:") as paket:
                fehler.extend(prüfe_veröffentlichungsliste(paket.getnames()))
    else:
        warnungen.append("Archivprüfung übersprungen: Es existiert noch kein Commit.")
    return fehler, warnungen


def _hole_url(url: str, *, vollständig: bool = False, versuche: int = 2) -> tuple[int | None, bytes, str | None]:
    letzter_fehler: str | None = None
    for versuch in range(versuche):
        try:
            kopfzeilen = {"User-Agent": "KI-Sicherheitskonzept-Quellenpruefung/0.1 (+https://github.com/adrianweidig/allgemeines-ki-it-sicherheitskonzept)"}
            if not vollständig:
                kopfzeilen["Range"] = "bytes=0-4095"
            anfrage = urllib.request.Request(url, headers=kopfzeilen, method="GET")
            with urllib.request.urlopen(anfrage, timeout=25) as antwort:
                daten = antwort.read() if vollständig else antwort.read(4096)
                if vollständig and "gzip" in (antwort.headers.get("Content-Encoding") or "").lower():
                    daten = gzip.decompress(daten)
                return antwort.status, daten, None
        except urllib.error.HTTPError as exc:
            if exc.code in {403, 405, 429}:
                return exc.code, b"", str(exc)
            letzter_fehler = str(exc)
            if exc.code in {404, 410}:
                return exc.code, b"", letzter_fehler
        except Exception as exc:
            letzter_fehler = str(exc)
        if versuch + 1 < versuche:
            time.sleep(1.0)
    return None, b"", letzter_fehler


def _normalisierter_pdf_text(daten: bytes) -> str:
    text = "\n".join(seite.extract_text() or "" for seite in PdfReader(io.BytesIO(daten)).pages)
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def prüfe_onlinequellen(register: dict[str, Any]) -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    warnungen: list[str] = []
    quellen = register["quellen"]
    with ThreadPoolExecutor(max_workers=8) as executor:
        aufgaben = {executor.submit(_hole_url, q["öffentliche_url"]): q for q in quellen}
        for aufgabe in as_completed(aufgaben):
            q = aufgaben[aufgabe]
            status, _, meldung = aufgabe.result()
            if status in {404, 410}:
                fehler.append(f"{q['id']}: öffentliche Quelle antwortet mit HTTP {status}.")
            elif status in {403, 405, 429}:
                warnungen.append(f"{q['id']}: HTTP {status}; manuelle Erreichbarkeitsprüfung erforderlich.")
            elif status is None or status >= 500:
                warnungen.append(f"{q['id']}: temporärer Abruffehler; manuelle Prüfung erforderlich ({meldung}).")
            elif status < 200 or status >= 400:
                fehler.append(f"{q['id']}: unerwarteter HTTP-Status {status}.")

    for q in quellen:
        lokal = q.get("lokale_fassung")
        if not lokal:
            continue
        pdf_url = lokal.get("offizielle_pdf_url") or q["öffentliche_url"]
        status, daten, meldung = _hole_url(pdf_url, vollständig=True)
        if status is None or status >= 400:
            if status in {403, 405, 429} or status is None or (status and status >= 500):
                warnungen.append(f"{q['id']}: offizieller PDF-Abgleich temporär nicht möglich ({status or meldung}).")
                continue
            fehler.append(f"{q['id']}: offizieller PDF-Abgleich scheitert mit HTTP {status}.")
            continue
        remote_hash = hashlib.sha256(daten).hexdigest()
        erwartet = lokal.get("offizielle_sha256_am_prüftag")
        if remote_hash != erwartet:
            fehler.append(f"{q['id']}: offizielle PDF-Prüfsumme hat sich seit der Inhaltsprüfung geändert.")
            continue
        if remote_hash != lokal["sha256"]:
            text_hash = hashlib.sha256(_normalisierter_pdf_text(daten).encode("utf-8")).hexdigest()
            registriert = lokal.get("normalisierter_text_sha256_beider_fassungen")
            verfahren = lokal.get("normalisierungsverfahren", "")
            lokaler_pfad = WURZEL / lokal["pfad"]
            lokal_text_hash = registriert
            if lokaler_pfad.is_file():
                lokal_daten = lokaler_pfad.read_bytes()
                lokal_text_hash = hashlib.sha256(_normalisierter_pdf_text(lokal_daten).encode("utf-8")).hexdigest()
            if f"pypdf {PYPDF_VERSION}" not in verfahren:
                fehler.append(f"{q['id']}: Normalisierungsverfahren passt nicht zur installierten pypdf-Version.")
            elif not registriert or text_hash != lokal_text_hash or text_hash != registriert:
                fehler.append(f"{q['id']}: binär abweichende offizielle PDF ist nicht mehr textidentisch zur lokalen Fassung.")
    return fehler, warnungen


def führe_prüfungen_aus(
    *, streng: bool, online: bool, repository_modus: bool, lokale_dateien_erforderlich: bool
) -> int:
    fehler: list[str] = []
    warnungen: list[str] = []
    status = lade_json(STATUS_PFAD)
    register = lade_json(REGISTER_PFAD)
    katalog = lade_json(KATALOG_PFAD)

    for funktion, argumente in [
        (prüfe_schemata, (katalog, register)),
        (prüfe_quellenregister, (register, katalog)),
        (prüfe_katalog, (katalog,)),
        (prüfe_projektstatus, (status, katalog)),
        (prüfe_inhaltsgrenzen, (katalog, register)),
        (prüfe_git, ()),
    ]:
        if funktion is prüfe_projektstatus:
            ergebnis = funktion(*argumente, repository_modus=repository_modus)
        elif funktion is prüfe_quellenregister:
            ergebnis = funktion(*argumente, lokale_dateien_erforderlich=lokale_dateien_erforderlich)
        else:
            ergebnis = funktion(*argumente)
        if isinstance(ergebnis, tuple):
            neue_fehler, neue_warnungen = ergebnis
            fehler.extend(neue_fehler)
            warnungen.extend(neue_warnungen)
        else:
            fehler.extend(ergebnis)

    dokument_fehler, dokument_warnungen = prüfe_dokumente(katalog, status)
    fehler.extend(dokument_fehler)
    warnungen.extend(dokument_warnungen)
    if online:
        online_fehler, online_warnungen = prüfe_onlinequellen(register)
        fehler.extend(online_fehler)
        warnungen.extend(online_warnungen)

    print(f"Validierung: {len(fehler)} Fehler, {len(warnungen)} Warnungen")
    for meldung in warnungen:
        print(f"WARNUNG: {meldung}")
    for meldung in fehler:
        print(f"FEHLER: {meldung}")
    if fehler or (streng and any("überfällig" in w.lower() for w in warnungen)):
        return 1
    print("ERGEBNIS: alle verbindlichen Prüfungen bestanden")
    return 0


def parser() -> argparse.ArgumentParser:
    befehle = argparse.ArgumentParser(description=__doc__)
    befehle.add_argument("--streng", action="store_true", help="Verbindlicher Prüfmodus für Veröffentlichungen.")
    befehle.add_argument("--online", action="store_true", help="Öffentliche Quellen und offizielle PDF-Fassungen online prüfen.")
    befehle.add_argument(
        "--ohne-lokale-eingaben", action="store_true",
        help="Nur für CI-Checkouts: registrierte Metadaten und amtliche Online-Fassungen ohne ignorierte lokale PDFs prüfen.",
    )
    befehle.add_argument(
        "--offline-anpassung", action="store_true",
        help="Organisationsspezifischen Offline-Modus erlauben; niemals im öffentlichen Repository verwenden.",
    )
    return befehle


if __name__ == "__main__":
    argumente = parser().parse_args()
    sys.exit(führe_prüfungen_aus(
        streng=argumente.streng,
        online=argumente.online,
        repository_modus=not argumente.offline_anpassung,
        lokale_dateien_erforderlich=not argumente.ohne_lokale_eingaben,
    ))
