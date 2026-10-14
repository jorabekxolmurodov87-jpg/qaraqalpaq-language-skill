#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tekseriw.py — Qaraqalpaq tili (2016 latın álipbesi) ushın avtomatik tekseriw quralı.

Uch rejim:
  python tekseriw.py check    [FAYL | -]   # xatolar ro'yxati (standart)
  python tekseriw.py fix      [FAYL | -]   # ISHONCHLI xatolarni avtomatik tuzatadi
  python tekseriw.py translit [FAYL | -]   # kirill qoraqalpoq → lotin (2016)

Qo'shimcha: --json (check uchun), --min-level XATO|OGOH|MASLAHAT

Darajalar:
  XATO      — deyarli aniq imlo xatosi (eski apostrof, boshqa alifbo harfi,
              aralash yozuv, Unicode). `fix` bularni o'zi tuzatadi.
  OGOH      — ehtimoliy xato (o'zbekizm, qo'shimcha moslashuvi, Í/I).
              Avtomatik tuzatilmaydi: kontekstni tekshiring.
  MASLAHAT  — shubhali joy, ko'pincha to'g'ri bo'lishi ham mumkin.

Muhim: bu skript filolog emas. U faqat mexanik ravishda aniqlanadigan
xatolarni ushlaydi. Skriptdan o'tgan matn hali "to'g'ri" degani emas.

