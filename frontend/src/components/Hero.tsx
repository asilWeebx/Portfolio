import { ArrowUpRight, Phone, Play } from 'lucide-react'
import { useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useSite } from '../api/client'
import { telHref } from '../lib/format'
import { SocialIcon } from './Icons'

/** "AY" monogrammasining shisha harflari (logodagi shakllar: A — cho'qqi, Y — shox). */
function GlassLetters() {
  return (
    <div className="glass" aria-hidden="true">
      <div className="glass__blur" />
      <svg className="glass__svg" viewBox="0 0 1040 660">
        <defs>
          <linearGradient id="glass-fill" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#fff" stopOpacity=".26" />
            <stop offset=".55" stopColor="#fff" stopOpacity=".07" />
            <stop offset="1" stopColor="#fff" stopOpacity=".14" />
          </linearGradient>
          <filter id="glass-edge" x="-5%" y="-5%" width="110%" height="110%">
            <feMorphology in="SourceAlpha" operator="erode" radius="2.5" result="inner" />
            <feComposite in="SourceAlpha" in2="inner" operator="out" result="edge" />
            <feFlood floodColor="#fff" floodOpacity=".55" />
            <feComposite in2="edge" operator="in" />
          </filter>
          <g id="ay-shape">
            <path
              fillRule="evenodd"
              d="M40 600 300 40l260 560H40Zm260-262-104 262h208L300 338Z"
              stroke="#fff"
              strokeWidth="40"
              strokeLinejoin="round"
              fill="#fff"
            />
            <path d="M610 70l180 260 180-260M790 330v260" fill="none" stroke="#fff" strokeWidth="120" strokeLinecap="round" strokeLinejoin="round" />
          </g>
        </defs>
        <mask id="ay-mask">
          <use href="#ay-shape" />
        </mask>
        <rect width="1040" height="660" fill="url(#glass-fill)" mask="url(#ay-mask)" />
        <use href="#ay-shape" filter="url(#glass-edge)" />
      </svg>
    </div>
  )
}

export default function Hero() {
  const { data } = useSite()
  const s = data?.settings
  const bg = useRef<HTMLDivElement>(null)

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
      <div ref={bg} className="hero__bg" aria-hidden="true" />
      <div className="hero__shade" aria-hidden="true" />
      <GlassLetters />

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
