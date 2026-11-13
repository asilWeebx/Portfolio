import { ArrowRight, ArrowUpRight, Check, Gem, Phone, Quote, Star, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useHome, useSite } from '../api/client'
import type { ProjectListItem } from '../api/types'
import Hero from '../components/Hero'
import { ServiceIcon, SocialIcon } from '../components/Icons'
import PostCard, { PostCardSkeleton } from '../components/PostCard'
import { BentoGrid } from '../components/ProjectCard'
import QuickForm from '../components/QuickForm'
import Reveal from '../components/Reveal'
import SectionHead from '../components/SectionHead'
import Seo from '../components/Seo'
import { telHref } from '../lib/format'

const PROCESS = [
  { n: '01', title: 'Brief va tahlil', text: "Muammoni, auditoriyani va maqsadni aniqlaymiz. Natijada — aniq vazifa, muddat va narx." },
  { n: '02', title: 'Dizayn va prototip', text: "Figma'da sahifalar maketi. Kod yozishdan oldin hammasini ko'rib, kelishib olamiz." },
  { n: '03', title: 'Ishlab chiqish', text: "Har hafta oraliq natijani ko'rsataman. Siz jarayonni doim ko'rib turasiz." },
  { n: '04', title: 'Ishga tushirish', text: "Serverga joylash, App Store / Play Market, o'rgatish va qo'llab-quvvatlash." },
]

function techRows<T>(items: T[]): T[][] {
  const half = Math.ceil(items.length / 2)
  const rows = items.length > 8 ? [items.slice(0, half), items.slice(half)] : [items]
  return rows.map((row) => {
    let out = row
    while (out.length < 10) out = [...out, ...row]
    return out
  })
}

/** "Men haqimda" blokidagi rasm: foto bo'lsa — foto, bo'lmasa — loyiha mockup'i brend rangida. */
function AboutImage({ src, project, className }: { src?: string | null; project?: ProjectListItem; className: string }) {
  if (src) return <div className={className}><img src={src} alt="" loading="lazy" /></div>
  if (project?.cover) {
    return (
      <div className={`${className} about-img--mock`} style={{ background: project.accent_color }}>
        <img src={project.cover} alt={project.title} loading="lazy" />
      </div>
    )
  }
  return <div className={`${className} skeleton`} />
}