Manbalar: KNAB 2016 kirill–lotin jadvali (Eesti Keele Instituut);
"Qaraqalpaq tiliniń orfografiyalıq sózligi", Nókis, «Bilim», 2020;
Qaraqalpaqsha Wikipedia "Atlıq" (seplik jadvali). Batafsil: references/manbalar.md
"""
import argparse
import json
import re
import sys
import unicodedata

# ---------------------------------------------------------------- alifbo
BACK = set("aouı")          # juwan dawıslılar
FRONT = set("áeióú")        # jińishke dawıslılar
VOWELS = BACK | FRONT
# únsiz (jarangsiz) dawıssızlar — x va h ataylab kiritilmagan (manbada tasdiqlanmadi)
VOICELESS = set("ptkqsfc")  # + 'sh', 'ch' alohida tekshiriladi
VOICED_CONS = set("bdgǵjlmnńrvwyz")
NASALS = set("mnń")
NONNASAL_VOICED = set("bdgǵjlrvwyz")

CYR = re.compile(r"[\u0400-\u04FF]")
LAT = re.compile(r"[A-Za-zÁáǴǵÍıŃńÓóÚú]")

# Eski (1995) apostrofli imlo → 2016 akut
APOS = "\u0027\u2018\u2019\u02BB\u02BC\u0060\u00B4"
OLD_APOS = re.compile(r"([AaGgOoUuNn])[" + APOS + "]")
OLD_MAP = {"a": "á", "A": "Á", "g": "ǵ", "G": "Ǵ", "o": "ó", "O": "Ó",
           "u": "ú", "U": "Ú", "n": "ń", "N": "Ń"}

# Boshqa turkiy lotin alifbolaridan "sizib kiradigan" harflar
LOOKALIKE = {
    "ğ": "ǵ", "Ğ": "Ǵ", "ñ": "ń", "Ñ": "Ń", "ŋ": "ń", "Ŋ": "Ń",
    "ä": "á", "Ä": "Á", "ə": "á", "Ə": "Á", "ö": "ó", "Ö": "Ó",
    "ü": "ú", "Ü": "Ú", "ş": "sh", "Ş": "Sh", "ç": "ch", "Ç": "Ch",
    "İ": "I", "ǧ": "ǵ", "Ǧ": "Ǵ", "ɣ": "ǵ",
}

# Kirill → lotin (KNAB 2016 jadvali + 2020 lug'at §19)
CYR2LAT = {
    "а": "a", "ә": "á", "б": "b", "в": "v", "г": "g", "ғ": "ǵ", "д": "d",
    "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k",
    "қ": "q", "л": "l", "м": "m", "н": "n", "ң": "ń", "о": "o", "ө": "ó",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ү": "ú", "ў": "w",
    "ф": "f", "х": "x", "ҳ": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "ı", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "\u0259": "á",  # lotin ə ba'zan kirill ә o'rnida yoziladi
}
CYR2LAT_UPPER = {
    "А": "A", "Ә": "Á", "Б": "B", "В": "V", "Г": "G", "Ғ": "Ǵ", "Д": "D",
    "Е": "E", "Ё": "Yo", "Ж": "J", "З": "Z", "И": "I", "Й": "Y", "К": "K",
    "Қ": "Q", "Л": "L", "М": "M", "Н": "N", "Ң": "Ń", "О": "O", "Ө": "Ó",
    "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U", "Ү": "Ú", "Ў": "W",
    "Ф": "F", "Х": "X", "Ҳ": "H", "Ц": "C", "Ч": "Ch", "Ш": "Sh", "Щ": "Sh",
    "Ъ": "", "Ы": "Í", "Ь": "", "Э": "E", "Ю": "Yu", "Я": "Ya",
    "\u018F": "Á",
}

# O'zbekcha (va bir nechta qozoqcha) so'zlar → qoraqalpoqcha taklif.
# Faqat manbalarda tasdiqlangan qoraqalpoqcha shakllar (references/ozbekizm-qazaqizm.md).
FOREIGN_WORDS = {
    "va": "hám", "bilan": "menen / penen / benen", "uchun": "ushın",
    "bu": "bul", "shu": "sol / usı", "ushbu": "usı / bul", "u": "ol",
    "menga": "maǵan", "unga": "oǵan", "bunga": "buǵan", "shunga": "soǵan",
    "kerak": "kerek", "yaxshi": "jaqsı", "katta": "úlken", "eng": "eń",
    "juda": "dım / asa", "hozir": "házir", "hozirgi": "házirgi",
    "bugun": "búgin", "bugungi": "búgingi", "emas": "emes", "yoq": "joq",
    "haqida": "haqqında / tuwralı", "boyicha": "boyınsha", "orqali": "arqalı",
    "kabi": "kibi / sıyaqlı", "hamma": "hámme", "albatta": "álbette",
    "balki": "bálkim", "ham": "hám (diakritika)", "maktab": "mektep",
    "kitob": "kitap", "kutubxona": "kitapxana", "qishloq": "awıl",
    "xalq": "xalıq", "dunyo": "dúnya", "tarix": "tariyx",
    "adabiyot": "ádebiyat", "madaniyat": "mádeniyat", "jamiyat": "jámiyet",
    "tabiat": "tábiyat", "tabiiy": "tábiyiy", "ilmiy": "ilimiy",
    "vaqt": "waqıt", "masala": "másele", "maqsad": "maqset",
    "natija": "nátiyje", "xususiyat": "ózgeshelik", "xususiyatlari": "ózgeshelikleri",
    "darslik": "sabaqlıq", "oquvchi": "oqıwshı", "harf": "hárip",
    "ovoz": "dawıs", "alifbo": "álipbe", "imlo": "imla", "tarjima": "awdarma",
    "dehqon": "diyqan", "fuqaro": "puqara", "ruxsat": "ruqsat", "fan": "pán",
    "suv": "suw", "yil": "jıl", "yer": "jer", "yol": "jol", "bosh": "bas",
    "ish": "is", "qish": "qıs", "uch": "úsh", "kuch": "kúsh", "bola": "bala",
    "bolalar": "balalar", "mustaqillik": "ǵárezsizlik", "tadqiqot": "izertlew",
    "tahlil": "tallaw (tallanǵan)", "soz": "sóz", "sozlar": "sózler",
    # qozoqcha
    "jatır": "atır (-ıp atır)", "jatir": "atır (-ıp atır)", "osı": "usı",
    "üşin": "ushın",
}
# Uzun o'zbekcha o'zaklar: so'z shu bilan boshlansa (qo'shimchali shakllar uchun)
FOREIGN_STEMS = {
    "xususiyat": "ózgeshelik", "madaniyat": "mádeniyat", "adabiyot": "ádebiyat",
    "kutubxona": "kitapxana", "mustaqillik": "ǵárezsizlik", "tadqiqot": "izertlew",
    "qishloq": "awıl", "maktab": "mektep", "darslik": "sabaqlıq",
    "maqola": "maqala", "sintaktik": "sintaksislik",
}

# i/ı evristikasi uchun istisnolar (manbada tasdiqlangan to'g'ri so'zlar)
I_EXCEPTIONS = {"biraq", "birqansha", "birqatar", "birqıylı"}

# Qo'shimchalar — uyg'unlik tekshiruvi uchun (uzunroqlari oldin)
HARMONY_SUFFIXES = sorted({
    "lardıń", "lerdiń", "larǵa", "lerge", "lardan", "lerden", "larda", "lerde",
    "ları", "leri", "lar", "ler",
    "nıń", "niń", "dıń", "diń", "tıń", "tiń",
    "ǵa", "ge", "qa", "ke",
    "nan", "nen", "dan", "den", "tan", "ten",
    "nda", "nde", "da", "de", "ta", "te",
    "daǵı", "degi", "taǵı", "tegi",
    "atuǵın", "etuǵın", "ǵan", "gen", "qan", "ken",
    "lıq", "lik", "sız", "siz", "shı", "shi",
    "ımız", "imiz", "mız", "miz", "ıp", "ip", "ıw", "iw",
}, key=len, reverse=True)


def vclass(ch):
    if ch in BACK:
        return "B"
    if ch in FRONT:
        return "F"
    return None


def stem_last_vowel_class(stem):
    """Negizdagi oxirgi unli sinfi. 'iy' dagi i hisobga olinmaydi (tariyx, tiykar)."""
    for i in range(len(stem) - 1, -1, -1):
        ch = stem[i]
        if ch == "i" and i + 1 < len(stem) and stem[i + 1] == "y":
            continue
        c = vclass(ch)
        if c:
            return c
    return None


def suffix_class(suf):
    classes = {vclass(c) for c in suf if vclass(c)}
    if len(classes) == 1:
        return classes.pop()
    return "MIXED" if classes else None


def harmonize(suf, stem, devoice=False):
    """Qo'shimchani negizga moslab qayta yozadi: unli qatori + (ixtiyoriy) jarangsizlashtirish."""
    cls = stem_last_vowel_class(stem)
    out = []
    for i, ch in enumerate(suf):
        if devoice and i == 0:
            ch = {"d": "t", "ǵ": "q", "g": "k"}.get(ch, ch)
        if cls == "B":
            ch = {"e": "a", "i": "ı", "g": "ǵ", "k": "q"}.get(ch, ch)
        elif cls == "F":
            ch = {"a": "e", "ı": "i", "ǵ": "g", "q": "k"}.get(ch, ch)
        out.append(ch)
    return "".join(out)


