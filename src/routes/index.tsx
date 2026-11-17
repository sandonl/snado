import { pageHead, site } from '@/lib/seo'
import { createFileRoute, Link } from '@tanstack/react-router'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'
import PortfolioHero from '@/components/portfolio-hero'

export const Route = createFileRoute('/')({
  head: () => pageHead({
    title: 'Sandon Lai | AI & Software Engineer',
    description: site.description,
    path: '/',
  }),
  component: HomePage
})

function HomePage() {
  return (
    <div className="min-h-48 border-b pb-8">
      <PortfolioHero />
      <section id="portfolio" className="portfolio-projects" aria-labelledby="portfolio-title">
        <div className="portfolio-projects-heading"><h2 id="portfolio-title">Portfolio</h2><span>01 / In progress</span></div>
        <Link to="/world" className="portfolio-project">
          <img src="/images/portfolio/cafe-world.jpg" width="1440" height="810" alt="A watercolour café laneway connecting Melbourne and Seoul" loading="lazy" />
          <p className="portfolio-project-type">Three.js / Blender</p>
          <h3>Café world</h3>
          <p>A small, playable neighbourhood inspired by Melbourne laneways and Seoul’s workshop cafés.</p>
          <span className="portfolio-project-open">Open app <span aria-hidden="true">↗</span></span>
        </Link>
      </section>
      <div className="flex flex-col gap-6">
        <div className="flex pb-3">
          <LetterSwapPingPong label="About" className="text-3xl font-bold" />
        </div>
        <p className="text-sm">Hi,</p>
        <p className="text-sm">
          I&apos;m an AI / Software Engineer living in Melbourne, Australia and currently work at{" "}
          <a
            href="https://tilt.legal"
            className="text-zinc-400 hover:text-zinc-500"
            target="_blank"
            rel="noopener noreferrer"
          >
            Tilt legal
          </a>
          . Currently I&apos;m working on making tools and products for legal
          professionals.
        </p>
        <p className="text-sm">
          I graduated from the University of Melbourne with a Bachelor of
          Commerce and Masters of Information Technology at the end of 2022.
        </p>
        <p className="text-sm">
          To find out more about my professional journey and interests, feel
          free to explore my{" "}
          <Link to="/posts" className="text-zinc-400 hover:text-zinc-500">
            written works
          </Link>{" "}
          and various social media profiles.
        </p>
      </div>
    </div>
  )
}
