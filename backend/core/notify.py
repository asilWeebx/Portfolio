"""Yangi brief kelganda Telegram'ga xabar yuborish (TELEGRAM_BOT_TOKEN va TELEGRAM_CHAT_ID .env'da bo'lsa)."""
import json
import threading
import urllib.request
from html import escape

from django.conf import settings


def _send(text: str) -> None:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=8).read()
    except Exception:
        pass


def notify_new_request(obj) -> None:
    if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
        return
    services = ", ".join(s.title for s in obj.services.all()) or "—"
    lines = [
        "🆕 <b>Yangi brief</b>",
        f"👤 {escape(obj.name)}",
        f"📞 {escape(obj.phone)}",
    ]
    if obj.email:
        lines.append(f"✉️ {escape(obj.email)}")
    if obj.company:
        lines.append(f"🏢 {escape(obj.company)}")
    lines += [
        f"🧩 {escape(services)}",
        f"💰 {escape(obj.get_budget_display())}",
    ]
    if obj.message:
        lines.append(f"\n💬 {escape(obj.message[:1500])}")
    threading.Thread(target=_send, args=("\n".join(lines),), daemon=True).start()
