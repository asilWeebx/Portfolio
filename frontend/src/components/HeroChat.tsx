import { ArrowUpRight, RotateCcw } from 'lucide-react'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useSite } from '../api/client'
import type { Service } from '../api/types'
import { cx } from '../lib/format'
import { ServiceIcon } from './Icons'
import { LogoMark } from './Logo'

type Msg = { id: number; from: 'me' | 'them'; text: string; serviceId?: number }

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

/**
 * Hero'dagi jonli mini-chat: mehmon xizmatni tanlaydi → qisqa javob va narx → "Brief" tugmasi.
 * Hech kim bosmasa, o'zi namoyish rejimida xizmatlarni navbat bilan "tanlab" turadi.
 */
export default function HeroChat() {
  const { data } = useSite()
  const services = useMemo(() => (data?.services ?? []).slice(0, 6), [data?.services])
  const avatar = data?.settings.avatar

  const [msgs, setMsgs] = useState<Msg[]>([])
  const [typing, setTyping] = useState(false)
  const [stage, setStage] = useState<'intro' | 'choose' | 'answered'>('intro')
  const [picked, setPicked] = useState<Service | null>(null)
  const userTouched = useRef(false)
  const runId = useRef(0)
  const nextId = useRef(1)
  const listRef = useRef<HTMLDivElement>(null)

  const push = (m: Omit<Msg, 'id'>) => setMsgs((xs) => [...xs, { ...m, id: nextId.current++ }])

  const botSay = useCallback(async (text: string, run: number, delay = 750) => {
    setTyping(true)
    await sleep(delay)
    if (run !== runId.current) return false
    setTyping(false)
    push({ from: 'me', text })
    return true
  }, [])

  const intro = useCallback(async () => {
    const run = ++runId.current
    setMsgs([])
    setPicked(null)
    setStage('intro')
    await sleep(400)
    if (!(await botSay('Salom! 👋', run, 600))) return
    if (!(await botSay("Qanday loyiha ustida o'ylayapsiz? Tanlang — qisqacha aytib beraman.", run, 900))) return
    setStage('choose')
  }, [botSay])

  const choose = useCallback(async (s: Service, auto = false) => {
    if (!auto) userTouched.current = true
    const run = ++runId.current
    setPicked(s)
    setStage('answered')
    push({ from: 'them', text: s.title, serviceId: s.id })
    if (!(await botSay(s.short, run, 1000))) return
    if (s.price_from) {
      const price = /\d/.test(s.price_from) ? `Narxi ${s.price_from.replace(/\s*dan$/i, '')} dan boshlanadi.` : `Narxi: ${s.price_from.toLowerCase()}.`
      await botSay(`${price} Batafsil gaplashamizmi?`, run, 900)
    }
  }, [botSay])

  // boshlanish
  useEffect(() => {
    if (services.length) intro()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [services.length])

  // namoyish rejimi: foydalanuvchi bosmaguncha xizmatlarni navbat bilan ko'rsatadi
  useEffect(() => {
    if (userTouched.current || !services.length) return
    let cancelled = false
    let k = 0
    const loop = async () => {
      while (!cancelled && !userTouched.current) {
        await sleep(stage === 'choose' ? 2600 : 6500)
        if (cancelled || userTouched.current) return
        if (stage === 'choose') {
          choose(services[k % services.length], true)
          k++
          return
        }
        if (stage === 'answered') {
          intro()
          return
        }
      }
    }
    loop()
    return () => {
      cancelled = true
    }
  }, [stage, services, choose, intro])

  useEffect(() => {
    const el = listRef.current
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
  }, [msgs, typing, stage])

  if (!data) return <div className="chat chat--loading" aria-hidden="true" />
  if (!services.length) return null

  return (
    <div
      className="chat"
      onPointerDown={() => {
        userTouched.current = true
      }}
    >
      <header className="chat__head">
        <span className="chat__avatar">{avatar ? <img src={avatar} alt="" /> : <LogoMark size={26} />}</span>
        <span className="chat__who">
          <b>Asilbek</b>
          <small><i /> onlayn · odatda 1 soatda javob beradi</small>
        </span>
      </header>

      <div className="chat__body" ref={listRef} aria-live="polite">
        {msgs.map((m) => (
          <div key={m.id} className={cx('bubble', m.from === 'me' ? 'bubble--in' : 'bubble--out')}>
            {m.from === 'them' && m.serviceId && (() => {
              const s = services.find((x) => x.id === m.serviceId)
              return s ? <ServiceIcon name={s.icon} size={16} /> : null
            })()}
            {m.text}
          </div>
        ))}
        {typing && (
          <div className="bubble bubble--in bubble--typing" aria-label="yozmoqda">
            <i /><i /><i />
          </div>
        )}
      </div>

      <div className="chat__foot">
        {stage === 'choose' && (
          <div className="chat__chips">
            {services.map((s) => (
              <button key={s.id} type="button" className="chat__chip" onClick={() => choose(s)}>
                <ServiceIcon name={s.icon} size={16} /> {s.title}
              </button>
            ))}
          </div>
        )}
        {stage === 'answered' && picked && !typing && (
          <div className="chat__actions">
            <Link to={`/brief?s=${picked.id}`} className="btn btn--primary btn--sm">
              Brief to'ldirish <ArrowUpRight size={16} />
            </Link>
            <button
              type="button"
              className="chat__again"
              onClick={() => {
                userTouched.current = true
                intro()
              }}
            >
              <RotateCcw size={15} /> Boshqa variant
            </button>
          </div>
        )}
        {stage === 'intro' && <div className="chat__placeholder" />}
      </div>
    </div>
  )
}
