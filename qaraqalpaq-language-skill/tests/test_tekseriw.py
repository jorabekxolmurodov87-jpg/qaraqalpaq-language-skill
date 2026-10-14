"""
tekseriw.py uchun testlar.

Ishga tushirish (repozitoriya ildizidan):
    python -m unittest discover -s tests -v
"""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "qaraqalpaq-language", "scripts", "tekseriw.py")
DATA = os.path.join(ROOT, "tests", "data")
sys.path.insert(0, os.path.dirname(SCRIPT))

import tekseriw  # noqa: E402


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


def flagged_words(text):
    return {i.word for i in tekseriw.check_text(text)}


class TogriMatn(unittest.TestCase):
    """Manbalardan olingan to'g'ri matnda soxta xato bo'lmasligi kerak."""

    def test_togri_matn(self):
        issues = tekseriw.check_text(read("togri_matn.txt"))
        self.assertEqual([], [(i.word, i.kind) for i in issues])

    def test_yangi_togri_matn(self):
        # Bu matn skriptni sozlashda ishlatilmagan (held-out)
        issues = tekseriw.check_text(read("yangi_togri_matn.txt"))
        self.assertEqual([], [(i.word, i.kind) for i in issues])

    def test_ozlashmalar_va_qoshma_sozlar(self):
        for w in ["gazeta", "konfeta", "anketa", "qaysıbir", "geybir", "biraq",
                  "birqansha", "imlalıq", "insanlıq", "xızmettegi", "tariyxı",
                  "tiykarǵı", "grammatikalıq", "Qaraqalpaqstannıń", "respublikamızdıń"]:
            with self.subTest(soz=w):
                self.assertEqual([], tekseriw.check_text(w))


class XatoMatn(unittest.TestCase):
    """Ataylab qo'yilgan xatolar topilishi kerak."""

    def setUp(self):
        self.words = flagged_words(read("xato_matn.txt"))

    def test_hamma_xatolar_topiladi(self):
        kutilgan = {
            "tilinin'", "a'lipbesi", "o'zgerdi", "so‘zligi",       # eski imlo
            "Ğalaba", "tiliniñ",                                     # boshqa alifbo
            "bergenде",                                              # aralash yozuv
            "Bu", "tilining", "maqolada", "xususiyatlari", "tahlil", "qilingan",
            "va", "bilan", "jatır",                                  # o'zbekizm/qozoqizm
            "mektepda", "kitapdı", "Awılnıń", "kimden", "mektepga",  # undosh moslashuvi
            "kelıp", "xaliq",                                        # i/ı
            "XALIQ", "JUMBAQLARI",                                   # katta Í
            "kitaplari", "Nókista", "Mektepqa", "Balaga", "Kitaplerdi",  # uyg'unlik
            "Bilimni",
        }
        topilmagan = kutilgan - self.words
        self.assertEqual(set(), topilmagan)


class Takliflar(unittest.TestCase):
    def suggestion(self, word):
        issues = tekseriw.check_text(word)
        self.assertTrue(issues, word)
        return issues[0].suggestion

    def test_uygunlikka_mos_taklif(self):
        self.assertEqual("mektepte", self.suggestion("mektepda"))
        self.assertEqual("mektepke", self.suggestion("mektepga"))
        self.assertEqual("kitaplardı", self.suggestion("kitaplerdi"))
        self.assertEqual("kimnen", self.suggestion("kimden"))
        self.assertEqual("balaǵa", self.suggestion("balaga"))


class FixVaTranslit(unittest.TestCase):
    def test_fix(self):
        src = "Qaraqalpaq tilinin' a'lipbesi o'zgerdi. Ğalaba tiliniñ. bergenде. Ol 'Bala' dedi."
        out, _ = tekseriw.fix_text(src)
        self.assertEqual("Qaraqalpaq tiliniń álipbesi ózgerdi. Ǵalaba tiliniń. bergende. Ol 'Bala' dedi.", out)

    def test_nfc(self):
        out, changes = tekseriw.fix_text("ta\u0301biyiy")
        self.assertEqual("tábiyiy", out)
        self.assertTrue(changes)

    def test_translit(self):
        cases = {
            "Нөкис — Қарақалпақстан Республикасының пайтахты.":
                "Nókis — Qaraqalpaqstan Respublikasınıń paytaxtı.",
            "ҚАРАҚАЛПАҚ ХАЛЫҚ ЖУМБАҚЛАРЫ ТИЛИНИҢ":
                "QARAQALPAQ XALÍQ JUMBAQLARÍ TILINIŃ",
            "съезд, пьеса, медаль, Шымбай, ҳәм":
                "syezd, pyesa, medal, Shımbay, hám",
        }
        for cyr, lat in cases.items():
            with self.subTest(cyr=cyr):
                self.assertEqual(lat, tekseriw.translit_text(cyr))


class CLI(unittest.TestCase):
    def run_cli(self, *args, stdin=""):
        return subprocess.run([sys.executable, SCRIPT, *args], input=stdin,
                              capture_output=True, text=True, encoding="utf-8")

    def test_check_chiqish_kodi(self):
        self.assertEqual(0, self.run_cli("check", "-", stdin="Bul maqalada.").returncode)
        self.assertEqual(1, self.run_cli("check", "-", stdin="tilinin'").returncode)

    def test_json(self):
        r = self.run_cli("check", "-", "--json", stdin="mektepda")
        self.assertIn('"undosh-moslashuvi"', r.stdout)


if __name__ == "__main__":
    unittest.main()
