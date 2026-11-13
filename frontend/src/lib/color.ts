/** Hex rangning yorqinligi (0..1) — kartochkada oq yoki qora matn tanlash uchun. */
export function luminance(hex: string): number {
  const m = hex.replace('#', '').match(/^([\da-f]{2})([\da-f]{2})([\da-f]{2})/i)
  if (!m) return 0
  const [r, g, b] = m.slice(1).map((x) => {
    const c = parseInt(x, 16) / 255
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

export const isLight = (hex?: string) => (hex ? luminance(hex) > 0.45 : false)