def plausible_suffix(suf, stem):
    """Qo'shimchaning bosh undoshi negiz oxiriga mos kelsa — haqiqiy qo'shimcha bo'lishi ehtimoli bor."""
    c = suf[0]
    last = stem[-1] if stem else ""
    if c in "tqk":
        return ends_voiceless(stem)
    if c in "dǵg":
        return last in VOWELS or last in VOICED_CONS
    if c == "n" and suf[:2] in ("na", "ne", "nı", "ni") and len(suf) == 2:
        return last in VOWELS
    return True


def ends_voiceless(stem):
    if stem.endswith("sh") or stem.endswith("ch"):
        return True
    return bool(stem) and stem[-1] in VOICELESS


class Issue:
    def __init__(self, level, line, word, kind, msg, suggestion=""):
        self.level, self.line, self.word = level, line, word
        self.kind, self.msg, self.suggestion = kind, msg, suggestion

    def as_dict(self):
        return self.__dict__


LEVELS = {"XATO": 3, "OGOH": 2, "MASLAHAT": 1}

TOKEN = re.compile(r"[\w\u0300-\u036f" + APOS + "-]+", re.UNICODE)
# Qo'shtirnoqdagi so'zlarni eski imlodan ajratish: 'bala' yoki ‘bala’
QUOTED = re.compile(r"(?<![\w])([\u0027\u2018])([^\u0027\u2018\u2019\n]{1,80}?)([\u0027\u2019])(?![\w])")


