import { Calendar, Eye } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { PostListItem } from '../api/types'
import { formatViews } from '../lib/format'

function shortDate(iso: string) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const p = (n: number) => String(n).padStart(2, '0')
  return `${p(d.getDate())}.${p(d.getMonth() + 1)}.${d.getFullYear()}`
}

/** UIC blog uslubi: rasm chapda (kartochkadan chiqib turadi), matn o'ngda, pastda sana va ko'rishlar. */
export default function PostCard({ post }: { post: PostListItem }) {
  return (
    <Link to={`/blog/${post.slug}`} className="prow">
      <div className="prow__media">
        {post.cover ? (
          <img src={post.cover} alt="" loading="lazy" decoding="async" />
        ) : (
          <div className="prow__placeholder" aria-hidden="true"><span>{post.category?.emoji || '✍️'}</span></div>
        )}
        {post.category && <span className="prow__tag">{post.category.name}</span>}
      </div>
      <div className="prow__body">
        <h3 className="prow__title">{post.title}</h3>
        {post.excerpt && <p className="prow__excerpt">{post.excerpt}</p>}
        <div className="prow__meta">
          <span><Calendar size={16} /> {shortDate(post.published_at)}</span>
          <span><Eye size={16} /> {formatViews(post.views)}</span>
        </div>
      </div>
    </Link>
  )
}

export function PostCardSkeleton() {
  return (
    <div className="prow" aria-hidden="true">
      <div className="prow__media skeleton" />
      <div className="prow__body">
        <div className="skeleton skeleton--title" />
        <div className="skeleton skeleton--line" />
        <div className="skeleton skeleton--line" style={{ width: '60%' }} />
      </div>
    </div>
  )
}
