import { LoaderCircle } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'
import { useProjectCategories, useProjects } from '../api/client'
import PageHero from '../components/PageHero'
import { BentoGrid } from '../components/ProjectCard'
import Seo from '../components/Seo'
import { cx } from '../lib/format'

export default function Portfolio() {
  const [params, setParams] = useSearchParams()
  const category = params.get('category') || undefined
  const { data: cats } = useProjectCategories()
  const { data, isLoading, isFetching, hasNextPage, fetchNextPage, isFetchingNextPage } = useProjects(category)
  const projects = data?.pages.flatMap((p) => p.results) ?? []
  const total = cats?.reduce((a, c) => a + c.count, 0)

  const choose = (slug?: string) => {
    const next = new URLSearchParams(params)
    if (slug) next.set('category', slug)
    else next.delete('category')
    setParams(next, { replace: true })
  }

  return (
    <>
      <Seo title="Portfolio" description="Asilbek Yuldoshev loyihalari: onlayn do'konlar, mobil ilovalar, POS/ERP tizimlar va korporativ saytlar." />
      <PageHero
        eyebrow="Ishlarim"
        title="Portfolio"
        upper
        text="Har bir loyiha ortida real biznes va uning muammosi bor. Kartochkani bosib, batafsil ko'ring."
        crumbs={[{ to: '/portfolio', label: 'Portfolio' }]}
      >
        <div className="tabs" role="tablist" aria-label="Loyiha turlari">
          <button type="button" role="tab" aria-selected={!category} className={cx('tab', !category && 'is-active')} onClick={() => choose()}>
            Barchasi {total ? <em>{total}</em> : null}
          </button>
          {cats?.map((c) => (
            <button key={c.slug} type="button" role="tab" aria-selected={category === c.slug} className={cx('tab', category === c.slug && 'is-active')} onClick={() => choose(c.slug)}>
              {c.name} <em>{c.count}</em>
            </button>
          ))}
        </div>
      </PageHero>

      <section className="section section--flush">
        <div className={cx('container', isFetching && !isFetchingNextPage && 'is-dim')}>
          <BentoGrid projects={projects} loading={isLoading} />
          {!isLoading && projects.length === 0 && <p className="empty">Bu turda hozircha loyiha yo'q.</p>}
          {hasNextPage && (
            <div className="load-more">
              <button type="button" className="btn btn--outline btn--lg" onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
                {isFetchingNextPage && <LoaderCircle className="spin" size={18} />} Yana ko'rsatish
              </button>
            </div>
          )}
        </div>
      </section>
    </>
  )
}