def mask_quotes(text):
    return QUOTED.sub(lambda m: "\uE000" + m.group(2) + "\uE001", text)


def unmask_quotes(text, original):
    # asl qo'shtirnoq belgilarini tartib bilan qaytarish
    opens = [m.group(1) for m in QUOTED.finditer(original)]
    closes = [m.group(3) for m in QUOTED.finditer(original)]
    out, oi, ci = [], 0, 0
    for ch in text:
        if ch == "\uE000":
            out.append(opens[oi]); oi += 1
        elif ch == "\uE001":
            out.append(closes[ci]); ci += 1
        else:
            out.append(ch)
    return "".join(out)


def to_lower(word):
    # Í → ı, I → i (qoraqalpoq qoidasi), qolgani oddiy
    out = []
    for ch in word:
        if ch == "Í":
            out.append("ı")
        elif ch == "I":
            out.append("i")
        else:
            out.append(ch.lower())
    return "".join(out)


def check_word(raw, lineno, issues):
    word = raw.strip("-" + APOS)
    if not word:
        return
    has_cyr, has_lat = bool(CYR.search(word)), bool(LAT.search(word))
    if has_cyr and has_lat:
        issues.append(Issue("XATO", lineno, raw, "aralash-yozuv",
                            "So'z ichida kirill va lotin harflari aralash.",
                            translit_text(word)))
        return
    if has_cyr:
        issues.append(Issue("OGOH", lineno, raw, "kirill-soz",
                            "Lotin matn ichida kirill so'z.", translit_text(word)))
        return
    for ch in word:
        if ch in LOOKALIKE:
            issues.append(Issue("XATO", lineno, raw, "boshqa-alifbo",
                                f"'{ch}' qoraqalpoq 2016 alifbosida yo'q (boshqa turkiy alifbodan).",
                                fix_lookalikes(word)))
            break
    if OLD_APOS.search(raw):
        issues.append(Issue("XATO", lineno, raw, "eski-imlo",
                            "Eski (1995) apostrofli imlo. 2016-yildan akutli harflar.",
                            fix_old_apos(raw)))
        return

    # ---- Katta harf: Í (ı) va I (i)
    letters = [c for c in word if c.isalpha()]
    if len(letters) >= 2 and all(c.isupper() for c in letters):
        up = word
        has_q = "Q" in up or "Ǵ" in up
        has_k = "K" in up or "G" in up
        back = sum(up.count(c) for c in "AOUÍ")
        front = sum(up.count(c) for c in "ÁEÓÚ")
        plain_i = re.findall(r"I(?!Y)", up)
        if plain_i and has_q and not has_k and front == 0 and back > 0:
            issues.append(Issue("OGOH", lineno, raw, "katta-Í",
                                "Orqa qatordagi so'zda 'I' — katta ı harfi 'Í' bo'lishi kerak.",
                                re.sub(r"I(?!Y)", "Í", up)))
    elif word[:1] in ("I", "Í") and len(word) > 2:
        rest = to_lower(word[1:])
        b = any(c in BACK for c in rest)
        f = any(c in FRONT - {"i"} for c in rest)
        q = ("q" in rest or "ǵ" in rest) and not ("k" in rest or "g" in rest)
        if word[0] == "I" and b and not f and q and word[1:2] != "y":
            issues.append(Issue("OGOH", lineno, raw, "katta-Í",
                                "So'z orqa qatorda: bosh harf 'Í' (katta ı) bo'lishi mumkin.",
                                "Í" + word[1:]))

    low = to_lower(word)
    parts = [p for p in low.split("-") if p]
    for p in parts:
        check_part(p, raw, lineno, issues)


