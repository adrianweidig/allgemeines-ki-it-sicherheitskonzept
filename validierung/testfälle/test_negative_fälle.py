from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


WURZEL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WURZEL / "validierung"))

import validiere_projekt as vp  # noqa: E402


class NegativeFälle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.katalog = json.loads(vp.KATALOG_PFAD.read_text(encoding="utf-8"))
        cls.register = json.loads(vp.REGISTER_PFAD.read_text(encoding="utf-8"))
        cls.status = json.loads(vp.STATUS_PFAD.read_text(encoding="utf-8"))

    def kontrollen(self, katalog):
        return {c["id"]: c for c in vp.katalogkontrollen(katalog)}

    def test_doppelte_kontroll_id_wird_abgewiesen(self):
        katalog = copy.deepcopy(self.katalog)
        katalog["catalog"]["groups"][0]["controls"].append(copy.deepcopy(katalog["catalog"]["groups"][0]["controls"][0]))
        self.assertTrue(any("doppelte Kontroll-IDs" in f for f in vp.prüfe_katalog(katalog)))

    def test_fehlende_internetquelle_wird_abgewiesen(self):
        register = copy.deepcopy(self.register)
        register["quellen"][0]["öffentliche_url"] = ""
        self.assertTrue(any("HTTPS-Fundstelle fehlt" in f for f in vp.prüfe_quellenregister(register, self.katalog)))

    def test_quelle_ohne_abrufdatum_wird_abgewiesen(self):
        register = copy.deepcopy(self.register)
        register["quellen"][0]["abrufdatum"] = None
        self.assertTrue(any("Abruf- oder Inhaltsprüfdatum fehlt" in f for f in vp.prüfe_quellenregister(register, self.katalog)))

    def test_quelle_ohne_fundstelle_wird_abgewiesen(self):
        register = copy.deepcopy(self.register)
        register["quellen"][0]["verwendete_fundstellen"] = []
        self.assertTrue(any("konkrete Fundstelle fehlt" in f for f in vp.prüfe_quellenregister(register, self.katalog)))

    def test_lokale_pdf_ohne_öffentliche_url_wird_abgewiesen(self):
        register = copy.deepcopy(self.register)
        lokale = next(q for q in register["quellen"] if q["lokale_fassung"])
        lokale["öffentliche_url"] = ""
        self.assertTrue(any("öffentliche" in f for f in vp.prüfe_quellenregister(register, self.katalog)))

    def test_ci_darf_ignorierte_lokale_pdf_auslassen(self):
        register = copy.deepcopy(self.register)
        lokale = next(q for q in register["quellen"] if q["lokale_fassung"])
        lokale["lokale_fassung"]["pfad"] = "quellen/lokale-eingaben/nicht-vorhanden.pdf"
        fehler = vp.prüfe_quellenregister(
            register, self.katalog, lokale_dateien_erforderlich=False
        )
        self.assertFalse(any("registrierte lokale Fassung fehlt" in f for f in fehler))

    def test_unbegründete_verschärfung_wird_abgewiesen(self):
        katalog = copy.deepcopy(self.katalog)
        control = next(vp.katalogkontrollen(katalog))
        control["props"] = [p for p in control["props"] if p["name"] != "verschaerfungsbegruendung"]
        self.assertTrue(any("Verschärfung fehlt" in f for f in vp.prüfe_katalog(katalog)))

    def test_öffentlicher_status_mit_organisationsdaten_wird_abgewiesen(self):
        status = copy.deepcopy(self.status)
        status["organisationsspezifisch"] = True
        self.assertTrue(any("organisationsspezifische Fassung" in f for f in vp.prüfe_projektstatus(status)))
        self.assertEqual(vp.wirksame_kennzeichnung(status), vp.NICHT_ÖFFENTLICH)

    def test_training_und_feinabstimmung_werden_abgewiesen(self):
        training = copy.deepcopy(self.status)
        training["modelltraining"] = True
        feinabstimmung = copy.deepcopy(self.status)
        feinabstimmung["feinabstimmung"] = True
        self.assertTrue(any("Modelltraining" in f for f in vp.prüfe_projektstatus(training)))
        self.assertTrue(any("Feinabstimmung" in f for f in vp.prüfe_projektstatus(feinabstimmung)))

    def test_externe_inferenz_ohne_aktive_kontrollen_wird_abgewiesen(self):
        status = copy.deepcopy(self.status)
        status["externe-inferenz"] = True
        fehler = vp.prüfe_projektstatus(status, self.katalog, repository_modus=False)
        self.assertTrue(any("noch nicht anwendbar" in f for f in fehler))

    def test_rag_ohne_berechtigungsgrenze_wird_abgewiesen(self):
        katalog = copy.deepcopy(self.katalog)
        control = self.kontrollen(katalog)["ki-rag-002"]
        for teil in control["parts"]:
            teil["prose"] = "Die Verarbeitung wird nach einer allgemeinen technischen Regel geprüft und dokumentiert."
        self.assertTrue(any("Berechtigungsgrenze" in f for f in vp.prüfe_katalog(katalog)))

    def test_rag_ohne_löschanforderung_wird_abgewiesen(self):
        katalog = copy.deepcopy(self.katalog)
        control = self.kontrollen(katalog)["ki-rag-003"]
        for teil in control["parts"]:
            teil["prose"] = "Die Verarbeitung wird nach einer allgemeinen technischen Regel geprüft und dokumentiert."
        self.assertTrue(any("Löschanforderung" in f for f in vp.prüfe_katalog(katalog)))

    def test_agent_ohne_toolbegrenzung_wird_abgewiesen(self):
        katalog = copy.deepcopy(self.katalog)
        control = self.kontrollen(katalog)["ki-tol-001"]
        for teil in control["parts"]:
            teil["prose"] = "Die Agentenfunktion wird nach einer allgemeinen technischen Regel geprüft und dokumentiert."
        self.assertTrue(any("Tool- und Befehlsfähigkeiten" in f for f in vp.prüfe_katalog(katalog)))

    def test_abweichende_dokumentversion_wird_abgewiesen(self):
        fehler = vp.prüfe_versionsgleichheit("0.1.0", "Version 0.2.0", "Version 0.1.0")
        self.assertTrue(any("DOCX" in f for f in fehler))

    def test_erfasste_eingangs_pdf_wird_abgewiesen(self):
        fehler = vp.prüfe_veröffentlichungsliste(["README.md", "quellen/lokale-eingaben/eingang.pdf"])
        self.assertTrue(any("lokale Eingangsdatei" in f for f in fehler))


if __name__ == "__main__":
    unittest.main()
