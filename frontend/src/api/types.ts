export interface SiteSettings {
  full_name: string
  role: string
  hero_title: string
  hero_subtitle: string
  available_for_work: boolean
  about_title: string
  about_text: string
  avatar: string | null
  about_photo: string | null
  cv_file: string | null
  years_experience: number
  happy_clients: number
  phone: string
  email: string
  location: string
  telegram: string
  github: string
  linkedin: string
  instagram: string
  youtube: string
  meta_description: string
  og_image: string | null
}

export interface Service {
  id: number
  title: string
  short: string
  icon: string
  features: string[]
  price_from: string
}

export interface SiteData {
  settings: SiteSettings
  services: Service[]
}

export interface Technology {
  id: number
  name: string
  group: string
  group_label: string
  icon: string | null
  color: string
}

export interface Experience {
  id: number
  company: string
  position: string
  period: string
  description: string
  url: string
}

export interface Testimonial {
  id: number
  author: string
  position: string
  avatar: string | null
  text: string
  rating: number
}

export interface ClientLogo {
  id: number
  name: string
  logo: string
  url: string
}

export interface ProjectCategory {
  id: number
  name: string
  slug: string
  count: number
}

export interface ProjectListItem {
  id: number
  title: string
  slug: string
  category: ProjectCategory | null
  short_description: string
  cover: string | null
  accent_color: string
  year: number | null
  client: string
  technologies: string[]
  is_featured: boolean
  platforms: Platform[]
  logo: string | null
}

export type Platform = 'web' | 'android' | 'ios' | 'desktop' | 'telegram'

export interface ProjectNav {
  title: string
  slug: string
  cover: string | null
}

export interface ProjectDetail extends Omit<ProjectListItem, 'technologies'> {
  technologies: Technology[]
  content: string
  role: string
  duration: string
  live_url: string
  github_url: string
  app_store_url: string
  play_store_url: string
  telegram_url: string
  desktop_url: string
  images: { id: number; image: string; caption: string; w: number | null; h: number | null }[]
  seo_title: string
  seo_description: string
  prev: ProjectNav | null
  next: ProjectNav | null
}

export interface BlogCategory {
  id: number
  name: string
  slug: string
  description: string
  emoji: string
  count: number
}

export interface TagItem {
  id: number
  name: string
  slug: string
  count: number
}

export interface PostListItem {
  id: number
  title: string
  slug: string
  excerpt: string
  cover: string | null
  category: { name: string; slug: string; emoji: string } | null
  tags: { name: string; slug: string }[]
  published_at: string
  reading_time: number
  views: number
  is_featured: boolean
}

export interface PostDetail extends PostListItem {
  content: string
  updated_at: string
  seo_title: string
  seo_description: string
  related: PostListItem[]
}

export interface HomeData {
  technologies: Technology[]
  experience: Experience[]
  testimonials: Testimonial[]
  clients: ClientLogo[]
  featured_projects: ProjectListItem[]
  latest_posts: PostListItem[]
  stats: { years: number; projects: number; apps: number; clients: number; posts: number }
}

export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ContactPayload {
  name: string
  phone: string
  email?: string
  company?: string
  services?: number[]
  budget?: string
  message?: string
  website?: string
}