def check_part(p, raw, lineno, issues):
    plain = re.sub("[" + APOS + "]", "", p)
    # ---- O'zbekcha / qozoqcha so'zlar
    if plain in FOREIGN_WORDS:
        issues.append(Issue("OGOH", lineno, raw, "ozbekizm/qazaqizm",
                            "O'zbekcha (yoki qozoqcha) so'z bo'lishi mumkin.",
                            FOREIGN_WORDS[plain]))
        return
    for st, sug in FOREIGN_STEMS.items():
        if plain.startswith(st) and plain != st:
            issues.append(Issue("OGOH", lineno, raw, "ozbekizm",
                                f"O'zbekcha o'zak '{st}'.", sug + " + qoraqalpoqcha qo'shimcha"))
            return
    # ---- O'zbekcha qo'shimchalar
    uz_suffix_rules = [
        (r"ning$", "O'zbekcha -ning.", "-nıń/-niń, -dıń/-diń, -tıń/-tiń"),
        (r"[aoui]dagi$|[aoui]tagi$", "O'zbekcha -dagi (orqa so'zda).", "-daǵı / -taǵı"),
        (r"(a|y)digan$", "O'zbekcha -adigan.", "-atuǵın / -etuǵın"),
        (r"yapti$|yapmiz$|yapman$", "O'zbekcha -yapti.", "-ıp atır"),
        (r"moq$", "O'zbekcha -moq infinitivi.", "-ıw / -iw"),
        (r"ingiz$|ngiz$", "O'zbekcha -ingiz.", "-ıńız / -ińiz"),
    ]
    for pat, msg, sug in uz_suffix_rules:
        if re.search(pat, plain):
            issues.append(Issue("OGOH", lineno, raw, "ozbekcha-qoshimcha", msg, sug))
            return
    m_qi = re.search(r"[qǵ]i(?!y)", plain)
    if m_qi and plain not in I_EXCEPTIONS:
        issues.append(Issue("OGOH", lineno, raw, "i/ı",
                            "'q'/'ǵ' dan keyin odatda 'ı' keladi ('qi' o'zbekcha yozuvga xos). "
                            "Butun so'zni qayta tekshiring (masalan: qilingan → qılınǵan).",
                            re.sub(r"([qǵ])i(?!y)", r"\1ı", plain) + " (+ qolgan qismi)"))
    if plain.endswith("ng") and len(plain) > 3:
        issues.append(Issue("MASLAHAT", lineno, raw, "ng",
                            "So'z oxirida 'ng' — qoraqalpoqda odatda 'ń' (o'zlashma bo'lmasa).",
                            plain[:-2] + "ń"))

    # ---- i/ı uyg'unligi evristikasi (o'z so'zlarda q/ǵ faqat orqa unlilar bilan)
    core = plain.replace("bir", "")  # qaysıbir, geybir, birqansha: 'bir' alohida komponent
    if plain not in I_EXCEPTIONS and len(core) >= 3:
        has_q = "q" in core or "ǵ" in core
        has_k = "k" in core or "g" in core
        other_front = any(c in "áeóú" for c in core)
        has_back = any(c in BACK for c in core)
        # so'z boshidagi 'i' hisobga olinmaydi: imla, insan kabi arabcha o'zlashmalar aralash unlili
        bad_i = re.findall(r"(?<!^)i(?!y)", core)
        # 'i' orqa unlidan KEYIN kelsa (xaliq, jumbaqlari) — ehtimoliy xato
        i_after_back = re.search(r"[aouı][^aouıáeióú]*i(?!y)", core)
        if bad_i and i_after_back and has_q and not has_k and not other_front and has_back:
            issues.append(Issue("OGOH", lineno, raw, "i/ı",
                                "Orqa qatordagi so'zda 'i' — 'ı' bo'lishi mumkin.",
                                re.sub(r"(?<!^)i(?!y)", "ı", plain)))
        # 'ı' old unlidan KEYIN kelsa (kelıp) — ehtimoliy xato; xızmet kabi o'zlashmalarda ı oldinda
        ı_after_front = re.search(r"[áeióú][^aouıáeióú]*ı", plain)
        if ı_after_front and not has_q and not any(c in "aou" for c in plain):
            issues.append(Issue("OGOH", lineno, raw, "i/ı",
                                "Old qatordagi so'zda 'ı' — 'i' bo'lishi mumkin.",
                                plain.replace("ı", "i")))

    if len(plain) < 4:
        return
    # ---- Qo'shimcha: undosh moslashuvi
    def stem_of(suf):
        return plain[: -len(suf)]

    # (a) únsiz dawıssızdan keyin d/ǵ/g bilan boshlanadigan qo'shimcha
    for suf, exp in [("dıń", "tıń"), ("diń", "tiń"), ("dan", "tan"), ("den", "ten"),
                     ("daǵı", "taǵı"), ("degi", "tegi"), ("da", "ta"), ("de", "te"),
                     ("dı", "tı"), ("di", "ti"), ("ǵan", "qan"), ("gen", "ken"),
                     ("ǵa", "qa"), ("ge", "ke"), ("ga", "qa/ke")]:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and ends_voiceless(st):
                exp = harmonize(suf, st, devoice=True)
                issues.append(Issue("OGOH", lineno, raw, "undosh-moslashuvi",
                                    f"Jarangsiz undoshdan keyin '-{suf}' emas, '-{exp}'.",
                                    st + exp))
                return
            break
    # (b) jarangli/unlidan keyin t-li qo'shimcha
    for suf, exp in [("tıń", "nıń/dıń"), ("tiń", "niń/diń"), ("tan", "dan/nan"), ("ten", "den/nen")]:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and (st[-1] in VOWELS or st[-1] in VOICED_CONS) and not st.endswith("s"):
                issues.append(Issue("OGOH", lineno, raw, "undosh-moslashuvi",
                                    f"Unli/jarangli tovushdan keyin '-{suf}' emas ('-{exp}').", ""))
                return
            break
    # (c) burun tovushlari (m, n, ń) dan keyin chiqish kelishigi -nan/-nen
    for suf, exp in [("dan", "nan"), ("den", "nen")]:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 2 and st[-1] in NASALS:
                issues.append(Issue("OGOH", lineno, raw, "undosh-moslashuvi",
                                    f"m/n/ń dan keyin chiqish kelishigi '-{exp}' (kimnen, ózimnen).",
                                    st + exp))
                return
    # (d) l, r, w, y, z ... dan keyin -nan/-nen emas, -dan/-den
    for suf, exp in [("nan", "dan"), ("nen", "den")]:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and st[-1] in NONNASAL_VOICED:
                issues.append(Issue("OGOH", lineno, raw, "undosh-moslashuvi",
                                    f"'{st[-1]}' dan keyin '-{exp}' (awıldan).", st + exp))
                return
    # (e) undoshdan keyin -nıń/-niń (n, ń, m dan tashqari) noto'g'ri
    for suf in ("nıń", "niń"):
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and st[-1] not in VOWELS and st[-1] not in NASALS:
                exp = ("tıń" if suf == "nıń" else "tiń") if ends_voiceless(st) else \
                      ("dıń" if suf == "nıń" else "diń")
                issues.append(Issue("OGOH", lineno, raw, "undosh-moslashuvi",
                                    f"Undoshdan keyin qaratqich '-{exp}' (mekteptiń, awıldıń).",
                                    st + exp))
                return
    # (f) undoshdan keyin tushum -nı/-ni (o'zbekcha -ni ta'siri)
    for suf in ("nı", "ni"):
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and st[-1] not in VOWELS:
                exp = ("tı" if suf == "nı" else "ti") if ends_voiceless(st) else \
                      ("dı" if suf == "nı" else "di")
                issues.append(Issue("MASLAHAT", lineno, raw, "undosh-moslashuvi",
                                    f"Undoshdan keyin tushum kelishigi odatda '-{exp}' (kimdi, mektepti).",
                                    st + exp))
                return
    # (g) orqa negizdan keyin o'zbekcha -ga / -gan (oddiy g)
    for suf, exp in [("ga", "ǵa"), ("gan", "ǵan")]:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) >= 3 and stem_last_vowel_class(st) == "B" and not ends_voiceless(st):
                issues.append(Issue("OGOH", lineno, raw, "uygunlik",
                                    f"Orqa qatordagi so'zda '-{suf}' emas, '-{exp}'.", st + exp))
                return
    if plain.endswith("lari") and stem_last_vowel_class(plain[:-4]) == "B":
        issues.append(Issue("OGOH", lineno, raw, "uygunlik",
                            "'-lari' o'zbekcha; qoraqalpoqda '-ları' (orqa) yoki '-leri' (old).",
                            plain[:-4] + "ları"))
        return

    # ---- So'z ichidagi -lar/-ler (kitapler-di kabi)
    for m in re.finditer(r"l([ae])r", plain):
        st = plain[: m.start()]
        if len(st) < 3:
            continue
        nc = stem_last_vowel_class(st)
        sc = "B" if m.group(1) == "a" else "F"
        if nc and nc != sc and not (nc == "B" and (st.endswith("k") or st.endswith("g"))):
            issues.append(Issue("OGOH", lineno, raw, "uygunlik",
                                f"Ko'plik qo'shimchasi negizga mos emas: '{st}' + "
                                f"'-l{m.group(1)}r' → '-{'lar' if nc == 'B' else 'ler'}'.",
                                st + ("lar" if nc == "B" else "ler")
                                + harmonize(plain[m.end():], st + ("lar" if nc == "B" else "ler"))))
            return
        break

    # ---- Unli uyg'unligi (qo'shimcha negizning oxirgi unlisiga moslashadi)
    for suf in HARMONY_SUFFIXES:
        if plain.endswith(suf):
            st = stem_of(suf)
            if len(st) < 3:
                return
            if not plausible_suffix(suf, st):
                return
            sc, nc = suffix_class(suf), stem_last_vowel_class(st)
            if not nc or sc in (None, "MIXED"):
                return
            # o'zlashmalar: -k, -kt, -nk bilan tugasa old qo'shimcha olishi mumkin (akt → aktke)
            if nc == "B" and sc == "F" and (st.endswith("k") or st.endswith("g")):
                return
            if sc != nc:
                lvl = "OGOH" if len(st) >= 4 else "MASLAHAT"
                issues.append(Issue(lvl, lineno, raw, "uygunlik",
                                    f"Unli uyg'unligi: negiz {'orqa' if nc == 'B' else 'old'} qatorda, "
                                    f"'-{suf}' esa {'orqa' if sc == 'B' else 'old'} qatorda. "
                                    f"(Ruscha o'zlashma bo'lsa, lug'atdan tekshiring.)", ""))
            return


