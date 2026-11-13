import { ArrowRight, Download, MapPin } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useHome, useSite } from '../api/client'
import type { Technology } from '../api/types'
import { LogoMark } from '../components/Logo'
import PageHero from '../components/PageHero'
import Reveal from '../components/Reveal'
import Seo from '../components/Seo'

function groupTech(techs: Technology[]) {
  const map = new Map<string, { label: string; items: Technology[] }>()
  techs.forEach((t) => {
    if (!map.has(t.group)) map.set(t.group, { label: t.group_label, items: [] })
    map.get(t.group)!.items.push(t)
  })
  return Array.from(map.values())
}

export default function About() {
  const { data: site } = useSite()
  const { data } = useHome()
  const s = site?.settings

  return (
    <>
      <Seo title="Men haqimda" description={s?.meta_description} />
      <PageHero
        eyebrow="Men haqimda"
        title={s?.about_title || 'Salom, men Asilbek'}
        crumbs={[{ to: '/about', label: 'Men haqimda' }]}
      />

      <section className="section section--flush">
        <div className="container about">
          <Reveal from="left" className="about__photo">
            {s?.avatar ? <img src={s.avatar} alt={s.full_name} /> : <div className="about__placeholder"><LogoMark size={120} /></div>}
            <div className="about__card">
              <b>{s?.full_name}</b>
              <span>{s?.role}</span>
              {s?.location && <small><MapPin size={14} /> {s.location}</small>}
            </div>
          </Reveal>

          <Reveal from="right" className="about__text">
            {(s?.about_text || '').split(/\n{2,}/).filter(Boolean).map((para, i) => <p key={i}>{para}</p>)}
            <div className="about__actions">
              <Link to="/brief" className="btn btn--primary btn--lg">Birga ishlaymiz <ArrowRight size={20} /></Link>
              {s?.cv_file && (
                <a href={s.cv_file} className="btn btn--outline btn--lg" download>
                  <Download size={20} /> Rezyume (PDF)
                </a>
              )}
            </div>
          </Reveal>
        </div>
      </section>

      {data && data.experience.length > 0 && (
        <section className="section">
          <div className="container">
            <span className="eyebrow">Tajriba</span>
            <h2 className="section-title">Yo'lim</h2>
            <ol className="timeline">
              {data.experience.map((e, i) => (
                <Reveal as="li" key={e.id} delay={i * 80} className="timeline__item">
                  <span className="timeline__period">{e.period}</span>
                  <div>
                    <h3>{e.position}</h3>
                    <span className="timeline__company">
                      {e.url ? <a href={e.url} target="_blank" rel="noreferrer">{e.company}</a> : e.company}
                    </span>
                    {e.description && <p>{e.description}</p>}
                  </div>
                </Reveal>
              ))}
            </ol>
          </div>
        </section>
      )}

      {data && data.technologies.length > 0 && (
        <section className="section">
          <div className="container">
            <span className="eyebrow">Stek</span>
            <h2 className="section-title">Texnologiyalar</h2>
            <div className="stack-grid">
              {groupTech(data.technologies).map((g, i) => (
                <Reveal key={g.label} delay={(i % 3) * 80} className="stack-card">
                  <h3>{g.label}</h3>
                  <ul className="chips">
                    {g.items.map((t) => (
                      <li key={t.id} className="chip"><i className="dot" style={{ background: t.color || 'var(--accent)' }} />{t.name}</li>
                    ))}
                  </ul>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      )}
    </>
  )
}
