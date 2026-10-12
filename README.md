# Semantic Search

Matnlarni vektor ko‘rinishida saqlash va ma’nosiga qarab qidirish uchun FastAPI ilovasi. Matn vektorlari **Qwen3-Embedding-0.6B** modeli bilan yaratiladi, **Qdrant** bazasida saqlanadi. **React/Vite** interfeysida matn qo‘shish, ro‘yxatni ko‘rish, o‘chirish va qidiruvni sinash mumkin.

## Talablar

- Docker va Docker Compose (`docker compose` buyrug‘i ishlashi kerak).
- Modelni birinchi marta yuklash uchun internet aloqasi va diskda yetarli joy.
- Standart holatda kompyuterning `127.0.0.1:8080` porti bo‘sh bo‘lishi kerak.

Docker obrazi frontendni Node.js 24 bilan yig‘adi va backendni Python 3.12 hamda CPU uchun PyTorch bilan ishga tushiradi. Odatdagi ishga tushirish uchun Python yoki Node.js ni kompyuteringizga alohida o‘rnatish shart emas.

## Tez ishga tushirish

Buyruqlarni loyiha ildiz katalogida bajaring. PowerShell uchun:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose up -d --build
docker compose ps
docker compose logs -f app
```

Linux/macOS terminalida `.env` fayli hali bo‘lmasa `cp .env.example .env` ishlating. Mavjud `.env` faylini qayta nusxalab yozmang. `.env` faylida kerakli sozlamalarni, ayniqsa `JWT_SECRET_KEY` qiymatini, o‘zingizga moslang. Compose `.env.example` dagi standart qiymatlarni va mavjud bo‘lsa `.env` dagi qiymatlarni app konteyneriga uzatadi.

Birinchi ishga tushishda embedding modeli yuklab olinadi. Shu sababli app tayyor bo‘lishi odatdagidan uzoqroq davom etishi mumkin. Model keshi `qwen_model_cache` Docker volume’ida saqlanadi.

App tayyorligini tekshirish:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/api/health
```

Javob: `status: ok`. Keyin quyidagilarni oching:

| Manzil | Vazifasi |
| --- | --- |
| `http://127.0.0.1:8080/` | Matnlarni boshqarish interfeysi |
| `http://127.0.0.1:8080/test` | Semantik qidiruvni sinash |
| `http://127.0.0.1:8080/docs` | Interaktiv API hujjatlari (Swagger) |
| `http://127.0.0.1:8080/openapi.json` | OpenAPI sxemasi |
| `http://127.0.0.1:8080/api/health` | Sog‘lik tekshiruvi |

`APP_PORT` yoki `APP_BIND_IP` ni o‘zgartirsangiz, manzillarda ham shu qiymatlardan foydalaning.

## Interfeysdan foydalanish

1. Bosh sahifada **Yangi matnlar** maydoniga qidiruv bazasiga kiritiladigan matnni yozing. **Yana matn** tugmasi bilan bir nechta matnni bitta so‘rovda qo‘shishingiz mumkin.
2. **Matnni saqlash** tugmasini bosing. Saqlangan yozuvlar o‘ng tomondagi ro‘yxatda chiqadi; keraksiz yozuvni o‘chirish belgisi orqali olib tashlang.
3. `/test` sahifasida qidiruv matnini kiriting va **O‘xshashlarini topish** tugmasini bosing. `Ctrl + Enter` ham qidiruvni boshlaydi.
4. Natijalar moslik darajasi bo‘yicha saralanadi. `score_percent` vektor o‘xshashligidan hisoblangan ko‘rsatkich; uni aniq javob ehtimoli deb talqin qilmang.

## API bilan ishlash

Barcha asosiy endpointlar `/api/v1` prefiksidan foydalanadi. Quyidagi PowerShell misollarida standart `8080` porti ishlatilgan.