def check_text(text):
    issues = []
    if unicodedata.normalize("NFC", text) != text:
        issues.append(Issue("XATO", 0, "(butun matn)", "unicode",
                            "Matnda birikma diakritika bor (NFC emas): ba'zi qurilmalarda harf buziladi.",
                            "fix rejimi NFC ga keltiradi"))
        text = unicodedata.normalize("NFC", text)
    for i, line in enumerate(mask_quotes(text).splitlines(), 1):
        for m in TOKEN.finditer(line):
            tok = m.group(0)
            if re.fullmatch(r"[\d\-]+", tok):
                continue
            check_word(tok, i, issues)
    # Katta harfli so'z uchun 'katta-Í' berilgan bo'lsa, o'sha so'zning takroriy i/ı xabarlarini olib tashlash
    caps = {(x.line, x.word) for x in issues if x.kind == "katta-Í"}
    issues = [x for x in issues
              if not ((x.line, x.word) in caps and x.kind in ("i/ı", "uygunlik"))]
    return issues


# ---------------------------------------------------------------- fix / translit
def fix_old_apos(s):
    return OLD_APOS.sub(lambda m: OLD_MAP[m.group(1)], s)


def fix_lookalikes(s):
    return "".join(LOOKALIKE.get(c, c) for c in s)


