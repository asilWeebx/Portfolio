# flake8: noqa — namunaviy maqolalar va blog g'oyalari (seed buyrug'i uchun)

POSTS = [
    {
        "title": "Django loyihani VPS serverga chiqarish: Nginx + Gunicorn + SSL",
        "category": "DevOps va server",
        "tags": ["django", "nginx", "linux", "python"],
        "excerpt": "Ubuntu server, Gunicorn, Nginx va bepul Let's Encrypt sertifikati bilan Django loyihani "
                   "production'ga chiqarishning qadamma-qadam yo'riqnomasi.",
        "content": """
<p>Lokal kompyuterda <code>runserver</code> bilan ishlagan loyihani internetga chiqarish ko'pchilik uchun eng chalkash bosqich. Bu maqolada Ubuntu serverda eng ko'p qo'llanadigan sxemani ko'rib chiqamiz: <b>Nginx → Gunicorn → Django</b>.</p>

<h2>1. Serverni tayyorlash</h2>
<p>Avval tizimni yangilaymiz va kerakli paketlarni o'rnatamiz:</p>
<pre><code class="language-bash">sudo apt update &amp;&amp; sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip nginx postgresql git
sudo adduser --disabled-password deploy</code></pre>
<p>Loyihani <code>root</code> nomidan ishga tushirmang — alohida <code>deploy</code> foydalanuvchisi xavfsizroq.</p>

<h2>2. Loyiha va virtual muhit</h2>
<pre><code class="language-bash">cd /home/deploy
git clone https://github.com/username/project.git app
cd app/backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # SECRET_KEY, DEBUG=0, ALLOWED_HOSTS ni to'ldiring
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput</code></pre>

<h2>3. Gunicorn'ni systemd xizmati qilish</h2>
<p>Server qayta yonganda loyiha avtomatik ishga tushishi uchun systemd xizmatini yozamiz:</p>
<pre><code class="language-ini">[Unit]
Description=Django (gunicorn)
After=network.target

[Service]
User=deploy
WorkingDirectory=/home/deploy/app/backend
ExecStart=/home/deploy/app/backend/.venv/bin/gunicorn config.wsgi:application \\
    --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target</code></pre>
<pre><code class="language-bash">sudo systemctl enable --now gunicorn
sudo systemctl status gunicorn</code></pre>

<h2>4. Nginx — tashqi eshik</h2>
<p>Nginx statik fayllarni o'zi beradi, qolgan so'rovlarni Gunicorn'ga uzatadi:</p>
<pre><code class="language-nginx">server {
    server_name example.uz www.example.uz;
    client_max_body_size 20M;

    location /static/ { alias /home/deploy/app/backend/staticfiles/; }
    location /media/  { alias /home/deploy/app/backend/media/; }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}</code></pre>

<h2>5. Bepul SSL (HTTPS)</h2>
<pre><code class="language-bash">sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.uz -d www.example.uz</code></pre>
<p>Certbot sertifikatni har 90 kunda o'zi yangilaydi.</p>

<h2>Tez-tez uchraydigan xatolar</h2>
<ul>
<li><b>502 Bad Gateway</b> — Gunicorn ishlamayapti: <code>journalctl -u gunicorn -n 50</code> bilan logni ko'ring.</li>
<li><b>Statik fayllar yuklanmayapti</b> — <code>collectstatic</code> qilinmagan yoki Nginx'dagi yo'l noto'g'ri.</li>
<li><b>CSRF xatosi</b> — <code>CSRF_TRUSTED_ORIGINS</code> ga <code>https://example.uz</code> qo'shilmagan.</li>
</ul>
<p>Shu sxema kichik va o'rta loyihalar uchun yillar davomida muammosiz ishlaydi. Keyingi qadam — Docker va avtomatik deploy (CI/CD), bu haqda alohida yozaman.</p>
""",
    },
    {
        "title": "DRF'da API loyihalash: har bir loyihada qo'llaydigan 8 ta qoida",
        "category": "Backend va Django",
        "tags": ["django", "drf", "api", "python"],
        "excerpt": "Frontend va mobil dasturchilar rahmat aytadigan API: nomlash, sahifalash, xatolar formati, "
                   "N+1 muammosi va boshqa amaliy qoidalar.",
        "content": """
<p>Yaxshi API — bu frontend yoki mobil dasturchi hujjatga qaramasdan ham taxmin qila oladigan API. Quyidagi qoidalarni deyarli har bir Django REST Framework loyihamda qo'llayman.</p>

<h2>1. Resurslar — ko'plikda, fe'lsiz</h2>
<p><code>/api/posts/</code>, <code>/api/posts/{slug}/</code> — yaxshi. <code>/api/getAllPosts/</code> — yomon. Harakatni HTTP metodi bildiradi: GET, POST, PATCH, DELETE.</p>

<h2>2. Har doim sahifalash</h2>
<p>Bugun 20 ta yozuv bor, bir yildan keyin 20 000 ta bo'ladi. Sahifalashni boshidanoq yoqing:</p>
<pre><code class="language-python">REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}</code></pre>

<h2>3. N+1 so'rovlardan qoching</h2>
<p>Serializer ichida bog'langan obyekt chiqarilsa, har bir qator uchun alohida SQL so'rov ketadi. Yechim — <code>select_related</code> va <code>prefetch_related</code>:</p>
<pre><code class="language-python">def get_queryset(self):
    return (
        Post.objects.filter(status="published")
        .select_related("category")
        .prefetch_related("tags")
    )</code></pre>

<h2>4. Ro'yxat va batafsil uchun alohida serializer</h2>
<p>Ro'yxatda maqolaning to'liq matni kerak emas. <code>PostListSerializer</code> va <code>PostDetailSerializer</code> javob hajmini bir necha barobar kamaytiradi.</p>

<h2>5. Bir xil xato formati</h2>
<p>Frontend xatoni har doim bir joydan o'qishi kerak. DRF standart formati (<code>{"field": ["xato"]}</code>) yaxshi boshlang'ich nuqta — faqat har bir view o'zicha boshqa format qaytarmasin.</p>

<h2>6. Filtr, qidiruv, saralash — query parametrlarda</h2>
<p><code>django-filter</code> bilan: <code>/api/posts/?category=django&amp;search=deploy&amp;ordering=-views</code>. Yangi endpoint ochish shart emas.</p>

<h2>7. Ommaviy endpoint'larni cheklang (throttling)</h2>
<p>Kontakt formasi kabi ochiq POST endpoint'lar spam uchun nishon. <code>ScopedRateThrottle</code> bilan soatiga 5 ta so'rov — oddiy, lekin samarali himoya.</p>

<h2>8. ID o'rniga slug — ommaviy sahifalar uchun</h2>
<p><code>/blog/django-deploy</code> — ham SEO uchun, ham foydalanuvchi uchun <code>/blog/42</code> dan yaxshiroq.</p>

<p>Bu qoidalar murakkab emas, lekin loyiha o'sgani sari ularning qiymati oshib boradi. Sizda qanday qoidalar bor? Telegram orqali yozing.</p>
""",
    },
    {
        "title": "Sayt yoki bot buyurtma qilishdan oldin javob berishingiz kerak bo'lgan 10 savol",
        "category": "Freelance va biznes",
        "tags": ["freelance", "startap"],
        "excerpt": "Dasturchiga murojaat qilishdan oldin shu savollarga javob tayyorlasangiz — narx aniqroq, "
                   "muddat qisqaroq va natija kutganingizdek bo'ladi.",
        "content": """
<p>Ko'p loyihalar kod yozilishidan oldin, aniqroq aytganda — <b>vazifa noaniq qo'yilgani uchun</b> qiyinlashadi. Quyidagi savollarga oldindan javob tayyorlasangiz, ish ancha tez va arzon bo'ladi.</p>

<h2>1. Qaysi muammoni hal qilmoqchisiz?</h2>
<p>"Sayt kerak" emas, balki "mijozlar narxni bilish uchun har kuni 50 marta qo'ng'iroq qilyapti" — mana bu muammo. Yechimni shu muammodan kelib chiqib tanlaymiz.</p>

<h2>2. Foydalanuvchi kim?</h2>
<p>Yoshi, qurilmasi (ko'pincha telefon), tili. O'zbekistonda ko'p hollarda auditoriya Telegram'da — balki sayt emas, bot yoki Mini App yetarlidir.</p>

<h2>3. Natijani qanday o'lchaymiz?</h2>
<p>Buyurtmalar soni, qo'ng'iroqlar, vaqt tejalishi. Raqamsiz maqsad — maqsad emas.</p>

<h2>4. Birinchi versiyada nima bo'lishi shart?</h2>
<p>Hamma g'oyalarni ro'yxatga yozing, keyin ularni "shart" va "keyinroq" ga ajrating. Birinchi versiya kichik bo'lsa, tez ishga tushadi va real fikr-mulohaza olasiz.</p>

<h2>5. Kim kontentni yuritadi?</h2>
<p>Tovarlar, narxlar, maqolalarni kim qo'shadi? Bunga qarab admin panel qanchalik qulay bo'lishi kerakligi aniqlanadi.</p>

<h2>6. Qanday integratsiyalar kerak?</h2>
<p>Click/Payme, SMS, 1C, Uzum, yetkazib berish xizmatlari — har biri muddat va narxga ta'sir qiladi.</p>

<h2>7. O'xshash namunalar bormi?</h2>
<p>Yoqqan 2–3 ta sayt yoki ilova havolasi uzun tushuntirishdan foydaliroq.</p>

<h2>8. Byudjet va muddat qanday?</h2>
<p>Aniq raqam bo'lmasa ham, oraliq ayting. Bu sizga mos yechimni taklif qilishga yordam beradi.</p>

<h2>9. Domen, hosting, akkauntlar kimning nomida bo'ladi?</h2>
<p>Har doim <b>sizning</b> nomingizda bo'lishi kerak. Bu — loyiha ustidan to'liq nazorat.</p>

<h2>10. Ishga tushgandan keyin nima bo'ladi?</h2>
<p>Qo'llab-quvvatlash, yangilanishlar, zaxira nusxa. Loyiha ishga tushishi — boshlanish, oxiri emas.</p>

<p>Shu savollarga javob tayyor bo'lsa — <a href="/brief">brief to'ldiring</a>, 24 soat ichida bog'lanaman.</p>
""",
    },
]

