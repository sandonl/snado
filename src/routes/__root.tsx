import { Outlet, createRootRoute, HeadContent, Scripts } from '@tanstack/react-router'
import Header from '@/components/header'
import Footer from '@/components/footer'
import { Analytics } from '@vercel/analytics/react'
import '@fontsource/geist-sans/400.css'
import '@fontsource/geist-sans/700.css'
import '@fontsource/geist-mono/400.css'
import appCss from '../app/globals.css?url'

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { title: 'Sandon Lai' },
      { name: 'description', content: "Sandon Lai's personal website" }
    ],
    links: [
      { rel: 'stylesheet', href: appCss }
    ]
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
      <body className="font-sans antialiased bg-[#1b1b1b] max-w-2xl mx-auto px-4 selection:bg-sky-300 selection:text-sky-900">
        <Header />
        {children}
        <Footer />
        <Analytics />
        <Scripts />
      </body>
    </html>
  )
}
