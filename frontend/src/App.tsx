import { lazy, Suspense } from 'react'
import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import PageLoader from './components/PageLoader'
import Home from './pages/Home'

const Portfolio = lazy(() => import('./pages/Portfolio'))
const ProjectDetail = lazy(() => import('./pages/ProjectDetail'))
const Blog = lazy(() => import('./pages/Blog'))
const PostDetail = lazy(() => import('./pages/PostDetail'))
const About = lazy(() => import('./pages/About'))
const Brief = lazy(() => import('./pages/Brief'))
const NotFound = lazy(() => import('./pages/NotFound'))

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="portfolio" element={<Suspense fallback={<PageLoader />}><Portfolio /></Suspense>} />
        <Route path="portfolio/:slug" element={<Suspense fallback={<PageLoader />}><ProjectDetail /></Suspense>} />
        <Route path="blog" element={<Suspense fallback={<PageLoader />}><Blog /></Suspense>} />
        <Route path="blog/:slug" element={<Suspense fallback={<PageLoader />}><PostDetail /></Suspense>} />
        <Route path="about" element={<Suspense fallback={<PageLoader />}><About /></Suspense>} />
        <Route path="brief" element={<Suspense fallback={<PageLoader />}><Brief /></Suspense>} />
        <Route path="*" element={<Suspense fallback={<PageLoader />}><NotFound /></Suspense>} />
      </Route>
    </Routes>
  )
}
