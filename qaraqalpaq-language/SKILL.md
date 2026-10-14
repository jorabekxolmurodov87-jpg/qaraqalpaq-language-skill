---
name: qaraqalpaq-language
description: Qoraqalpoq tili (qaraqalpaq tili, Karakalpak, kaa) bo'yicha har qanday ish uchun ishlat — qoraqalpoqcha matn yozish yoki tahrirlash, o'zbekcha/ruscha/inglizcha ↔ qoraqalpoqcha tarjima, imlo va grammatika tekshiruvi, eski apostrofli imloni yoki kirill yozuvni 2016 lotin alifbosiga o'girish, qoraqalpoq tilshunoslik atamalari. Foydalanuvchi qoraqalpoqcha yozsa, "qaraqalpaqsha", "qoraqalpoqcha", "Karakalpak", "Qaraqalpaq tili" desa yoki javobni qoraqalpoq tilida kutsa — ochiq so'ramagan bo'lsa ham — har qanday qoraqalpoqcha matn chiqarishdan OLDIN shu skillni o'qi.
---

# Qoraqalpoq tili skill (v2)

## Nega bu skill kerak

Qoraqalpoq tili kam resursli til. Model o'zbek va qozoq tillarini ancha ko'p ko'rgan, shuning uchun qoraqalpoqcha yozganda uch xil xato tabiiy ravishda chiqadi:

1. **O'zbekizm** — o'zbekcha so'z yoki qo'shimcha: `va`, `bilan`, `-ning`, `-ga`, `-adigan`, `qil-`.
2. **Qozoqizm** — qozoqcha shakl yoki harf: `jatır`, `ğ`, `ñ`, `ä`.
3. **Eski yoki aralash imlo** — 1995-yilgi apostrofli yozuv (`a'`, `n'`), kirill harfi aralashgan so'z, `I`/`Í` adashishi.

Bu skill shu uch xatoni muntazam ushlash uchun qurilgan: aniq ma'lumotnoma (xotiradan emas) + mexanik tekshiruv skripti + o'z cheklovini ochiq aytish.

## Ish tartibi

1. **Vazifani aniqla**: yozish, tarjima, tahrirlash, kirill → lotin o'girish yoki grammatika savoli.
2. **Kerakli ma'lumotnomani o'qi** (quyidagi jadval). Qo'shimcha va so'z shaklini xotiradan emas, jadvaldan ol.
3. **Matnni yoz.**
4. **Skript bilan tekshir** — 2 gapdan uzun har qanday qoraqalpoqcha matn uchun:
   ```bash
   python scripts/tekseriw.py check matn.txt        # yoki: echo "..." | python scripts/tekseriw.py check -
   ```
