import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// Dev rejimida /api, /media, /admin so'rovlari Django'ga (8010) uzatiladi.
// Production'da hammasi bitta domenda Nginx orqali ishlaydi (deploy/nginx.conf).
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backend = env.VITE_BACKEND_URL || 'http://127.0.0.1:8010'
  const proxied = ['/api', '/media', '/admin', '/static', '/ckeditor5', '/sitemap.xml', '/robots.txt']

  return {
    plugins: [react()],
    server: {
      port: 5180,
      strictPort: true,
      proxy: Object.fromEntries(proxied.map((p) => [p, { target: backend, changeOrigin: false }])),
    },
    preview: { port: 5180 },
    build: {
      target: 'es2020',
      rollupOptions: {
        output: {
          manualChunks: {
            react: ['react', 'react-dom', 'react-router-dom'],
            query: ['@tanstack/react-query'],
          },
        },
      },
    },
  }
})
