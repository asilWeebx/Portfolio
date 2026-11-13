import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import Reveal from './Reveal'

interface Props {
  eyebrow: string
  title: ReactNode
  text?: ReactNode
  crumbs?: { to: string; label: string }[]
  children?: ReactNode
  upper?: boolean
}

/** Ichki sahifalar sarlavhasi (ochiq fon, yengil indigo nur). */
export default function PageHero({ eyebrow, title, text, crumbs, children, upper }: Props) {
  return (
    <section className="page-hero">
      <div className="page-hero__glow" aria-hidden="true" />
      <div className="container">
        {crumbs && (
          <nav className="crumbs" aria-label="Breadcrumb">
            <Link to="/">Bosh sahifa</Link>
            {crumbs.map((c) => (
              <span key={c.to}>
                <i>/</i>
                <Link to={c.to}>{c.label}</Link>
              </span>
            ))}
          </nav>
        )}
        <Reveal from="left">
          <span className="eyebrow">{eyebrow}</span>
          <h1 className={`page-hero__title${upper ? ' page-hero__title--upper' : ''}`}>{title}</h1>
          {text && <p className="page-hero__text">{text}</p>}
        </Reveal>
        {children}
      </div>
    </section>
  )
}
