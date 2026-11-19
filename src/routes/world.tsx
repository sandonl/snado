import { createFileRoute } from '@tanstack/react-router'
import { pageHead } from '@/lib/seo'
import PortfolioWorld from '@/world/portfolio-world'
import worldStyles from '@/world/world.css?url'

export const Route = createFileRoute('/world')({
  head: () => {
    const head = pageHead({ title: 'Explore the neighbourhood | Sandon Lai', description: 'Walk past tree-lined shopfronts to a print yard and workshop café in an illustrated neighbourhood, and discover Sandon’s work and writing.', path: '/world' })
    return { ...head, links: [...head.links, { rel: 'stylesheet', href: worldStyles }] }
  },
  component: PortfolioWorld,
})
