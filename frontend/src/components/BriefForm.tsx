import { ArrowRight, CircleCheck, LoaderCircle } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { ApiError, useContact, useSite } from '../api/client'
import { cx } from '../lib/format'
import { ServiceIcon } from './Icons'

const BUDGETS = [
  { value: 'lt500', label: '$500 gacha' },
  { value: '500_1500', label: '$500 — 1 500' },
  { value: '1500_5000', label: '$1 500 — 5 000' },
  { value: 'gt5000', label: '$5 000+' },
  { value: 'unknown', label: 'Hali bilmayman' },
]

type Errors = Partial<Record<'name' | 'phone' | 'email' | 'form', string>>

function formatPhone(raw: string) {
  let d = raw.replace(/\D/g, '')
  if (d.startsWith('998')) d = d.slice(3)
  d = d.slice(0, 9)
  const parts = [d.slice(0, 2), d.slice(2, 5), d.slice(5, 7), d.slice(7, 9)].filter(Boolean)
  return `+998 ${parts.join(' ')}`.trimEnd()
}

export default function BriefForm({ compact = false }: { compact?: boolean }) {
  const { data } = useSite()
  const contact = useContact()
  const [services, setServices] = useState<number[]>([])
  const [budget, setBudget] = useState('unknown')
  const [form, setForm] = useState({ name: '', phone: '+998 ', email: '', company: '', message: '', website: '' })
  const [errors, setErrors] = useState<Errors>({})

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm((f) => ({ ...f, [k]: k === 'phone' ? formatPhone(e.target.value) : e.target.value }))

  const toggle = (id: number) => setServices((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]))

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    const errs: Errors = {}
    if (form.name.trim().length < 2) errs.name = 'Ismingizni kiriting'
    if (form.phone.replace(/\D/g, '').length < 12) errs.phone = "Telefon raqamni to'liq kiriting"
    if (form.email && !/^\S+@\S+\.\S+$/.test(form.email)) errs.email = "Email noto'g'ri"
    setErrors(errs)
    if (Object.keys(errs).length) return
    try {
      await contact.mutateAsync({ ...form, services, budget })
    } catch (err) {
      if (err instanceof ApiError && err.status === 429) {
        setErrors({ form: "Juda ko'p urinish. Birozdan keyin qayta yuboring yoki Telegram orqali yozing." })
      } else if (err instanceof ApiError && err.data && typeof err.data === 'object') {
        const d = err.data as Record<string, string[]>
        setErrors({ name: d.name?.[0], phone: d.phone?.[0], email: d.email?.[0], form: d.detail as unknown as string })
      } else {
        setErrors({ form: "Yuborib bo'lmadi. Internet aloqasini tekshirib, qayta urinib ko'ring." })
      }
    }
  }

  if (contact.isSuccess) {
    return (
      <div className="brief-success" role="status">
        <CircleCheck size={56} strokeWidth={1.5} />
        <h3>Rahmat, {form.name.split(' ')[0]}!</h3>
        <p>So'rovingiz qabul qilindi. 24 soat ichida siz bilan bog'lanaman.</p>
        {data?.settings.telegram && (
          <a className="btn btn--outline" href={data.settings.telegram} target="_blank" rel="noreferrer">
            Telegram'da yozish
          </a>
        )}
      </div>
    )
  }

  return (
    <form className={cx('brief-form', compact && 'brief-form--compact')} onSubmit={submit} noValidate>
      {data && data.services.length > 0 && (
        <fieldset className="brief-form__group">
          <legend>Qanday yechim kerak?</legend>
          <div className="option-grid">
            {data.services.map((s) => (
              <button
                key={s.id}
                type="button"
                className={cx('option', services.includes(s.id) && 'is-selected')}
                aria-pressed={services.includes(s.id)}
                onClick={() => toggle(s.id)}
              >
                <ServiceIcon name={s.icon} size={20} />
                <span>{s.title}</span>
              </button>
            ))}
          </div>
        </fieldset>
      )}

      <fieldset className="brief-form__group">
        <legend>Taxminiy byudjet</legend>
        <div className="chips">
          {BUDGETS.map((b) => (
            <button
              key={b.value}
              type="button"
              className={cx('chip chip--btn', budget === b.value && 'is-active')}
              aria-pressed={budget === b.value}
              onClick={() => setBudget(b.value)}
            >
              {b.label}
            </button>
          ))}
        </div>
      </fieldset>

      <div className="brief-form__fields">
        <label className={cx('field', errors.name && 'has-error')}>
          <span>Ismingiz *</span>
          <input value={form.name} onChange={set('name')} autoComplete="name" placeholder="Ism Familiya" />
          {errors.name && <small>{errors.name}</small>}
        </label>
        <label className={cx('field', errors.phone && 'has-error')}>
          <span>Telefon *</span>
          <input value={form.phone} onChange={set('phone')} inputMode="tel" autoComplete="tel" placeholder="+998 90 123 45 67" />
          {errors.phone && <small>{errors.phone}</small>}
        </label>
        {!compact && (
          <>
            <label className={cx('field', errors.email && 'has-error')}>
              <span>Email</span>
              <input value={form.email} onChange={set('email')} type="email" autoComplete="email" placeholder="siz@kompaniya.uz" />
              {errors.email && <small>{errors.email}</small>}
            </label>
            <label className="field">
              <span>Kompaniya</span>
              <input value={form.company} onChange={set('company')} autoComplete="organization" placeholder="Kompaniya nomi" />
            </label>
          </>
        )}
        <label className="field field--full">
          <span>Loyiha haqida qisqacha</span>
          <textarea value={form.message} onChange={set('message')} rows={compact ? 3 : 5} placeholder="Qanday muammoni hal qilmoqchisiz? Namuna saytlar, muddat..." />
        </label>
        {/* bot tuzog'i — foydalanuvchiga ko'rinmaydi */}
        <input className="hp" tabIndex={-1} autoComplete="off" value={form.website} onChange={set('website')} aria-hidden="true" />
      </div>

      {errors.form && <p className="form-error" role="alert">{errors.form}</p>}

      <div className="brief-form__submit">
        <button type="submit" className="btn btn--primary btn--lg" disabled={contact.isPending}>
          {contact.isPending ? <LoaderCircle className="spin" size={20} /> : null}
          {contact.isPending ? 'Yuborilmoqda...' : 'Yuborish'}
          {!contact.isPending && <ArrowRight size={20} />}
        </button>
        <p className="muted">24 soat ichida javob beraman. Ma'lumotlaringiz uchinchi shaxslarga berilmaydi.</p>
      </div>
    </form>
  )
}