def translit_word(w):
    letters = [c for c in w if c.isalpha()]
    all_caps = len(letters) > 1 and all(c.isupper() for c in letters)
    out = []
    prev = ""
    for c in w:
        if c in ("Е", "е") and prev in ("ъ", "ь", "Ъ", "Ь"):
            r = "ye" if c == "е" else "Ye"
        elif c in CYR2LAT_UPPER:
            r = CYR2LAT_UPPER[c]
        elif c in CYR2LAT:
            r = CYR2LAT[c]
        else:
            r = c
        if all_caps:
            r = r.upper().replace("I", "I")
            if c == "Ы":
                r = "Í"
            elif c == "И":
                r = "I"
        out.append(r)
        prev = c
    return "".join(out)


def translit_text(s):
    return re.sub(r"[\w\u0400-\u04FF\u0259\u018F]+", lambda m: translit_word(m.group(0)), s)


def fix_text(text):
    changes = []
    new = unicodedata.normalize("NFC", text)
    if new != text:
        changes.append("Unicode NFC ga keltirildi")
    masked = mask_quotes(new)
    t2 = unmask_quotes(fix_old_apos(masked), new)
    if t2 != new:
        changes.append("eski apostrofli harflar → á ǵ ó ú ń")
    t3 = fix_lookalikes(t2)
    if t3 != t2:
        changes.append("boshqa alifbo harflari almashtirildi")

    def fix_mixed(m):
        w = m.group(0)
        if CYR.search(w) and LAT.search(w):
            changes.append(f"aralash yozuv: {w} → {translit_word(w)}")
            return translit_word(w)
        return w
    t4 = re.sub(r"[\w\u0400-\u04FF]+", fix_mixed, t3)
    return t4, changes


