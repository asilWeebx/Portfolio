import { CircleCheck, LoaderCircle, Rocket } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { ApiError, useContact } from '../api/client'
import { cx } from '../lib/format'

function formatPhone(raw: string) {
  let d = raw.replace(/\D/g, '')
  if (d.startsWith('998')) d = d.slice(3)
  d = d.slice(0, 9)
  return [d.slice(0, 2), d.slice(2, 5), d.slice(5, 7), d.slice(7, 9)].filter(Boolean).join(' ')
}

/** Bosh sahifadagi qisqa forma: ism + telefon + yuborish (UIC'dagi "Hello..." bloki kabi). */
export default function QuickForm() {
  const contact = useContact()
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [err, setErr] = useState<{ name?: string; phone?: string; form?: string }>({})

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    const errs: typeof err = {}
    if (name.trim().length < 2) errs.name = 'Ismingizni kiriting'
    if (phone.replace(/\D/g, '').length < 9) errs.phone = "Raqamni to'liq kiriting"
    setErr(errs)
    if (Object.keys(errs).length) return
    try {
      await contact.mutateAsync({ name: name.trim(), phone: `+998 ${phone}`, message: 'Bosh sahifadagi qisqa forma' })
    } catch (e) {
      setErr({ form: e instanceof ApiError && e.status === 429 ? "Juda ko'p urinish, birozdan keyin qayta yuboring" : "Yuborib bo'lmadi, qayta urinib ko'ring" })
    }
  }

  if (contact.isSuccess) {
    return (
      <div className="qform qform--done" role="status">
        <CircleCheck size={28} />
        <span>Rahmat! 24 soat ichida qo'ng'iroq qilaman.</span>
      </div>
    )
  }

  return (
    <form className="qform" onSubmit={submit} noValidate>
      <label className={cx('qform__field', err.name && 'has-error')}>
        <span>Ismingiz</span>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Ismingizni kiriting" autoComplete="name" />
      </label>
      <label className={cx('qform__field', err.phone && 'has-error')}>
        <span>Telefon raqamingiz</span>
        <div className="qform__phone">
          <span className="qform__flag" aria-hidden="true"><i /><i /><i /></span>
          <em>+998</em>
          <input value={phone} onChange={(e) => setPhone(formatPhone(e.target.value))} inputMode="tel" autoComplete="tel-national" placeholder="90 123 45 67" />
        </div>
      </label>
      <button type="submit" className="btn btn--primary btn--lg qform__submit" disabled={contact.isPending}>
        {contact.isPending ? <LoaderCircle className="spin" size={20} /> : null}
        Yuborish {!contact.isPending && <Rocket size={20} />}
      </button>
      {(err.name || err.phone || err.form) && <p className="qform__err" role="alert">{err.form || err.name || err.phone}</p>}
    </form>
  )
}
