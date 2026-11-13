import { ArrowLeft, ArrowRight, ArrowUpRight, Monitor, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useProject } from '../api/client'
import { SocialIcon } from '../components/Icons'
import PageLoader from '../components/PageLoader'
import { PLATFORM_LABEL, projectKind } from '../components/ProjectCard'
import Reveal from '../components/Reveal'
import RichContent from '../components/RichContent'
import Seo from '../components/Seo'
import { isLight } from '../lib/color'
import NotFound from './NotFound'

function AppleIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M16.37 12.7c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.78-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-3-.79-1.54.02-2.96.9-3.76 2.28-1.6 2.78-.41 6.9 1.15 9.16.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.23-.02 2.01-1.12 2.76-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.4-.92-2.38-3.69ZM14.1 5.95c.63-.77 1.06-1.83.94-2.89-.91.04-2.01.61-2.67 1.37-.58.67-1.09 1.76-.95 2.8 1.01.08 2.05-.51 2.68-1.28Z" />
    </svg>
  )
}

function PlayIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="currentColor" d="M3.6 1.8c-.3.3-.4.7-.4 1.2v18c0 .5.1.9.4 1.2l10.1-10.2L3.6 1.8Zm11.5 8.8 2.9-2.9-12-6.9c-.3-.2-.6-.2-.9-.2l10 10Zm0 2.8-10 10c.3 0 .6 0 .9-.2l12-6.9-2.9-2.9Zm4.4-4.3-3.1 3 3.1 3 3.4-2c.6-.3.9-.8.9-1.3s-.3-1-.9-1.3l-3.4-1.4Z" />
    </svg>
  )
}

