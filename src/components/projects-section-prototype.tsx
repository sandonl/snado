import { useEffect, useState } from 'react'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

// Three variants of the dedicated projects page, switchable with ?variant=a|b|c.
const variants = ['a', 'b', 'c'] as const
type Variant = (typeof variants)[number]

type Project = {
  name: string
  category: string
  description: string
} & (
  | { exposure: 'public'; sourceUrl: string }
  | { exposure: 'private' }
)

const projects: ReadonlyArray<Project> = [
  {
    name: 'Eve Korean Tutor',
    category: 'Language learning',
    description:
      'A personal Korean tutor with long-term learning memory, sentence mining and daily Telegram lessons.',
    exposure: 'public',
    sourceUrl: 'https://github.com/sandonl/eve-kr-tutor'
  },
  {
    name: 'Quarry',
    category: 'Korean learning',
    description:
      'A private Korean-learning app built with Alchemy on Cloudflare Workers, D1 and Workflows, with Better Auth handling Google sign-in and user sessions. Its secure MCP lets AI assistants work with lessons, saved vocabulary and spaced-repetition reviews.',
    exposure: 'private'
  }
]

function isVariant(value: string | null): value is Variant {
  return variants.some((variant) => variant === value)
}

function ProjectLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="text-zinc-400 hover:text-zinc-200 transition-colors"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  )
}

function ProjectSourceLink({ project }: { project: Project }) {
  if (project.exposure === 'private') return null
  return <ProjectLink href={project.sourceUrl}>GitHub ↗</ProjectLink>
}

function VariantA() {
  return (
    <div>
      {projects.map((project) => (
        <article key={project.name} className="border-t border-zinc-800 py-6">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between sm:gap-8">
            <div className="space-y-2">
              <h3 className="text-base font-bold text-zinc-100">{project.name}</h3>
              <p className="max-w-lg text-sm leading-6 text-zinc-400">
                {project.description}
              </p>
            </div>
            <div className="flex shrink-0 gap-4 text-xs sm:pt-1">
              <ProjectSourceLink project={project} />
            </div>
          </div>
        </article>
      ))}
    </div>
  )
}

function VariantB() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {projects.map((project) => (
        <article key={project.name} className="flex flex-col rounded-lg border border-zinc-700 bg-zinc-900/60 p-6">
          <span className="mb-8 font-mono text-[10px] uppercase tracking-[0.2em] text-sky-300">
            {project.category}
          </span>
          <h3 className="mb-2 text-xl font-bold text-zinc-100">{project.name}</h3>
          <p className="mb-6 flex-1 text-sm leading-6 text-zinc-400">
            {project.description}
          </p>
          <div className="flex gap-5 text-xs">
            <ProjectSourceLink project={project} />
          </div>
        </article>
      ))}
    </div>
  )
}

function VariantC() {
  return (
    <div className="border-t border-zinc-800">
      {projects.map((project, index) => (
        <article key={project.name} className="grid grid-cols-[3rem_1fr] border-b border-zinc-800 py-6 sm:grid-cols-[5rem_1fr]">
          <span className="font-mono text-xs text-zinc-600">
            {String(index + 1).padStart(2, '0')}
          </span>
          <div>
            <h3 className="mb-2 text-sm font-bold text-zinc-100">{project.name}</h3>
            <p className="max-w-md text-xs leading-5 text-zinc-400">{project.description}</p>
            {project.exposure === 'public' && (
              <a
                href={project.sourceUrl}
                className="mt-3 inline-block rounded-sm text-xs leading-5 text-zinc-400 underline decoration-zinc-700 underline-offset-4 transition-colors hover:text-zinc-200 hover:decoration-zinc-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-zinc-400"
                target="_blank"
                rel="noopener noreferrer"
              >
                View on GitHub
              </a>
            )}
          </div>
        </article>
      ))}
    </div>
  )
}

const variantDetails: Record<Variant, { label: string; component: () => React.JSX.Element }> = {
  a: { label: 'Editorial row', component: VariantA },
  b: { label: 'Feature card', component: VariantB },
  c: { label: 'Project index', component: VariantC }
}

function PrototypeSwitcher({ current, onChange }: { current: Variant; onChange: (variant: Variant) => void }) {
  if (!import.meta.env.DEV) return null

  const currentIndex = variants.indexOf(current)
  const selectOffset = (offset: number) => {
    const nextIndex = (currentIndex + offset + variants.length) % variants.length
    onChange(variants[nextIndex])
  }

  return (
    <div className="fixed bottom-5 left-1/2 z-50 flex -translate-x-1/2 items-center gap-4 rounded-full border border-zinc-600 bg-zinc-950 px-4 py-2 text-xs text-zinc-100 shadow-2xl">
      <button type="button" onClick={() => selectOffset(-1)} aria-label="Previous variant">←</button>
      <span className="min-w-32 text-center">
        {current.toUpperCase()} · {variantDetails[current].label}
      </span>
      <button type="button" onClick={() => selectOffset(1)} aria-label="Next variant">→</button>
    </div>
  )
}

export default function ProjectsSectionPrototype() {
  const [variant, setVariant] = useState<Variant>('a')

  useEffect(() => {
    const queryVariant = new URLSearchParams(window.location.search).get('variant')
    if (isVariant(queryVariant)) setVariant(queryVariant)
  }, [])

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const target = event.target
      const isEditing =
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        (target instanceof HTMLElement && target.isContentEditable)
      if (isEditing || (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight')) return

      const currentIndex = variants.indexOf(variant)
      const offset = event.key === 'ArrowLeft' ? -1 : 1
      const nextIndex = (currentIndex + offset + variants.length) % variants.length
      selectVariant(variants[nextIndex])
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [variant])

  const selectVariant = (nextVariant: Variant) => {
    const url = new URL(window.location.href)
    url.searchParams.set('variant', nextVariant)
    window.history.replaceState({}, '', url)
    setVariant(nextVariant)
  }

  const SelectedVariant = variantDetails[variant].component

  return (
    <main className="min-h-[calc(100vh-16rem)] border-b pb-12 pt-8">
      <div className="mb-12 flex pb-3">
        <LetterSwapPingPong label="Projects" className="text-3xl font-bold" />
      </div>
      <SelectedVariant />
      <PrototypeSwitcher current={variant} onChange={selectVariant} />
    </main>
  )
}
