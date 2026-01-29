import { createFileRoute, Link } from '@tanstack/react-router'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

export const Route = createFileRoute('/')({
  component: HomePage
})

function HomePage() {
  return (
    <div className="min-h-48 border-b pb-8">
      <div className="flex flex-col gap-6">
        <div className="flex pb-3">
          <LetterSwapPingPong label="About" className="text-3xl font-bold" />
        </div>
        <p className="text-sm">Hi,</p>
        <p className="text-sm">
          I&apos;m a software engineer living in Melbourne, Australia and
          currently work at{" "}
          <a
            href="https://tilt.legal"
            className="text-zinc-400 hover:text-zinc-500"
            target="_blank"
            rel="noopener noreferrer"
          >
            TILT Legal
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