export default function Home() {
  const { data: site } = useSite()
  const { data, isLoading } = useHome()
  const s = site?.settings
  const featured = data?.featured_projects ?? []
  const years = data?.stats.years ?? s?.years_experience

  return (
    <>
      <Seo />
      <Hero />

      {/* ------------------------------------------------ Men haqimda */}
      <section className="section about-home" id="about">
        <div className="container about-home__grid">
          <div className="about-home__media">
            <Reveal from="left" className="about-home__col">
              <AboutImage className="about-img about-img--a" src={s?.avatar} project={featured[0]} />
              <div className="about-home__stat">
                <b>{years ?? 3}+</b>
                <span>yillik<br />tajriba</span>
              </div>
            </Reveal>
            <Reveal from="left" delay={120} className="about-home__col about-home__col--low">
              <AboutImage className="about-img about-img--b" src={s?.about_photo} project={featured[2] ?? featured[1]} />
            </Reveal>
            <svg viewBox="0 0 140 140" className="about-home__ring" aria-hidden="true">
              <defs><path id="about-ring" d="M70 70m-52 0a52 52 0 1 1 104 0a52 52 0 1 1-104 0" /></defs>
              <text><textPath href="#about-ring" textLength="324" lengthAdjust="spacing">G'OYA • DIZAYN • KOD • </textPath></text>
            </svg>
          </div>

          <Reveal from="right" className="about-home__text">
            <span className="eyebrow">Salom...</span>
            <h2 className="section-title">Men haqimda</h2>
            <p className="lead">
              {years ?? 3} yildan beri do'konlar va bizneslar uchun savdo tizimlari, onlayn do'konlar,
              mobil ilovalar va Telegram botlar yaratib kelaman.
            </p>
            <p className="muted-p">
              G'oyani tahlil qilishdan tortib serverga chiqarish, App Store va Play Market'ga joylash hamda
              qo'llab-quvvatlashgacha — butun jarayonni o'zim olib boraman.
            </p>
            <div className="features">
              <div className="feature"><span><Zap size={22} /></span>Tezkor<br />yechimlar</div>
              <div className="feature"><span><Gem size={22} /></span>Noyob<br />loyihalar</div>
            </div>
            <div className="about-home__actions">
              <Link to="/brief" className="btn btn--primary btn--lg">
                Brief to'ldirish <span className="btn__bubble"><ArrowUpRight size={16} /></span>
              </Link>
              {s?.phone ? (
                <a href={telHref(s.phone)} className="btn btn--outline btn--lg">
                  Qo'ng'iroq <span className="btn__bubble"><Phone size={15} /></span>
                </a>
              ) : s?.telegram ? (
                <a href={s.telegram} target="_blank" rel="noreferrer" className="btn btn--outline btn--lg">
                  Telegram <span className="btn__bubble"><SocialIcon name="telegram" size={15} /></span>
                </a>
              ) : (
                <Link to="/about" className="btn btn--outline btn--lg">Batafsil</Link>
              )}
            </div>
          </Reveal>
        </div>
      </section>

      {/* ------------------------------------------------ Portfolio */}
      <section className="section section--alt" id="portfolio">
        <div className="container">
          <SectionHead
            eyebrow="Ishlarim"
            title="Portfolio"
            upper
            action={<Link to="/portfolio" className="btn btn--outline">Barcha loyihalar <ArrowRight size={18} /></Link>}
          />
          <BentoGrid projects={featured} loading={isLoading} />
        </div>
      </section>

      {/* ------------------------------------------------ Xizmatlar */}
      <section className="section" id="services">
        <div className="container">
          <SectionHead eyebrow="Xizmatlar" title="Nimalar qila olaman" />
          <div className="services">
            {site?.services.map((sv, i) => (
              <Reveal key={sv.id} delay={(i % 3) * 90} className="service">
                <span className="service__icon"><ServiceIcon name={sv.icon} /></span>
                <h3>{sv.title}</h3>
                <p>{sv.short}</p>
                {sv.features.length > 0 && (
                  <ul className="service__list">
                    {sv.features.map((f) => <li key={f}><Check size={16} /> {f}</li>)}
                  </ul>
                )}
                <div className="service__foot">
                  {sv.price_from && <span className="service__price">{sv.price_from}</span>}
                  <Link to="/brief" className="service__link" aria-label={`${sv.title} — buyurtma`}>
                    <ArrowUpRight size={20} />
                  </Link>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ------------------------------------------------ Texnologiyalar */}
      {data && data.technologies.length > 0 && (
        <section className="section section--tight section--alt">
          <div className="container">
            <SectionHead eyebrow="Texnologiyalar" title="Ishlatadigan vositalarim" />
          </div>
          <div className="marquee" aria-label="Texnologiyalar ro'yxati">
            {techRows(data.technologies).map((row, r) => (
              <div key={r} className={`marquee__track${r ? ' marquee__track--reverse' : ''}`}>
                {[...row, ...row].map((t, i) => (
                  <span key={`${t.id}-${i}`} className="tech-pill" aria-hidden={i >= row.length || undefined}>
                    {t.icon ? <img src={t.icon} alt="" /> : <i style={{ background: t.color && t.color !== '#FFFFFF' ? t.color : 'var(--text)' }} />}
                    {t.name}
                  </span>
                ))}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ------------------------------------------------ Jarayon */}
      <section className="section">
        <div className="container">
          <SectionHead eyebrow="Jarayon" title="Qanday ishlayman" text="Shaffof jarayon — har bir bosqichda nima bo'layotganini bilasiz." />
          <ol className="process">
            {PROCESS.map((p, i) => (
              <Reveal as="li" key={p.n} delay={i * 90} className="process__item">
                <span className="process__n">{p.n}</span>
                <h3>{p.title}</h3>
                <p>{p.text}</p>
              </Reveal>
            ))}
          </ol>
        </div>
      </section>

      {/* ------------------------------------------------ Mijozlar fikri */}
      {data && data.testimonials.length > 0 && (
        <section className="section section--alt">
          <div className="container">
            <SectionHead eyebrow="Mijozlar fikri" title="Men bilan ishlaganlar nima deydi" />
            <div className="testimonials">
              {data.testimonials.map((t, i) => (
                <Reveal key={t.id} delay={(i % 3) * 90} className="testimonial">
                  <Quote size={28} className="testimonial__q" />
                  <div className="testimonial__stars" aria-label={`${t.rating} / 5`}>
                    {Array.from({ length: 5 }).map((_, k) => <Star key={k} size={16} fill={k < t.rating ? 'currentColor' : 'none'} />)}
                  </div>
                  <p>{t.text}</p>
                  <div className="testimonial__author">
                    {t.avatar ? <img src={t.avatar} alt="" /> : <span>{t.author.slice(0, 1)}</span>}
                    <div><b>{t.author}</b><small>{t.position}</small></div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ------------------------------------------------ Blog */}
      <section className="section section--alt">
        <div className="container">
          <SectionHead
            eyebrow="Blog"
            title="So'nggi maqolalar"
            action={<Link to="/blog" className="btn btn--outline">Barcha maqolalar <ArrowRight size={18} /></Link>}
          />
          <div className="prow-grid">
            {isLoading
              ? Array.from({ length: 2 }).map((_, i) => <PostCardSkeleton key={i} />)
              : data?.latest_posts.map((p, i) => (
                  <Reveal key={p.id} delay={(i % 2) * 90}>
                    <PostCard post={p} />
                  </Reveal>
                ))}
          </div>
        </div>
      </section>

      {/* ------------------------------------------------ Salom... (qisqa forma) */}
      <section className="hello" id="brief">
        <div className="hello__band">
          <div className="container">
            <Reveal from="left">
              <span className="eyebrow">Salom...</span>
              <h2 className="section-title">Hal qilinmagan muammo bormi?</h2>
            </Reveal>
          </div>
        </div>
        <div className="container hello__form">
          <Reveal>
            <QuickForm />
          </Reveal>
          <p className="hello__more">
            Batafsilroq yozmoqchimisiz? <Link to="/brief">To'liq brief to'ldiring <ArrowUpRight size={16} /></Link>
          </p>
        </div>
      </section>
    </>
  )
}