export default function ProjectDetail() {
  const { slug = '' } = useParams()
  const { data: p, isLoading, isError } = useProject(slug)
  const [lightbox, setLightbox] = useState<number | null>(null)

  useEffect(() => {
    if (lightbox === null || !p) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setLightbox(null)
      if (e.key === 'ArrowRight') setLightbox((i) => (i === null ? i : (i + 1) % p.images.length))
      if (e.key === 'ArrowLeft') setLightbox((i) => (i === null ? i : (i - 1 + p.images.length) % p.images.length))
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [lightbox, p])

  if (isLoading) return <PageLoader />
  if (isError || !p) return <NotFound />

  const color = p.accent_color || '#1F2433'
  const wide = p.images.map((img, i) => ({ ...img, i })).filter((img) => !img.w || !img.h || img.w >= img.h)
  const tall = p.images.map((img, i) => ({ ...img, i })).filter((img) => img.w && img.h && img.w < img.h)
  const kind = projectKind(p)

  const facts = [
    { k: 'Mijoz', v: p.client },
    { k: 'Rolim', v: p.role },
    { k: 'Platforma', v: p.platforms.map((x) => PLATFORM_LABEL[x]).join(', ') },
    { k: 'Yil', v: p.year },
    { k: 'Muddat', v: p.duration },
  ].filter((f) => f.v)

  return (
    <>
      <Seo title={p.seo_title || p.title} description={p.seo_description || p.short_description} image={p.cover} />
      <div className="case-page">
        <div className="container">
          <nav className="crumbs" aria-label="Breadcrumb">
            <Link to="/">Bosh sahifa</Link><i>/</i><Link to="/portfolio">Portfolio</Link><i>/</i><span>{p.title}</span>
          </nav>

          <Reveal as="article" className="case">
            <header className="case__top">
              <div className="case__brand">
                {p.logo ? <img src={p.logo} alt={`${p.title} logo`} /> : <span style={{ background: color }}>{p.title.slice(0, 1)}</span>}
              </div>
              <div className="case__tags">
                {p.technologies.length > 0 && <span className="case__tech">{p.technologies.slice(0, 4).map((t) => t.name).join(', ')}</span>}
                {kind && <span className="case__kind">{kind}</span>}
              </div>
            </header>

            <div className="case__titlebox">
              <h1>{p.title}</h1>
              <p>{p.short_description}</p>
            </div>

            <div className="case__actions">
              {p.live_url && (
                <a href={p.live_url} target="_blank" rel="noreferrer" className="btn btn--primary btn--lg">
                  Saytga o'tish <span className="btn__bubble"><ArrowUpRight size={16} /></span>
                </a>
              )}
              {p.app_store_url && (
                <a href={p.app_store_url} target="_blank" rel="noreferrer" className="store-btn">
                  <AppleIcon /><span><small>Yuklab oling</small>App Store</span>
                </a>
              )}
              {p.play_store_url && (
                <a href={p.play_store_url} target="_blank" rel="noreferrer" className="store-btn">
                  <PlayIcon /><span><small>Yuklab oling</small>Google Play</span>
                </a>
              )}
              {p.telegram_url && (
                <a href={p.telegram_url} target="_blank" rel="noreferrer" className="store-btn">
                  <SocialIcon name="telegram" size={18} /><span><small>Ochish</small>Telegram bot</span>
                </a>
              )}
              {p.desktop_url && (
                <a href={p.desktop_url} target="_blank" rel="noreferrer" className="store-btn">
                  <Monitor size={18} /><span><small>Yuklab oling</small>Desktop</span>
                </a>
              )}
            </div>

            <div className={`case__show${isLight(color) ? ' case__show--light' : ''}`} style={{ background: color }}>
              <div className="case__show-glow" aria-hidden="true" />
              {p.cover && <img src={p.cover} alt={p.title} />}
            </div>
          </Reveal>
        </div>

        <section className="case-text">
          <div className="container case-text__grid">
            <dl className="facts">
              {facts.map((f) => (
                <div key={f.k}><dt>{f.k}</dt><dd>{f.v}</dd></div>
              ))}
              {p.technologies.length > 0 && (
                <div className="facts__tech">
                  <dt>Texnologiyalar</dt>
                  <dd>
                    <ul className="chips chips--sm">
                      {p.technologies.map((t) => (
                        <li key={t.id} className="chip"><i className="dot" style={{ background: t.color && t.color !== '#FFFFFF' ? t.color : 'var(--text)' }} />{t.name}</li>
                      ))}
                    </ul>
                  </dd>
                </div>
              )}
            </dl>
            <div className="case-text__body">
              {p.content ? <RichContent html={p.content} /> : <p className="muted">Batafsil ma'lumot tez orada qo'shiladi.</p>}
            </div>
          </div>
        </section>

        {(wide.length > 0 || tall.length > 0) && (
          <section className="container case-gallery">
            {wide.map((img) => (
              <Reveal key={img.id} className="shot shot--wide">
                <button type="button" onClick={() => setLightbox(img.i)} aria-label="Kattalashtirish">
                  <img src={img.image} alt={img.caption || p.title} loading="lazy" />
                </button>
              </Reveal>
            ))}
            {tall.length > 0 && (
              <div className="shots-row" style={{ background: color }}>
                {tall.map((img) => (
                  <button key={img.id} type="button" className="shot shot--tall" onClick={() => setLightbox(img.i)} aria-label="Kattalashtirish">
                    <img src={img.image} alt={img.caption || p.title} loading="lazy" />
                  </button>
                ))}
              </div>
            )}
          </section>
        )}

        <nav className="container case-nav" aria-label="Boshqa loyihalar">
          {p.prev ? (
            <Link to={`/portfolio/${p.prev.slug}`} className="case-nav__item">
              <ArrowLeft size={20} /><span><small>Oldingi loyiha</small>{p.prev.title}</span>
            </Link>
          ) : <span />}
          {p.next && (
            <Link to={`/portfolio/${p.next.slug}`} className="case-nav__item case-nav__item--next">
              <span><small>Keyingi loyiha</small>{p.next.title}</span><ArrowRight size={20} />
            </Link>
          )}
        </nav>
      </div>

      {lightbox !== null && p.images[lightbox] && (
        <div className="lightbox" role="dialog" aria-modal="true" onClick={() => setLightbox(null)}>
          <button type="button" className="lightbox__close" aria-label="Yopish"><X size={28} /></button>
          <img src={p.images[lightbox].image} alt={p.images[lightbox].caption || p.title} onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </>
  )
}
