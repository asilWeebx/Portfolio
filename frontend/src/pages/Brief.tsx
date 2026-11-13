import { Clock, Mail, MessageCircle, Phone } from 'lucide-react'
import { useSite } from '../api/client'
import BriefForm from '../components/BriefForm'
import { SocialIcon } from '../components/Icons'
import PageHero from '../components/PageHero'
import Seo from '../components/Seo'
import { formatPhone, telegramHandle, telHref } from '../lib/format'

export default function Brief() {
  const { data } = useSite()
  const s = data?.settings

  return (
    <>
      <Seo title="Brief to'ldirish" description="Loyihangiz haqida qisqacha yozing — 24 soat ichida bog'lanaman." />
      <PageHero
        eyebrow="Brief"
        title={<>Qanday yechim <span className="text-accent">kerak?</span></>}
        text="Bir necha savolga javob bering — vazifani aniqlashtirib, taxminiy narx va muddatni aytaman. Bu sizni hech narsaga majburlamaydi."
        crumbs={[{ to: '/brief', label: 'Brief' }]}
      />
      <section className="section section--flush">
        <div className="container brief-page">
          <div className="brief-page__form">
            <BriefForm />
          </div>
          <aside className="brief-page__aside">
            <div className="aside-card">
              <h4>Keyin nima bo'ladi?</h4>
              <ol className="steps">
                <li><MessageCircle size={18} /> 24 soat ichida bog'lanaman va savollar beraman</li>
                <li><Clock size={18} /> 1–2 kunda taklif: yechim, narx, muddat</li>
                <li><Mail size={18} /> Kelishsak — shartnoma va ish boshlanadi</li>
              </ol>
            </div>
            <div className="aside-card">
              <h4>To'g'ridan-to'g'ri aloqa</h4>
              <ul className="direct">
                {s?.telegram && <li><SocialIcon name="telegram" size={18} /><a href={s.telegram} target="_blank" rel="noreferrer">{telegramHandle(s.telegram)}</a></li>}
                {s?.phone && <li><Phone size={18} /><a href={telHref(s.phone)}>{formatPhone(s.phone)}</a></li>}
                {s?.email && <li><Mail size={18} /><a href={`mailto:${s.email}`}>{s.email}</a></li>}
                {!s?.telegram && !s?.phone && !s?.email && <li className="muted">Kontaktlar admin paneldagi "Sayt sozlamalari"dan qo'shiladi.</li>}
              </ul>
            </div>
          </aside>
        </div>
      </section>
    </>
  )
}
