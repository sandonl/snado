import { Outlet, createRootRoute, HeadContent, Scripts } from '@tanstack/react-router'
import Header from '@/components/header'
import Footer from '@/components/footer'
import { Analytics } from '@vercel/analytics/react'
import '@fontsource/geist-sans/400.css'
import '@fontsource/geist-sans/700.css'
import '@fontsource/geist-mono/400.css'
import { site, siteUrl, structuredData } from '@/lib/seo'
import appCss from '../app/globals.css?url'

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { title: site.name },
      { name: 'description', content: site.description }
    ],
    links: [
      { rel: 'stylesheet', href: appCss },
      { rel: 'describedby', href: '/llms.txt', type: 'text/plain' },
      { rel: 'icon', href: '/favicon.ico?v=2', sizes: '16x16 32x32 48x48' },
      { rel: 'icon', href: '/favicon.png?v=2', type: 'image/png', sizes: '192x192' },
      { rel: 'apple-touch-icon', href: '/apple-touch-icon.png', sizes: '180x180' }
    ],
    scripts: [structuredData({
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'Person',
          '@id': siteUrl('/#person'),
          name: site.name,
          url: siteUrl('/'),
          jobTitle: 'AI / Software Engineer',
          sameAs: [
            'https://linkedin.com/in/sandonlai',
            'https://github.com/sandonl',
            'https://x.com/snads_build',
          ],
        },
        {
          '@type': 'WebSite',
          '@id': siteUrl('/#website'),
          name: site.name,
          url: siteUrl('/'),
          description: site.description,
          author: { '@id': siteUrl('/#person') },
          inLanguage: 'en',
        },
      ],
    })],
  }),
  component: RootLayout,
  notFoundComponent: () => (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Page not found</h1>
    </div>
  )
})

function RootLayout() {
  return (
    <RootDocument>
      <Outlet />
    </RootDocument>
  )
}

function RootDocument({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body className="font-sans antialiased bg-[#1b1b1b] max-w-2xl mx-auto overflow-x-hidden px-4 selection:bg-sky-300 selection:text-sky-900">
        <Header />
        {children}
        <Footer />
        <Analytics />
        <Scripts />
      </body>
    </html>
  )
}
