import { createFileRoute } from '@tanstack/react-router'
import { allPosts } from 'content-collections'
import { siteUrl } from '@/lib/seo'

function escapeXml(value: string) {
  return value.replace(/[<>&"']/g, (character) => `&#${character.charCodeAt(0)};`)
}

export const Route = createFileRoute('/sitemap.xml')({
  server: {
    handlers: {
      GET: () => {
        const paths = ['/', '/projects', '/posts', ...allPosts.map((post) => `/posts/${post.slug}`)]
        // Omit lastmod until we track real content updates, rather than build times.
        const urls = paths.map((path) => `<url><loc>${escapeXml(siteUrl(path))}</loc></url>`)
        return new Response(
          `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`,
          { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
        )
      },
    },
  },
})
