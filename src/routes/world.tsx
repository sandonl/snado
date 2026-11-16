import { createFileRoute } from '@tanstack/react-router'
import { pageHead } from '@/lib/seo'
import PortfolioWorld from '@/world/portfolio-world'
import worldStyles from '@/world/world.css?url'

export const Route = createFileRoute('/world')({
  head: () => {
    const head = pageHead({ title: 'Explore Melbourne & Seoul | Sandon Lai', description: 'Walk through a small illustrated neighbourhood of Melbourne cafés and Seoul workshops to discover Sandon’s work, writing and interests.', path: '/world' })
    return { ...head, links: [...head.links, { rel: 'stylesheet', href: worldStyles }] }
  },
  component: PortfolioWorld,
})
