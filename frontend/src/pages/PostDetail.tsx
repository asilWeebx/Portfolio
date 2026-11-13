import { Calendar, Check, Clock, Eye, Link2 } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { trackPostView, usePost, useSite } from '../api/client'
import { SocialIcon } from '../components/Icons'
import PageLoader from '../components/PageLoader'
import PostCard from '../components/PostCard'
import RichContent, { prepareHtml } from '../components/RichContent'
import Seo from '../components/Seo'
import { formatDate, formatViews } from '../lib/format'
import NotFound from './NotFound'

function useViewOnce(slug: string, enabled: boolean) {
  useEffect(() => {
    if (!enabled) return
    const key = `viewed:${slug}`
    try {
      if (sessionStorage.getItem(key)) return
      sessionStorage.setItem(key, '1')
    } catch {
      /* storage yopiq bo'lsa ham hisoblayveramiz */
    }
    trackPostView(slug)
  }, [slug, enabled])
}

function useActiveHeading(ids: string[]) {
  const [active, setActive] = useState<string>()
  useEffect(() => {
    if (!ids.length) return
    const io = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
        if (visible[0]) setActive(visible[0].target.id)
      },
      { rootMargin: '-90px 0px -65% 0px' },
    )
    ids.forEach((id) => {
      const el = document.getElementById(id)
      if (el) io.observe(el)
    })
    return () => io.disconnect()
  }, [ids])
  return active
}

function ReadingProgress() {
  const [p, setP] = useState(0)
  useEffect(() => {
    const onScroll = () => {
      const h = document.documentElement
      const max = h.scrollHeight - h.clientHeight
      setP(max > 0 ? Math.min(1, h.scrollTop / max) : 0)
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])
  return <div className="reading-progress" style={{ transform: `scaleX(${p})` }} aria-hidden="true" />
}

export default function PostDetail() {
  const { slug = '' } = useParams()
  const { data: post, isLoading, isError } = usePost(slug)
  const { data: site } = useSite()
  const [copied, setCopied] = useState(false)
  useViewOnce(slug, Boolean(post))

  const toc = useMemo(() => (post ? prepareHtml(post.content).toc.filter((t) => t.level === 2) : []), [post])
  const ids = useMemo(() => toc.map((t) => t.id), [toc])
  const active = useActiveHeading(ids)

  if (isLoading) return <PageLoader />
  if (isError || !post) return <NotFound />

  const url = typeof window !== 'undefined' ? window.location.href : ''
  const copy = () => {
    navigator.clipboard?.writeText(url).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1600)
    })
  }

  return (
    <>
      <Seo
        title={post.seo_title || post.title}
        description={post.seo_description || post.excerpt}
        image={post.cover}
        type="article"
        publishedAt={post.published_at}
      />
      <ReadingProgress />
      <article className="post">
        <header className="post__head">
          <div className="page-hero__glow" aria-hidden="true" />
          <div className="container container--narrow">
            <nav className="crumbs" aria-label="Breadcrumb">
              <Link to="/">Bosh sahifa</Link><i>/</i><Link to="/blog">Blog</Link>
              {post.category && (<><i>/</i><Link to={`/blog?category=${post.category.slug}`}>{post.category.name}</Link></>)}
            </nav>
            {post.category && (
              <Link to={`/blog?category=${post.category.slug}`} className="eyebrow">{post.category.emoji} {post.category.name}</Link>
            )}
            <h1 className="post__title">{post.title}</h1>
            {post.excerpt && <p className="post__lead">{post.excerpt}</p>}
            <div className="post__meta">
              <span className="post__author">
                <img src={site?.settings.avatar || '/brand/logo-mark.svg'} alt="" />
                {site?.settings.full_name || 'Asilbek Yuldashev'}
              </span>
              <span><Calendar size={16} /> {formatDate(post.published_at)}</span>
              <span><Clock size={16} /> {post.reading_time} daqiqa</span>
              <span><Eye size={16} /> {formatViews(post.views)}</span>
            </div>
          </div>
        </header>

        {post.cover && (
          <div className="container container--wide post__cover">
            <img src={post.cover} alt={post.title} />
          </div>
        )}

        <div className="container post__layout">
          <aside className="post__toc">
            {toc.length > 1 && (
              <nav aria-label="Mundarija">
                <h4>Mundarija</h4>
                <ol>
                  {toc.map((t) => (
                    <li key={t.id}>
                      <a href={`#${t.id}`} className={active === t.id ? 'is-active' : ''} onClick={(e) => {
                        e.preventDefault()
                        document.getElementById(t.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
                        history.replaceState(null, '', `#${t.id}`)
                      }}>{t.text}</a>
                    </li>
                  ))}
                </ol>
              </nav>
            )}
          </aside>

          <div className="post__body">
            <RichContent html={post.content} />

            {post.tags.length > 0 && (
              <div className="post__tags">
                {post.tags.map((t) => <Link key={t.slug} to={`/blog?tag=${t.slug}`} className="chip">#{t.name}</Link>)}
              </div>
            )}

            <div className="post__share">
              <span>Ulashish:</span>
              <a className="icon-btn" href={`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(post.title)}`} target="_blank" rel="noreferrer" aria-label="Telegram'da ulashish">
                <SocialIcon name="telegram" size={18} />
              </a>
              <a className="icon-btn" href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`} target="_blank" rel="noreferrer" aria-label="LinkedIn'da ulashish">
                <SocialIcon name="linkedin" size={18} />
              </a>
              <button type="button" className="icon-btn" onClick={copy} aria-label="Havolani nusxalash">
                {copied ? <Check size={18} /> : <Link2 size={18} />}
              </button>
            </div>

            <div className="author-box">
              <img src={site?.settings.avatar || '/brand/logo-mark.svg'} alt="" />
              <div>
                <b>{site?.settings.full_name || 'Asilbek Yuldashev'}</b>
                <p>{site?.settings.role || 'Full-stack dasturchi'}. Savollar yoki loyiha bo'yicha yozing — bajonidil javob beraman.</p>
                <div className="author-box__actions">
                  <Link to="/brief" className="btn btn--primary btn--sm">Loyiha muhokamasi</Link>
                  {site?.settings.telegram && <a href={site.settings.telegram} target="_blank" rel="noreferrer" className="btn btn--outline btn--sm">Telegram</a>}
                </div>
              </div>
            </div>
          </div>
        </div>
      </article>

      {post.related.length > 0 && (
        <section className="section">
          <div className="container">
            <h2 className="section-title section-title--sm">O'xshash maqolalar</h2>
            <div className="prow-grid">
              {post.related.map((r) => <PostCard key={r.id} post={r} />)}
            </div>
          </div>
        </section>
      )}
    </>
  )
}
