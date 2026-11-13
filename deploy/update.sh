#!/usr/bin/env bash
# Serverda yangilanishni chiqarish (GitHub'dan):  sudo bash /opt/portfolio/deploy/update.sh
set -euo pipefail
cd /opt/portfolio
git pull --ff-only
cd backend
venv/bin/pip install -q -r requirements.txt
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput | tail -1
# nginx (www-data) o'qiy olishi uchun
chmod -R a+rX staticfiles
find /opt/portfolio -path '*/venv' -prune -o -name __pycache__ -type d -exec chmod -R a+rX {} +
systemctl restart portfolio
sleep 2 && systemctl is-active portfolio
