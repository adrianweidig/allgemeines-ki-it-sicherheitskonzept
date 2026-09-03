#!/usr/bin/env python3
"""Erzeugt die SVG- und PNG-Ableitungen der PlantUML-Diagramme."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


WURZEL = Path(__file__).resolve().parents[1]
QUELLEN = WURZEL / "diagramme"
AUSGABE = WURZEL / "dokumentation" / "medien"
MANIFEST = QUELLEN / "diagramm-manifest.json"
WERKZEUGVERZEICHNIS = WURZEL / ".arbeitsdaten" / "werkzeuge"

PLANTUML_VERSION = "1.2026.6"
PLANTUML_DATEI = f"plantuml-{PLANTUML_VERSION}.jar"
PLANTUML_URL = (
    f"https://github.com/plantuml/plantuml/releases/download/"
    f"v{PLANTUML_VERSION}/{PLANTUML_DATEI}"
)
PLANTUML_SHA256 = "89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690"
DIAGRAMME = (
    "architektur",
    "artefaktimport",
    "rag-datenfluss",
    "agentische-werkzeugnutzung",
)


def sha256(pfad: Path) -> str:
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def geprüfte_jar(pfad: Path) -> Path:
    if not pfad.is_file():
        raise FileNotFoundError(f"PlantUML-JAR nicht gefunden: {pfad}")
    ist = sha256(pfad)
    if ist != PLANTUML_SHA256:
        raise ValueError(
            f"PlantUML-JAR besitzt eine unerwartete SHA-256-Prüfsumme: {ist}"
        )
    return pfad


def lade_werkzeug_herunter() -> Path:
    WERKZEUGVERZEICHNIS.mkdir(parents=True, exist_ok=True)
    ziel = WERKZEUGVERZEICHNIS / PLANTUML_DATEI
    if ziel.is_file() and sha256(ziel) == PLANTUML_SHA256:
        return ziel

    zwischenstand = ziel.with_suffix(".jar.download")
    try:
        with urllib.request.urlopen(PLANTUML_URL, timeout=60) as antwort:
            zwischenstand.write_bytes(antwort.read())
        geprüfte_jar(zwischenstand)
        zwischenstand.replace(ziel)
    finally:
        zwischenstand.unlink(missing_ok=True)
    return ziel


def finde_java() -> str:
    java = shutil.which("java")
    if not java:
        raise FileNotFoundError("Java wurde nicht gefunden; erforderlich ist Java 17 oder neuer.")
    return java


def erzeuge_format(java: str, jar: Path, formatname: str) -> None:
    quellen = [QUELLEN / f"{name}.puml" for name in DIAGRAMME]
    fehlend = [str(p.relative_to(WURZEL)) for p in quellen if not p.is_file()]
    if fehlend:
        raise FileNotFoundError("PlantUML-Quelle fehlt: " + ", ".join(fehlend))

    AUSGABE.mkdir(parents=True, exist_ok=True)
    befehl = [
        java,
        "-DPLANTUML_LIMIT_SIZE=8192",
        "-jar",
        str(jar),
        "-charset",
        "UTF-8",
        f"-t{formatname}",
        "-o",
        str(AUSGABE),
        *(str(pfad) for pfad in quellen),
    ]
    subprocess.run(befehl, check=True, cwd=WURZEL)


def schreibe_manifest() -> None:
    einträge = []
    for name in DIAGRAMME:
        quelle = QUELLEN / f"{name}.puml"
        png = AUSGABE / f"{name}.png"
        svg = AUSGABE / f"{name}.svg"
        if not png.is_file() or not svg.is_file():
            raise FileNotFoundError(f"Ableitungen fehlen für {name}.")
        einträge.append(
            {
                "name": name,
                "quelle": str(quelle.relative_to(WURZEL)).replace("\\", "/"),
                "quelle_sha256": sha256(quelle),
                "png": str(png.relative_to(WURZEL)).replace("\\", "/"),
                "png_sha256": sha256(png),
                "svg": str(svg.relative_to(WURZEL)).replace("\\", "/"),
                "svg_sha256": sha256(svg),
            }
        )

    inhalt = {
        "format": "PlantUML",
        "plantuml_version": PLANTUML_VERSION,
        "plantuml_sha256": PLANTUML_SHA256,
        "auflösung_png_dpi": 180,
        "diagramme": einträge,
    }
    MANIFEST.write_text(
        json.dumps(inhalt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plantuml-jar", type=Path, help="Pfad zur geprüften PlantUML-JAR.")
    parser.add_argument(
        "--werkzeug-herunterladen",
        action="store_true",
        help="Festgelegte PlantUML-JAR laden und per SHA-256 prüfen.",
    )
    argumente = parser.parse_args()

    if argumente.plantuml_jar:
        jar = geprüfte_jar(argumente.plantuml_jar.expanduser().resolve())
    elif argumente.werkzeug_herunterladen:
        jar = lade_werkzeug_herunter()
    else:
        jar = geprüfte_jar(WERKZEUGVERZEICHNIS / PLANTUML_DATEI)

    java = finde_java()
    erzeuge_format(java, jar, "svg")
    erzeuge_format(java, jar, "png")
    schreibe_manifest()
    print(f"Vier PlantUML-Diagramme wurden mit PlantUML {PLANTUML_VERSION} erzeugt.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as fehler:
        print(f"FEHLER: {fehler}", file=sys.stderr)
        raise SystemExit(1)
