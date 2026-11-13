/** "AY" monogrammasi: A — tog' cho'qqisi, Y — firuza rangli shox. */
export function LogoMark({ size = 40, dark = false }: { size?: number; dark?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true" className="logo-mark">
      <path
        fill={dark ? '#0E0E0F' : 'currentColor'}
        fillRule="evenodd"
        d="M3 52 23 10l20 42H3Zm20-18-8.5 18h17L23 34Z"
      />
      <path
        d="M39 22l9 14 9-14M48 36v13"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export default function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <span className="logo">
      <LogoMark size={compact ? 34 : 40} />
      <span className="logo__text">
        <b>Asilbek</b>
        <span>Yuldoshev</span>
      </span>
    </span>
  )
}
