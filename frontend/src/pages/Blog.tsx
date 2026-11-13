import { LayoutGrid, LoaderCircle, Search, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useBlogCategories, usePosts, useTags } from '../api/client'
import PageHero from '../components/PageHero'
import PostCard, { PostCardSkeleton } from '../components/PostCard'
import Reveal from '../components/Reveal'
import Seo from '../components/Seo'
import { cx } from '../lib/format'

export default function Blog() {
  const [params, setParams] = useSearchParams()
  const category = params.get('category') || undefined
  const tag = params.get('tag') || undefined
  const search = params.get('q') || undefined
  const [q, setQ] = useState(search ?? '')

  const { data: cats } = useBlogCategories()
  const { data: tags } = useTags()
  const { data, isLoading, isFetching, hasNextPage, fetchNextPage, isFetchingNextPage } = usePosts({ category, tag, search })
  const posts = data?.pages.flatMap((p) => p.results) ?? []
  const total = data?.pages[0]?.count ?? 0

  const update = (key: string, value?: string) => {
    const next = new URLSearchParams(params)
    if (value) next.set(key, value)
    else next.delete(key)
    setParams(next, { replace: true })
  }

  useEffect(() => {
    const t = setTimeout(() => {
      if ((search ?? '') !== q.trim()) update('q', q.trim() || undefined)
    }, 350)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q])

  const activeCat = cats?.find((c) => c.slug === category)

  return (
    <>
      <Seo
        title={activeCat ? `${activeCat.name} — Blog` : 'Blog'}
        description={activeCat?.description || "Dasturlash, Django, React, Flutter, Telegram botlar, DevOps va freelance haqida amaliy maqolalar."}
      />
      <PageHero
        eyebrow="Blog"
        title={activeCat ? activeCat.name : 'Blog'}
        upper={!activeCat}
        text={activeCat?.description || "Ishimda duch kelgan muammolar, yechimlar va o'rgangan narsalarim — o'zbek tilida, amaliy misollar bilan."}
        crumbs={[{ to: '/blog', label: 'Blog' }]}
      >
        <div className="tabs" role="tablist" aria-label="Mavzular">
          <button type="button" role="tab" aria-selected={!category} aria-label="Barcha mavzular" className={cx('tab tab--icon', !category && 'is-active')} onClick={() => update('category')}>
            <LayoutGrid size={20} />
          </button>
          {cats?.filter((c) => c.count > 0).map((c) => (
            <button key={c.slug} type="button" role="tab" aria-selected={category === c.slug} className={cx('tab', category === c.slug && 'is-active')} onClick={() => update('category', category === c.slug ? undefined : c.slug)}>
              {c.name}
            </button>
          ))}
        </div>
        <label className="searchbar">
          <Search size={22} />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Qidirish" aria-label="Maqola qidirish" />
          {q && <button type="button" onClick={() => setQ('')} aria-label="Tozalash"><X size={18} /></button>}
        </label>
        {tags && tags.length > 0 && (
          <div className="tag-cloud">
            {tags.map((t) => (
              <button key={t.slug} type="button" className={cx('tag-link', tag === t.slug && 'is-active')} onClick={() => update('tag', tag === t.slug ? undefined : t.slug)}>
                #{t.name}
              </button>
            ))}
          </div>
        )}
      </PageHero>

      <section className="section section--flush">
        <div className="container">
          {(tag || search) && (
            <div className="active-filters">
              {tag && <button type="button" className="tab is-active" onClick={() => update('tag')}>#{tag} <X size={14} /></button>}
              {search && <span className="muted">"{search}" bo'yicha {total} ta natija</span>}
            </div>
          )}
          <div className={cx('prow-grid', isFetching && !isFetchingNextPage && 'is-dim')}>
            {isLoading
              ? Array.from({ length: 4 }).map((_, i) => <PostCardSkeleton key={i} />)
              : posts.map((p, i) => (
                  <Reveal key={p.id} delay={(i % 2) * 90}>
                    <PostCard post={p} />
                  </Reveal>
                ))}
          </div>
          {!isLoading && posts.length === 0 && (
            <div className="empty">
              <p>Hech narsa topilmadi.</p>
              <button type="button" className="btn btn--outline" onClick={() => { setQ(''); setParams({}, { replace: true }) }}>
                Filtrlarni tozalash
              </button>
            </div>
          )}
          {hasNextPage && (
            <div className="load-more">
              <button type="button" className="btn btn--outline btn--lg" onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
                {isFetchingNextPage && <LoaderCircle className="spin" size={18} />} Yana yuklash
              </button>
            </div>
          )}
        </div>
      </section>
    </>
  )
}