5. **Tuzat.** `XATO` darajasini albatta tuzat. `OGOH` darajasini kontekst bo'yicha ko'rib chiq (ko'pincha haqiqiy xato). `MASLAHAT` — shubhali joy.
6. **Ishonchsiz joylarni foydalanuvchiga ayt** (pastdagi "Halollik" bo'limi).

| Vazifa | O'qiladigan fayl |
|---|---|
| Har qanday qoraqalpoqcha matn | `references/alipbe-imla.md` (birinchi marta) |
| Qo'shimcha, kelishik, fe'l shakli | `references/morfologiya.md` |
| O'zbekchadan tarjima yoki o'zbekcha ta'sirni tozalash | `references/ozbekizm-qazaqizm.md` |
| Tilshunoslik atamasi | `references/terminologiya.md` |
| Namuna kerak bo'lsa (uslub, tarjima sifati) | `references/misallar.md` |
| Manba ishonchliligi, test korpusi | `references/manbalar.md` |

## Eng muhim qoidalar

**1. Faqat 2016 lotin alifbosi.** Maxsus harflar: `á ǵ ı ń ó ú` va birikmalar `sh`, `ch` (ch faqat o'zlashmalarda), `c` (ruscha ц o'rnida). Apostrofli eski shakllar (`a'`, `g'`, `o'`, `u'`, `n'`) ishlatilmaydi. Har doim tayyor (precomposed) Unicode belgilardan foydalan.

**2. `ı` va `i` — eng ko'p xato shu yerda.** `ı` (kirill ы) va `i` (kirill и) — alohida harflar. Katta harfda: `ı` → **`Í`**, `i` → **`I`**. Masalan: `XALÍQ`, `TILINIŃ`, `USHÍN`. Orqa qatordagi so'zda (a, o, u, ı bilan) odatda `ı` yoziladi: `xalıq`, `jumbaqları`, `qılıw`. `q`/`ǵ` dan keyin deyarli hech qachon `i` kelmaydi (istisno: `biraq`, `birqansha`, `tiykar` kabi `iy` birikmalari).

**3. Unli uyg'unligi.** Qo'shimcha so'zning *oxirgi bo'g'inidagi* unliga moslashadi: orqa (a, o, u, ı) → orqa qo'shimcha; old (á, e, i, ó, ú) → old qo'shimcha. `kitaplar`, `tiller`, `mektepte`, `Moynaqta`. Ruscha o'zlashmalarda istisnolar bor — lug'atdan tekshir.

**4. Undosh moslashuvi.** Jarangsiz undoshdan (p, t, k, q, s, sh) keyin qo'shimcha `t/q/k` bilan boshlanadi: `mektepke`, `mektepten`, `Moynaqqa`, `kitaptı`. Unli va jarangli undoshdan keyin `d/ǵ/g`: `balaǵa`, `awıldan`. Unli bilan boshlanadigan qo'shimcha oldidan `p → b`, `k → g`, `q → ǵ`: `mektep → mektebi`.

**5. Olti kelishik — jadvaldan.** `references/morfologiya.md` dagi jadval Qoraqalpoq Vikipediyasidan olingan misollarga asoslangan. Ayniqsa: `kimniń`, `kimdi`, `kimnen` (burun tovushidan keyin), `awıldıń`, `awıldan`.

**6. Ko'plik faqat `-lar/-ler`.** Jarangsiz undoshdan keyin ham: `xalıqlar`, `buryatlar`, `grekler`. `-dar/-tar` — qozoqcha.

**7. O'zbekcha qo'shimchalar yo'q:** `-ning` → `-nıń/-niń/-dıń/-diń/-tıń/-tiń`; `-adigan` → `-atuǵın/-etuǵın`; `-yapti` → `-ıp atır`; `-moq` → `-ıw/-iw`; `-dagi` → `-daǵı/-degi`.

**8. Qozoqcha shakllar yo'q:** davomli zamon `-ıp atır` (`oynap atır`), `-ıp jatır` emas.

**9. Fonetik mosliklar (tendensiya, mexanik qoida emas):** o'zbekcha `y-` → `j-` (`jol`, `jer`, `jıl`); `sh` → `s` (`bas`, `is`, `qıs`); `ch` → `sh` (`úsh`, `kúsh`); eski o'zlashmalarda `x` → `q`, `f` → `p` (`diyqan`, `puqara`, `ruqsat`, `pán`).

**10. Atamalar** — `references/terminologiya.md` dagi tasdiqlangan atamalarni ishlat. "Tasdiqlanmagan" belgisi borlarini ishlatsang, foydalanuvchiga ayt.

**11. To'qima.** Qoraqalpoqcha so'z yoki shaklni bilmasang, uni o'zbekcha yoki qozoqchadan "yasab" qo'yma. To'qilgan, lekin ishonarli ko'rinadigan so'z eng zararli xato, chunki o'quvchi uni payqamaydi. O'rniga: "bu so'zning qoraqalpoqcha shakliga ishonchim komil emas" de va variantni belgilab ber.

**12. Adabiy norma asos.** Foydalanuvchi dialekt so'rasa, dialekt shaklini adabiy norma deb ko'rsatma. Qoraqalpoq tilining ikki asosiy shevasi bor: shimoli-sharqiy va janubi-g'arbiy.

## Halollik: o'z cheklovingni ochiq ayt

- Skriptdan o'tgan matn hali **to'g'ri matn emas**. Skript faqat mexanik xatolarni ushlaydi: imlo, harf, qo'shimcha moslashuvi, ma'lum o'zbekizmlar. So'z tanlash, ma'no, uslub va gap tuzilishini tekshirmaydi.
- Rasmiy hujjat, nashr, darslik yoki sud/davlat matni uchun yakunda ona tili egasi yoki filolog tekshirishi kerakligini bir gap bilan eslat. Har javobda takrorlama — faqat matn muhim bo'lsa.
- Bir nechta variant to'g'ri bo'lishi mumkin bo'lsa yoki manbalar farq qilsa, buni ochiq ayt.

## Rejimlar

### Yozish (qoraqalpoqcha matn yaratish)
Avval tarkibni rejalashtir, keyin yoz, keyin skript bilan tekshir. Ilmiy/rasmiy uslubda `references/misallar.md` dagi haqiqiy ilmiy matn iboralariga tayan (`Bul maqalada ... tallanǵan`, `Atap aytqanda`, `Búgingi kúnde`, `Usı maqala ... úyreniwge arnalǵan`).

### O'zbek → Qoraqalpoq tarjima
1. Ma'noni tushun; so'zma-so'z ko'chirma.
2. Gap bo'laklarini aniqla (baslawısh, bayanlawısh ...).
3. Har bir so'zni `references/ozbekizm-qazaqizm.md` jadvalidan tekshir — o'zbekcha so'z qoraqalpoqchada boshqacha bo'lishi mumkin (`maktab` → `mektep`, `xususiyat` → `ózgeshelik`).
4. Qo'shimchalarni `references/morfologiya.md` bo'yicha qayta qur (o'zbekcha qo'shimchani "almashtirma", qaytadan hosil qil).
5. Skript bilan tekshir.
6. Javobda faqat tarjimani ber; izohni foydalanuvchi so'rasa yoki ishonchsiz joy bo'lsa qo'sh.

### Qoraqalpoq → O'zbek tarjima
Qoraqalpoqcha morfologiyani tahlil qil (zamon, shaxs, son, kelishik), keyin tabiiy o'zbekchada yoz. Shevaga oid yoki noaniq so'z bo'lsa, ma'no to'qima — noaniqligini ayt.

### Ruscha/Inglizcha → Qoraqalpoq
Xuddi shunday. Ruscha o'zlashmalarda `ь` va `ъ` yozilmaydi (`medal`, `obyekt`, `syezd`), `gazeta`, `konfeta`, `minut` shakllari ishlatiladi (2020 imlo lug'ati).

### Tahrirlash (foydalanuvchi matnini tekshirish)
1. `python scripts/tekseriw.py check` bilan boshla.
2. `XATO` darajasidagilarni `python scripts/tekseriw.py fix` avtomatik tuzatadi (Unicode, eski apostrof, boshqa alifbo harflari, aralash yozuv).
3. `OGOH` larni qo'lda ko'rib chiq.
4. Har bir tuzatishni qisqa tushuntir: "eski imlo", "o'zbekizm", "unli uyg'unligi", "undosh moslashuvi".
5. Foydalanuvchi uslubini saqla; faqat xatoni tuzat.

### Kirill → Lotin
```bash
python scripts/tekseriw.py translit kirill_matn.txt
```
KNAB 2016 jadvali bo'yicha: `ы → ı` (katta: `Í`), `и → i` (katta: `I`), `ә → á`, `ғ → ǵ`, `ң → ń`, `ө → ó`, `ү → ú`, `ў → w`, `қ → q`, `ҳ → h`, `х → x`, `ц → c`, `ч → ch`, `ш/щ → sh`, `ъ/ь` → (yozilmaydi), `ъе/ье → ye`. O'girgandan keyin `check` bilan tekshir.

## Javob tili
Meta-izohlarni (tushuntirish, ogohlantirish) foydalanuvchi yozgan tilda ber. Qoraqalpoqcha matnning o'zini aralashtirma: unda o'zbekcha izoh bo'lmasin.
