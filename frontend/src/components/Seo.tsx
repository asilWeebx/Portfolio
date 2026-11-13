import { Helmet } from 'react-helmet-async'
import { useLocation } from 'react-router-dom'
import { useSite } from '../api/client'

const SITE = 'Asilbek Yuldashev'

interface Props {
  title?: string
  description?: string
  image?: string | null
  type?: 'website' | 'article'
  publishedAt?: string
}

export default function Seo({ title, description, image, type = 'website', publishedAt }: Props) {
  const { data } = useSite()
  const { pathname } = useLocation()
  const fullTitle = title ? `${title} — ${SITE}` : `${SITE} — ${data?.settings.role || 'Full-stack dasturchi'}`
  const desc = description || data?.settings.meta_description || ''
  const origin = typeof window !== 'undefined' ? window.location.origin : ''
  const img = image || data?.settings.og_image || '/og-image.png'
  const abs = (u: string) => (u.startsWith('http') ? u : `${origin}${u}`)

  return (
    <Helmet>
      <title>{fullTitle}</title>
      {desc && <meta name="description" content={desc} />}
      <link rel="canonical" href={`${origin}${pathname}`} />
      <meta property="og:title" content={fullTitle} />
      {desc && <meta property="og:description" content={desc} />}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={`${origin}${pathname}`} />
      <meta property="og:image" content={abs(img)} />
      <meta name="twitter:card" content="summary_large_image" />
      {publishedAt && <meta property="article:published_time" content={publishedAt} />}
    </Helmet>
  )
}
