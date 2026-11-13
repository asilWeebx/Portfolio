# asilbek-yuldashev.uz

Shaxsiy portfolio va blog: Django + DRF (admin panel, API) va React + Vite (sayt).

```
backend/    Django 5.1, DRF, Unfold admin, CKEditor 5
frontend/   React 18, TypeScript, Vite, React Query
deploy/     nginx.conf, portfolio.service (gunicorn)
assets/     loyihalar skrinshotlari (gitga kirmaydi)
```

## Lokal ishga tushirish

```bash
# backend — http://localhost:8010/admin
cd backend
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed              # xizmatlar, texnologiyalar, blog mavzulari, namunaviy maqolalar
.venv/bin/python manage.py import_projects   # assets/project-shots → loyihalar, mockup muqovalar
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver 127.0.0.1:8010

# frontend — http://localhost:5180 (/api va /media 8010'ga proxy qilinadi)
cd frontend
npm install
npm run dev
```

## Admin panelda nima qilinadi

| Bo'lim | Nima uchun |
| --- | --- |
| Sayt sozlamalari | Ism, hero matni, avatar, telefon, Telegram, ijtimoiy tarmoqlar, SEO |
| Loyihalar | Portfolio: muqova (shaffof mockup), logo, brend rangi, havolalar (sayt, App Store, Google Play), galereya |
| Maqolalar | Blog: CKEditor (rasm yuklash, kod bloklari, video), qoralama → chop etish |
| Mavzular / Teglar | Blog rubrikalari |
| Brief / So'rovlar | Saytdagi formalardan kelgan arizalar (holat: yangi → ko'rib chiqilmoqda → yakunlangan) |

Loyiha kartochkasi uchun muqova shaffof fonli bo'lsa, orqasida "Aksent rang" ko'rinadi. Yangi loyiha
qo'shganda `import_projects` buyrug'idagi `compose_cover()` (backend/portfolio/mockups.py) bilan
skrinshotdan monitor/telefon mockup yasash mumkin.

## Deploy (Ubuntu VPS)

```bash
# serverda: /srv/portfolio
cd backend && cp .env.example .env   # SECRET_KEY, DATABASE_URL va h.k.ni to'ldiring
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate && .venv/bin/python manage.py collectstatic --noinput
# media'ni lokal kompyuterdan ko'chiring: rsync -av backend/media/ server:/srv/portfolio/backend/media/

cd ../frontend && npm ci && npm run build

sudo cp deploy/portfolio.service /etc/systemd/system/ && sudo systemctl enable --now portfolio
sudo cp deploy/nginx.conf /etc/nginx/sites-available/asilbek-yuldashev.uz
sudo ln -s /etc/nginx/sites-available/asilbek-yuldashev.uz /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d asilbek-yuldashev.uz -d www.asilbek-yuldashev.uz
```

## Rasmlar litsenziyasi

Hero fotosurati: "Aurora Over Mendenhall Glacier" — USDA Forest Service (Harvey Hergett), Public Domain,
indigo rangga qayta ishlangan.
