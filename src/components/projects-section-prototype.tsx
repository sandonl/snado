import { useEffect, useState } from 'react'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

// Three variants of the dedicated projects page, switchable with ?variant=a|b|c.
const variants = ['a', 'b', 'c'] as const
type Variant = (typeof variants)[number]

const project = {
  name: 'Eve Korean Tutor',
  description:
    'A personal Korean tutor with long-term learning memory, sentence mining and daily Telegram lessons.',
  sourceUrl: 'https://github.com/sandonl/eve-kr-tutor'
}

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

function VariantA() {
  return (
    <article className="border-t border-zinc-800 py-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between sm:gap-8">
        <div className="space-y-2">
          <h3 className="text-base font-bold text-zinc-100">{project.name}</h3>
          <p className="max-w-lg text-sm leading-6 text-zinc-400">
            {project.description}
          </p>
        </div>
        <div className="flex shrink-0 gap-4 text-xs sm:pt-1">
          <ProjectLink href={project.sourceUrl}>GitHub ↗</ProjectLink>
        </div>
      </div>
    </article>
  )
}

function VariantB() {
  return (
    <article className="rounded-lg border border-zinc-700 bg-zinc-900/60 p-6">
      <div className="mb-8 flex items-center justify-between">
        <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-sky-300">
          Language learning
        </span>
        <span className="h-2 w-2 rounded-full bg-emerald-400" aria-label="Live" />
      </div>
      <h3 className="mb-2 text-xl font-bold text-zinc-100">{project.name}</h3>
      <p className="mb-6 max-w-lg text-sm leading-6 text-zinc-400">
        {project.description}
      </p>
      <div className="flex gap-5 text-xs">
        <ProjectLink href={project.sourceUrl}>View source ↗</ProjectLink>
      </div>
    </article>
  )
}

function VariantC() {
  return (
    <article className="grid grid-cols-[3rem_1fr] border-y border-zinc-800 py-6 sm:grid-cols-[5rem_1fr_auto]">
      <span className="font-mono text-xs text-zinc-600">01</span>
      <div>
        <h3 className="mb-2 text-sm font-bold text-zinc-100">{project.name}</h3>
        <p className="max-w-md text-xs leading-5 text-zinc-400">{project.description}</p>
      </div>
      <div className="col-start-2 mt-4 flex gap-4 text-xs sm:col-start-3 sm:row-start-1 sm:mt-0">
        <ProjectLink href={project.sourceUrl}>Code ↗</ProjectLink>
      </div>
    </article>
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
