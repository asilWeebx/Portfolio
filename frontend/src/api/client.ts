import { keepPreviousData, useInfiniteQuery, useMutation, useQuery } from '@tanstack/react-query'
import type {
  BlogCategory, ContactPayload, HomeData, Paginated, PostDetail, PostListItem,
  ProjectCategory, ProjectDetail, ProjectListItem, SiteData, TagItem,
} from './types'

const API = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') || '/api'

export class ApiError extends Error {
  status: number
  data: unknown
  constructor(status: number, data: unknown) {
    super(`API ${status}`)
    this.status = status
    this.data = data
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: { Accept: 'application/json', ...(init?.body ? { 'Content-Type': 'application/json' } : {}), ...init?.headers },
  })
  const data = res.status === 204 ? null : await res.json().catch(() => null)
  if (!res.ok) throw new ApiError(res.status, data)
  return data as T
}

function qs(params: Record<string, string | number | undefined | null>) {
  const s = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') s.set(k, String(v))
  })
  const str = s.toString()
  return str ? `?${str}` : ''
}

// ------------------------------------------------------------------ hooks
export const useSite = () => useQuery({ queryKey: ['site'], queryFn: () => request<SiteData>('/site/'), staleTime: 10 * 60_000 })

export const useHome = () => useQuery({ queryKey: ['home'], queryFn: () => request<HomeData>('/home/') })

export const useProjectCategories = () =>
  useQuery({ queryKey: ['project-categories'], queryFn: () => request<ProjectCategory[]>('/projects/categories/') })

export const useProjects = (category?: string) =>
  useInfiniteQuery({
    queryKey: ['projects', category ?? 'all'],
    initialPageParam: 1,
    queryFn: ({ pageParam }) => request<Paginated<ProjectListItem>>(`/projects/${qs({ category, page: pageParam })}`),
    getNextPageParam: (last, all) => (last.next ? all.length + 1 : undefined),
    placeholderData: keepPreviousData,
  })

export const useProject = (slug: string) =>
  useQuery({ queryKey: ['project', slug], queryFn: () => request<ProjectDetail>(`/projects/${slug}/`), retry: false })

export const useBlogCategories = () =>
  useQuery({ queryKey: ['blog-categories'], queryFn: () => request<BlogCategory[]>('/posts/categories/') })

export const useTags = () => useQuery({ queryKey: ['tags'], queryFn: () => request<TagItem[]>('/posts/tags/') })

export const usePosts = (filters: { category?: string; tag?: string; search?: string }) =>
  useInfiniteQuery({
    queryKey: ['posts', filters],
    initialPageParam: 1,
    queryFn: ({ pageParam }) => request<Paginated<PostListItem>>(`/posts/${qs({ ...filters, page: pageParam })}`),
    getNextPageParam: (last, all) => (last.next ? all.length + 1 : undefined),
    placeholderData: keepPreviousData,
  })

export const usePost = (slug: string) =>
  useQuery({ queryKey: ['post', slug], queryFn: () => request<PostDetail>(`/posts/${slug}/`), retry: false })

export const trackPostView = (slug: string) =>
  request<{ views: number }>(`/posts/${slug}/view/`, { method: 'POST' }).catch(() => null)

export const useContact = () =>
  useMutation({
    mutationFn: (payload: ContactPayload) =>
      request<{ ok: boolean }>('/contact/', { method: 'POST', body: JSON.stringify(payload) }),
  })