DRAFT_IDEAS = [
    {
        "title": "Multi-tenant SaaS POS'ni Django'da qurish: arxitektura va saboqlar",
        "category": "Case study", "tags": ["django", "pos", "postgresql"],
        "excerpt": "Bitta kod bazasida yuzlab do'konlar: tenant ajratish usullari, rollar, hisobotlar tezligi.",
        "outline": ["Muammo: har bir do'konga alohida server qimmat", "Tenant ajratish: schema vs company_id",
                    "Rollar va ruxsatlar", "Hisobotlarni tezlashtirish", "Nimani boshqacha qilgan bo'lardim"],
    },
    {
        "title": "Telegram Mini App: oddiy botdan to'liq onlayn do'kongacha",
        "category": "Telegram botlar", "tags": ["telegram", "react", "django"],
        "excerpt": "Mini App qanday ishlaydi, initData'ni tekshirish, to'lov va buyurtma oqimi.",
        "outline": ["Mini App nima va qachon kerak", "initData'ni backendda tekshirish", "Katalog va savat",
                    "To'lov integratsiyasi", "Deploy va domen"],
    },
    {
        "title": "Flutter'da offline-first ilova: internet yo'q paytda ham ishlash",
        "category": "Mobil (Flutter)", "tags": ["flutter"],
        "excerpt": "Lokal baza, sinxronizatsiya navbati va konfliktlarni hal qilish.",
        "outline": ["Nega offline-first", "Lokal saqlash (Hive/Isar/Drift)", "Sinxronizatsiya navbati",
                    "Konfliktlar", "Test qilish"],
    },
    {
        "title": "Click va Payme'ni Django'ga ulash: amaliy qo'llanma",
        "category": "Backend va Django", "tags": ["django", "api"],
        "excerpt": "Merchant API, callback'lar, imzo tekshiruvi va tranzaksiya holatlari.",
        "outline": ["Ro'yxatdan o'tish va kalitlar", "Buyurtma modeli", "Callback endpoint'lar",
                    "Xavfsizlik", "Test rejimi"],
    },
    {
        "title": "Next.js yoki oddiy React (Vite): qaysi biri qachon kerak?",
        "category": "Frontend", "tags": ["react", "nextjs", "seo"],
        "excerpt": "SEO, tezlik, hosting va murakkablik bo'yicha halol taqqoslash.",
        "outline": ["SPA va SSR farqi", "SEO kerakmi?", "Hosting va narx", "Mening tanlovim"],
    },
    {
        "title": "PostgreSQL indekslari: sekin so'rovni 10 barobar tezlashtirish",
        "category": "Backend va Django", "tags": ["postgresql", "django"],
        "excerpt": "EXPLAIN ANALYZE'ni o'qish, qaysi ustunga indeks kerak va qachon zarar qiladi.",
        "outline": ["Sekin so'rovni topish", "EXPLAIN ANALYZE", "B-tree, GIN, partial indeks",
                    "Django'da indeks e'lon qilish", "Ortiqcha indeks zarari"],
    },
    {
        "title": "Docker Compose bilan Django + PostgreSQL + Redis lokal muhit",
        "category": "DevOps va server", "tags": ["docker", "django", "postgresql"],
        "excerpt": "Jamoadagi har bir dasturchida bir xil muhit — 5 daqiqada.",
        "outline": ["Nega Docker", "docker-compose.yml", "Volume va .env", "Celery qo'shish", "Production farqlari"],
    },
    {
        "title": "Telegram botga AI ulash: Claude/OpenAI API bilan aqlli yordamchi",
        "category": "AI va avtomatlashtirish", "tags": ["ai", "telegram", "python"],
        "excerpt": "Mijozlar savoliga javob beradigan bot: kontekst, xarajat nazorati va xavfsizlik.",
        "outline": ["Qaysi vazifalar uchun mos", "API ulash", "Kontekst va tarix",
                    "Xarajatni nazorat qilish", "Cheklovlar"],
    },
    {
        "title": "Sayt tezligi: Core Web Vitals bo'yicha amaliy chek-list",
        "category": "Frontend", "tags": ["seo", "react"],
        "excerpt": "LCP, CLS, INP — nimani o'lchash va qanday tuzatish kerak.",
        "outline": ["Metrikalar", "Rasmlar", "Shriftlar", "JavaScript hajmi", "Server javobi"],
    },
    {
        "title": "Freelancer sifatida narx belgilash: soatbay, loyiha yoki qiymat asosida?",
        "category": "Freelance va biznes", "tags": ["freelance"],
        "excerpt": "Har bir usulning foyda va xavflari, shartnoma va oldindan to'lov.",
        "outline": ["Soatbay", "Loyiha bo'yicha", "Qiymat asosida", "Oldindan to'lov va bosqichlar",
                    "Qo'shimcha talablar bilan ishlash"],
    },
    {
        "title": "Talaba bo'la turib dasturchi bo'lib ishlash: vaqtni qanday taqsimlayman",
        "category": "Karyera va o'qish", "tags": ["freelance"],
        "excerpt": "O'qish, imtihonlar va real loyihalarni birga olib borish bo'yicha shaxsiy tizimim.",
        "outline": ["Kun tartibi", "Imtihon davrlari", "Mijozlarga muddat aytish", "Charchashdan saqlanish"],
    },
    {
        "title": "Dasturlashni noldan o'rganish: 2026 yil uchun yo'l xaritasi",
        "category": "Karyera va o'qish", "tags": ["python"],
        "excerpt": "Qaysi tildan boshlash, qaysi resurslar va birinchi pulni qanday topish.",
        "outline": ["Til tanlash", "Bepul resurslar", "Birinchi 3 ta loyiha", "Portfolio va GitHub",
                    "Birinchi buyurtma"],
    },
]