| Metod va manzil | Vazifasi | Muvaffaqiyatli status |
| --- | --- | --- |
| `GET /api/health` | App ishlayotganini tekshiradi | `200` |
| `POST /api/v1/documents/batch` | Matnlarni vektorga aylantirib Qdrant'ga saqlaydi | `201` |
| `GET /api/v1/documents` | Barcha saqlangan matnlarni qaytaradi | `200` |
| `POST /api/v1/search` | So‘rovga ma’nosi eng yaqin matnlarni topadi | `200` |
| `DELETE /api/v1/documents/{document_id}` | ID bo‘yicha bitta matnni o‘chiradi | `204` |

Misollardagi ID, vaqt va moslik ballari namuna qiymatlardir; haqiqiy javobda ular boshqacha bo‘ladi. API hozir autentifikatsiya talab qilmaydi.

### App holatini tekshirish

`GET /api/health` Qdrant yoki model holati haqida batafsil ma’lumot bermaydi; app so‘rovga javob bera olayotganini bildiradi.

```json
{"status":"ok"}
```

### Matn qo‘shish

```powershell
$body = @{
  items = @(
    @{ text = 'Yetkazib berish Toshkent bo‘ylab 2 kun davom etadi.' },
    @{ text = 'Buyurtma holatini shaxsiy kabinetda tekshirish mumkin.' }
  )
} | ConvertTo-Json -Depth 4

Invoke-RestMethod -Method Post `
  -Uri 'http://127.0.0.1:8080/api/v1/documents/batch' `
  -ContentType 'application/json; charset=utf-8' `
  -Body $body
