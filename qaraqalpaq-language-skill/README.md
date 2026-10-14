# Qaraqalpaq tili — Claude skill (v2)

Claude uchun qoraqalpoq tili skilli: qoraqalpoqcha matn yozish, o'zbek/rus/ingliz tillaridan tarjima, imlo tekshiruvi va kirill yozuvni **2016 lotin alifbosiga** o'girish.

> **English summary.** A Claude skill for the Karakalpak language (Qaraqalpaq, ISO 639-3: `kaa`). It gives Claude source-backed reference tables (2016 Latin alphabet, case endings, Uzbek/Kazakh interference) and ships `tekseriw.py`, a dependency-free checker that flags old apostrophe orthography, mixed Cyrillic/Latin, wrong Turkic letters, `I`/`Í` errors, vowel-harmony and consonant-assimilation mistakes, and common Uzbekisms. It also transliterates Karakalpak Cyrillic to the 2016 Latin script.

## Nega kerak

Qoraqalpoq tili kam resursli til. Til modellari o'zbek va qozoq tillarini ancha ko'p ko'rgan, shuning uchun qoraqalpoqcha yozganda uch xil xato tabiiy chiqadi:

1. **o'zbekizmlar**: `va`, `bilan`, `-ning`, `-adigan`;
2. **qozoqizmlar**: `jatır`, `ğ`, `ñ`;
3. **eski yoki aralash imlo**: `a'`, `n'`, so'z ichida kirill harfi, `XALIQ` o'rniga `XALÍQ`.

Skill bu xatolarni manbaga asoslangan ma'lumotnoma va avtomatik tekshiruv skripti bilan kamaytiradi.

## Tuzilma

```
qaraqalpaq-language/          ← skillning o'zi (Claude'ga shu papka yuklanadi)
├── SKILL.md                  ← ish tartibi va asosiy qoidalar
├── references/
│   ├── alipbe-imla.md        ← 2016 alifbo, kirill jadvali, imlo tamoyillari
│   ├── morfologiya.md        ← kelishiklar, egalik, olmoshlar, fe'l shakllari
│   ├── ozbekizm-qazaqizm.md  ← o'zbekcha/qozoqcha ta'sir jadvallari
│   ├── terminologiya.md      ← tilshunoslik atamalari (✓ / ? holati bilan)
│   ├── misallar.md           ← tarjima va tahrir namunalari
│   └── manbalar.md           ← manbalar, ishonchlilik, o'zgarishlar tarixi
└── scripts/
    └── tekseriw.py           ← tekshirish / tuzatish / kirill→lotin
evals/evals.json              ← skill sinov topshiriqlari
tests/                        ← tekseriw.py uchun avtomatik testlar
dist/qaraqalpaq-language.zip  ← Claude'ga yuklashga tayyor arxiv
```

## Claude'ga o'rnatish

1. `dist/qaraqalpaq-language.zip` faylini yuklab oling.
2. Claude'da skillar bo'limini oching (**Customize → Skills**; ba'zi rejalarda **Settings → Capabilities**).
3. **"+" → "Create skill" → "Upload a skill"** ni tanlab, ZIP faylni yuklang.
4. Sozlamalarda **code execution** yoqilgan bo'lsin: skill `tekseriw.py` skriptini ishlatadi.

Batafsil rasmiy yo'riqnoma: <https://support.claude.com/en/articles/12512180>

ZIP faylni o'zingiz yasamoqchi bo'lsangiz, `qaraqalpaq-language` **papkasining o'zini** arxivlang. Papka nomi skill nomiga (`qaraqalpaq-language`) mos bo'lishi shart.

## Tekshiruv skriptini alohida ishlatish

Faqat Python 3.8+ kerak, boshqa kutubxona shart emas.

```bash
# Xatolar ro'yxati
python qaraqalpaq-language/scripts/tekseriw.py check matn.txt
echo "Balalar mektepda oqıp jatır." | python qaraqalpaq-language/scripts/tekseriw.py check -

# Aniq xatolarni avtomatik tuzatish (eski apostrof, boshqa alifbo harflari, aralash yozuv, Unicode)
python qaraqalpaq-language/scripts/tekseriw.py fix matn.txt > tuzatilgan.txt

# Kirill → lotin (2016)
echo "Нөкис — Қарақалпақстан Республикасының пайтахты." | python qaraqalpaq-language/scripts/tekseriw.py translit -
# → Nókis — Qaraqalpaqstan Respublikasınıń paytaxtı.

# JSON chiqish (boshqa dasturlar uchun)
python qaraqalpaq-language/scripts/tekseriw.py check matn.txt --json
```

Darajalar:
- **XATO** — deyarli aniq xato, `fix` o'zi tuzatadi;
- **OGOH** — ehtimoliy xato, qo'lda ko'rib chiqing;
- **MASLAHAT** — shubhali joy.

## Testlar

```bash
python -m unittest discover -s tests -v
```

| Sinov | Natija |
|---|---|
| Manbalardan olingan to'g'ri matn (314 so'z) | 0 soxta xato |
| Sozlashda ishlatilmagan yangi to'g'ri matn (278 so'z) | 0 soxta xato |
| Ataylab xato yozilgan matn (31 ta xato) | 31 tasi ham topildi |

Bu kichik sinov. Katta korpusda, ayniqsa ruscha o'zlashmalarda, soxta xatolar biroz ko'payishi mumkin.

## Cheklovlar

- Skriptdan o'tgan matn hali **to'g'ri matn emas**. Skript faqat mexanik xatolarni ushlaydi; so'z tanlash, ma'no va uslubni tekshirmaydi.
- `terminologiya.md` dagi **?** belgili atamalar va `morfologiya.md` dagi **[Q]** belgili qatorlar manbada tasdiqlanmagan. Ularni filolog tekshirishi kerak (ro'yxat: `references/manbalar.md`).
- Rasmiy hujjat yoki nashr uchun yakuniy matnni ona tili egasi ko'rib chiqishi kerak.

## Manbalar

- M. Dáwletov, Sh. Abdinazimov. *Qaraqalpaq tiliniń orfografiyalıq sózligi.* Nókis, «Bilim», 2020.
- KNAB, Eesti Keele Instituut — Karakalpak Cyrillic ↔ Latin (2016 version).
- Qaraqalpaqsha Wikipedia: "Atlıq", "Almasıq", "Ráwish".
- Qaraqalpaq tili darsliklari (3-, 7-, 8-, 11-sinf).
- Mamasaidov, Shopulatov. *Open Language Data Initiative: Advancing Low-Resource Machine Translation for Karakalpak.* arXiv:2409.04269 (Dilmash korpusi, FLORES+).

To'liq ro'yxat va ishonchlilik bahosi: [`qaraqalpaq-language/references/manbalar.md`](qaraqalpaq-language/references/manbalar.md). Test matnlarining manbalari: [`tests/data/MANBALAR.md`](tests/data/MANBALAR.md).

## Hissa qo'shish

Ayniqsa qadrli yordam turlari:
- **?** va **[Q]** belgili joylarni manba bilan tasdiqlash yoki tuzatish;
- skript soxta xato bergan to'g'ri qoraqalpoqcha so'zlarni yuborish (Issues orqali);
- `tests/data/` ga yangi tekshirilgan matnlar qo'shish.

O'zgartirishdan keyin testlarni ishga tushiring: `python -m unittest discover -s tests -v`.