# ---------------------------------------------------------------- CLI
def read_input(path):
    if path in (None, "-"):
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="Qaraqalpaq tekst tekseriw quralı (2016 latın).")
    ap.add_argument("mode", choices=["check", "fix", "translit"], nargs="?", default="check")
    ap.add_argument("path", nargs="?", default="-")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-level", default="MASLAHAT", choices=list(LEVELS))
    a = ap.parse_args()
    text = read_input(a.path)

    if a.mode == "translit":
        sys.stdout.write(translit_text(text))
        return 0
    if a.mode == "fix":
        new, changes = fix_text(text)
        sys.stdout.write(new)
        for c in changes:
            print(f"[fix] {c}", file=sys.stderr)
        rest = [i for i in check_text(new) if LEVELS[i.level] >= LEVELS["OGOH"]]
        if rest:
            print(f"[fix] Avtomatik tuzatilmagan {len(rest)} ta ogohlantirish qoldi — "
                  f"'check' rejimida ko'ring.", file=sys.stderr)
        return 0

    issues = [i for i in check_text(text) if LEVELS[i.level] >= LEVELS[a.min_level]]
    issues.sort(key=lambda i: (-LEVELS[i.level], i.line))
    if a.json:
        print(json.dumps([i.as_dict() for i in issues], ensure_ascii=False, indent=2))
    else:
        if not issues:
            print("Mexanik xato topilmadi. (Bu matn to'g'ri degani emas — ma'no, so'z tanlash "
                  "va uslubni alohida tekshiring.)")
        for i in issues:
            sug = f"  →  {i.suggestion}" if i.suggestion else ""
            print(f"[{i.level}] {i.line}-qator «{i.word}» ({i.kind}): {i.msg}{sug}")
        counts = {lv: sum(1 for i in issues if i.level == lv) for lv in LEVELS}
        print(f"\nJami: XATO {counts['XATO']}, OGOH {counts['OGOH']}, MASLAHAT {counts['MASLAHAT']}")
    return 1 if any(i.level == "XATO" for i in issues) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