```

So‘rovdagi har bir matnning ortiqcha bosh va oxirgi bo‘sh joylari olib tashlanadi. App unga UUID yaratadi, model yordamida vektor hisoblaydi va matn hamda yaratilgan vaqtni Qdrant'ga yozadi. `201 Created` javobiga misol:

```json
{
  "added": 2,
  "items": [
    {
      "id": "d786c71e-0926-44bd-9d99-8e6dc33cbdd4",
      "text": "Yetkazib berish Toshkent bo‘ylab 2 kun davom etadi.",
      "created_at": "2026-10-12T08:30:00Z"
    },
    {
      "id": "7eea6db6-7e05-4f4a-bdf8-c44686388061",
      "text": "Buyurtma holatini shaxsiy kabinetda tekshirish mumkin.",
      "created_at": "2026-10-12T08:30:00Z"
    }
  ]
}
```

`added` — shu so‘rovda saqlangan matnlar soni. `id` yozuvni o‘chirishda ishlatiladi; `created_at` UTC vaqtidir. Javobda vektorning o‘zi qaytarilmaydi.

### Matnlar ro‘yxatini olish

```powershell
Invoke-RestMethod 'http://127.0.0.1:8080/api/v1/documents'
```

App Qdrant kolleksiyasidagi barcha yozuvlarni olib, yaratilgan vaqti bo‘yicha yangidan eskiga saralaydi. `200 OK` javobiga misol:

```json
{
  "total": 1,
  "items": [
    {
      "id": "d786c71e-0926-44bd-9d99-8e6dc33cbdd4",
      "text": "Yetkazib berish Toshkent bo‘ylab 2 kun davom etadi.",
      "created_at": "2026-10-12T08:30:00Z"
    }
  ]
}
```

`total` — qaytarilgan yozuvlar soni. Bazada matn bo‘lmasa `{"total":0,"items":[]}` qaytadi. Hozir bu endpointda sahifalash yo‘q.

### Qidirish

```powershell
$body = @{
  text = 'Buyurtmam qachon yetib keladi?'
  limit = 5
  score_threshold = 0.3
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri 'http://127.0.0.1:8080/api/v1/search' `
  -ContentType 'application/json; charset=utf-8' `
  -Body $body
```

App qidiruv matnini modelning `query` rejimida vektorga aylantiradi. Qdrant saqlangan matnlarni cosine o‘xshashlik bo‘yicha qidirib, eng moslarini birinchi qaytaradi. `limit` ko‘rsatilmasa `.env` dagi `DEFAULT_SEARCH_LIMIT` ishlatiladi (`10`); ruxsat etilgan oraliq `1–50`. `score_threshold` ixtiyoriy, `-1` dan `1` gacha: berilsa, undan past ball olgan natijalar chiqarilmaydi.

`200 OK` javobiga misol:

```json
{
  "query": "Buyurtmam qachon yetib keladi?",
  "total": 1,
  "results": [
    {
      "id": "d786c71e-0926-44bd-9d99-8e6dc33cbdd4",
      "text": "Yetkazib berish Toshkent bo‘ylab 2 kun davom etadi.",
      "score": 0.82,
      "score_percent": 82.0
    }
  ]
}
```

`query` — yuborilgan qidiruv matni, `total` — qaytarilgan natijalar soni. `score` — Qdrant o‘xshashlik balli. `score_percent` shu ballni `0–1` oralig‘iga keltirib, 100 ga ko‘paytirish orqali hisoblanadi; bu aniq javob ehtimoli emas. Hech narsa topilmasa `results: []` va `total: 0` qaytadi. Frontend hozir `limit: 10` ni aniq yuboradi, shuning uchun `DEFAULT_SEARCH_LIMIT` o‘zgarishi unga ta’sir qilmaydi.

### Matnni o‘chirish

```powershell
$documentId = 'BU_YERGA_YOZUV_ID_SINI_QOYING'
Invoke-RestMethod -Method Delete "http://127.0.0.1:8080/api/v1/documents/$documentId"
```

App avval ID mavjudligini tekshiradi, so‘ng yozuvni Qdrant'dan o‘chiradi. Muvaffaqiyatli javob `204 No Content`: javob tanasi bo‘lmaydi. ID topilmasa `404 Not Found` va quyidagi JSON qaytadi:

```json
{"detail":"Matn topilmadi"}
```

### Kiritish cheklovlari

- Har bir matn bo‘sh bo‘lmasligi va bo‘sh joylar olib tashlangandan keyin ko‘pi bilan `4000` belgidan iborat bo‘lishi kerak.
- Bitta `/documents/batch` so‘rovida `1–100` ta matn qabul qilinadi. Bir batch ichida bir xil matnni katta-kichik harfni hisobga olmasdan takrorlash mumkin emas.
- Qidiruv matni ham `1–4000` belgi bo‘lishi kerak.
- Noto‘g‘ri so‘rovlar `422 Unprocessable Entity` bilan qaytadi. Javobning `detail` massivida xato joyi (`loc`) va sababi (`msg`) ko‘rsatiladi. Masalan, `limit` qiymati `0` bo‘lsa, `loc` ichida `body` va `limit`, `msg` ichida kamida `1` bo‘lishi kerakligi ko‘rsatiladi.

## Sozlamalar

Standart qiymatlar `.env.example` faylida berilgan. `.env` ni yarating yoki mavjud bo‘lsa tahrirlang; bu fayl Git tomonidan e’tiborsiz qoldiriladi.

| O‘zgaruvchi | Standart | Izoh |
| --- | --- | --- |
| `CONTAINER_PREFIX` | `semantic_search` | Docker konteyner va app obrazi nomi prefiksi |
| `APP_BIND_IP` | `127.0.0.1` | Kompyuterda app porti bog‘lanadigan IP |
| `APP_PORT` | `8080` | Kompyuterda app uchun port; konteyner ichida `8000` |
| `QDRANT_HOST`, `QDRANT_PORT` | `qdrant`, `6333` | Docker tarmog‘idagi Qdrant manzili |
| `QDRANT_API_KEY` | bo‘sh | Qdrant API kaliti, agar Qdrant shuni talab qilsa |
| `QDRANT_TIMEOUT` | `5` | Qdrant so‘rovi taymauti, soniyada |
| `QDRANT_CONNECT_RETRIES` | `30` | Ulanish urinishlari soni |
| `QDRANT_RETRY_DELAY` | `1` | Urinishlar orasidagi kutish, soniyada |
| `EMBEDDING_MODEL_NAME` | `Qwen/Qwen3-Embedding-0.6B` | Sentence Transformers orqali yuklanadigan model |
| `EMBEDDING_DEVICE` | bo‘sh | Avtomatik tanlash; kerak bo‘lsa `cpu` yoki `cuda` |
| `EMBEDDING_BATCH_SIZE` | `8` | Vektor yaratishdagi batch hajmi |
| `EMBEDDING_SIZE` | `1024` | Qdrant vektor o‘lchami; app kodidagi standart qiymat |
| `DOCUMENTS_COLLECTION_NAME` | `semantic_documents` | Qdrant kolleksiyasi |
| `MAX_TEXT_LENGTH` | `4000` | Matn va qidiruv so‘rovi uzunligi |
| `MAX_BATCH_SIZE` | `100` | Bir so‘rovda qo‘shiladigan matnlar soni |
| `DEFAULT_SEARCH_LIMIT` | `10` | API qidiruvining standart natija limiti |
| `JWT_SECRET_KEY` | namuna qiymati | JWT utilitalari uchun maxfiy kalit |

Hozirgi API yo‘llarida autentifikatsiya qo‘llanmagan; ilovani tashqi tarmoqqa ochishda buni hisobga oling.

Modelni almashtirsangiz, yangi model chiqish vektori o‘lchami `EMBEDDING_SIZE` bilan mos bo‘lishi kerak. Mavjud Qdrant kolleksiyasidagi vektorlar eski model bilan yaratilgan bo‘lsa, ularni yangi model bilan qayta yaratish kerak bo‘ladi.

## Loyiha tuzilishi

```text
app/
  api/documents/       Matnlarni qo‘shish, ro‘yxatlash va o‘chirish
  api/search/          Semantik qidiruv
  config/              FastAPI, Qdrant va muhit sozlamalari
  resources/embedding/ Modelni yuklash va vektor yaratish
  resources/repositories/ Qdrant bilan ishlash
frontend/              React/Vite interfeysi
docker/                 App Dockerfile’i
scripts/                Supervisor va ishga tushirish skriptlari
requirements/           Python bog‘liqliklari
docker-compose.yml      App va Qdrant xizmatlari
```

Ishga tushishda app Qdrant bilan ulanadi, kolleksiya yo‘q bo‘lsa yaratadi va embedding modelini yuklaydi. Matn qo‘shishda UUID, matn, yaratilgan vaqt va vektor Qdrant’ga yoziladi. Qidiruvda so‘rov matni vektorga aylantirilib, Qdrant’da cosine o‘xshashlik bo‘yicha qidiriladi. Frontend ishlab chiqarish obrazida yig‘ilib, shu FastAPI app orqali servis qilinadi.

## Boshqarish va muammolarni tekshirish

```powershell
docker compose ps                 # Xizmatlar holati
docker compose logs -f app        # App jurnali
docker compose logs -f qdrant     # Qdrant jurnali
docker compose restart app        # App'ni qayta ishga tushirish
docker compose down               # Xizmatlarni to‘xtatish; volume'lar saqlanadi
```

`docker compose down -v` barcha Compose volume’larini, jumladan Qdrant’dagi matnlar va model keshini ham o‘chiradi. Uni faqat ma’lumotlarni butunlay tozalash kerak bo‘lganda ishlating.

- **App uzoq vaqt `starting` holatida:** birinchi model yuklab olinayotgan bo‘lishi mumkin; `docker compose logs -f app` ni ko‘ring. Healthcheck uchun 5 daqiqalik boshlang‘ich muddat berilgan.
- **Qdrant bilan ulanish xatosi:** `docker compose ps` va `docker compose logs qdrant` ni tekshiring. App Qdrant’ga qayta ulanishga urinadi.
- **Port band:** `.env` ichidagi `APP_PORT` ni boshqa bo‘sh portga o‘zgartirib, `docker compose up -d` ni qayta bajaring.
- **Model yuklanmayapti:** internet aloqasi, diskdagi bo‘sh joy va app jurnalini tekshiring. Dockerfile CPU uchun PyTorch o‘rnatadi; `EMBEDDING_DEVICE=cuda` GPU mos konfiguratsiyasiz ishlamaydi.
- **API `422` qaytaryapti:** matn uzunligi, batch hajmi, bir xil matnlar va qidiruv `limit`/`score_threshold` qiymatlarini tekshiring.
