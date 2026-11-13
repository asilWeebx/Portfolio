import DOMPurify from 'dompurify'
import { useEffect, useMemo, useRef } from 'react'
import { highlightAll } from '../lib/highlight'

export interface TocItem {
  id: string
  text: string
  level: number
}

function slugify(s: string) {
  return s
    .toLowerCase()
    .replace(/[ʻʼ'`‘’]/g, '')
    .replace(/[^a-z0-9а-яё\s-]/gi, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 60)
}

/** CKEditor'dan kelgan HTML: tozalash, sarlavhalarga id berish va kodni ranglash. */
export function prepareHtml(html: string): { html: string; toc: TocItem[] } {
  const clean = DOMPurify.sanitize(html, {
    ADD_TAGS: ['iframe'],
    ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'target'],
  })
  const doc = new DOMParser().parseFromString(`<div>${clean}</div>`, 'text/html')
  const root = doc.body.firstElementChild as HTMLElement
  const toc: TocItem[] = []
  const used = new Set<string>()
  root.querySelectorAll('h2, h3').forEach((h) => {
    let id = slugify(h.textContent || '') || 'bolim'
    while (used.has(id)) id += '-1'
    used.add(id)
    h.id = id
    toc.push({ id, text: h.textContent || '', level: h.tagName === 'H2' ? 2 : 3 })
  })
  root.querySelectorAll('a[href^="http"]').forEach((a) => {
    a.setAttribute('target', '_blank')
    a.setAttribute('rel', 'noopener noreferrer')
  })
  root.querySelectorAll('img').forEach((img) => {
    img.setAttribute('loading', 'lazy')
    img.setAttribute('decoding', 'async')
  })
  root.querySelectorAll('iframe').forEach((f) => {
    const src = f.getAttribute('src') || ''
    if (!/^https:\/\/(www\.)?(youtube\.com|youtube-nocookie\.com|player\.vimeo\.com)\//.test(src)) f.remove()
  })
  return { html: root.innerHTML, toc }
}

export default function RichContent({ html, className = '' }: { html: string; className?: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const prepared = useMemo(() => prepareHtml(html).html, [html])

  useEffect(() => {
    if (!ref.current) return
    highlightAll(ref.current)
    // kod bloklariga "nusxa olish" tugmasi
    ref.current.querySelectorAll('pre').forEach((pre) => {
      if (pre.querySelector('.copy-btn')) return
      const btn = document.createElement('button')
      btn.type = 'button'
      btn.className = 'copy-btn'
      btn.textContent = 'Nusxa olish'
      btn.addEventListener('click', () => {
        const code = pre.querySelector('code')?.textContent ?? pre.textContent ?? ''
        navigator.clipboard?.writeText(code).then(() => {
          btn.textContent = 'Nusxa olindi ✓'
          setTimeout(() => (btn.textContent = 'Nusxa olish'), 1600)
        })
      })
      pre.appendChild(btn)
    })
  }, [prepared])

  return <div ref={ref} className={`prose ${className}`} dangerouslySetInnerHTML={{ __html: prepared }} />
}
