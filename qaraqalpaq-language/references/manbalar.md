# Manbalar va ishonchlilik

## Asosiy manbalar (v2 da tekshirilgan)

| Belgi | Manba | Nima uchun ishlatildi | Ishonchlilik |
|---|---|---|---|
| [L] | M. Dáwletov, Sh. Abdinazimov. *Qaraqalpaq tiliniń orfografiyalıq sózligi.* Nókis, «Bilim», 2020, 540 bet. | Imlo tamoyillari, o'zlashmalar, olmosh shakllari, so'z shakllari, alifbo tarixi | Yuqori (rasmiy akademik lug'at). **Eslatma:** internetdagi PDF nusxasi OCR qilingan, diakritika yo'qolgan — so'zlarning diakritikasi kirill mosligi bo'yicha tiklandi. |
| [K] | KNAB, Eesti Keele Instituut. Karakalpak: Cyrillic ↔ new Roman alphabet (2016 version), 2018. | Kirill–lotin jadvali, `И → I i`, `Ы → Í ı` | Yuqori |
| [W] | Qaraqalpaqsha Wikipedia: "Atlıq" (seplik jadvali), "Almasıq", "Ráwish" | Kelishik qo'shimchalari va misollar, olmosh turlanishi | O'rta-yuqori (darslik materialiga tayangan, lekin vikimanba) |
| [D] | Maktab darsliklari: Qaraqalpaq tili 11-klass (Sh. Abdinazimov va b., «Bilim», 2018); 8-klass (M. Dáwletov va b.); 7-klass; Ana tili 3-klass; NDPI test materiallari | Ko'makchilar, fe'l shakllari, mashq misollari | Yuqori |
| [T] | Zenodo'dagi ilmiy maqolalar sarlavha va annotatsiyalari (Qoraqalpoq davlat universiteti mualliflari, 2025–2026) | Zamonaviy ilmiy uslub, haqiqiy foydalanish, `Í` bosh harfi | O'rta-yuqori (tahrir qilingan, lekin har biri alohida muallif) |
| [E] | Eurasianet, "Uzbekistan: Keeping the Karakalpak Language Alive" (ecoi.net, 2019) | 2016 islohoti, eski darsliklar, telefonda ko'rinish muammosi | O'rta (jurnalistik) |

## v1 manbalari (saqlanadi)

- M. Dáwletov, Y. Dáwenov, D. Seydullaeva. *Qaraqalpaq tili*, 9-klass ushın sabaqlıq, 2014. — **2016 islohotidan oldin**; imlosini 2016 me'yori bilan solishtirib ishlat.
- *Qaraqalpaq tili*, 8-klass ushın sabaqlıq, «Bilim», 2019.
- *O'zbekcha–Qoraqalpoqcha lingvistik terminlarning lug'ati*, Megaline.
- Tilmoch qaraqalpaqsha awdarma servisi — faqat solishtirish uchun.

## Test va o'lchov uchun ochiq resurslar

- **Dilmash korpusi** (tahrirchi/dilmash, Hugging Face): 300 000 gap jufti — o'zbek, rus va ingliz tillari bilan 100 000 tadan. Litsenziya: MIT. Manbalar: 23% yangiliklar, 34% kitoblar, 24% ikki tilli lug'atlar, 19% maktab darsliklari. Gaplar LaBSE bilan avtomatik tekislangan.
- **FLORES+ devtest** qoraqalpoqcha tarjimasi — Mamasaidov, Shopulatov, "Open Language Data Initiative: Advancing Low-Resource Machine Translation for Karakalpak", arXiv:2409.04269 (2024).
- **Ogohlantirish:** Dilmash README dagi namunaviy gapning o'zida `ıktıyatlılıq`, `katnasta`, `talan etedi` kabi xatolar bor (to'g'risi `ıqtıyatlılıq`, `qatnasta`, `talap etedi`). Korpus "oltin standart" emas: undan baholash uchun foydalan, lekin gapni namuna sifatida ko'chirishdan oldin `tekseriw.py` bilan tekshir.

### Qanday o'lchash mumkin
1. FLORES+ yoki Dilmash'dan 50–100 ta o'zbekcha gap ol.
2. Skill bilan va skillsiz tarjima qil.
3. Ikkala natijani `tekseriw.py check --json` bilan tekshirib, XATO/OGOH sonini solishtir.
4. Etalon tarjima bilan chrF yoki BLEU hisobla (sacrebleu).
5. Eng muhimi: 20–30 ta gapni ona tili egasi ko'r-ko'rona baholasin (qaysi variant yaxshi).

## Skript sinovi (v2)

- To'g'ri matn: manbalardagi 314 so'zlik haqiqiy qoraqalpoqcha matn → **0** soxta xato.
- Xato matn: ataylab qo'yilgan xatolar (eski imlo, boshqa alifbo harfi, aralash yozuv, `-ning`, `-dagi`, undosh moslashuvi, uyg'unlik, `Í/I`, o'zbekcha so'zlar, `jatır`) → barchasi topildi.
- Bu kichik sinov. Katta korpusda soxta xato darajasi biroz yuqori bo'lishi mumkin, ayniqsa ruscha o'zlashmalarda.

## Filolog tekshirishi kerak bo'lgan joylar

1. `terminologiya.md` dagi **?** belgili atamalar (tolıqlawısh, pısıqlawısh, ótken máhál, shárt meyil, xabar meyili, irkilis belgi, jay gáp).
2. `morfologiya.md` dagi **[Q]** belgili qatorlar: fe'l shaxs qo'shimchalari, 2-shaxs ko'plik egalik, `sen/biz/siz/olar` turlanishi, `benen` qoidasi, `x/h` dan keyingi qo'shimchalar.
3. `misallar.md` dagi **[Q]** namunalar.
4. 2020 lug'atdan OCR orqali olingan so'zlarning diakritikasi.

## O'zgarishlar tarixi

**v2** (2026-yil oktyabr)
- Eski imlo, aralash yozuv, boshqa alifbo harflari, uyg'unlik va undosh moslashuvi, o'zbekizmlarni topuvchi `scripts/tekseriw.py` qo'shildi (`check`, `fix`, `translit`).
- 2016 alifbosi va kirill jadvali (KNAB), `Í/I` qoidasi aniqlashtirildi.
- Kelishiklar jadvali va har bir variantni tanlash qoidasi (Vikipediya misollari asosida).
- O'zbekizm/qozoqizm jadvali, tovush mosliklari.
- Atamalar ✓/? holati bilan; v1 atamalari saqlandi, tasdiqlanmaganlari belgilandi.
- Har bir namuna va qoidaga manba belgisi qo'yildi.
- v1 dagi xatolar tuzatildi: 10-qoidadagi takrorlangan `ǵ`, `grammar_policy.md` dagi kirill `де`, `tabiǵiy` → `tábiyiy`.
- Ko'rsatmalar o'zbekcha yozildi (meta-matnni noto'g'ri qoraqalpoqchada yozib qo'ymaslik uchun); barcha qoraqalpoqcha misollar manbaga tayanadi.

**v1** — asosiy qoidalar, 29 ta atama, tarjima siyosati.
