import type { ReactNode } from 'react'
import Reveal from './Reveal'

interface Props {
  eyebrow: string
  title: ReactNode
  text?: ReactNode
  action?: ReactNode
  center?: boolean
  upper?: boolean
}

/** Bo'lim sarlavhasi: indigo kichik yozuv (chiziq bilan) + katta sarlavha. */
export default function SectionHead({ eyebrow, title, text, action, center, upper }: Props) {
  return (
    <div className={`section-head${center ? ' section-head--center' : ''}`}>
      <Reveal from="left">
        <span className="eyebrow">{eyebrow}</span>
        <h2 className={`section-title${upper ? ' section-title--upper' : ''}`}>{title}</h2>
        {text && <p className="section-text">{text}</p>}
      </Reveal>
      {action && <Reveal from="right" className="section-head__action">{action}</Reveal>}
    </div>
  )
}
