import { Menu, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'
import { useSite } from '../api/client'
import { cx, telHref } from '../lib/format'
import { SocialIcon } from './Icons'
import Logo from './Logo'

const NAV = [
  { to: '/about', label: 'Men haqimda' },
  { to: '/#services', label: 'Xizmatlar' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/blog', label: 'Blog' },
]

/** +998 90 123 45 67 → ["+998 90", "123 45 67"] (UIC uslubida: prefiks kulrang, raqam qalin) */
function splitPhone(phone: string): [string, string] {
  const m = phone.trim().match(/^(\+?\d{3}\s?\(?\d{2}\)?)\s?(.*)$/)
  return m ? [m[1], m[2]] : ['', phone]
}

export default function Header() {
  const { data } = useSite()
  const s = data?.settings
  const { pathname, hash } = useLocation()
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const overHero = pathname === '/' && !scrolled && !open

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => setOpen(false), [pathname, hash])

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  const [pre, num] = s?.phone ? splitPhone(s.phone) : ['', '']

  return (
    <header className={cx('header', overHero ? 'header--hero' : 'header--solid')}>
      <div className="container header__inner">
        <Link to="/" className="header__logo" aria-label="Bosh sahifa">
          <Logo />
        </Link>

        <nav className="header__nav" aria-label="Asosiy menyu">
          {NAV.map((n) =>
            n.to.includes('#') ? (
              <Link key={n.to} to={n.to} className="header__link">{n.label}</Link>
            ) : (
              <NavLink key={n.to} to={n.to} className={({ isActive }) => cx('header__link', isActive && 'is-active')}>
                {n.label}
              </NavLink>
            ),
          )}
        </nav>

        <div className="header__actions">
          {s?.phone ? (
            <a href={telHref(s.phone)} className="header__phone">
              <span>{pre}</span> {num}
            </a>
          ) : s?.telegram ? (
            <a href={s.telegram} target="_blank" rel="noreferrer" className="header__pill">
              <SocialIcon name="telegram" size={18} /> Telegram
            </a>
          ) : null}
          <Link to="/brief" className="btn btn--primary btn--sm header__cta">Brief</Link>
          <button
            type="button"
            className="header__burger"
            aria-label={open ? 'Menyuni yopish' : 'Menyuni ochish'}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      <div className={cx('mobile-menu', open && 'is-open')} aria-hidden={!open}>
        <nav className="container mobile-menu__nav">
          <Link to="/" className="mobile-menu__link">Bosh sahifa</Link>
          {NAV.map((n, i) => (
            <Link key={n.to} to={n.to} className="mobile-menu__link" style={{ transitionDelay: open ? `${60 + i * 40}ms` : '0ms' }}>
              {n.label}
            </Link>
          ))}
          <Link to="/brief" className="btn btn--primary btn--lg mobile-menu__cta">Brief to'ldirish</Link>
          <div className="mobile-menu__contacts">
            {s?.phone && <a href={telHref(s.phone)}>{s.phone}</a>}
            {s?.email && <a href={`mailto:${s.email}`}>{s.email}</a>}
            {s?.telegram && <a href={s.telegram} target="_blank" rel="noreferrer">Telegram</a>}
          </div>
        </nav>
      </div>
    </header>
  )
}
