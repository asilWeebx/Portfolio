import { ArrowUpRight, Mail, MapPin, Phone } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { useSite } from '../api/client'
import { formatPhone, telHref } from '../lib/format'
import { SOCIAL_KEYS, SocialIcon } from './Icons'
import Logo from './Logo'

export default function Footer() {
  const { data } = useSite()
  const { pathname } = useLocation()
  const s = data?.settings
  const showCta = pathname !== '/' && pathname !== '/brief'
  const year = new Date().getFullYear()
  const socials = SOCIAL_KEYS.filter((k) => s?.[k])

  return (
    <footer className="footer">
      <div className="container">
        {showCta && (
          <div className="footer__cta">
            <h2>
              G'oyangiz bormi?
              <span>Keling, uni birga quramiz.</span>
            </h2>
            <Link to="/brief" className="btn btn--primary btn--lg">
              Loyihani boshlash <span className="btn__bubble"><ArrowUpRight size={16} /></span>
            </Link>
          </div>
        )}

        <div className="footer__grid">
          <div className="footer__brand">
            <Logo />
            <p>{s?.role || 'Full-stack dasturchi'}. Onlayn do'konlar, mobil ilovalar, POS/ERP tizimlar va Telegram botlar.</p>
            {socials.length > 0 && (
              <div className="socials">
                {socials.map((k) => (
                  <a key={k} href={s![k]} target="_blank" rel="noreferrer" aria-label={k}><SocialIcon name={k} /></a>
                ))}
              </div>
            )}
          </div>
          <div>
            <h4>Sahifalar</h4>
            <ul>
              <li><Link to="/portfolio">Portfolio</Link></li>
              <li><Link to="/blog">Blog</Link></li>
              <li><Link to="/about">Men haqimda</Link></li>
              <li><Link to="/brief">Brief to'ldirish</Link></li>
            </ul>
          </div>
          <div>
            <h4>Xizmatlar</h4>
            <ul>
              {data?.services.slice(0, 5).map((sv) => <li key={sv.id}><Link to="/#services">{sv.title}</Link></li>)}
            </ul>
          </div>
          <div>
            <h4>Aloqa</h4>
            <ul className="footer__contacts">
              {s?.phone && <li><Phone size={16} /><a href={telHref(s.phone)}>{formatPhone(s.phone)}</a></li>}
              {s?.email && <li><Mail size={16} /><a href={`mailto:${s.email}`}>{s.email}</a></li>}
              {s?.telegram && <li><SocialIcon name="telegram" size={16} /><a href={s.telegram} target="_blank" rel="noreferrer">Telegram</a></li>}
              {s?.location && <li><MapPin size={16} /><span>{s.location}</span></li>}
            </ul>
          </div>
        </div>

        <div className="footer__bottom">
          <span>© {year} Asilbek Yuldashev</span>
          <span>asilbek-yuldashev.uz</span>
        </div>
      </div>
    </footer>
  )
}
