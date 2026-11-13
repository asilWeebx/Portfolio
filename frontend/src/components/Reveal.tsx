import { createElement, useEffect, useRef, useState, type CSSProperties, type ReactNode } from 'react'

interface Props {
  children: ReactNode
  as?: keyof JSX.IntrinsicElements
  className?: string
  delay?: number
  from?: 'up' | 'left' | 'right' | 'fade'
  style?: CSSProperties
}

/** Ekranga kirganda silliq paydo bo'ladigan blok (uic.group'dagi AOS effektiga o'xshash). */
export default function Reveal({ children, as = 'div', className = '', delay = 0, from = 'up', style }: Props) {
  const ref = useRef<HTMLElement | null>(null)
  const [shown, setShown] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    if (typeof IntersectionObserver === 'undefined') {
      setShown(true)
      return
    }
    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShown(true)
          io.disconnect()
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 },
    )
    io.observe(el)
    return () => io.disconnect()
  }, [])

  return createElement(
    as,
    {
      ref,
      className: `reveal reveal--${from}${shown ? ' is-shown' : ''}${className ? ` ${className}` : ''}`,
      style: { ...style, transitionDelay: delay ? `${delay}ms` : undefined },
    },
    children,
  )
}
