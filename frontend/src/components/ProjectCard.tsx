import { ArrowUpRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { Platform, ProjectListItem } from '../api/types'
import { isLight } from '../lib/color'
import { cx } from '../lib/format'

export const PLATFORM_LABEL: Record<Platform, string> = {
  web: 'Web', android: 'Android', ios: 'iOS', desktop: 'Desktop', telegram: 'Telegram',
}

/** Loyiha turi — kartochkadagi "WEBSITE / MOBILE APP" yozuvi o'rnida. */
export function projectKind(p: Pick<ProjectListItem, 'platforms' | 'category'>): string {
  const has = (x: Platform) => p.platforms.includes(x)
  const parts: string[] = []
  if (has('web')) parts.push('Veb-sayt')
  if (has('android') || has('ios')) parts.push('Mobil ilova')
  if (has('desktop')) parts.push('Desktop')
  if (!parts.length && p.category) parts.push(p.category.name)
  return parts.join(' · ')
}

/** UIC uslubidagi bento kartochka: rangli fon, sarlavha chap yuqorida, mockup o'ng pastda. */
export default function ProjectCard({ project, big = false }: { project: ProjectListItem; big?: boolean }) {
  const color = project.accent_color || '#1F2433'
  return (
    <Link
      to={`/portfolio/${project.slug}`}
      className={cx('pcard', big && 'pcard--big', isLight(color) && 'pcard--light')}
      style={{ '--c': color } as React.CSSProperties}
    >
      {project.cover && <img className="pcard__img" src={project.cover} alt="" loading="lazy" decoding="async" />}
      <div className="pcard__shade" aria-hidden="true" />
      <div className="pcard__head">
        <h3 className="pcard__title">{project.title}</h3>
        <span className="pcard__kind">{projectKind(project)}</span>
      </div>
      {project.logo && <img className="pcard__logo" src={project.logo} alt={`${project.title} logo`} loading="lazy" />}
      <span className="pcard__go" aria-hidden="true"><ArrowUpRight size={20} /></span>
    </Link>
  )
}

export function ProjectCardSkeleton({ big = false }: { big?: boolean }) {
  return <div className={cx('pcard pcard--skeleton skeleton', big && 'pcard--big')} aria-hidden="true" />
}

/** Bento to'r: har 5 ta kartochkadan biri katta (2x2), katta kartochka chap va o'rtada navbatlashadi. */
export function BentoGrid({ projects, loading }: { projects?: ProjectListItem[]; loading?: boolean }) {
  if (loading) {
    return (
      <div className="bento">
        {Array.from({ length: 5 }).map((_, i) => <ProjectCardSkeleton key={i} big={i === 0} />)}
      </div>
    )
  }
  return (
    <div className="bento">
      {projects?.map((p, i) => {
        const big = i % 5 === 0
        const group = Math.floor(i / 5)
        return (
          <div key={p.id} className={cx('bento__item', big && 'bento__item--big', big && group % 2 === 1 && 'bento__item--mid')}>
            <ProjectCard project={p} big={big} />
          </div>
        )
      })}
    </div>
  )
}
