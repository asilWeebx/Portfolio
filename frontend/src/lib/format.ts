const MONTHS = [
  'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
  'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr',
]

/** 2026-11-14 → "14-noyabr, 2026" */
export function formatDate(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  return `${d.getDate()}-${MONTHS[d.getMonth()]}, ${d.getFullYear()}`
}

export function formatViews(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(n >= 10000 ? 0 : 1).replace('.0', '')}K`
  return String(n)
}

/** Har qanday yozilgan raqamni "+998 97 802 20 08" ko'rinishiga keltiradi. */
export function formatPhone(phone: string): string {
  const d = phone.replace(/\D/g, '')
  const m = d.match(/^(998)(\d{2})(\d{3})(\d{2})(\d{2})$/)
  return m ? `+${m[1]} ${m[2]} ${m[3]} ${m[4]} ${m[5]}` : phone.trim()
}

export function telHref(phone: string): string {
  return `tel:${phone.replace(/[^\d+]/g, '')}`
}

/** Telegram havolasidan @username ko'rinishini olish */
export function telegramHandle(url: string): string {
  const m = url.match(/t\.me\/([\w_]+)/i)
  return m ? `@${m[1]}` : url
}

export function cx(...parts: (string | false | null | undefined)[]): string {
  return parts.filter(Boolean).join(' ')
}
