import { ArrowUpRight, Phone, Play } from 'lucide-react'
import { useEffect, useRef } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useSite } from '../api/client'
import { telHref } from '../lib/format'
import HeroChat from './HeroChat'
import { SocialIcon } from './Icons'

/** Fon variantlari — vaqtincha: /?bg=teton-pink kabi almashtirib ko'rish uchun. */
const BACKGROUNDS = ['teton-pink', 'teton-purple', 'denali'] as const

function bgVars(key: string): React.CSSProperties {
  return {
    '--hero-xl': `url('/images/hero-${key}-2400.webp')`,
    '--hero-md': `url('/images/hero-${key}-1440.webp')`,
    '--hero-sm': `url('/images/hero-${key}-mobile.webp')`,
  } as React.CSSProperties
}

export default function Hero() {
  const { data } = useSite()
  const s = data?.settings
  const bg = useRef<HTMLDivElement>(null)
  const [params] = useSearchParams()
  const choice = params.get('bg')
  const bgKey = BACKGROUNDS.includes(choice as never) ? (choice as string) : BACKGROUNDS[0]

  // yengil parallaks: foto skroll bilan sekinroq siljiydi
  useEffect(() => {
    const el = bg.current
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    let raf = 0
    const onScroll = () => {
      cancelAnimationFrame(raf)
      raf = requestAnimationFrame(() => {
        const y = Math.min(window.scrollY, 1000)
        el.style.transform = `translate3d(0, ${y * 0.25}px, 0) scale(1.06)`
      })
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', onScroll)
      cancelAnimationFrame(raf)
    }
  }, [])

  return (
    <section className="hero">
      <div ref={bg} className="hero__bg" style={bgVars(bgKey)} aria-hidden="true" />
      <div className="hero__shade" aria-hidden="true" />

      <div className="container hero__inner">
        <div className="hero__content">
          <h1 className="hero__title">{s?.hero_title || 'Raqamli yechimlar yarataman'}</h1>
          <p className="hero__sub">har qanday murakkablikda</p>
          <p className="hero__text">{s?.hero_subtitle}</p>
          <div className="hero__actions">
            <Link to="/brief" className="btn btn--primary btn--lg">
              Brief to'ldirish <span className="btn__bubble"><ArrowUpRight size={16} /></span>
            </Link>
            {s?.phone ? (
              <a href={telHref(s.phone)} className="btn btn--ghost btn--lg">
                Qo'ng'iroq <span className="btn__bubble"><Phone size={15} /></span>
              </a>
            ) : s?.telegram ? (
              <a href={s.telegram} target="_blank" rel="noreferrer" className="btn btn--ghost btn--lg">
                Telegram <span className="btn__bubble"><SocialIcon name="telegram" size={15} /></span>
              </a>
            ) : (
              <Link to="/portfolio" className="btn btn--ghost btn--lg">Portfolio</Link>
            )}
          </div>
        </div>
        <HeroChat />
      </div>

      <a href="#portfolio" className="reel" aria-label="Loyihalarni ko'rish">
        <svg viewBox="0 0 160 160" className="reel__ring" aria-hidden="true">
          <defs>
            <path id="reel-path" d="M80 80m-62 0a62 62 0 1 1 124 0a62 62 0 1 1-124 0" />
          </defs>
          <text>
            <textPath href="#reel-path" textLength="386" lengthAdjust="spacing">PORTFOLIO • LOYIHALAR • </textPath>
          </text>
        </svg>
        <span className="reel__play"><Play size={26} fill="currentColor" /></span>
      </a>
    </section>
  )
}
