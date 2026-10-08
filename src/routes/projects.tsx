import { createFileRoute } from '@tanstack/react-router'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

export const Route = createFileRoute('/projects')({
  component: ProjectsPage
})

function ProjectsPage() {
  return (
    <main className="min-h-[calc(100vh-16rem)] border-b pb-12 pt-8">
      <h1 className="mb-12 flex pb-3">
        <LetterSwapPingPong label="Projects" className="text-3xl font-bold" />
      </h1>
      <div className="border-t border-zinc-800">
        <article className="grid grid-cols-[3rem_1fr] border-b border-zinc-800 py-6 sm:grid-cols-[5rem_1fr]">
          <span className="font-mono text-xs text-zinc-600">01</span>
          <div>
            <h2 className="mb-2 text-sm font-bold text-zinc-100">Eve Korean Tutor</h2>
            <p className="max-w-md text-xs leading-5 text-zinc-400">
              A personal Korean tutor with long-term learning memory, sentence mining and daily Telegram lessons.
            </p>
            <a
              href="https://github.com/sandonl/eve-kr-tutor"
              className="mt-3 inline-block rounded-sm text-xs leading-5 text-zinc-400 underline decoration-zinc-700 underline-offset-4 transition-colors hover:text-zinc-200 hover:decoration-zinc-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-zinc-400"
              target="_blank"
              rel="noopener noreferrer"
            >
              View on GitHub
            </a>
          </div>
        </article>
        <article className="grid grid-cols-[3rem_1fr] border-b border-zinc-800 py-6 sm:grid-cols-[5rem_1fr]">
          <span className="font-mono text-xs text-zinc-600">02</span>
          <div>
            <h2 className="mb-2 text-sm font-bold text-zinc-100">Quarry</h2>
            <p className="max-w-md text-xs leading-5 text-zinc-400">
              A private Korean-learning app built with Alchemy on Cloudflare Workers, D1 and Workflows, with Better Auth handling Google sign-in and user sessions. Its secure MCP lets AI assistants work with lessons, saved vocabulary and spaced-repetition reviews.
            </p>
          </div>
        </article>
      </div>
    </main>
  )
}
