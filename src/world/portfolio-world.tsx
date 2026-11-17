import { useEffect, useRef, useState } from 'react'
import { discoveries, seats, type SeatId, type DiscoveryId } from './world-data'
import { characterPalettes, type CharacterPaletteId } from './character'
import type { Activity, MoveAction, WorldController } from './scene'

type LoadState = { phase: 'loading' } | { phase: 'ready' } | { phase: 'error'; message: string }

export default function PortfolioWorld() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const controllerRef = useRef<WorldController | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)
  const [load, setLoad] = useState<LoadState>({ phase: 'loading' })
  const [nearby, setNearby] = useState<DiscoveryId | null>(null)
  const [selected, setSelected] = useState<DiscoveryId | null>(null)
  const [panel, setPanel] = useState<'none' | 'places' | 'character'>('none')
  const [nearbySeat, setNearbySeat] = useState<SeatId | null>(null)
  const [activity, setActivity] = useState<Activity>('walking')
  const [palette, setPalette] = useState<CharacterPaletteId>('fern')
  const place = discoveries.find(value => value.id === selected)
  const seat = seats.find(value => value.id === nearbySeat)
  const nearbyPlace = discoveries.find(value => value.id === nearby)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    let disposed = false
    void import('./scene').then(({ createWorld }) => {
      if (disposed) return
      const controller = createWorld(canvas, { onNearby: setNearby, onDiscover: setSelected, onNearbySeat: setNearbySeat, onActivity: setActivity })
      controllerRef.current = controller
      return controller.ready.then(() => { if (!disposed) setLoad({ phase: 'ready' }) })
    }).catch((error: unknown) => {
      if (!disposed) setLoad({ phase: 'error', message: error instanceof Error ? error.message : 'The scene could not load.' })
    })
    return () => {
      disposed = true
      const controller = controllerRef.current
      if (controller) controller.dispose()
      controllerRef.current = null
    }
  }, [])

  useEffect(() => {
    const dialog = dialogRef.current
    const controller = controllerRef.current
    if (selected) {
      if (controller) controller.setPaused(true)
      if (dialog && !dialog.open) dialog.showModal()
    } else {
      if (dialog && dialog.open) dialog.close()
      if (controller) controller.setPaused(false)
    }
  }, [selected])

  function move(action: MoveAction, active: boolean) {
    const controller = controllerRef.current
    if (controller) controller.setAction(action, active)
  }

  function takeAction(action: 'jump' | 'sit' | 'stand') {
    const controller = controllerRef.current
    if (controller) controller[action]()
  }

  return (
    <main className="portfolio-world" aria-label="Explore the city">
      <canvas ref={canvasRef} className="world-canvas" aria-label="Walk through Melbourne and Seoul. Use W A S D or arrow keys to move, drag to look, Space to jump, and E to sit or read nearby." tabIndex={0} />
      <header className="world-header">
        <nav aria-label="World navigation">
          <button type="button" disabled={load.phase !== 'ready'} onClick={() => setPanel(value => value === 'character' ? 'none' : 'character')} aria-expanded={panel === 'character'}>Character</button>
          <button type="button" onClick={() => setPanel(value => value === 'places' ? 'none' : 'places')} aria-expanded={panel === 'places'}>Places</button>
          <a href="/">Read portfolio <span aria-hidden="true">↗</span></a>
        </nav>
      </header>

      {panel === 'places' && <section className="world-places" aria-label="Places to explore">
        {discoveries.map(value => <button className="world-place-link" key={value.id} onClick={() => { setSelected(value.id); setPanel('none') }}>{value.title}<span aria-hidden="true">↗</span></button>)}
      </section>}

      {panel === 'character' && <section className="world-places world-character" aria-label="Character appearance">
        {characterPalettes.map(value => <button key={value.id} aria-pressed={palette === value.id} onClick={() => {
          const controller = controllerRef.current
          if (controller) controller.setCharacterPalette(value.id)
          setPalette(value.id)
        }}><span className="world-palette-swatch" style={{ background: value.cap }} aria-hidden="true" />{value.label}</button>)}
      </section>}

      {load.phase === 'loading' && <div className="world-status" role="status"><span className="world-loading-mark" aria-hidden="true" /><h2>Loading…</h2></div>}
      {load.phase === 'error' && <div className="world-status" role="alert"><h2>The city couldn’t load</h2><p>You can still read everything in the portfolio.</p><a href="/">Read about Sandon ↗</a><details><summary>Loading details</summary><p>{load.message}</p></details></div>}

      {load.phase === 'ready' && <>
        <div className="world-help"><span><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> walk</span><span>drag to look</span><span><kbd>shift</kbd> run</span><span><kbd>space</kbd> jump</span></div>
        <div className="world-actions">
          {activity === 'walking' && seat && <button className="world-discover" onClick={() => takeAction('sit')}><kbd>E</kbd><span>Sit & drink</span><small>{seat.label}</small></button>}
          {activity === 'seated' && <button className="world-discover" onClick={() => takeAction('stand')}><kbd>E</kbd><span>Stand up</span></button>}
          {activity === 'walking' && nearbyPlace && <button className="world-discover" onClick={() => setSelected(nearbyPlace.id)}>{!seat && <kbd>E</kbd>}<span>{nearbyPlace.title}</span><span aria-hidden="true">↗</span></button>}
        </div>
        <div className="world-touch-controls" aria-label="Movement controls">
          <button className="world-jump" aria-label="Jump" disabled={activity !== 'walking'} onClick={() => takeAction('jump')}>Jump</button>
          {(['forward', 'left', 'backward', 'right'] as const).map((action, index) => <button key={action} disabled={activity !== 'walking'} aria-label={`Walk ${action}`} className={`world-move-${action}`} onPointerDown={event => { event.preventDefault(); event.currentTarget.setPointerCapture(event.pointerId); move(action, true) }} onPointerUp={() => move(action, false)} onPointerCancel={() => move(action, false)} onLostPointerCapture={() => move(action, false)}>{['↑', '←', '↓', '→'][index]}</button>)}
        </div>
      </>}

      <dialog className="world-dialog" ref={dialogRef} onClose={() => setSelected(null)} onCancel={() => setSelected(null)} aria-labelledby="world-discovery-title">
        {place && <><button className="world-dialog-close" onClick={() => setSelected(null)} aria-label="Close discovery">×</button><p className="world-eyebrow">{place.origin}</p><h2 id="world-discovery-title">{place.title}</h2><p>{place.body}</p><a className="world-story-link" href={place.href}>{place.linkLabel} <span aria-hidden="true">↗</span></a><button className="world-keep-walking" onClick={() => setSelected(null)}>Keep walking</button></>}
      </dialog>
    </main>
  )
}
